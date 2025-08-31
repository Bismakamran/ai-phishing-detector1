# 🚀 Deployment Guide - AI Phishing Email Detection

## **📋 Pre-Deployment Checklist**

### **1. Code Preparation**
- [ ] All files are committed to Git
- [ ] Requirements.txt is up to date
- [ ] Environment variables are documented
- [ ] Database connection is configured
- [ ] Static files are properly organized

### **2. Environment Variables Needed**
```bash
SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://localhost:27017/phishing_detector
HUGGINGFACE_API_KEY=your_huggingface_api_key
EMAIL_ADDRESS=mailguard849@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

---

## **🎯 Option 1: Render (Recommended - Free Tier)**

### **Step 1: Prepare Your Code**
1. **Create `render.yaml` file:**
```yaml
services:
  - type: web
    name: phishing-detector
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
      - key: SECRET_KEY
        generateValue: true
      - key: MONGO_URI
        sync: false
      - key: HUGGINGFACE_API_KEY
        sync: false
      - key: EMAIL_ADDRESS
        sync: false
      - key: EMAIL_PASSWORD
        sync: false

databases:
  - name: phishing-detector-db
    databaseName: phishing_detector
    user: phishing_detector_user
```

2. **Update `requirements.txt`:**
```txt
Flask==2.3.3
pymongo==4.5.0
Werkzeug==2.3.7
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
dnspython==2.4.2
scikit-learn==1.3.0
numpy==1.24.3
pandas==2.0.3
```

3. **Create `gunicorn.conf.py`:**
```python
bind = "0.0.0.0:10000"
workers = 2
timeout = 120
```

### **Step 2: Deploy to Render**
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure environment variables in Render dashboard
5. Deploy!

### **Step 3: Configure MongoDB Atlas (Free)**
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create free account
3. Create a new cluster
4. Get connection string
5. Update `MONGO_URI` in Render environment variables

---

## **🎯 Option 2: Railway (Alternative Free Option)**

### **Step 1: Prepare for Railway**
1. **Create `railway.json`:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### **Step 2: Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Add environment variables
4. Deploy automatically

---

## **🎯 Option 3: Heroku (Paid but Reliable)**

### **Step 1: Prepare for Heroku**
1. **Create `Procfile`:**
```
web: gunicorn app:app
```

2. **Create `runtime.txt`:**
```
python-3.9.16
```

3. **Install Heroku CLI:**
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### **Step 2: Deploy to Heroku**
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-phishing-detector

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set SECRET_KEY=your_secret_key
heroku config:set HUGGINGFACE_API_KEY=your_api_key
heroku config:set EMAIL_ADDRESS=mailguard849@gmail.com
heroku config:set EMAIL_PASSWORD=your_app_password

# Deploy
git push heroku main
```

---

## **🎯 Option 4: AWS (Production Ready)**

### **Step 1: AWS Setup**
1. Create AWS account
2. Install AWS CLI
3. Configure AWS credentials

### **Step 2: Deploy with Elastic Beanstalk**
1. **Create `requirements.txt` and `Procfile`**
2. **Create `.ebextensions/python.config`:**
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    SECRET_KEY: your_secret_key
    HUGGINGFACE_API_KEY: your_api_key
    EMAIL_ADDRESS: mailguard849@gmail.com
    EMAIL_PASSWORD: your_app_password
```

3. **Deploy:**
```bash
eb init
eb create phishing-detector-env
eb deploy
```

---

## **🔧 Required Code Changes for Deployment**

### **1. Update `app.py` for Production**
```python
# Add at the top of app.py
import os
from dotenv import load_dotenv

load_dotenv()

# Update MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)

# Update Flask app configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Add production configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### **2. Create `wsgi.py` (Alternative)**
```python
from app import app

if __name__ == "__main__":
    app.run()
```

---

## **📊 Database Setup for Production**

### **MongoDB Atlas (Recommended)**
1. **Create Cluster:**
   - Go to MongoDB Atlas
   - Create free cluster
   - Choose cloud provider (AWS/Google Cloud/Azure)
   - Select region close to your deployment

2. **Configure Network Access:**
   - Add IP address: `0.0.0.0/0` (allow all)
   - Or add specific IP ranges

3. **Create Database User:**
   - Username: `phishing_detector_user`
   - Password: strong password
   - Role: `Read and write to any database`

4. **Get Connection String:**
```
mongodb+srv://phishing_detector_user:<password>@cluster0.xxxxx.mongodb.net/phishing_detector?retryWrites=true&w=majority
```

---

## **🔐 Security Considerations**

### **1. Environment Variables**
- Never commit secrets to Git
- Use environment variables for all sensitive data
- Rotate API keys regularly

### **2. HTTPS/SSL**
- Enable HTTPS in production
- Use SSL certificates (Let's Encrypt for free)
- Redirect HTTP to HTTPS

### **3. Database Security**
- Use strong passwords
- Enable network security
- Regular backups
- Monitor access logs

---

## **📈 Monitoring and Maintenance**

### **1. Health Checks**
Add health check endpoint:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### **2. Logging**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### **3. Error Monitoring**
- Set up error tracking (Sentry)
- Monitor application performance
- Set up alerts for downtime

---

## **🚀 Quick Start: Render Deployment**

### **Step-by-Step Instructions:**

1. **Prepare Repository:**
```bash
# Create render.yaml file (see above)
# Update requirements.txt
# Commit all changes
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Deploy to Render:**
   - Go to render.com
   - Sign up with GitHub
   - Click "New Web Service"
   - Connect your repository
   - Configure environment variables
   - Deploy!

3. **Set up MongoDB Atlas:**
   - Create free MongoDB Atlas account
   - Create cluster
   - Get connection string
   - Update MONGO_URI in Render

4. **Test Your Deployment:**
   - Visit your Render URL
   - Test user registration
   - Test email analysis
   - Check database connections

---

## **💰 Cost Comparison**

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| **Render** | ✅ Yes | $7/month | Students, small projects |
| **Railway** | ✅ Yes | $5/month | Quick deployments |
| **Heroku** | ❌ No | $7/month | Reliable, established |
| **AWS** | ✅ Limited | Pay-per-use | Production, scalable |
| **Vercel** | ✅ Yes | $20/month | Frontend-heavy apps |

---

## **🎯 Recommended for Your Project**

**For Students/Demo:**
1. **Render** (Free tier) + MongoDB Atlas (Free)
2. **Railway** (Free tier) + MongoDB Atlas (Free)

**For Production:**
1. **AWS Elastic Beanstalk** + MongoDB Atlas
2. **Heroku** + MongoDB Atlas

**For Learning:**
1. Start with Render (easiest)
2. Move to AWS when ready for production

---

## **🔧 Troubleshooting**

### **Common Issues:**

1. **Build Failures:**
   - Check requirements.txt
   - Verify Python version
   - Check for missing dependencies

2. **Database Connection:**
   - Verify MONGO_URI format
   - Check network access
   - Test connection locally

3. **Environment Variables:**
   - Ensure all variables are set
   - Check for typos
   - Verify API keys are valid

4. **Email Issues:**
   - Verify Gmail App Password
   - Check SMTP settings
   - Test email sending locally

---

## **📞 Support Resources**

- **Render Documentation:** https://render.com/docs
- **MongoDB Atlas:** https://docs.atlas.mongodb.com
- **Heroku Documentation:** https://devcenter.heroku.com
- **AWS Documentation:** https://aws.amazon.com/documentation

---

**🎉 Ready to Deploy!**

Choose your preferred platform and follow the step-by-step instructions above. Start with Render for the easiest deployment experience!
