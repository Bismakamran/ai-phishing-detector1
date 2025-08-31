# MailGuard Setup Instructions

## Quick Start Guide

### 1. Install Python Dependencies

First, install all required Python packages:

```bash
# On Windows
py -m pip install -r requirements.txt

# On macOS/Linux
pip3 install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the template
cp env_example.txt .env

# Edit the .env file with your configuration
```

Required configuration in `.env`:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/mailguard

# Hugging Face API Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key-here

# Email Configuration (for OTP)
EMAIL_ADDRESS=mailguard984@gmail.com
EMAIL_PASSWORD=Mailguard123
```

### 3. Set Up MongoDB

#### Option A: Local MongoDB
1. Download and install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service
3. The application will create the database automatically

#### Option B: MongoDB Atlas (Cloud)
1. Create a free account at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `MONGO_URI` in `.env` file

### 4. Get Hugging Face API Key

1. Sign up at [huggingface.co](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create a new token
4. Add it to your `.env` file

### 5. Configure Email (Optional)

The application uses the provided Gmail account for OTP delivery. For production:

1. Enable 2-factor authentication on the Gmail account
2. Generate an App Password
3. Update the `EMAIL_PASSWORD` in `.env`

### 6. Run the Application

#### Option A: Using the startup script (Recommended)
```bash
py run.py
```

#### Option B: Direct execution
```bash
py app.py
```

### 7. Access the Application

Open your browser and go to: `http://localhost:5000`

## Testing Your Setup

Run the test script to verify everything is working:

```bash
py test_setup.py
```

This will check:
- ✅ Python version
- ✅ Dependencies installation
- ✅ Flask application
- ✅ MongoDB connection
- ✅ Hugging Face API
- ✅ Email configuration

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   - Solution: Install dependencies with `py -m pip install -r requirements.txt`

2. **"MongoDB connection failed"**
   - Solution: Start MongoDB service or check your connection string

3. **"Hugging Face API test failed"**
   - Solution: Get a valid API key from Hugging Face

4. **"Email configuration test failed"**
   - Solution: Configure Gmail app password or use a different email service

### Getting Help

1. Check the console output for error messages
2. Verify all environment variables are set correctly
3. Ensure MongoDB is running
4. Test your Hugging Face API key separately

## Application Features

Once running, you can:

1. **Register** - Create an account with strong password requirements
2. **Login** - Use MFA for enhanced security
3. **Analyze Emails** - Upload or paste email content for phishing detection
4. **View Results** - Get confidence scores and detailed analysis
5. **Track History** - See your previous analyses

## Security Notes

- Change the default `SECRET_KEY` in production
- Use environment variables for sensitive data
- Consider using a dedicated email service for OTP
- Regularly update dependencies
- Monitor application logs

## Next Steps

After successful setup:

1. Test user registration and login
2. Try analyzing sample phishing emails
3. Explore the analysis results
4. Customize the detection algorithm if needed
5. Deploy to production environment

## Support

If you encounter issues:

1. Check the README.md for detailed documentation
2. Review the console output for error messages
3. Verify all prerequisites are met
4. Test individual components separately

---

**Happy phishing detection! 🛡️**
