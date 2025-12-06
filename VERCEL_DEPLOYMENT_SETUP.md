# 🚀 Vercel Automated Deployment Setup Guide

This guide walks you through setting up automatic deployment to Vercel using GitHub Actions.

## ✅ What Was Set Up

I've created:
- ✅ `vercel.json` - Vercel build configuration
- ✅ `.github/workflows/vercel-deploy.yml` - GitHub Actions workflow for auto-deployment

## 🔑 Step 1: Get Your Vercel Tokens

### 1.1 Create a Vercel Account (if you don't have one)
1. Go to https://vercel.com
2. Sign up with your GitHub account (recommended)
3. Authorize Vercel to access your GitHub repositories

### 1.2 Get Your Vercel Tokens

**Personal Access Token:**
1. Log in to Vercel at https://vercel.com/dashboard
2. Go to Settings → Tokens (or https://vercel.com/account/tokens)
3. Click "Create Token"
4. Name it: `github-actions-deployment`
5. Select Scope: **Full Account**
6. Copy the token (you'll need it in Step 2)

**Organization ID:**
1. Go to https://vercel.com/dashboard/settings
2. Look for "Organization ID" (usually in Settings → General)
3. Copy this value

**Project ID:**
You'll get this when you first deploy to Vercel. See Step 2.

## 🎯 Step 2: Create Vercel Project

### Option A: Via Vercel Dashboard (Recommended)
1. Go to https://vercel.com/new
2. Click "Import Project"
3. Paste your repo URL: `https://github.com/ahmed22138/1st-hackathon`
4. Click "Continue"
5. Vercel will auto-detect settings:
   - **Project Name**: `1st-hackathon` (or your preferred name)
   - **Framework**: Docusaurus 2
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/build`
6. Click "Deploy"
7. **Copy the Project ID** from the deployment page (you'll see it in the URL or settings)

### Option B: Via Vercel CLI
```bash
cd "E:\🧠 AIDD 30-Day Challenge\New-hackathon"
vercel login  # Authenticate with your Vercel account
vercel link   # Link to Vercel project
vercel env pull  # Pull environment variables
```

## 🔐 Step 3: Add GitHub Secrets

### 3.1 Add Secrets to Your GitHub Repository

1. Go to your GitHub repository: https://github.com/ahmed22138/1st-hackathon
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these three secrets:

**Secret 1: VERCEL_TOKEN**
- Name: `VERCEL_TOKEN`
- Value: [Paste your Personal Access Token from Step 1.2]
- Click "Add secret"

**Secret 2: VERCEL_ORG_ID**
- Name: `VERCEL_ORG_ID`
- Value: [Paste your Organization ID from Step 1.2]
- Click "Add secret"

**Secret 3: VERCEL_PROJECT_ID**
- Name: `VERCEL_PROJECT_ID`
- Value: [Paste your Project ID from Step 2]
- Click "Add secret"

### 3.2 Verify Secrets Are Added
You should see all three secrets listed in the Secrets page:
- ✅ VERCEL_TOKEN
- ✅ VERCEL_ORG_ID
- ✅ VERCEL_PROJECT_ID

## 🚀 Step 4: Test the Workflow

### Option A: Push to Main (Automatic)
```bash
cd "E:\🧠 AIDD 30-Day Challenge\New-hackathon"
git add .
git commit -m "setup: Configure Vercel auto-deployment"
git push origin main
```

Then:
1. Go to GitHub: https://github.com/ahmed22138/1st-hackathon/actions
2. You should see "Deploy to Vercel" workflow running
3. Wait for completion (usually 2-5 minutes)
4. Check the deployment status

### Option B: Create a Pull Request (Preview)
```bash
git checkout -b feature/test-vercel
git add .
git commit -m "test: Vercel deployment workflow"
git push origin feature/test-vercel
```

Then create a PR on GitHub - you'll get an automatic preview deployment!

## 📊 Workflow Behavior

### On Push to Main Branch
- ✅ Builds the Docusaurus frontend
- ✅ Deploys to Vercel **Production**
- ✅ Gets a permanent URL like: `https://1st-hackathon.vercel.app`

### On Pull Request
- ✅ Builds the Docusaurus frontend
- ✅ Deploys to Vercel **Preview**
- ✅ Adds a comment to your PR with the preview link
- ✅ Useful for testing before merging

## ✨ Deployment URLs

After first deployment, you'll have:

**Production URL:**
```
https://1st-hackathon.vercel.app
```

**Custom Domain (Optional):**
1. Go to Vercel dashboard → your project
2. Click "Settings" → "Domains"
3. Add your custom domain (e.g., `textbook.example.com`)
4. Follow DNS instructions

## 🔍 Monitoring Deployments

### GitHub Actions Tab
Monitor builds at: https://github.com/ahmed22138/1st-hackathon/actions
- See build logs
- Check for errors
- Track deployment history

### Vercel Dashboard
Monitor at: https://vercel.com/dashboard
- View all deployments
- Check analytics
- Manage environment variables
- See performance metrics

## 🐛 Troubleshooting

### Issue: Workflow fails with "Invalid token"
**Solution:**
- Verify `VERCEL_TOKEN` is correctly set in GitHub Secrets
- Try regenerating the token in Vercel dashboard

### Issue: "Project not found"
**Solution:**
- Verify `VERCEL_PROJECT_ID` is correct
- Make sure you deployed the project in Vercel first

### Issue: Build fails
**Solution:**
1. Check the GitHub Actions logs
2. Verify `frontend/package.json` has all dependencies
3. Run locally: `cd frontend && npm install && npm run build`

### Issue: Preview URLs not working
**Solution:**
- Make sure your PR is against the `main` branch
- Check GitHub Actions tab for errors
- Vercel preview may take 1-2 minutes to be ready

## 📋 Checklist for Complete Setup

Before you're done, verify:

- [ ] Vercel account created
- [ ] Vercel Personal Access Token generated
- [ ] Vercel Organization ID copied
- [ ] Vercel project created
- [ ] Vercel Project ID copied
- [ ] GitHub repository secrets added (all 3)
- [ ] `vercel.json` exists in project root
- [ ] `.github/workflows/vercel-deploy.yml` exists
- [ ] First push to main completed
- [ ] Workflow ran successfully in GitHub Actions
- [ ] Deployment visible in Vercel dashboard
- [ ] Live URL is accessible

## 🎉 You're Done!

Once all checks pass, you have:
- ✅ Automatic deployment on every push to main
- ✅ Preview deployments on pull requests
- ✅ Zero-downtime production deployments
- ✅ Global CDN distribution
- ✅ Automatic SSL certificates
- ✅ Built-in analytics and monitoring

## 🔄 Deployment Workflow

```
Your local changes
    ↓
git push origin main
    ↓
GitHub Actions triggered
    ↓
Build Docusaurus
    ↓
Deploy to Vercel
    ↓
Live at https://1st-hackathon.vercel.app
    ↓
Vercel CDN distributes globally
```

## 📞 Next Steps

1. **Complete the setup** following this guide
2. **Test with a push** to main branch
3. **Monitor the workflow** in GitHub Actions
4. **Visit your live site** at Vercel URL
5. **Add a custom domain** (optional)
6. **Set up analytics** in Vercel dashboard (optional)

## ℹ️ Additional Resources

- Vercel Docs: https://vercel.com/docs
- GitHub Actions: https://docs.github.com/en/actions
- Docusaurus Deployment: https://docusaurus.io/docs/deployment

---

**Last Updated:** December 6, 2025
**Status:** ✅ Ready for deployment

Built with ❤️ using Claude Code
