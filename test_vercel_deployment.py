#!/usr/bin/env python3
"""
Test script for Vercel deployment
"""
import requests
import json
import sys

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Kafka Status: {data.get('kafka_status')}")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_ingest_endpoint(base_url):
    """Test the ingest endpoint with Google Sheets"""
    try:
        payload = {
            "reason": "vercel-deployment-test",
            "file_path": "https://docs.google.com/spreadsheets/d/1qgOZD8peOf5bOMR6fTJ4Dhx3CNtRp8pXSapKQYXwPR4/edit?gid=0#gid=0",
            "query_param_a": "3",
            "date": "2025-10-22"
        }
        
        response = requests.post(
            f"{base_url}/api/ingest",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30
        )
        
        print(f"Ingest Test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Processed Count: {data.get('processed_count')}")
            print(f"Error Count: {data.get('error_count')}")
            return True
        else:
            print(f"Ingest test failed: {response.text}")
            return False
    except Exception as e:
        print(f"Ingest test error: {e}")
        return False

def main():
    """Main test function"""
    if len(sys.argv) != 2:
        print("Usage: python test_vercel_deployment.py <vercel-url>")
        print("Example: python test_vercel_deployment.py https://your-project.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    print(f"Testing Vercel deployment at: {base_url}")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing Health Endpoint...")
    health_ok = test_health_endpoint(base_url)
    print()
    
    # Test ingest endpoint
    print("2. Testing Ingest Endpoint...")
    ingest_ok = test_ingest_endpoint(base_url)
    print()
    
    # Summary
    print("=" * 50)
    print("Test Summary:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Ingest Test: {'✅ PASS' if ingest_ok else '❌ FAIL'}")
    
    if health_ok and ingest_ok:
        print("\n🎉 All tests passed! Your Vercel deployment is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
