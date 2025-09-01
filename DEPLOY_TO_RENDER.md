# 🚀 Deploy to Render - Step by Step Guide

## **Step 1: GitHub Setup**

### **1.1 Create GitHub Repository**
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Repository name: `ai-phishing-detector`
4. Make it **Public** (required for free tier)
5. Click "Create repository"

### **1.2 Push to GitHub**
Run these commands in your terminal:

```bash
# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-phishing-detector.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## **Step 2: MongoDB Atlas Setup**

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
4. Password: Create a strong password
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
6. Replace `<dbname>` with `mailguard`

**Example connection string:**
```
mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

## **Step 3: Render Deployment**

### **3.1 Create Render Account**
1. Go to [render.com](https://render.com)
2. Click "Get Started"
3. Sign up with GitHub

### **3.2 Create New Web Service**
1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Select `ai-phishing-detector` repository

### **3.3 Configure Service**
- **Name**: `phishing-detector`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### **3.4 Set Environment Variables**
Click "Environment" tab and add these variables:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | `your-super-secret-key-here-12345` |
| `MONGO_URI` | `mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority` |
| `HUGGINGFACE_API_KEY` | `hf_tKUvfyK...` (your existing key) |
| `EMAIL_ADDRESS` | `mailguard849@gmail.com` |
| `EMAIL_PASSWORD` | `awvlcrrnpktpzbuo` (your Gmail App Password) |

### **3.5 Deploy**
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Your app will be available at: `https://phishing-detector.onrender.com`

## **Step 4: Test Your Deployment**

### **4.1 Test Basic Functionality**
1. Visit your Render URL
2. Test user registration
3. Test email analysis
4. Check if database is working

### **4.2 Monitor Logs**
1. Go to your Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. Check for any errors

## **Step 5: Troubleshooting**

### **Common Issues:**

**Build Fails:**
- Check `requirements.txt` is complete
- Verify Python version in `runtime.txt`

**Database Connection Error:**
- Verify MongoDB Atlas connection string
- Check network access settings
- Ensure database user has correct permissions

**Email Not Working:**
- Verify Gmail App Password
- Check email configuration

**App Crashes:**
- Check Render logs for error messages
- Verify all environment variables are set

## **Step 6: Post-Deployment**

### **6.1 Update Documentation**
- Update README with your live URL
- Document any deployment-specific notes

### **6.2 Monitor Performance**
- Check Render dashboard for resource usage
- Monitor application logs
- Set up alerts if needed

### **6.3 Share Your App**
- Share your Render URL with others
- Test with different users
- Gather feedback

---

## **🎉 Success!**

Your AI Phishing Email Detection System is now live on the internet!

**Your app URL will be:** `https://phishing-detector.onrender.com`

**Remember:**
- Free tier has limitations (sleeps after inactivity)
- Monitor your usage
- Consider upgrading for production use

---

## **📞 Need Help?**

- **Render Documentation**: https://render.com/docs
- **MongoDB Atlas Docs**: https://docs.atlas.mongodb.com
- **GitHub Help**: https://help.github.com
