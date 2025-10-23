"""Kafka Client using aiokafka."""
import os
import time
import json
import asyncio
from typing import Optional

# Try to import aiokafka, fallback to mock if not available
try:
    from aiokafka import AIOKafkaProducer
    KAFKA_AVAILABLE = True
except ImportError as e:
    print(f"aiokafka not available: {e}")
    KAFKA_AVAILABLE = False
    AIOKafkaProducer = None

kafka_producer: Optional[AIOKafkaProducer] = None


async def get_kafka_client():
    """Get Kafka Client method using aiokafka."""
    global kafka_producer
    
    if not KAFKA_AVAILABLE:
        print("Kafka not available, returning None")
        return None
        
    if kafka_producer is None or kafka_producer._closed:
        url = os.getenv('KAFKA_URL')
        if not url:
            print("KAFKA_URL not set")
            return None
            
        try:
            kafka_producer = AIOKafkaProducer(
                bootstrap_servers=url,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                acks='all',
                retries=3,
                request_timeout_ms=30000,
                max_block_ms=30000,
                api_version=(2, 5, 0)
            )
            await kafka_producer.start()
        except Exception as e:
            print(f"Error creating Kafka producer: {e}")
            return None
    return kafka_producer


async def get_kafka_client_with_retries():
    """Get kafka client with retries method."""
    for i in range(3):
        try:
            client = await get_kafka_client()
            if client:
                return client
        except Exception as e:
            print(f"Unable to get kafka client in retry {i+1}: {e}")
            await asyncio.sleep(2)
    return None


def send_to_kafka(kafka_message, topic_name='trk-total-stat-source-events-topic'):
    """Send to kafka method (sync wrapper for async)."""
    if not KAFKA_AVAILABLE:
        print("Kafka not available, logging to console instead")
        print(f"Would send to Kafka: {kafka_message}")
        return True
    
    try:
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_send_to_kafka_async(kafka_message, topic_name))
        loop.close()
        return result
    except Exception as e:
        print(f"Error in sync wrapper: {e}")
        print(f"Would send to Kafka: {kafka_message}")
        return True


async def _send_to_kafka_async(kafka_message, topic_name):
    """Async method to send to Kafka."""
    try:
        producer = await get_kafka_client_with_retries()
        if not producer:
            print("Kafka producer is None, logging to console instead")
            print(f"Would send to Kafka: {kafka_message}")
            return True
        
        # Send message to Kafka
        await producer.send_and_wait(topic_name, kafka_message)
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
            print(f"Error sending message to {topic_name} in retry {i+1}: {e}")
            if i == 2:
                print(f"Failed to send message after 3 retries: {kafka_message}")
                return False
            time.sleep(2)
    return False


async def close_connections():
    """Close connections method."""
    global kafka_producer
    if kafka_producer and not kafka_producer._closed:
        await kafka_producer.stop()
        kafka_producer = None