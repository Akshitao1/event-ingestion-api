# Deployment Guide

## Vercel Deployment Steps

### 1. Prepare Your Project
All necessary files have been created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Vercel entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Git ignore rules
- ✅ `README.md` - Project documentation

### 2. Create GitHub Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit for Vercel deployment"

# Create repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/event-ingestion-api.git
git branch -M main
git push -u origin main
```

### 3. Deploy to Vercel

1. **Go to**: https://vercel.com/dashboard
2. **Click**: "New Project"
3. **Import Git Repository**: Select your GitHub repository
4. **Framework Preset**: Python
5. **Click**: "Deploy"

### 4. Set Environment Variables

In Vercel dashboard → Your project → Settings → Environment Variables:

```
KAFKA_URL = b-1.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092,b-2.trkdatapipelinekafkav.b4dp67.c16.kafka.us-east-1.amazonaws.com:9092

SNOWFLAKE_ACCOUNT = vya01839.us-east-1
SNOWFLAKE_PASSWORD = KX8Qqz25CS
SNOWFLAKE_PRIVATE_KEY = -----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPzCw/iZ0C/bdz\nw6Hqlzvo9QNTYyiWULw9Yz4VPiO+5zyJKBzEqOc6yNBnox0AcqpzyYzjQlyp/eUf\nsoonTt18v4KE26VrxA/QfeXnxd6Cn5i0RTGGkwBzpqmNz9Sfqan8LLwnmrqdu60r\n/XMlbXy0QVtZC/YwMuxMW5cG7zoPcszCSlztYibmCuJQulxo4icnLE2KkAj7H5cx\nuqiMOO6kec0ytycuXG/0VRorXN4gC2zCAldyD+6jVffR9ywdEqy+1Gb23RfM+sSk\nWUdrAftr2x5x0cz8onQYkHpj8gUmjkX5+z5XpSbVnIRD6l2s+wOBj2633vop0cRX\nr2VrBBtZAgMBAAECggEAC09SjTbBO/txM7TPKESI9zn2r2AzQlMsm66+H0vdiDNv\nwQtU3YNP6owpg6qGFpMnIdwzdd8TyhDOmrYN/Ou29GY8BV0rGL14GuHvVHkZjkR/\nfDhT5L41hRXqHpTUPshuPxJ0PzeVtqYTW9SUotHdurXf8e3LvX3YDKPjiXYV0+dT\njjtTqFaYi0oREwWzKbH5IbQK1MapBPv3knGceF1f1DSBaImbdCXQBCAZCJi/hA4b\ngDHr6LV9pVePfLiJgJS40aZZ18kW9fNC4LobeGyI73Y30KonuBdaygZLiyrNyxsB\nF4P7kgWARaUQJ+nveRoBqB0avApg+UeNiBzY76pPHQKBgQDsnR9+aMDA9xfYeNY+\nGbWNBlPscW7yAhTtddHu92hFfo8y77CpWXIXUDH9bfeqzPnsfQMkxIG31QFlBtfS\nZvEcMuFtnSaQoUlNWzTm/ZXtoV8Ey6m1iG7AYcGKhx1DOnioASNFAp1Pt4OTBaHh\ngaJrRfkjKzNCspjLdJHszMLlCwKBgQDg0qQ9D9gYNz+pYSEuNrD03hZrzgYMKUV5\nQq2X7GJo348Nl2yw8uVPh+x8EiuP2U2s41xYvfZA7/mng7Xn4Jot+y3KC31YqVhE\n+fth5X3BSRMCsP7wwLPReJQeDHX0GGFkFsQWeFX5xYKsIaQI1XnXTyAaO9nKlK6L\nGsfY5Td3qwKBgQCrBwt7qKYjFLfEvdtGOfkTvY4t6vQhs8WCutYK4AQbr1Y8oCpW\nzpN8LHhl0fXiHJVODjKWgf+tbCa86oxXxhbjphdxztTQV/SPGK0NhiC4ChuPcNLz\np3E+V6q4wd8x9/K8pU3kFPa2Z1SQkdKoGLbYyVRCyngb7tIoxdKwknURbwKBgAzo\nq1uCNGM3kOU12YTgyQpWUi1AeCJsoDuVM4h8ny3sYDdkkW4blEUbxd1d4bhxvr8F\nkwDZb3FNFiWjL2ewAspPGNL4E+tqVdIoFGILnkvh2UCXTxwdxHVrmf2bs44fdEAd\n+oZbxHwB9j3R9Kw5LbTKK0q2UwwJu3frQrxWdPffAoGAIY7sF5qtrc47MgAmQ6nD\n0lELC6TKKWhhU8TDpOB/Qy/K847KiNYmrsGMdKtK0ScZ7euOEhII8/jMBJ8NRAxJ\nQWs6NZV6J1DTSGgm3By8E9kCbZg5OLQZeOmoTKE5o/aytja3DIJPib+QEQBt9j+L\nKE8nrS63XO4pe8tBvbHcbq4=\n-----END PRIVATE KEY-----

SNOWFLAKE_USERNAME = EXT_VERCEL_SSH_USER
SNOWFLAKE_URL = vya01839.us-east-1.snowflakecomputing.com

GOOGLE_SERVICE_ACCOUNT_KEY = {"type": "service_account", "project_id": "eventingestion", "private_key_id": "YOUR_PRIVATE_KEY_ID", "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n", "client_email": "event-ingestion-service@eventingestion.iam.gserviceaccount.com", "client_id": "YOUR_CLIENT_ID", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/event-ingestion-service%40eventingestion.iam.gserviceaccount.com", "universe_domain": "googleapis.com"}
```

### 5. Test Your Deployment

```bash
# Test health endpoint
curl https://your-project-name.vercel.app/health

# Test event ingestion
curl -X POST https://your-project-name.vercel.app/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "vercel-test",
    "file_path": "https://docs.google.com/spreadsheets/d/1qgOZD8peOf5bOMR6fTJ4Dhx3CNtRp8pXSapKQYXwPR4/edit?gid=0#gid=0",
    "query_param_a": "3",
    "date": "2025-10-22"
  }'
```

## Important Notes

### Vercel Limitations
- **Serverless functions** have execution time limits (10 seconds for Hobby plan)
- **Cold starts** may cause initial delays
- **Kafka connectivity** might need VPN (consider using AWS Lambda for better Kafka integration)

### Production Considerations
- Monitor function execution times
- Consider using AWS Lambda for better Kafka integration
- Set up proper monitoring and alerting
- Use custom domain for production

## Troubleshooting

### Common Issues
1. **Environment variables not set** - Check Vercel dashboard
2. **Kafka connection timeout** - Verify VPN connectivity
3. **Google Sheets API errors** - Check service account permissions
4. **Function timeout** - Optimize code or upgrade Vercel plan

### Debug Steps
1. Check Vercel function logs
2. Test locally with same environment variables
3. Verify all external service connections
4. Check API rate limits
