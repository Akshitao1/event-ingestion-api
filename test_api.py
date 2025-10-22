import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:5002"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_validate_file():
    """Test file validation"""
    payload = {
        "file_path": "sample.csv"
    }
    response = requests.post(f"{BASE_URL}/api/validate-file", json=payload)
    print("File Validation:", response.json())

def test_ingest():
    """Test event ingestion"""
    payload = {
        "reason": "JTSE-12345",
        "file_path": "sample.csv",
        "query_param_a": "3",
        "date": "2025-10-21"
    }
    response = requests.post(f"{BASE_URL}/api/ingest", json=payload)
    print("Event Ingestion:", response.json())

def test_processed_events():
    """Test getting processed events"""
    response = requests.get(f"{BASE_URL}/api/processed-events")
    print("Processed Events (JSON):", response.text)
    print("Processed Events (Python):", response.json())

if __name__ == "__main__":
    print("Testing Event Ingestion API...")
    print("=" * 50)
    
    try:
        test_health()
        print()
        test_validate_file()
        print()
        test_ingest()
        print()
        test_processed_events()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on localhost:5001")
    except Exception as e:
        print(f"Error: {str(e)}")
