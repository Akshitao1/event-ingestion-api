#!/usr/bin/env python3
"""
Simple test script to run event ingestion
"""
import os
import requests
import json

# Set environment variables
os.environ['KAFKA_URL'] = 'b-1.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092,b-2.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092'
os.environ['SNOWFLAKE_ACCOUNT'] = 'vya01839.us-east-1'
os.environ['SNOWFLAKE_PASSWORD'] = 'KX8Qqz25CS'
os.environ['SNOWFLAKE_PRIVATE_KEY'] = '-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzb7gWbj+g7egx\\nJ/AmyluQHHvgV4BjwLInKE8+qIhvdZR4snqUiOF+t1fEoNM01OtbwAYMhrT5EWfq\\nHizQertShTuRjSupRxErnjdx0J40+ZZLlzOtNl7yhKwhyqKTj9UrgP4yHnWrilD0\\nX/cyV25/MbHgPKU2czeL9GcC4KMHRW+BeJAV52F7nfaEeT+QTaYH9m1h90Ttlk7z\\ntGcZc2/hlkPuOpEnAJuK9cHCxh4cOCTWnbMp1VDVvuuXvqGgEbSP5qOsOws65oe6\\nNkozC3z9bZS7DDv9bvZRcDRqd3l0pYvpwHntPMtEz/edZRFwEtKIE68l8NblprO4\\n6kDJ8C9fAgMBAAECggEAHykWieapbBQEj4zE+qeHkRYxOPtZE3miNoSchmAUGW8M\\n0o0EFolSx4OlXUMkinczTCKjqkc2ZE5ugkytMaMuppz2hEdEvsfVpoJ6VGyLHN3/\\nCK+ATOM1R95cWh3rb765oS1sd12sx5ZkipujvP1L9hC2OB+v/S2zBr3xqaFDDn7o\\no3WSN1DgLpZ/fj1SVGzxz6z+zttcmmjoVKakSiU2JNCskiPUfDnszjZvTtuDEYh0\\n1UYg6QSY9/2Iviud6lqcCEVVTZikINN/4ydDVFj6sN97vRnB8qts8JKy9usgTAAR\\n5XjnHvi9lf/5hUc2w7IKuBJbNbf6CLrk8GZbtA1xUQKBgQDrUNiizmyhZJo/O3JX\\nHah/2NjDoPnaLBFrzRoRSOBYINEdxGq5YF2OcPptitNI3sIe4z52OZfgihC9+J5C\\nj7wbHb+ig8TPm28lwqcdyjtSCdUiNKSR4cgmltTH7EUvxM3b8fldlIA+9y+2IOKQ\\n7dggcFzBIIKYgTjOYS4tkDs3twKBgQDDNXTE1pT3ezVVyAH4Firp15j2WRaINIo/\\nIx3yYAzYI/LY8marzLNyxQSVqx64Pqnz6rZ8l5TIHroPk6WIHYa9QipMVVaAJobG\\nV2a4FMUfXuLdclRXY6r1hKzvKsP5Z36o8AtjVt9mkJOxUapWVc8IJpTHMg3GK6Jt\\nCkhMThU1mQKBgQC3afqRW6hcW9fGdYV31Ywiqli6ktxsa3Dgv6sT0ePbjSixtQki\\nmLQTdIgdndl1sPtJrAJhkB6LS9Ik4IYqh3ItCJD4ERD0aMjHe+NaWujF1xgjYzjq\\n5DtnqKUNd2GuDA4Q45hkkn0rluu/X/54zIprLml9tuNUD1TBuAmQRh2CHQKBgGmR\\nVS7GJRWZigRz/6ycwGRp9gzzrN3IHCN86EsVapzRBBoTLTcnorwklBAk1J4rNVn1\\nyu6iQxHenBykalasMRvU1m8lj3wKWcSVq7VNdjU66VF87OO9wMy6DZPh+s28DKFr\\n/5yfdH1RHq48TfQWv7nWs4ruJMjQ/Cwf7W1mpM2xAoGAY9yPyKovic6j84q+ghIi\\nXjAQ7O0b3mY9OmLgwPT+J4+tiKO443u/eBSMDeeA8dAU3IwhZf8AjSxxXchea3WE\\nTY55tIyOMryL5tVr3sLi72WJy6YPK6K2nQ/8dIhgXkYK6uBsMLTD3JD7QsdCiTNj\\ndF1D1gNIw8PYWaacQlJgmek=\\n-----END PRIVATE KEY-----'
os.environ['SNOWFLAKE_URL'] = 'vya01839.us-east-1.snowflakecomputing.com'

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
