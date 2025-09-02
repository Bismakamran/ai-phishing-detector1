# Railway Deployment Guide

## 🚀 Quick Deploy to Railway

This guide will help you deploy your AI Phishing Email Detection app to Railway with an optimized, lightweight build.

## ✨ What We Optimized

- **Removed heavy ML libraries**: Eliminated `torch` and `transformers` (saved ~3-4GB)
- **Lightweight dependencies**: Used specific versions of essential packages
- **Docker optimization**: Multi-stage build with slim Python base image
- **Rule-based analysis**: Replaced local ML models with efficient rule-based detection
- **API-based ML**: Content analysis still uses Hugging Face API (no local models)

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Git Repository**: Your code should be in a Git repository
3. **Environment Variables**: Set up your API keys and database connections

## 🛠️ Deployment Steps

### Option 1: Automatic Deployment (Recommended)

1. **Push your optimized code to Git**
   ```bash
   git add .
   git commit -m "Optimize for Railway deployment"
   git push origin main
   ```

2. **Connect Railway to your Git repository**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Railway will automatically detect the Dockerfile and deploy**

### Option 2: Manual Deployment with Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Link to your project**
   ```bash
   railway link
   ```

4. **Deploy**
   ```bash
   railway up
   ```

### Option 3: Windows Batch Script

Run the included `deploy_railway.bat` file:
```bash
deploy_railway.bat
```

## 🔧 Environment Variables

Set these in your Railway project dashboard:

```env
MONGO_URI=your_mongodb_connection_string
HUGGINGFACE_API_KEY=your_huggingface_api_key
SECRET_KEY=your_secret_key
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_email_password
```

## 📊 Expected Results

- **Before optimization**: ~6.0 GB image size ❌
- **After optimization**: ~1.5-2.0 GB image size ✅
- **Deployment time**: Reduced from ~6 minutes to ~2-3 minutes
- **Functionality**: Maintained with API-based ML analysis

## 🔍 What Changed

### Files Modified:
- `requirements.txt` - Removed heavy ML libraries
- `Dockerfile` - Optimized multi-stage build
- `.dockerignore` - Excluded unnecessary files
- `railway.json` - Switched to Docker builder
- `header_ml_model.py` - Lightweight rule-based analysis
- `comprehensive_email_analyzer.py` - Updated to use lightweight analysis

### Files Removed:
- `train_header_model.py` - No longer needed
- Various test and debug files (excluded from Docker build)

## 🚨 Troubleshooting

### Build Still Fails?
1. **Check Dockerfile**: Ensure it's in your root directory
2. **Verify .dockerignore**: Make sure it's not excluding essential files
3. **Check requirements.txt**: Ensure all dependencies are compatible

### App Not Working After Deploy?
1. **Check logs**: Use `railway logs` command
2. **Verify environment variables**: Ensure all required vars are set
3. **Check health endpoint**: Visit your app's root URL

### Performance Issues?
1. **Monitor Railway metrics**: Check CPU and memory usage
2. **Optimize database queries**: Ensure MongoDB queries are efficient
3. **Consider caching**: Add Redis for frequently accessed data

## 📈 Monitoring & Scaling

- **Railway Dashboard**: Monitor deployment status and logs
- **Health Checks**: Built-in health check endpoint at `/`
- **Auto-scaling**: Railway can auto-scale based on traffic
- **Custom domains**: Add your own domain in Railway settings

## 🎯 Next Steps

After successful deployment:

1. **Test your app**: Ensure all features work correctly
2. **Set up monitoring**: Configure alerts for any issues
3. **Add custom domain**: Point your domain to Railway
4. **Set up CI/CD**: Automate deployments from Git pushes

## 📞 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Open an issue in your repository

---

**Happy Deploying! 🚀**

Your app should now deploy successfully on Railway with a much smaller image size and faster build times.
