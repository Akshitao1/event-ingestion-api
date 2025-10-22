from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import requests
import pandas as pd
from datetime import datetime
import logging
import json
from dotenv import load_dotenv
from service.event_ingestion_service import EventIngestionService
from utils.error_handler import ErrorHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize services
event_service = EventIngestionService()
error_handler = ErrorHandler()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Check Kafka connectivity
    kafka_status = "connected"
    try:
        from service.kafka_client import get_kafka_client
        client = get_kafka_client()
        if not client.producer:
            kafka_status = "disconnected"
    except Exception:
        kafka_status = "disconnected"
    
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "kafka_status": kafka_status,
        "environment": {
            "kafka_url": os.getenv('KAFKA_URL', 'not_set'),
            "snowflake_account": os.getenv('SNOWFLAKE_ACCOUNT', 'not_set')
        }
    })

@app.route('/api/ingest', methods=['POST'])
def ingest_events():
    """
    Main endpoint for event ingestion
    Expected payload:
    {
        "reason": "JTSE-12345",
        "file_path": "path/to/file.csv" or "https://docs.google.com/spreadsheets/...",
        "query_param_a": "3",
        "date": "2024-04-04"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['reason', 'file_path', 'query_param_a', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}",
                    "status": "error"
                }), 400
        
        # Validate date format
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "error": "Invalid date format. Use YYYY-MM-DD",
                "status": "error"
            }), 400
        
        # Process the ingestion
        result = event_service.process_ingestion(
            reason=data['reason'],
            file_path=data['file_path'],
            query_param_a=data['query_param_a'],
            date=data['date']
        )
        
        return jsonify({
            "status": "success",
            "message": "Events processed successfully",
            "processed_count": result.get('processed_count', 0),
            "error_count": result.get('error_count', 0)
        })
        
    except Exception as e:
        logger.error(f"Error in ingest_events: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/validate-file', methods=['POST'])
def validate_file():
    """
    Validate file before processing
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        if not file_path:
            return jsonify({
                "error": "file_path is required",
                "status": "error"
            }), 400
        
        validation_result = event_service.validate_file(file_path)
        
        return jsonify({
            "status": "success",
            "valid": validation_result['valid'],
            "message": validation_result['message'],
            "headers": validation_result.get('headers', [])
        })
        
    except Exception as e:
        logger.error(f"Error in validate_file: {str(e)}")
        return jsonify({
            "error": f"Error validating file: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/processed-events', methods=['GET'])
def get_processed_events():
    """
    Get list of processed events (for debugging/viewing)
    """
    try:
        # Read the actual processed events from the log file
        import json
        import os
        
        log_file = "processed_events.log"
        processed_events = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            event_data = json.loads(line.strip())
                            processed_events.append(event_data)
                        except json.JSONDecodeError:
                            continue
        
        if not processed_events:
            return jsonify({
                "status": "success",
                "processed_events": [],
                "total_count": 0,
                "note": "No processed events found. Run event ingestion first."
            })
        
        return jsonify({
            "status": "success",
            "processed_events": processed_events,
            "total_count": len(processed_events),
            "note": "These are the actual processed events from the log file"
        })
        
    except Exception as e:
        logger.error(f"Error getting processed events: {str(e)}")
        return jsonify({
            "error": f"Error retrieving events: {str(e)}",
            "status": "error"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "status": "error"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": "error"}), 500

@app.teardown_appcontext
def close_connections(error):
    """Close database connections on app teardown"""
    try:
        from service.kafka_client import get_kafka_client
        client = get_kafka_client()
        client.close()
    except Exception as e:
        logger.error(f"Error closing Kafka client: {str(e)}")
    
    try:
        from service.snowflake_client import snowflake_client
        snowflake_client.close()
    except Exception as e:
        logger.error(f"Error closing Snowflake client: {str(e)}")

if __name__ == '__main__':
    # For local development
    # Set environment variables if not already set
    if not os.getenv('KAFKA_URL'):
        logger.warning("KAFKA_URL environment variable not set")
    if not os.getenv('SNOWFLAKE_ACCOUNT'):
        logger.warning("SNOWFLAKE_ACCOUNT environment variable not set")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
else:
    # For Vercel deployment
    # Vercel will handle the server
    pass
