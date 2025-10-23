#!/usr/bin/env python3
"""
Test Kafka connection and infrastructure
"""
import os
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json

def test_kafka_connection():
    """Test connection to Kafka cluster"""
    print("Testing Kafka Infrastructure...")
    print("=" * 50)
    
    # Get Kafka URL from environment
    kafka_url = os.getenv('KAFKA_URL', 'YOUR_KAFKA_URL_HERE')
    bootstrap_servers = kafka_url.split(',')
    
    print(f"Kafka Servers: {bootstrap_servers}")
    
    try:
        # Test Producer Connection
        print("\n1. Testing Producer Connection...")
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            request_timeout_ms=10000,
            retries=3
        )
        
        # Test sending a message
        test_message = {"test": "connection", "timestamp": "2024-01-01"}
        future = producer.send('test_topic', test_message)
        
        try:
            record_metadata = future.get(timeout=10)
            print(f"✅ Producer connected successfully!")
            print(f"   Topic: {record_metadata.topic}")
            print(f"   Partition: {record_metadata.partition}")
            print(f"   Offset: {record_metadata.offset}")
        except Exception as e:
            print(f"❌ Producer test failed: {str(e)}")
            return False
        finally:
            producer.close()
        
        # Test Consumer Connection
        print("\n2. Testing Consumer Connection...")
        try:
            consumer = KafkaConsumer(
                'test_topic',
                bootstrap_servers=bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                consumer_timeout_ms=5000,
                auto_offset_reset='latest'
            )
            
            # Try to get metadata
            partitions = consumer.partitions_for_topic('test_topic')
            print(f"✅ Consumer connected successfully!")
            print(f"   Partitions for test_topic: {partitions}")
            
            consumer.close()
            
        except Exception as e:
            print(f"❌ Consumer test failed: {str(e)}")
            return False
        
        # Test Required Topics
        print("\n3. Testing Required Topics...")
        required_topics = ['clickmeter_click', 'clickmeter_conversion']
        
        for topic in required_topics:
            try:
                consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=bootstrap_servers,
                    consumer_timeout_ms=3000,
                    auto_offset_reset='latest'
                )
                
                partitions = consumer.partitions_for_topic(topic)
                if partitions:
                    print(f"✅ Topic '{topic}' exists with {len(partitions)} partitions")
                else:
                    print(f"⚠️  Topic '{topic}' may not exist or is empty")
                
                consumer.close()
                
            except Exception as e:
                print(f"❌ Topic '{topic}' test failed: {str(e)}")
                print(f"   This topic may not exist or may not be accessible")
        
        print("\n4. Testing Event Ingestion Topics...")
        # Test sending to actual topics
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                request_timeout_ms=10000
            )
            
            # Test clickmeter_click topic
            click_event = {
                "event_type": "link_tracking_click",
                "data": {
                    "id": "test-uuid",
                    "ref_number": "TEST_001",
                    "ip": "192.168.1.1",
                    "source": "LINK_TRACKING",
                    "reason": "TEST_CONNECTION"
                }
            }
            
            future = producer.send('clickmeter_click', click_event)
            record_metadata = future.get(timeout=10)
            print(f"✅ Successfully sent test event to clickmeter_click")
            print(f"   Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
            
            # Test clickmeter_conversion topic
            conversion_event = {
                "event_type": "cookie_conversion", 
                "data": {
                    "id": "test-uuid-2",
                    "ref_number": "TEST_002",
                    "ip": "192.168.1.2",
                    "source": "COOKIE",
                    "reason": "TEST_CONNECTION"
                }
            }
            
            future = producer.send('clickmeter_conversion', conversion_event)
            record_metadata = future.get(timeout=10)
            print(f"✅ Successfully sent test event to clickmeter_conversion")
            print(f"   Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
            
            producer.close()
            
        except Exception as e:
            print(f"❌ Event ingestion test failed: {str(e)}")
            return False
        
        print("\n🎉 All Kafka infrastructure tests passed!")
        print("Your Kafka cluster is ready for event ingestion.")
        return True
        
    except Exception as e:
        print(f"❌ Kafka connection failed: {str(e)}")
        print("\nPossible issues:")
        print("1. Network connectivity to AWS Kafka cluster")
        print("2. Security groups or firewall blocking access")
        print("3. Authentication/authorization issues")
        print("4. Kafka cluster not running or accessible")
        return False

if __name__ == "__main__":
    # Set environment variables
    os.environ['KAFKA_URL'] = 'YOUR_KAFKA_URL_HERE'
    
    test_kafka_connection()
