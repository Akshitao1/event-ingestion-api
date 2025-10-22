"""Kafka Client."""
import os
import time
import json

from kafka import KafkaProducer

kafka_producer = None


def get_kafka_client():
    """Get Kafka Client method."""
    global kafka_producer
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
    kafka_producer = get_kafka_client_with_retries()
    if kafka_producer is None or kafka_producer._closed:
        raise Exception("Kafka producer is None or closed")
    
    try:
        future = kafka_producer.send(topic_name, kafka_message)
        result = future.get(timeout=10)
        return True
    except Exception as e:
        raise e


def send_to_kafka_with_three_retries(kafka_message, topic_name):
    """Send to kafka with three retries method."""
    for i in range(3):
        try:
            send_to_kafka(kafka_message, topic_name)
            break
        except Exception as e:
            if i == 2:
                raise e