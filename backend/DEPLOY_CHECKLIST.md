# 🚀 Render Deployment Checklist

Quick checklist for deploying to Render. Follow these steps in order!

## ✅ Pre-Deployment (Do These First!)

### 1. Set Up Services

- [ ] **Neon Database** (Free PostgreSQL)
  - Go to https://neon.tech
  - Create account
  - Create new project: "ai-textbook"
  - Copy connection string

- [ ] **Qdrant Cloud** (Vector Database)
  - Go to https://cloud.qdrant.io
  - Create account
  - Create cluster: "textbook-embeddings"
  - Copy cluster URL and API key

- [ ] **OpenAI API**
  - Go to https://platform.openai.com/api-keys
  - Create API key
  - Add $5-10 credits

### 2. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare backend for Render deployment"

# Create GitHub repo and push
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

## 🌐 Render Deployment

### 3. Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Connect GitHub repository
   - Select `render.yaml`

2. **Add Environment Variables**

   Copy these from your services:

   ```bash
   DATABASE_URL=postgresql://user:pass@host.neon.tech:5432/db
   QDRANT_URL=https://xxxxx.gcp.cloud.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   OPENAI_API_KEY=sk-proj-your-openai-key
   ```

   Additional variables:
   ```bash
   ENVIRONMENT=production
   DEBUG=false
   LOG_LEVEL=INFO
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```

3. **Deploy**
   - Click "Create Blueprint Instance"
   - Wait 5-10 minutes for build
   - Check logs for errors

### 4. Verify Deployment

Test your backend:

```bash
# Health check
curl https://your-backend.onrender.com/health

# Should return:
{
  "status": "healthy",
  "services": {
    "database": "ok",
    "qdrant": "ok",
    "openai": "ok"
  }
}
```

### 5. Ingest Content

**IMPORTANT**: Run this once after first deployment

1. Render Dashboard → Your Service → Shell
2. Run:
```bash
python -m backend.ingest_content
```
3. Wait for completion (~2-5 minutes)
4. Verify in logs: "Ingestion complete!"

## 🎨 Frontend Integration

### 6. Update Frontend

Update frontend environment variable:

```bash
# frontend/.env.local
REACT_APP_API_URL=https://your-backend-name.onrender.com
```

### 7. Test Integration

1. Run frontend locally
2. Open chatbot
3. Ask: "What is embodied AI?"
4. Should get response from backend!

## ✅ Post-Deployment Checks

- [ ] Health endpoint returns "healthy"
- [ ] API docs accessible: `/docs`
- [ ] Chatbot responds to queries
- [ ] CORS working (no errors in browser console)
- [ ] Content ingested successfully
- [ ] Frontend connected to backend

## 🐛 Common Issues & Fixes

### Backend build fails
```bash
# Check Python version in render.yaml
PYTHON_VERSION=3.12.0
```

### Health check fails
- Verify all environment variables are set
- Check Neon database is accessible
- Verify Qdrant cluster is running

### CORS errors
- Add frontend URL to `CORS_ORIGINS`
- Use exact URL (with https://)
- Redeploy backend after changing

### Slow response (Free tier)
- Free tier sleeps after 15 min inactivity
- First request after sleep takes 30-60 seconds
- Upgrade to Starter ($7/month) for always-on

## 💰 Cost Breakdown

**Free Tier** (Good for testing):
- Render: Free (sleeps after 15min)
- Neon: Free (3GB storage)
- Qdrant: Free (1GB cluster)
- OpenAI: ~$0.10-1/day

**Paid Tier** (Production):
- Render Starter: $7/month (always-on)
- Neon Pro: $19/month
- Qdrant: $25/month
- OpenAI: $10-30/month
- **Total**: ~$60-80/month

## 📊 Monitoring

### Check Logs
```
Render Dashboard → Logs
```

### Monitor Usage
- OpenAI: https://platform.openai.com/usage
- Neon: Check dashboard
- Qdrant: Check cluster metrics

## 🎉 You're Done!

Your backend is now live at:
`https://your-backend-name.onrender.com`

Test it:
- Health: `/health`
- Docs: `/docs`
- Chat: POST `/chat`

---

## Need Help?

- Render Support: https://render.com/docs
- Our README: `DEPLOYMENT.md`
- GitHub Issues: Create an issue in your repo
