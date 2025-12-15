# Backend Deployment Guide - Render

Complete guide for deploying the Physical AI Textbook Backend to Render.

## Prerequisites

1. **Render Account**: Sign up at https://render.com
2. **Neon Database**: PostgreSQL database from https://neon.tech
3. **Qdrant Cloud**: Vector database from https://cloud.qdrant.io
4. **OpenAI API Key**: From https://platform.openai.com/api-keys
5. **GitHub Repository**: Push your code to GitHub

## Step-by-Step Deployment

### Step 1: Prepare Environment Variables

You'll need these environment variables for Render:

```bash
# Required
DATABASE_URL=postgresql://user:password@host.neon.tech:5432/database
QDRANT_URL=https://your-cluster.gcp.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
OPENAI_API_KEY=sk-your-openai-api-key

# Optional (defaults provided)
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
QDRANT_COLLECTION_NAME=textbook_embeddings
QDRANT_VECTOR_SIZE=1536
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

### Step 2: Deploy to Render

#### Option A: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Go to https://dashboard.render.com/
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml`
6. Add environment variables in Render Dashboard
7. Click "Deploy"

#### Option B: Manual Web Service

1. Go to https://dashboard.render.com/
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: physical-ai-textbook-backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid for better performance)
5. Add Environment Variables (see Step 1)
6. Click "Create Web Service"

### Step 3: Add Environment Variables

In Render Dashboard → Your Service → Environment:

Add each variable:
1. Click "Add Environment Variable"
2. Key: `DATABASE_URL`
3. Value: Your Neon PostgreSQL URL
4. Click "Add"
5. Repeat for all variables

**IMPORTANT CORS Settings:**
Add your frontend URL to `CORS_ORIGINS`:
```
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

### Step 4: Update Frontend API URL

After deployment, update your frontend `.env`:

```bash
# frontend/.env.local
REACT_APP_API_URL=https://your-backend-name.onrender.com
```

Redeploy your frontend with the new API URL.

### Step 5: Ingest Content (One-time)

After first deployment, ingest your textbook content:

1. Go to Render Dashboard → Your Service → Shell
2. Run:
```bash
python -m backend.ingest_content
```

This will populate Qdrant with textbook embeddings.

## Monitoring & Logs

### View Logs
- Render Dashboard → Your Service → Logs
- Real-time streaming logs
- Search and filter capabilities

### Health Check
Visit: `https://your-backend-name.onrender.com/health`

Should return:
```json
{
  "status": "healthy",
  "services": {
    "database": "ok",
    "qdrant": "ok",
    "openai": "ok"
  }
}
```

### API Documentation
- Swagger UI: `https://your-backend-name.onrender.com/docs`
- ReDoc: `https://your-backend-name.onrender.com/redoc`

## Troubleshooting

### 1. Build Fails

**Problem**: Dependencies not installing

**Solution**:
- Check `requirements.txt` is in backend folder
- Verify Python version (3.10+)
- Check Render build logs for specific errors

### 2. App Crashes on Start

**Problem**: Missing environment variables

**Solution**:
- Verify all required env vars are set in Render
- Check Render logs for specific missing variables
- Ensure DATABASE_URL format is correct

### 3. Health Check Fails

**Problem**: Services not connecting

**Solution**:
- **Database**: Verify Neon PostgreSQL is running and connection string is correct
- **Qdrant**: Check Qdrant Cloud cluster is active and API key is valid
- **OpenAI**: Verify API key has credits and is active

### 4. CORS Errors

**Problem**: Frontend can't connect to backend

**Solution**:
Update `CORS_ORIGINS` in Render environment:
```
CORS_ORIGINS=["https://your-exact-frontend-url.com"]
```

### 5. Slow Cold Starts

**Problem**: Free tier sleeps after 15 minutes

**Solution**:
- Upgrade to paid tier ($7/month) for always-on
- Or use a cron job to ping `/health` every 10 minutes

## Performance Optimization

### 1. Database Connection Pooling
Already configured in `database.py`:
- Pool size: 5
- Max overflow: 10
- Pool timeout: 30s

### 2. Caching
Consider adding Redis for caching:
1. Add Redis on Render
2. Update `REDIS_URL` env var
3. Enable caching in `config.py`

### 3. Rate Limiting
Configured in `.env`:
- Chat: 100 req/min
- Translate: 50 req/min
- Agent: 20 req/min

## Scaling

### Vertical Scaling
Upgrade Render plan:
- **Starter**: 512MB RAM, $7/month
- **Standard**: 2GB RAM, $25/month
- **Pro**: 4GB RAM, $85/month

### Horizontal Scaling
- Render auto-scales on Standard+ plans
- Configure in Render Dashboard → Scaling

## Security Checklist

- [ ] `DEBUG=false` in production
- [ ] Strong `JWT_SECRET_KEY` (random 32+ chars)
- [ ] HTTPS enforced (automatic on Render)
- [ ] CORS configured with specific origins
- [ ] API keys stored as environment variables
- [ ] `.env` file in `.gitignore`
- [ ] Database credentials not in code

## Cost Estimation

**Free Tier**:
- Render Web Service: Free (with limitations)
- Neon PostgreSQL: Free tier (3 GB storage)
- Qdrant Cloud: Free tier (1GB cluster)
- OpenAI API: Pay per use (~$0.10-1/day for moderate use)

**Paid (Recommended for Production)**:
- Render Starter: $7/month
- Neon Pro: $19/month
- Qdrant Cloud: $25/month (1GB)
- OpenAI API: ~$10-30/month

**Total**: ~$60-80/month for production-ready setup

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **FastAPI Docs**: https://fastapi.tiangolo.com

## Next Steps

1. Deploy backend to Render
2. Test all endpoints
3. Ingest content
4. Update frontend API URL
5. Test full integration
6. Set up monitoring/alerts
7. Consider custom domain
