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
        'KAFKA_URL': 'b-1.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092,b-2.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092',
        'SNOWFLAKE_ACCOUNT': 'vya01839.us-east-1',
        'SNOWFLAKE_PASSWORD': 'KX8Qqz25CS',
        'SNOWFLAKE_PRIVATE_KEY': '-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzb7gWbj+g7egx\\nJ/AmyluQHHvgV4BjwLInKE8+qIhvdZR4snqUiOF+t1fEoNM01OtbwAYMhrT5EWfq\\nHizQertShTuRjSupRxErnjdx0J40+ZZLlzOtNl7yhKwhyqKTj9UrgP4yHnWrilD0\\nX/cyV25/MbHgPKU2czeL9GcC4KMHRW+BeJAV52F7nfaEeT+QTaYH9m1h90Ttlk7z\\ntGcZc2/hlkPuOpEnAJuK9cHCxh4cOCTWnbMp1VDVvuuXvqGgEbSP5qOsOws65oe6\\nNkozC3z9bZS7DDv9bvZRcDRqd3l0pYvpwHntPMtEz/edZRFwEtKIE68l8NblprO4\\n6kDJ8C9fAgMBAAECggEAHykWieapbBQEj4zE+qeHkRYxOPtZE3miNoSchmAUGW8M\\n0o0EFolSx4OlXUMkinczTCKjqkc2ZE5ugkytMaMuppz2hEdEvsfVpoJ6VGyLHN3/\\nCK+ATOM1R95cWh3rb765oS1sd12sx5ZkipujvP1L9hC2OB+v/S2zBr3xqaFDDn7o\\no3WSN1DgLpZ/fj1SVGzxz6z+zttcmmjoVKakSiU2JNCskiPUfDnszjZvTtuDEYh0\\n1UYg6QSY9/2Iviud6lqcCEVVTZikINN/4ydDVFj6sN97vRnB8qts8JKy9usgTAAR\\n5XjnHvi9lf/5hUc2w7IKuBJbNbf6CLrk8GZbtA1xUQKBgQDrUNiizmyhZJo/O3JX\\nHah/2NjDoPnaLBFrzRoRSOBYINEdxGq5YF2OcPptitNI3sIe4z52OZfgihC9+J5C\\nj7wbHb+ig8TPm28lwqcdyjtSCdUiNKSR4cgmltTH7EUvxM3b8fldlIA+9y+2IOKQ\\n7dggcFzBIIKYgTjOYS4tkDs3twKBgQDDNXTE1pT3ezVVyAH4Firp15j2WRaINIo/\\nIx3yYAzYI/LY8marzLNyxQSVqx64Pqnz6rZ8l5TIHroPk6WIHYa9QipMVVaAJobG\\nV2a4FMUfXuLdclRXY6r1hKzvKsP5Z36o8AtjVt9mkJOxUapWVc8IJpTHMg3GK6Jt\\nCkhMThU1mQKBgQC3afqRW6hcW9fGdYV31Ywiqli6ktxsa3Dgv6sT0ePbjSixtQki\\nmLQTdIgdndl1sPtJrAJhkB6LS9Ik4IYqh3ItCJD4ERD0aMjHe+NaWujF1xgjYzjq\\n5DtnqKUNd2GuDA4Q45hkkn0rluu/X/54zIprLml9tuNUD1TBuAmQRh2CHQKBgGmR\\nVS7GJRWZigRz/6ycwGRp9gzzrN3IHCN86EsVapzRBBoTLTcnorwklBAk1J4rNVn1\\nyu6iQxHenBykalasMRvU1m8lj3wKWcSVq7VNdjU66VF87OO9wMy6DZPh+s28DKFr\\n/5yfdH1RHq48TfQWv7nWs4ruJMjQ/Cwf7W1mpM2xAoGAY9yPyKovic6j84q+ghIi\\nXjAQ7O0b3mY9OmLgwPT+J4+tiKO443u/eBSMDeeA8dAU3IwhZf8AjSxxXchea3WE\\nTY55tIyOMryL5tVr3sLi72WJy6YPK6K2nQ/8dIhgXkYK6uBsMLTD3JD7QsdCiTNj\\ndF1D1gNIw8PYWaacQlJgmek=\\n-----END PRIVATE KEY-----',
        'SNOWFLAKE_URL': 'vya01839.us-east-1.snowflakecomputing.com'
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
