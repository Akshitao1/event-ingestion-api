#!/usr/bin/env python3
"""
Simple server startup script
"""
import os
import sys

# Set environment variables
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['FORCE_DEV_MODE'] = 'false'  # Set to 'true' for development mode
# Set environment variables - Replace with your actual values
os.environ['KAFKA_URL'] = 'YOUR_KAFKA_URL_HERE'
# Add Kafka authentication credentials (uncomment and set if needed)
# os.environ['KAFKA_USERNAME'] = 'your_actual_username'
# os.environ['KAFKA_PASSWORD'] = 'your_actual_password'
os.environ['SNOWFLAKE_ACCOUNT'] = 'YOUR_SNOWFLAKE_ACCOUNT'
os.environ['SNOWFLAKE_PASSWORD'] = 'YOUR_SNOWFLAKE_PASSWORD'
os.environ['SNOWFLAKE_PRIVATE_KEY'] = 'YOUR_SNOWFLAKE_PRIVATE_KEY_HERE'
os.environ['SNOWFLAKE_USERNAME'] = 'YOUR_SNOWFLAKE_USERNAME'
os.environ['SNOWFLAKE_URL'] = 'YOUR_SNOWFLAKE_URL'

# Google Service Account - Set via environment variable in production
os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'] = 'YOUR_GOOGLE_SERVICE_ACCOUNT_KEY_HERE'

print("Environment variables set successfully!")
print(f"KAFKA_URL: {os.getenv('KAFKA_URL')}")
print(f"SNOWFLAKE_ACCOUNT: {os.getenv('SNOWFLAKE_ACCOUNT')}")
print(f"SNOWFLAKE_URL: {os.getenv('SNOWFLAKE_URL')}")
print("\nStarting Flask server on http://localhost:5003")

# Import and run the Flask app
if __name__ == '__main__':
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5003)
