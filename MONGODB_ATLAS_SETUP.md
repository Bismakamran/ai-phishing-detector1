# 🗄️ MongoDB Atlas Cluster Setup Guide

## **Step 1: Create MongoDB Atlas Account**

### **1.1 Go to MongoDB Atlas**
1. Open your web browser
2. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
3. Click **"Try Free"** button

### **1.2 Sign Up**
1. **Choose your sign-up method:**
   - Email/Password
   - Google Account
   - GitHub Account
2. **Fill in your details:**
   - Email address
   - Password
   - Account name (your name or organization)
3. Click **"Create Account"**

### **1.3 Verify Email**
1. Check your email for verification link
2. Click the verification link
3. Return to MongoDB Atlas

---

## **Step 2: Create Your First Cluster**

### **2.1 Choose Plan**
1. Click **"Build a Database"**
2. Select **"FREE"** tier (M0)
3. Click **"Create"**

### **2.2 Configure Cluster**
1. **Cloud Provider & Region:**
   - Choose **AWS** (recommended)
   - Select region closest to you (e.g., **US East (N. Virginia)**)
2. **Cluster Name:**
   - Default: `Cluster0` (or name it `phishing-detector-cluster`)
3. Click **"Create"**

### **2.3 Wait for Creation**
- Cluster creation takes 2-3 minutes
- You'll see a progress indicator
- Status will change to "Active" when ready

---

## **Step 3: Configure Database Access**

### **3.1 Create Database User**
1. In the left sidebar, click **"Database Access"**
2. Click **"Add New Database User"**
3. **Configure user:**
   - **Username:** `phishing_detector_user`
   - **Password:** Create a strong password (save this!)
   - **Database User Privileges:** Select **"Read and write to any database"**
4. Click **"Add User"**

### **3.2 Configure Network Access**
1. In the left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. **Choose access method:**
   - Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - This allows your Render app to connect
4. Click **"Confirm"**

---

## **Step 4: Get Connection String**

### **4.1 Connect to Your Cluster**
1. In the left sidebar, click **"Database"**
2. Click **"Connect"** button
3. Choose **"Connect your application"**

### **4.2 Copy Connection String**
1. **Copy the connection string** (it looks like this):
   ```
   mongodb+srv://phishing_detector_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### **4.3 Customize Connection String**
1. **Replace `<password>`** with your database user password
2. **Add database name** after the hostname:
   ```
   mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
   ```

**Final connection string format:**
```
mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

---

## **Step 5: Test Connection**

### **5.1 Test Locally (Optional)**
You can test the connection by updating your `.env` file:
```bash
MONGO_URI=mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

### **5.2 Run Your App**
```bash
python app.py
```

---

## **Step 6: Use in Render Deployment**

### **6.1 Set Environment Variable**
When deploying to Render, set this environment variable:
- **Variable Name:** `MONGO_URI`
- **Value:** Your complete connection string

### **6.2 Example for Render:**
```
MONGO_URI=mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority
```

---

## **🔧 Troubleshooting**

### **Common Issues:**

**Connection Failed:**
- Check if password is correct
- Verify network access allows all IPs (0.0.0.0/0)
- Ensure database user has correct permissions

**Authentication Error:**
- Verify username and password
- Check if database user was created successfully

**Network Error:**
- Make sure you added "Allow Access from Anywhere"
- Check if cluster is active

---

## **📊 Cluster Management**

### **Monitor Your Cluster:**
1. **Dashboard:** View cluster performance
2. **Metrics:** Monitor CPU, memory, and storage usage
3. **Logs:** Check for any errors or issues

### **Free Tier Limitations:**
- **Storage:** 512MB
- **RAM:** Shared
- **Backup:** 7-day retention
- **Perfect for development and small projects**

---

## **🎯 Next Steps**

1. **Save your connection string** - you'll need it for Render
2. **Test the connection** locally
3. **Proceed with Render deployment**
4. **Monitor your cluster** after deployment

---

## **📞 Need Help?**

- **MongoDB Atlas Documentation:** https://docs.atlas.mongodb.com
- **MongoDB Community:** https://community.mongodb.com
- **Support:** Available in Atlas dashboard

---

**🎉 Your MongoDB Atlas cluster is ready for deployment!**
