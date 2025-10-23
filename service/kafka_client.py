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
                bootstrap_servers=url, 
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                acks='all', 
                retries=3,
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
            print(
                "Unable to get kafka producer in retry number:-{} due to:-{}".format(
                    str(i), str(e)),
            )
            print(e)
            time.sleep(2)
    return kafka_producer


def send_to_kafka(kafka_message, topic_name='trk-total-stat-source-events-topic'):
    """Send to kafka method."""
    global kafka_producer
    
    # Get a fresh producer if needed
    kafka_producer = get_kafka_client_with_retries()
    if kafka_producer is None:
        raise Exception("Kafka producer is None")
    
    # Check if producer is closed and recreate if needed
    if hasattr(kafka_producer, '_closed') and kafka_producer._closed:
        kafka_producer = None
        kafka_producer = get_kafka_client()
    
    try:
        future = kafka_producer.send(topic_name, kafka_message)
        result = future.get(timeout=10)
        if result is None:
            print("failed to send following message to kafka:-{}".format(str(kafka_message)))
            raise Exception("Error sending message to kafka as fut.get() is None")
        else:
            print("Send event successfully - ")
    except Exception as e:
        print(f"Error sending to Kafka: {e}")
        # Try to recreate producer on error
        kafka_producer = None
        raise e


def send_to_kafka_with_three_retries(kafka_message, topic_name):  # noqa: C901
    """Send to kafka with three retries method."""
    for i in range(3):
        try:
            send_to_kafka(kafka_message, topic_name)
            break
        except Exception as e:
            if i == 2:
                print(
                    "Error sending the following message to {} after 3 retries:-{}".format(
                        topic_name, str(kafka_message),
                    ),
                )
                print(e)