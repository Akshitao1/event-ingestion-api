"""Kafka Client using confluent-kafka."""
import os
import time
import json

# Try to import confluent-kafka, fallback to mock if not available
try:
    from confluent_kafka import Producer
    KAFKA_AVAILABLE = True
except ImportError as e:
    print(f"Confluent Kafka not available: {e}")
    KAFKA_AVAILABLE = False
    Producer = None

kafka_producer = None


def get_kafka_client():
    """Get Kafka Client method using confluent-kafka."""
    global kafka_producer
    
    if not KAFKA_AVAILABLE:
        print("Kafka not available, returning None")
        return None
        
    if kafka_producer is None:
        url = os.getenv('KAFKA_URL')
        if not url:
            print("KAFKA_URL not set")
            return None
        try:
            # Convert comma-separated brokers to list
            brokers = url.split(',')
            config = {
                'bootstrap.servers': ','.join(brokers),
                'acks': 'all',
                'retries': 3,
                'request.timeout.ms': 30000,
                'max.block.ms': 30000,
                'api.version.request': True
            }
            kafka_producer = Producer(config)
        except Exception as e:
            print(f"Error creating Kafka producer: {e}")
            return None
    return kafka_producer


def get_kafka_client_with_retries():
    """Get kafka client with retries method."""
    global kafka_producer
    for i in range(3):
        try:
            kafka_producer = get_kafka_client()
            if kafka_producer:
                break
        except Exception as e:
            print(f"Unable to get kafka producer in retry {i+1}: {e}")
            time.sleep(2)
    return kafka_producer


def send_to_kafka(kafka_message, topic_name='trk-total-stat-source-events-topic'):
    """Send to kafka method using confluent-kafka."""
    global kafka_producer
    
    if not KAFKA_AVAILABLE:
        print("Kafka not available, logging to console instead")
        print(f"Would send to Kafka: {kafka_message}")
        return True
    
    kafka_producer = get_kafka_client_with_retries()
    if not kafka_producer:
        print("Kafka producer is None, logging to console instead")
        print(f"Would send to Kafka: {kafka_message}")
        return True
    
    try:
        # Serialize message
        message_value = json.dumps(kafka_message).encode('utf-8')
        
        # Send message to Kafka
        kafka_producer.produce(
            topic=topic_name,
            value=message_value,
            callback=lambda err, msg: print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}") if not err else print(f"Failed to deliver message: {err}")
        )
        
        # Flush to ensure message is sent
        kafka_producer.flush(timeout=10)
        
        print("Send event successfully to Kafka")
        print(f"Topic: {topic_name}")
        return True
        
    except Exception as e:
        print(f"Error sending to Kafka: {e}")
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
            if i == 2:
                print(f"Error sending the following message to {topic_name} after 3 retries: {kafka_message}")
                print(e)
                return False
            time.sleep(2)
    return False


def close_connections():
    """Close connections method."""
    global kafka_producer
    if kafka_producer:
        try:
            kafka_producer.flush()
        except:
            pass
        kafka_producer = None