#!/usr/bin/env python3
"""
Simple server startup script
"""
import os
import sys

# Set environment variables
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['FORCE_DEV_MODE'] = 'false'  # Set to 'true' for development mode
os.environ['KAFKA_URL'] = 'b-1.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092,b-2.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092'
# Add Kafka authentication credentials (uncomment and set if needed)
# os.environ['KAFKA_USERNAME'] = 'your_actual_username'
# os.environ['KAFKA_PASSWORD'] = 'your_actual_password'
os.environ['SNOWFLAKE_ACCOUNT'] = 'vya01839.us-east-1'
os.environ['SNOWFLAKE_PASSWORD'] = 'KX8Qqz25CS'
os.environ['SNOWFLAKE_PRIVATE_KEY'] = '-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPzCw/iZ0C/bdz\\nw6Hqlzvo9QNTYyiWULw9Yz4VPiO+5zyJKBzEqOc6yNBnox0AcqpzyYzjQlyp/eUf\\nsoonTt18v4KE26VrxA/QfeXnxd6Cn5i0RTGGkwBzpqmNz9Sfqan8LLwnmrqdu60r\\n/XMlbXy0QVtZC/YwMuxMW5cG7zoPcszCSlztYibmCuJQulxo4icnLE2KkAj7H5cx\\nuqiMOO6kec0ytycuXG/0VRorXN4gC2zCAldyD+6jVffR9ywdEqy+1Gb23RfM+sSk\\nWUdrAftr2x5x0cz8onQYkHpj8gUmjkX5+z5XpSbVnIRD6l2s+wOBj2633vop0cRX\\nr2VrBBtZAgMBAAECggEAC09SjTbBO/txM7TPKESI9zn2r2AzQlMsm66+H0vdiDNv\\nwQtU3YNP6owpg6qGFpMnIdwzdd8TyhDOmrYN/Ou29GY8BV0rGL14GuHvVHkZjkR/\\nfDhT5L41hRXqHpTUPshuPxJ0PzeVtqYTW9SUotHdurXf8e3LvX3YDKPjiXYV0+dT\\njjtTqFaYi0oREwWzKbH5IbQK1MapBPv3knGceF1f1DSBaImbdCXQBCAZCJi/hA4b\\ngDHr6LV9pVePfLiJgJS40aZZ18kW9fNC4LobeGyI73Y30KonuBdaygZLiyrNyxsB\\nF4P7kgWARaUQJ+nveRoBqB0avApg+UeNiBzY76pPHQKBgQDsnR9+aMDA9xfYeNY+\\nGbWNBlPscW7yAhTtddHu92hFfo8y77CpWXIXUDH9bfeqzPnsfQMkxIG31QFlBtfS\\nZvEcMuFtnSaQoUlNWzTm/ZXtoV8Ey6m1iG7AYcGKhx1DOnioASNFAp1Pt4OTBaHh\\ngaJrRfkjKzNCspjLdJHszMLlCwKBgQDg0qQ9D9gYNz+pYSEuNrD03hZrzgYMKUV5\\nQq2X7GJo348Nl2yw8uVPh+x8EiuP2U2s41xYvfZA7/mng7Xn4Jot+y3KC31YqVhE\\n+fth5X3BSRMCsP7wwLPReJQeDHX0GGFkFsQWeFX5xYKsIaQI1XnXTyAaO9nKlK6L\\nGsfY5Td3qwKBgQCrBwt7qKYjFLfEvdtGOfkTvY4t6vQhs8WCutYK4AQbr1Y8oCpW\\nzpN8LHhl0fXiHJVODjKWgf+tbCa86oxXxhbjphdxztTQV/SPGK0NhiC4ChuPcNLz\\np3E+V6q4wd8x9/K8pU3kFPa2Z1SQkdKoGLbYyVRCyngb7tIoxdKwknURbwKBgAzo\\nq1uCNGM3kOU12YTgyQpWUi1AeCJsoDuVM4h8ny3sYDdkkW4blEUbxd1d4bhxvr8F\\nkwDZb3FNFiWjL2ewAspPGNL4E+tqVdIoFGILnkvh2UCXTxwdxHVrmf2bs44fdEAd\\n+oZbxHwB9j3R9Kw5LbTKK0q2UwwJu3frQrxWdPffAoGAIY7sF5qtrc47MgAmQ6nD\\n0lELC6TKKWhhU8TDpOB/Qy/K847KiNYmrsGMdKtK0ScZ7euOEhII8/jMBJ8NRAxJ\\nQWs6NZV6J1DTSGgm3By8E9kCbZg5OLQZeOmoTKE5o/aytja3DIJPib+QEQBt9j+L\\nKE8nrS63XO4pe8tBvbHcbq4=\\n-----END PRIVATE KEY-----'
os.environ['SNOWFLAKE_USERNAME'] = 'EXT_VERCEL_SSH_USER'
os.environ['SNOWFLAKE_URL'] = 'vya01839.us-east-1.snowflakecomputing.com'

# Google Service Account - Set via environment variable in production
# os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'] = 'your-service-account-json-here'

print("Environment variables set successfully!")
print(f"KAFKA_URL: {os.getenv('KAFKA_URL')}")
print(f"SNOWFLAKE_ACCOUNT: {os.getenv('SNOWFLAKE_ACCOUNT')}")
print(f"SNOWFLAKE_URL: {os.getenv('SNOWFLAKE_URL')}")
print("\nStarting Flask server on http://localhost:5003")

# Import and run the Flask app
if __name__ == '__main__':
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5003)
