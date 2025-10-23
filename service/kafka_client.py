"""Kafka Client using REST API."""
import os
import time
import json
import requests

# Use Kafka REST API instead of kafka-python
KAFKA_AVAILABLE = True


def get_kafka_client():
    """Get Kafka Client method using REST API."""
    if not KAFKA_AVAILABLE:
        print("Kafka not available, returning None")
        return None
        
    # For REST API, we don't need a persistent client
    return "REST_API"


def get_kafka_client_with_retries():
    """Get kafka client with retries method."""
    for i in range(3):
        try:
            client = get_kafka_client()
            if client:
                return client
        except Exception as e:
            print(f"Unable to get kafka client in retry {i+1}: {e}")
            time.sleep(2)
    return None


def send_to_kafka(kafka_message, topic_name='trk-total-stat-source-events-topic'):
    """Send to kafka using REST API."""
    if not KAFKA_AVAILABLE:
        print("Kafka not available, logging to console instead")
        print(f"Would send to Kafka: {kafka_message}")
        return True
    
    try:
        # Use Kafka REST API
        kafka_url = os.getenv('KAFKA_URL')
        if not kafka_url:
            print("KAFKA_URL not set, logging to console instead")
            print(f"Would send to Kafka: {kafka_message}")
            return True
        
        # Extract broker URL (use first broker for REST API)
        broker_url = kafka_url.split(',')[0]
        rest_url = f"http://{broker_url}/topics/{topic_name}"
        
        # Prepare message for REST API
        message_data = {
            "records": [
                {
                    "value": kafka_message
                }
            ]
        }
        
        # Send to Kafka REST API
        response = requests.post(
            rest_url,
            json=message_data,
            headers={'Content-Type': 'application/vnd.kafka.json.v2+json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("Send event successfully to Kafka via REST API")
            print(f"Topic: {topic_name}")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Kafka REST API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending to Kafka via REST API: {e}")
        # Fallback to console logging
        print(f"Would send to Kafka: {kafka_message}")
        return True


def send_to_kafka_with_three_retries(kafka_message, topic_name):
    """Send to kafka with three retries method."""
    for i in range(3):
        try:
            success = send_to_kafka(kafka_message, topic_name)
            if success:
                return True
        except Exception as e:
            print(f"Error sending message to {topic_name} in retry {i+1}: {e}")
            if i == 2:
                print(f"Failed to send message after 3 retries: {kafka_message}")
                return False
            time.sleep(2)
    return False


def close_connections():
    """Close connections method."""
    # REST API doesn't need connection closing
    pass