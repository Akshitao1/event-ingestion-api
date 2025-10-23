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
KAFKA_URL = your-kafka-broker-url
GOOGLE_SERVICE_ACCOUNT_KEY = your-google-service-account-json
FORCE_DEV_MODE = false
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
