#!/usr/bin/env python3
"""
Simple test script to run event ingestion
"""
import os
import requests
import json

# Set environment variables
os.environ['KAFKA_URL'] = 'YOUR_KAFKA_URL_HERE'
os.environ['SNOWFLAKE_ACCOUNT'] = 'YOUR_SNOWFLAKE_ACCOUNT'
os.environ['SNOWFLAKE_PASSWORD'] = 'YOUR_SNOWFLAKE_PASSWORD'
os.environ['SNOWFLAKE_PRIVATE_KEY'] = 'YOUR_SNOWFLAKE_PRIVATE_KEY_HERE'
os.environ['SNOWFLAKE_URL'] = 'YOUR_SNOWFLAKE_URL'

BASE_URL = "http://localhost:5001"

def test_ingest():
    """Test event ingestion with correct date"""
    print("Testing Event Ingestion with 1 event...")
    print("=" * 50)
    
    # Clear any existing log
    if os.path.exists("processed_events.log"):
        os.remove("processed_events.log")
    
    payload = {
        "reason": "JTSE-12345",
        "file_path": "sample.csv",
        "query_param_a": "3",
        "date": "2025-10-21"  # Correct date matching CSV
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ingest", json=payload)
        result = response.json()
        print("Event Ingestion Result:")
        print(f"  Status: {result.get('status')}")
        print(f"  Processed Count: {result.get('processed_count')}")
        print(f"  Error Count: {result.get('error_count')}")
        print(f"  Message: {result.get('message')}")
        
        # Check processed events
        print("\nChecking Processed Events...")
        events_response = requests.get(f"{BASE_URL}/api/processed-events")
        events_result = events_response.json()
        
        print(f"  Total Events: {events_result.get('total_count', 0)}")
        print(f"  Note: {events_result.get('note', '')}")
        
        if events_result.get('processed_events'):
            event = events_result['processed_events'][0]
            print(f"\nFirst Event Details:")
            print(f"  ID: {event.get('id')}")
            print(f"  Ref Number: {event.get('ref_number')}")
            print(f"  IP: {event.get('ip')}")
            print(f"  Source: {event.get('source')}")
            print(f"  Reason: {event.get('reason')}")
            print(f"  Timestamp: {event.get('timestamp')}")
            print(f"  Date in timestamp: {event.get('timestamp', '')[:10]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_ingest()
