#!/usr/bin/env python3
"""
Script to run the application with environment variables
This script sets the environment variables and starts the Flask app
"""

import os
import sys
import subprocess

def set_environment_variables():
    """Set environment variables from the provided configuration"""
    env_vars = {
        'PYTHONUNBUFFERED': '1',
        'KAFKA_URL': 'YOUR_KAFKA_URL_HERE',
        'SNOWFLAKE_ACCOUNT': 'YOUR_SNOWFLAKE_ACCOUNT',
        'SNOWFLAKE_PASSWORD': 'YOUR_SNOWFLAKE_PASSWORD',
        'SNOWFLAKE_PRIVATE_KEY': 'YOUR_SNOWFLAKE_PRIVATE_KEY_HERE',
        'SNOWFLAKE_URL': 'YOUR_SNOWFLAKE_URL'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"Set {key}")

def main():
    """Main function to run the application"""
    print("Setting environment variables...")
    set_environment_variables()
    
    print("Starting Flask application...")
    print("Environment variables configured:")
    print(f"KAFKA_URL: {os.getenv('KAFKA_URL')}")
    print(f"SNOWFLAKE_ACCOUNT: {os.getenv('SNOWFLAKE_ACCOUNT')}")
    print(f"SNOWFLAKE_URL: {os.getenv('SNOWFLAKE_URL')}")
    print("\nStarting server on http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()
