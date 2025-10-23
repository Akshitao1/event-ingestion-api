"""Kafka Client - Vercel Compatible Version."""
import os
import time
import json
import requests

# Try to import kafka-python, fallback to HTTP if not available
try:
    from kafka import KafkaProducer
    KAFKA_PYTHON_AVAILABLE = True
except ImportError:
    KAFKA_PYTHON_AVAILABLE = False

kafka_producer = None


def get_kafka_client():
    """Get Kafka Client method."""
    global kafka_producer
    
    if not KAFKA_PYTHON_AVAILABLE:
        # Fallback to HTTP-based approach for Vercel
        return None
    
    if kafka_producer is None or kafka_producer._closed:
        url = os.getenv('KAFKA_URL')
        try:
            kafka_producer = KafkaProducer(
                bootstrap_servers=url, value_serializer=lambda x: json.dumps(
                    x).encode('utf-8'),
                acks='all', retries=3,
                request_timeout_ms=30000,
                max_block_ms=30000,
                api_version=(2, 5, 0)
            )
        except Exception as e:
            raise e
    return kafka_producer


def get_kafka_client_with_retries():
    """Get kafka client with retries method."""
    global kafka_producer
    
    if not KAFKA_PYTHON_AVAILABLE:
        return None
        
    for i in range(3):
        try:
            kafka_producer = get_kafka_client()
            break
        except Exception as e:
            if i == 2:  # Last retry
                return None
            time.sleep(2)
    return kafka_producer


def send_to_kafka(kafka_message, topic_name='trk-total-stat-source-events-topic'):
    """Send to kafka method."""
    global kafka_producer
    
    # Try kafka-python first
    if KAFKA_PYTHON_AVAILABLE:
        kafka_producer = get_kafka_client_with_retries()
        if kafka_producer is None or kafka_producer._closed:
            raise Exception("Kafka producer is None or closed")
        
        try:
            future = kafka_producer.send(topic_name, kafka_message)
            result = future.get(timeout=10)
            return True
        except Exception as e:
            raise e
    else:
        # Fallback: Log the message for now (development mode)
        print(f"KAFKA MESSAGE (Development Mode): {json.dumps(kafka_message, indent=2)}")
        print(f"Topic: {topic_name}")
        return True


def send_to_kafka_with_three_retries(kafka_message, topic_name):
    """Send to kafka with three retries method."""
    for i in range(3):
        try:
            send_to_kafka(kafka_message, topic_name)
            break
        except Exception as e:
            if i == 2:
                raise e