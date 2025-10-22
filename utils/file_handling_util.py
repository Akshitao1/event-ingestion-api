import os
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

ERROR_FILE_PATH = "error_log.csv"

def handle_error(file_path, row_data, exception):
    """
    Handle errors during file processing
    
    Args:
        file_path: Path to the file being processed
        row_data: Row data that caused the error
        exception: Exception that occurred
    """
    try:
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'file_path': file_path or 'unknown',
            'row_data': str(row_data),
            'error': str(exception)
        }
        
        # Write error to CSV file
        file_exists = os.path.exists(ERROR_FILE_PATH)
        
        with open(ERROR_FILE_PATH, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'file_path', 'row_data', 'error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(error_entry)
        
        logger.error(f"Error logged: {str(exception)}")
        
    except Exception as e:
        logger.error(f"Failed to log error: {str(e)}")

def flush_error_file():
    """Clear the error log file"""
    try:
        if os.path.exists(ERROR_FILE_PATH):
            os.remove(ERROR_FILE_PATH)
            logger.info("Error file flushed successfully")
    except Exception as e:
        logger.error(f"Failed to flush error file: {str(e)}")

def get_error_log():
    """Get error log entries"""
    try:
        if not os.path.exists(ERROR_FILE_PATH):
            return []
        
        errors = []
        with open(ERROR_FILE_PATH, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                errors.append(row)
        
        return errors
    except Exception as e:
        logger.error(f"Failed to read error log: {str(e)}")
        return []
