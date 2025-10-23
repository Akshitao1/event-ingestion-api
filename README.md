# Event Ingestion API

A production-ready Flask API for processing event data from CSV files and Google Sheets, with Kafka integration for real-time event streaming.

## Features

- ✅ **Google Sheets Integration** - Process data directly from Google Sheets URLs
- ✅ **CSV File Processing** - Support for local CSV files
- ✅ **Kafka Production Integration** - Real-time event streaming to Kafka
- ✅ **Event Validation** - Comprehensive data validation and error handling
- ✅ **Service Account Authentication** - Secure Google Sheets access
- ✅ **Production Ready** - Deployed on Vercel with monitoring

## API Endpoints

### POST /api/ingest
Process event data from CSV or Google Sheets

**Request Body:**
```json
{
  "reason": "string",
  "file_path": "string",
  "query_param_a": "string", 
  "date": "string"
}
```

**Response:**
```json
{
  "status": "success",
  "processed_count": 1,
  "error_count": 0,
  "message": "Events processed successfully"
}
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "kafka_status": "connected",
  "timestamp": "2025-10-22T13:34:55.123456"
}
```

### GET /api/processed-events
Get processed events (development mode only)

## Environment Variables

```bash
KAFKA_URL=your-kafka-broker-url
GOOGLE_SERVICE_ACCOUNT_KEY=your-google-service-account-json
FORCE_DEV_MODE=false
```

## Google Sheets Setup

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account
4. Download the JSON key file
5. Share your Google Sheet with the service account email

## CSV Format

Required columns:
```
DATE,REF_NUMBER,IP,USER_AGENT,USER_FP,URL,SOURCE
```

Example:
```
2025-10-22,US_EN_97_043800_2250981,172.56.209.0,"Mozilla/5.0...",817d5da2-bb2c-4b05-ae98-c2f09cb1f8c75,https://example.com,COOKIE
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export KAFKA_URL=your-kafka-url
export GOOGLE_SERVICE_ACCOUNT_KEY='your-google-service-account-json'

# Run the server
python start_server.py
```

## Deployment

This project is configured for deployment on Vercel:

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

## Event Processing Logic

- **SOURCE = COOKIE AND a = 3**: `event_type = CONVERSION`, `conversion_type = APPLY`
- **SOURCE = COOKIE AND a = 2**: `event_type = CONVERSION`, `conversion_type = APPLY_START`  
- **SOURCE = COOKIE AND a = 1**: `event_type = CONVERSION`, `conversion_type = VIEW`
- **SOURCE = LINK_TRACKING**: `event_type = CLICK`

## Kafka Topics

- **Conversion Events**: `trk-jobcloud-conversion-destination-events-topic`
- **Click Events**: `trk-jobcloud-click-destination-events-topic`

## Error Handling

- Comprehensive error logging
- Graceful fallback to development mode
- Detailed error messages for debugging
- Thread-safe error persistence

## License

Private - Joveo Internal Use