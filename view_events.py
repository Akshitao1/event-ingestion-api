#!/usr/bin/env python3
"""
View processed events from the log file
"""
import json
import os
from datetime import datetime

def view_processed_events():
    """Display processed events from the log file"""
    log_file = "processed_events.log"
    
    if not os.path.exists(log_file):
        print("❌ No processed events found.")
        print("Run the event ingestion first to generate events.")
        return
    
    print("📊 Processed Events Log")
    print("=" * 80)
    
    try:
        with open(log_file, 'r') as f:
            events = []
            for line in f:
                if line.strip():
                    try:
                        event_data = json.loads(line.strip())
                        events.append(event_data)
                    except json.JSONDecodeError:
                        continue
            
            if not events:
                print("No valid events found in log file.")
                return
            
            print(f"Found {len(events)} processed events:\n")
            
            for i, event_data in enumerate(events, 1):
                print(f"Event #{i}")
                print(f"  Timestamp: {event_data.get('timestamp', 'unknown')}")
                print(f"  Topic: {event_data.get('topic', 'unknown')}")
                print(f"  Status: {event_data.get('status', 'unknown')}")
                
                event = event_data.get('event', {})
                print(f"  Event ID: {event.get('id', 'unknown')}")
                print(f"  Ref Number: {event.get('ref_number', 'unknown')}")
                print(f"  IP: {event.get('ip', 'unknown')}")
                print(f"  Source: {event.get('source', 'unknown')}")
                print(f"  Reason: {event.get('reason', 'unknown')}")
                print(f"  URL: {event.get('url', 'unknown')[:50]}...")
                print(f"  User Agent: {event.get('user_agent', 'unknown')[:50]}...")
                print("-" * 80)
    
    except Exception as e:
        print(f"Error reading log file: {str(e)}")

def clear_events():
    """Clear the processed events log"""
    log_file = "processed_events.log"
    if os.path.exists(log_file):
        os.remove(log_file)
        print("✅ Processed events log cleared.")
    else:
        print("No log file to clear.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_events()
    else:
        view_processed_events()
