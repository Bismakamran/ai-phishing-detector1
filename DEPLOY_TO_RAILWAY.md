# 🚀 Deploy to Railway - Step by Step Guide

## **Prerequisites**
- GitHub account
- Railway account (free)
- MongoDB Atlas account (free)
- Hugging Face API key (free)

---

## **Step 1: Prepare Your Code**

### **1.1 Update Your Repository**
Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### **1.2 Verify Files**
Ensure you have these files in your repository:
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process definition
- ✅ `app.py` - Main Flask application

---

## **Step 2: Set Up MongoDB Atlas**

### **2.1 Create MongoDB Atlas Account**
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Click "Try Free"
3. Create account or sign in

### **2.2 Create Cluster**
1. Click "Build a Database"
2. Choose "FREE" tier (M0)
3. Select cloud provider (AWS/Google Cloud/Azure)
4. Choose region close to you
5. Click "Create"

### **2.3 Configure Database Access**
1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. Username: `phishing_detector_user`
4. Password: Create a strong password (save this!)
5. Role: "Read and write to any database"
6. Click "Add User"

### **2.4 Configure Network Access**
1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Click "Confirm"

### **2.5 Get Connection String**
1. Go to "Database" in left sidebar
2. Click "Connect"
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user password
6. Add `/mailguard` before `?retryWrites=true`

**Example:**
```
mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

---

## **Step 3: Get Hugging Face API Key**

### **3.1 Create Hugging Face Account**
1. Go to [huggingface.co](https://huggingface.co)
2. Sign up or sign in

### **3.2 Generate API Key**
1. Go to Settings → Access Tokens
2. Click "New token"
3. Name: `phishing-detector`
4. Role: Read
5. Click "Generate token"
6. Copy the token (starts with `hf_`)

---

## **Step 4: Set Up Gmail App Password**

### **4.1 Enable 2-Factor Authentication**
1. Go to your Google Account settings
2. Enable 2-factor authentication

### **4.2 Generate App Password**
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Other (Custom name)"
3. Name: `MailGuard`
4. Click "Generate"
5. Copy the 16-character password

---

## **Step 5: Deploy to Railway**

### **5.1 Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with GitHub

### **5.2 Deploy from GitHub**
1. Click "Deploy from GitHub repo"
2. Select your repository
3. Click "Deploy Now"

### **5.3 Configure Environment Variables**
1. Go to your project dashboard
2. Click "Variables" tab
3. Add these environment variables:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | `mailguard-secret-key-2024-production` |
| `MONGO_URI` | `mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority` |
| `HUGGINGFACE_API_KEY` | `hf_your_api_key_here` |
| `EMAIL_ADDRESS` | `your-email@gmail.com` |
| `EMAIL_PASSWORD` | `your-16-character-app-password` |
| `PORT` | `8000` |

### **5.4 Configure Service**
1. Click on your service
2. Go to "Settings" tab
3. **Start Command**: `gunicorn app:app`
4. **Health Check Path**: `/`
5. Click "Save"

### **5.5 Deploy**
1. Railway will automatically deploy when you push to GitHub
2. Or click "Deploy" in the dashboard
3. Wait for build to complete (3-5 minutes)
4. Your app will be available at: `https://your-project-name.railway.app`

---

## **Step 6: Test Your Deployment**

### **6.1 Basic Functionality Test**
1. Visit your app URL
2. Try to register a new user
3. Test email analysis functionality
4. Check if data is saved to MongoDB

### **6.2 Verify Environment Variables**
1. Go to your Railway dashboard
2. Check "Deployments" tab for any errors
3. Check "Logs" for any issues

---

## **Step 7: Custom Domain (Optional)**

### **7.1 Add Custom Domain**
1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

---

## **Step 8: Monitor and Scale**

### **8.1 Monitor Performance**
1. Check Railway dashboard for metrics
2. Monitor response times
3. Check error rates

### **8.2 Scale if Needed**
1. Go to "Settings" tab
2. Adjust resources as needed
3. Railway will auto-scale based on usage

---

## **Troubleshooting**

### **Common Issues:**

**1. Build Fails**
- Check `requirements.txt` for compatibility
- Ensure all imports are correct
- Check Railway logs for specific errors

**2. Environment Variables Not Working**
- Verify all variables are set correctly
- Check for typos in variable names
- Ensure MongoDB URI is correct

**3. Database Connection Issues**
- Verify MongoDB Atlas network access
- Check database user credentials
- Ensure connection string format is correct

**4. Email Not Working**
- Verify Gmail app password
- Check 2-factor authentication is enabled
- Ensure email address is correct

**5. Port Issues**
- Ensure `PORT` environment variable is set
- Check if Railway is using the correct port

---

## **Railway Advantages**

✅ **Simple Deployment** - Just connect GitHub
✅ **Automatic Scaling** - Scales based on traffic
✅ **Free Tier** - Generous limits
✅ **Easy Environment Management** - Built-in variable management
✅ **Great Performance** - Fast deployment and execution
✅ **Built-in Monitoring** - Dashboard with metrics

---

## **Railway vs Vercel Comparison**

| Feature | Railway | Vercel |
|---------|---------|--------|
| **Deployment Speed** | 3-5 minutes | 2-3 minutes |
| **Free Tier** | ✅ Yes | ✅ Yes |
| **Auto-scaling** | ✅ Yes | ✅ Yes |
| **Custom Domains** | ✅ Yes | ✅ Yes |
| **Environment Variables** | ✅ Yes | ✅ Yes |
| **GitHub Integration** | ✅ Yes | ✅ Yes |
| **HTTPS** | ✅ Yes | ✅ Yes |
| **Best For** | Full-stack apps | Frontend-heavy apps |

---

## **Next Steps**

1. **Monitor Performance** - Check Railway analytics
2. **Set Up Monitoring** - Add error tracking
3. **Optimize** - Monitor resource usage
4. **Scale** - Upgrade if needed

Your AI Phishing Email Detection app is now live on Railway! 🎉

---

## **Quick Commands**

### **Update and Redeploy:**
```bash
git add .
git commit -m "Update app"
git push origin main
# Railway will automatically redeploy
```

### **Check Logs:**
- Go to Railway dashboard
- Click "Logs" tab
- Monitor real-time logs

### **Restart Service:**
- Go to Railway dashboard
- Click "Deploy" to restart
