import csv
import uuid
import datetime
import random
import hashlib
import os
import tempfile
import requests
import pandas as pd
import json
from urllib.parse import urlparse, parse_qs
from service.kafka_client import send_to_kafka
from service.file_handling_util import handle_error, flush_error_file
from utils.error_handler import ErrorHandler
import constants

# Google Sheets support using direct CSV export URLs
GOOGLE_SHEETS_AVAILABLE = True

class EventIngestionService:
    def __init__(self):
        self.error_handler = ErrorHandler()
        # Define mandatory columns (updated format)
        self.mandatory_columns = constants.MANDATORY_COLUMNS
        
        # Default values for empty fields
        self.default_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.111"
        self.default_user_fp = "817d5da2-bb2c-4b05-ae98-c2f09cb1f8c75"
        self.default_source = constants.COOKIE_SOURCE
        
        # Define source constants
        self.LINK_TRACKING_SOURCE = constants.LINK_TRACKING_SOURCE
        self.TWO_PANE_SOURCE = constants.TWO_PANE_SOURCE
        self.COOKIE_SOURCE = constants.COOKIE_SOURCE
        self.COOKIELESS_SOURCE = constants.COOKIELESS_SOURCE
        self.CLIENT_S2S_SOURCE = constants.CLIENT_S2S_SOURCE
        
        # Kafka topics
        self.CLICKMETER_CLICK_KAFKA_TOPIC = constants.CLICKMETER_CLICK_KAFKA_TOPIC
        self.CLICKMETER_CONVERSION_KAFKA_TOPIC = constants.CLICKMETER_CONVERSION_KAFKA_TOPIC
    
    def download_google_sheet(self, url):
        """Download Google Sheet as CSV using direct export URL"""
        try:
            if 'docs.google.com/spreadsheets' in url:
                # Extract sheet ID from URL
                sheet_id = url.split('/d/')[1].split('/')[0]
                
                # Extract GID from URL if present, otherwise use 0
                gid = '0'
                if 'gid=' in url:
                    gid = url.split('gid=')[1].split('&')[0].split('#')[0]
                
                # Use direct CSV export URL (works with publicly accessible sheets)
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
                
                response = requests.get(csv_url)
                response.raise_for_status()
                
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False)
                temp_file.write(response.text)
                temp_file.close()
                
                return temp_file.name
            else:
                raise ValueError("Invalid Google Sheets URL")
        except Exception as e:
            raise Exception(f"Error downloading Google Sheet: {str(e)}")
    
    
    def validate_file(self, file_path):
        """Validate file and return validation result"""
        try:
            # Check if it's a Google Sheets URL
            if file_path.startswith('http'):
                # Download and validate
                temp_file = self.download_google_sheet(file_path)
                try:
                    with open(temp_file, 'r', newline='') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        headers = next(csv_reader)
                        headers_upper = [h.upper() for h in headers]
                        
                        # Check mandatory columns
                        missing_columns = []
                        for col in self.mandatory_columns:
                            if col not in headers_upper:
                                missing_columns.append(col)
                        
                        return {
                            'valid': len(missing_columns) == 0,
                            'message': f"Missing columns: {missing_columns}" if missing_columns else "File is valid",
                            'headers': headers
                        }
                finally:
                    os.unlink(temp_file)
            else:
                # Local file validation
                if not os.path.exists(file_path):
                    return {
                        'valid': False,
                        'message': "File does not exist",
                        'headers': []
                    }
                
                with open(file_path, 'r', newline='') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    headers = next(csv_reader)
                    headers_upper = [h.upper() for h in headers]
                    
                    # Check mandatory columns
                    missing_columns = []
                    for col in self.mandatory_columns:
                        if col not in headers_upper:
                            missing_columns.append(col)
                    
                    return {
                        'valid': len(missing_columns) == 0,
                        'message': f"Missing columns: {missing_columns}" if missing_columns else "File is valid",
                        'headers': headers
                    }
        except Exception as e:
            return {
                'valid': False,
                'message': f"Error validating file: {str(e)}",
                'headers': []
            }
    
    def process_ingestion(self, reason, file_path, query_param_a, date):
        """Main method to process event ingestion"""
        processed_count = 0
        error_count = 0
        
        try:
            # Flush error file at start
            flush_error_file()
            
            # Determine if it's a Google Sheet or local file
            if file_path.startswith('http'):
                temp_file = self.download_google_sheet(file_path)
                csv_file_path = temp_file
                is_temp_file = True
            else:
                csv_file_path = file_path
                is_temp_file = False
            
            # Process the CSV file
            with open(csv_file_path, newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = {}
                
                for index, row in enumerate(csv_reader):
                    if index == 0:
                        headers = row
                        if not self.validate_headers(headers):
                            raise Exception("Mandatory columns missing")
                        continue
                    
                    try:
                        self.process_row(
                            self.get_row_with_headers(row, headers), 
                            reason, 
                            query_param_a, 
                            date
                        )
                        processed_count += 1
                    except Exception as e:
                        error_count += 1
                        self.error_handler.log_error(f"Error processing row {index}: {str(e)}")
            
            # Clean up temporary file if created
            if is_temp_file and os.path.exists(csv_file_path):
                os.unlink(csv_file_path)
            
            return {
                'processed_count': processed_count,
                'error_count': error_count
            }
            
        except Exception as e:
            self.error_handler.log_error(f"Error in process_ingestion: {str(e)}")
            raise
    
    def send_event_to_collector(self, details):
        """Send event to collector based on source"""
        source = details['source']
        
        if source == self.LINK_TRACKING_SOURCE:
            event = self.prepare_link_tracking_click(details)
            send_to_kafka(event, self.CLICKMETER_CLICK_KAFKA_TOPIC)
            print(str(event))
        elif source == self.TWO_PANE_SOURCE:
            event = self.prepare_two_pane_click(details)
            send_to_kafka(event, self.CLICKMETER_CLICK_KAFKA_TOPIC)
            print(str(event))
        elif source == self.COOKIE_SOURCE:
            event = self.prepare_cookie_conversion(details)
            send_to_kafka(event, self.CLICKMETER_CONVERSION_KAFKA_TOPIC)
            print(str(event))
        elif source == self.COOKIELESS_SOURCE:
            event = self.prepare_cookieless_conversion(details)
            send_to_kafka(event, self.CLICKMETER_CONVERSION_KAFKA_TOPIC)
            print(str(event))
        elif source == self.CLIENT_S2S_SOURCE:
            event = self.prepare_client_s2s_conversion(details)
            send_to_kafka(event, self.CLICKMETER_CONVERSION_KAFKA_TOPIC)
            print(str(event))
        else:
            error_message = 'unknown source to send the event to kafka'
            raise Exception(error_message)
    
    def get_time_stamp(self, datestr):
        """Generate timestamp from date string - matches original code logic"""
        day = int(datestr.split('-')[2])
        month = int(datestr.split('-')[1])
        year = int(datestr.split('-')[0])

        # Use random time like original code (10-15 hours)
        random_hour = random.randint(10, 15)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        random_datetime = datetime.datetime(year, month, day, random_hour, random_minute, random_second)
        epoch_timestamp = int(random_datetime.timestamp())

        return epoch_timestamp * 1000
    
    def get_user_fp(self, ip, user_agent):
        """Generate user fingerprint from IP and user agent"""
        return hashlib.md5(
            ip.encode('utf-8') + user_agent.encode('utf-8'),
        ).hexdigest()
    
    def get_params_from_url(self, url):
        """Extract parameters from URL"""
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)
        query_params_list = []
        
        for key in captured_value.keys():
            query_params_list.append(str(key) + "=" + str(captured_value.get(key)[0]))
        
        jz = captured_value.get("jz")[0] if captured_value.get("jz") else ""
        jx = captured_value.get("jx")[0] if captured_value.get("jx") else ""

        return {
            'url': url,
            'jz': jz,
            'jx': jx,
            'click_query_params': '&'.join(str(e) for e in query_params_list),
            'query_params': {
                'a': '3',  # This will be overridden by dynamic parameter
                'c': jz[1:5] if jz else ""
            }
        }
    
    def process_row(self, row, reason, query_param_a, date):
        """Process individual CSV row"""
        try:
            ref_number = row['REF_NUMBER']
            ip = row['IP']
            
            # Handle empty USER_AGENT with default value
            user_agent = row['USER_AGENT'].strip() if row['USER_AGENT'].strip() else self.default_user_agent
            
            # Handle empty USER_FP with default value
            user_fp = row['USER_FP'].strip() if row['USER_FP'].strip() else self.default_user_fp
            
            url = row['URL']
            
            # Handle empty SOURCE with default value
            source = row['SOURCE'].strip() if row['SOURCE'].strip() else self.default_source
            
            derived_params_from_url = self.get_params_from_url(url)
            jclick_id = str(uuid.uuid4())

            details = {
                "id": str(uuid.uuid4()),
                "url": derived_params_from_url['url'],
                "jz": derived_params_from_url['jz'],
                "jx": derived_params_from_url['jx'],
                "click_query_params": derived_params_from_url['click_query_params'],
                "query_params": derived_params_from_url['query_params'],
                'timestamp': self.get_time_stamp(date),
                'ref_number': ref_number,
                'ip': ip,
                'user_agent': user_agent,
                'user_fp': user_fp if user_fp else self.get_user_fp(ip, user_agent),
                'reason': reason,
                'jclick_id': jclick_id,
                'source': source
            }

            # Update query_params with dynamic 'a' value
            details['query_params']['a'] = query_param_a

            self.send_event_to_collector(details)

        except Exception as e:
            error_message = 'Error processing row - ' + str(row) + ' with exception ' + str(e)
            handle_error(None, row, e)
            print(error_message)
            raise
    
    def validate_headers(self, row):
        """Validate CSV headers"""
        for column in self.mandatory_columns:
            if column not in [element.upper() for element in row]:
                print('Mandatory column - ' + str(column) + ' not present in the sheet headers')
                return False
        return True
    
    def get_row_with_headers(self, row, headers):
        """Map row data to headers"""
        response = {}
        for index in range(len(headers)):
            response[headers[index].upper()] = row[index]
        return response
    
    # Event preparation methods (these would need to be implemented based on your business logic)
    def prepare_link_tracking_click(self, details):
        event = {
            "cookie_event": True,
            "eventSource": "LINK_TRACKING",
            "event_timestamp": details['timestamp'],
            "id": details['reason'] + '_' + details['jclick_id'],
            "ip": details['ip'],
            "jclick_id": details['jclick_id'],
            "jx": details['jx'],
            "jz": details['jz'],
            "pixel_hashid": details['jz'][1:5],
            "query_parameters": details['query_params'],
            "request_url": details['url'],
            "shadow_event": False,
            "user_agent": details['user_agent'],
            "user_fp": details['user_fp'],
            "reason": details['reason']
        }
        return event
    
    def prepare_two_pane_click(self, details):
        event = {
            "cookie_event": True,
            "eventSource": "TWO_PANE",
            "event_timestamp": details['timestamp'],
            "id": details['reason'] + '_' + details['jclick_id'],
            "ip": details['ip'],
            "jclick_id": details['jclick_id'],
            "jx": details['jx'],
            "jz": details['jz'],
            "pixel_hashid": details['jz'][1:5],
            "query_parameters": details['query_params'],
            "request_url": details['url'],
            "shadow_event": False,
            "user_agent": details['user_agent'],
            "user_fp": details['user_fp'],
            "reason": details['reason']
        }
        return event
    
    def prepare_cookie_conversion(self, details):
        event = {
            "click_event_id": None,
            "click_event_query_parameters": details['click_query_params'],
            "conv_type": "3", # TODO
            "cookie_event": True,
            "event_timestamp": details['timestamp'],
            "family_pixel_hashid": None,
            "id": details['reason'] + '_' + details['jclick_id'],
            "ip": details['ip'],
            "jclick_id": details['jclick_id'],
            "jx": details['jx'],
            "jz": details['jz'],
            "pixel_hashid": details['jz'][1:5],
            "pixel_s2s_event": False,
            "query_parameters": details['query_params'],
            "ref_number": details['ref_number'],
            "referrer_url": None,
            "shadow_event": False,
            "user_agent": details['user_agent'],
            "user_fp": details['user_fp'],
            "reason": details['reason']
        }
        return event
    
    def prepare_cookieless_conversion(self, details):
        event = {
            "click_event_id": None,
            "click_event_query_parameters": details['click_query_params'],
            "conv_type": "3", # TODO
            "cookie_event": False,
            "cookieless_event": True,
            "cp11": "1",
            "cp12": details['timestamp'],
            "cp13": "1",
            "cp14": "0",
            "event_timestamp": details['timestamp'],
            "family_pixel_hashid": None,
            "id": details['reason'] + '_' + details['jclick_id'],
            "ip": details['ip'],
            "jclick_id": details['jclick_id'],
            "jx": details['jx'],
            "jz": details['jz'],
            "pixel_hashid": details['jz'][1:5],
            "query_parameters": details['query_params'],
            "ref_number": details['ref_number'],
            "referrer_url": None,
            "user_agent": details['user_agent'],
            "user_fp": details['user_fp'],
            "reason": details['reason']
        }
        return event
    
    def prepare_client_s2s_conversion(self, details):
        event = {
            "click_event_id": None,
            "click_event_query_parameters": details['click_query_params'],
            "client_s2s_event": True,
            "conv_type": "3", # TODO
            "event_timestamp": details['timestamp'],
            "id": details['reason'] + '_' + details['jclick_id'] + '_s2s',
            "ip": details['ip'],
            "jclick_id": details['jclick_id'],
            "jx": details['jx'],
            "jz": details['jz'],
            "query_parameters": details['query_params'],
            "shadow_event": False,
            "user_agent": details['user_agent'],
            "user_fp": details['user_fp'],
            "reason": details['reason']
        }
        return event
