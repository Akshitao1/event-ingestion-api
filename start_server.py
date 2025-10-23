#!/usr/bin/env python3
"""
Simple server startup script
"""
import os
import sys

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

print("Environment variables loaded from .env file")
print("Starting Flask server on http://localhost:5003")

# Import and run the Flask app
if __name__ == '__main__':
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5003)
