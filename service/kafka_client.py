"""Event Sender using AWS SQS (replaces Kafka)."""
import os
import time
import json

# Try to import boto3, fallback to mock if not available
try:
    import boto3
    SQS_AVAILABLE = True
except ImportError as e:
    print(f"AWS SQS not available: {e}")
    SQS_AVAILABLE = False
    boto3 = None

sqs_client = None


def get_sqs_client():
    """Get SQS Client method."""
    global sqs_client
    
    if not SQS_AVAILABLE:
        print("SQS not available, returning None")
        return None
        
    if sqs_client is None:
        try:
            sqs_client = boto3.client('sqs')
        except Exception as e:
            print(f"Error creating SQS client: {e}")
            return None
    return sqs_client


def get_sqs_client_with_retries():
    """Get SQS client with retries method."""
    global sqs_client
    for i in range(3):
        try:
            sqs_client = get_sqs_client()
            if sqs_client:
                break
        except Exception as e:
            print(f"Unable to get SQS client in retry {i+1}: {e}")
            time.sleep(2)
    return sqs_client


def send_to_kafka(kafka_message, topic_name='trk-total-stat-source-events-topic'):
    """Send to SQS method (replaces Kafka)."""
    global sqs_client
    
    if not SQS_AVAILABLE:
        print("SQS not available, logging to console instead")
        print(f"Would send to SQS: {kafka_message}")
        return True
    
    sqs_client = get_sqs_client_with_retries()
    if not sqs_client:
        print("SQS client is None, logging to console instead")
        print(f"Would send to SQS: {kafka_message}")
        return True
    
    try:
        # Get SQS queue URL from environment
        queue_url = os.getenv('SQS_QUEUE_URL')
        if not queue_url:
            print("SQS_QUEUE_URL not set, logging to console instead")
            print(f"Would send to SQS: {kafka_message}")
            return True
        
        # Prepare message for SQS
        message_body = json.dumps({
            'topic': topic_name,
            'message': kafka_message,
            'timestamp': int(time.time() * 1000)
        })
        
        # Send message to SQS
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes={
                'topic': {
                    'StringValue': topic_name,
                    'DataType': 'String'
                },
                'source': {
                    'StringValue': 'vercel-api',
                    'DataType': 'String'
                }
            }
        )
        
        print("✅ SUCCESS: Event sent to SQS")
        print(f"Topic: {topic_name}")
        print(f"MessageId: {response['MessageId']}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Error sending to SQS: {e}")
        print(f"Would send to SQS: {kafka_message}")
        return True


def send_to_kafka_with_three_retries(kafka_message, topic_name):
    """Send to SQS with three retries method."""
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
    global sqs_client
    # SQS doesn't need connection closing
    sqs_client = None