# 🗄️ MongoDB Atlas Cluster Deployment Checklist

## **✅ Pre-Deployment Checklist**

- [ ] **MongoDB Atlas Account Created**
- [ ] **Free Tier Cluster Created (M0)**
- [ ] **Database User Created** (`phishing_detector_user`)
- [ ] **Network Access Configured** (0.0.0.0/0)
- [ ] **Connection String Obtained**
- [ ] **Connection Tested Locally**

---

## **🚀 Quick Deployment Steps**

### **Step 1: Create Account**
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Click "Try Free"
3. Sign up with email or Google/GitHub

### **Step 2: Create Cluster**
1. Click "Build a Database"
2. Select "FREE" tier (M0)
3. Choose AWS as provider
4. Select region close to you
5. Click "Create"
6. Wait 2-3 minutes for cluster to be ready

### **Step 3: Configure Access**
1. **Database Access:**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Username: `phishing_detector_user`
   - Password: Create strong password
   - Role: "Read and write to any database"

2. **Network Access:**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)

### **Step 4: Get Connection String**
1. Go to "Database"
2. Click "Connect"
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your password
6. Add `/mailguard` at the end

**Final Format:**
```
mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

### **Step 5: Test Connection**
```bash
python test_mongodb_atlas.py
```

---

## **🔧 Environment Variables for Render**

When deploying to Render, set this environment variable:

| Variable | Value |
|----------|-------|
| `MONGO_URI` | Your complete connection string |

**Example:**
```
MONGO_URI=mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

---

## **📊 Cluster Information**

### **Free Tier (M0) Limits:**
- **Storage:** 512MB
- **RAM:** Shared
- **Backup:** 7-day retention
- **Perfect for:** Development and small projects

### **Monitoring:**
- **Dashboard:** View cluster performance
- **Metrics:** CPU, memory, storage usage
- **Logs:** Error tracking and debugging

---

## **🎯 Success Indicators**

✅ **Cluster Status:** Active  
✅ **Database User:** Created with correct permissions  
✅ **Network Access:** Allows all IPs (0.0.0.0/0)  
✅ **Connection Test:** Passes locally  
✅ **Collections:** Can be created and accessed  

---

## **📞 Need Help?**

- **MongoDB Atlas Docs:** https://docs.atlas.mongodb.com
- **Community Support:** https://community.mongodb.com
- **Test Script:** `python test_mongodb_atlas.py`

---

**🎉 Your MongoDB Atlas cluster is ready for production deployment!**
