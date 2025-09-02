from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from comprehensive_email_analyzer import ComprehensiveEmailAnalyzer

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Simple healthcheck endpoint for platforms
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mailguard')
mongo = PyMongo(app)

# Test MongoDB connection
try:
    mongo.db.command('ping')
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"⚠️ MongoDB connection failed: {e}")
    print("⚠️ Using in-memory storage for development")
    # Create a simple in-memory storage for development
    class MockDB:
        def __init__(self):
            self.users = {}
            self.detections = []
        
        def insert_one(self, data):
            if 'username' in data:
                self.users[data['username']] = data
            else:
                self.detections.append(data)
            return type('obj', (object,), {'inserted_id': 'mock_id'})()
        
        def find_one(self, query):
            if 'username' in query:
                return self.users.get(query['username'])
            return None
        
        def update_one(self, query, update):
            if 'username' in query:
                username = query['username']
                if username in self.users:
                    if '$set' in update:
                        self.users[username].update(update['$set'])
                    if '$unset' in update:
                        for key in update['$unset']:
                            self.users[username].pop(key, None)
            return type('obj', (object,), {'modified_count': 1})()
        
        def command(self, cmd):
            return {'ok': 1}
    
    class MockMongo:
        def __init__(self):
            self.db = MockDB()
    
    mongo = MockMongo()

# Email configuration for OTP
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'mailguard849@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'Mailguard123')

# Hugging Face API configuration
# Using a more reliable text classification model for phishing detection
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
# Fallback model in case the primary model is not available
FALLBACK_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', 'your-huggingface-api-key')

# Check if API key is properly configured
if HUGGINGFACE_API_KEY == 'your-huggingface-api-key':
    print("⚠️ Warning: Using default Hugging Face API key. Please set HUGGINGFACE_API_KEY environment variable.")
else:
    print(f"✅ Hugging Face API key configured (first 10 chars: {HUGGINGFACE_API_KEY[:10]}...)")

# Check email configuration
print(f"📧 Email configuration: {EMAIL_ADDRESS}")
if EMAIL_PASSWORD == 'Mailguard123':
    print("⚠️ Warning: Using default email password. Please set EMAIL_PASSWORD environment variable.")
else:
    print("✅ Email password configured")

def send_otp_email(email, otp):
    """Send OTP via email"""
    try:
        print(f"📧 Attempting to send OTP to: {email}")
        print(f"📧 Using email: {EMAIL_ADDRESS}")
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "MailGuard - Your OTP Code"
        
        body = f"""
        Your MailGuard OTP code is: {otp}
        
        This code will expire in 10 minutes.
        If you didn't request this code, please ignore this email.
        
        Best regards,
        MailGuard Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Use Gmail SMTP with proper error handling
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print(f"📧 Attempting to login with email: {EMAIL_ADDRESS}")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, email, text)
        server.quit()
        
        print(f"✅ OTP email sent successfully to: {email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Email authentication failed: {e}")
        print("❌ Please check your email credentials in the environment variables")
        return False
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Email recipient refused: {e}")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ SMTP server disconnected: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Email sending error: {e}")
        return False

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def analyze_email_phishing(email_text, url):
    """Analyze email for phishing indicators using Hugging Face"""
    
    # Check if we have a valid API key
    if HUGGINGFACE_API_KEY == 'your-huggingface-api-key':
        print("🔍 Debug: No valid API key, using manual analysis")
        return manual_phishing_analysis(email_text, url)
    
    try:
        # Prepare the text for analysis - combine email content and URL
        analysis_text = f"Email content: {email_text}\nURL: {url}"
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Use BART model for zero-shot classification
        payload = {
            "inputs": analysis_text,
            "parameters": {
                "candidate_labels": ["phishing", "legitimate", "suspicious"]
            }
        }
        
        print(f"🔍 Debug: Making API request to {HUGGINGFACE_API_URL}")
        print(f"🔍 Debug: API Key (first 10 chars): {HUGGINGFACE_API_KEY[:10]}...")
        print(f"🔍 Debug: Payload: {payload}")
        
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"🔍 Debug: Response status code: {response.status_code}")
        print(f"🔍 Debug: Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔍 Debug: Response JSON: {result}")
            
            # BART zero-shot classification returns format: {"labels": [...], "scores": [...]}
            if isinstance(result, dict) and 'labels' in result and 'scores' in result:
                labels = result['labels']
                scores = result['scores']
                
                # Get the highest scoring label
                max_score_index = scores.index(max(scores))
                label = labels[max_score_index]
                confidence_score = scores[max_score_index]
                
                # Convert confidence score to percentage
                confidence_percentage = int(confidence_score * 100)
                
                # Determine phishing indicators based on the model's prediction
                phishing_indicators = []
                
                # Add indicators based on the prediction confidence
                if confidence_percentage > 80:
                    phishing_indicators.append("High confidence phishing detection")
                elif confidence_percentage > 60:
                    phishing_indicators.append("Medium confidence suspicious content")
                
                # Additional manual checks for common phishing indicators
                if any(word in email_text.lower() for word in ['urgent', 'immediate', 'account suspended', 'verify now']):
                    phishing_indicators.append("Contains urgent language")
                
                if any(word in email_text.lower() for word in ['password', 'credit card', 'ssn', 'social security']):
                    phishing_indicators.append("Requests sensitive information")
                
                if 'http' in url and not url.startswith('https'):
                    phishing_indicators.append("Uses HTTP instead of HTTPS")
                
                if '@' in url or any(suspicious in url for suspicious in ['login', 'verify', 'secure']):
                    phishing_indicators.append("Suspicious URL structure")
                
                # Determine result based on model prediction
                if label.lower() == 'phishing' or confidence_percentage > 70:
                    result_text = f"⚠️ HIGH RISK - Phishing detected ({confidence_percentage}% confidence)"
                elif label.lower() == 'suspicious' or confidence_percentage > 40:
                    result_text = f"⚠️ MEDIUM RISK - Suspicious email ({confidence_percentage}% confidence)"
                else:
                    result_text = f"✅ LOW RISK - Email appears safe ({confidence_percentage}% confidence)"
                
                return {
                    "result": result_text,
                    "confidence": confidence_percentage,
                    "indicators": phishing_indicators,
                    "model_prediction": label
                }
            else:
                print(f"🔍 Debug: Unexpected response format, falling back to manual analysis")
                print(f"🔍 Debug: Response type: {type(result)}")
                # Fallback to manual analysis if model response is unexpected
                return manual_phishing_analysis(email_text, url)
        else:
            print(f"🔍 Debug: API request failed with status {response.status_code}")
            print(f"🔍 Debug: Response text: {response.text}")
            
            # Try to get more specific error information
            try:
                error_detail = response.json()
                error_message = error_detail.get('error', 'Unknown API error')
                return {
                    "result": f"❌ API Error: {error_message}",
                    "confidence": 0,
                    "indicators": []
                }
            except:
                return {
                    "result": f"❌ Error: API request failed (Status: {response.status_code})",
                    "confidence": 0,
                    "indicators": []
                }
            
    except requests.exceptions.Timeout:
        print("🔍 Debug: Request timed out")
        return {
            "result": "❌ Error: Request timed out. Please try again.",
            "confidence": 0,
            "indicators": []
        }
    except requests.exceptions.ConnectionError:
        print("🔍 Debug: Connection error")
        return {
            "result": "❌ Error: Connection failed. Please check your internet connection.",
            "confidence": 0,
            "indicators": []
        }
    except Exception as e:
        print(f"🔍 Debug: Exception occurred: {str(e)}")
        print("🔍 Debug: Trying fallback model...")
        return try_fallback_model(email_text, url)

def try_fallback_model(email_text, url):
    """Try the fallback model if the primary model fails"""
    try:
        print(f"🔍 Debug: Using fallback model: {FALLBACK_MODEL_URL}")
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": f"Email content: {email_text}\nURL: {url}",
            "parameters": {
                "max_length": 100,
                "temperature": 0.7
            }
        }
        
        response = requests.post(FALLBACK_MODEL_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("🔍 Debug: Fallback model successful, using manual analysis")
            return manual_phishing_analysis(email_text, url)
        else:
            print(f"🔍 Debug: Fallback model also failed: {response.status_code}")
            return manual_phishing_analysis(email_text, url)
            
    except Exception as e:
        print(f"🔍 Debug: Fallback model exception: {str(e)}")
        return manual_phishing_analysis(email_text, url)

def manual_phishing_analysis(email_text, url):
    """Fallback manual analysis when model is unavailable"""
    phishing_indicators = []
    confidence = 0
    
    # Check for common phishing indicators
    if any(word in email_text.lower() for word in ['urgent', 'immediate', 'account suspended', 'verify now']):
        phishing_indicators.append("Contains urgent language")
        confidence += 20
    
    if any(word in email_text.lower() for word in ['password', 'credit card', 'ssn', 'social security']):
        phishing_indicators.append("Requests sensitive information")
        confidence += 25
    
    if 'http' in url and not url.startswith('https'):
        phishing_indicators.append("Uses HTTP instead of HTTPS")
        confidence += 15
    
    if '@' in url or any(suspicious in url for suspicious in ['login', 'verify', 'secure']):
        phishing_indicators.append("Suspicious URL structure")
        confidence += 20
    
    if len(email_text) < 50:
        phishing_indicators.append("Very short email content")
        confidence += 10
    
    # Determine result based on confidence
    if confidence >= 70:
        result_text = f"⚠️ HIGH RISK - Phishing detected ({confidence}% confidence)"
    elif confidence >= 40:
        result_text = f"⚠️ MEDIUM RISK - Suspicious email ({confidence}% confidence)"
    else:
        result_text = f"✅ LOW RISK - Email appears safe ({confidence}% confidence)"
    
    return {
        "result": result_text,
        "confidence": confidence,
        "indicators": phishing_indicators
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/detector.html')
def detector():
    if 'user_id' not in session:
        return redirect('/login.html')
    return render_template('detector.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({"message": "All fields are required"}), 400
    
    # Validate password strength
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({"message": message}), 400
    
    # Check if user already exists
    try:
        existing_user = mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]})
    except:
        # Fallback for mock database
        existing_user = mongo.db.users.find_one({"username": username})
        if not existing_user:
            existing_user = mongo.db.users.find_one({"email": email})
    
    if existing_user:
        return jsonify({"message": "Username or email already exists"}), 400
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    # Generate OTP
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    # Store user in database
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "otp": otp,
        "otp_expiry": otp_expiry,
        "mfa_enabled": True,  # Enable MFA for all users
        "created_at": datetime.utcnow()
    }
    
    mongo.db.users.insert_one(user_data)
    
    # Send OTP email
    if send_otp_email(email, otp):
        return jsonify({
            "message": "Account created successfully! Please check your email for OTP verification.",
            "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        }), 200
    else:
        # If email sending fails, delete the user account and return error
        mongo.db.users.delete_one({"_id": user_data.get("_id")})
        return jsonify({
            "message": "Failed to send OTP email. Please check your email address and try again."
        }), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    # Find user
    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    # Always require MFA for security
    # Generate new OTP
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    # Update OTP in database
    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"otp": otp, "otp_expiry": otp_expiry}}
    )
    
    # Send OTP email
    if send_otp_email(user['email'], otp):
        return jsonify({
            "message": "OTP sent to your email",
            "mfa_required": True
        }), 200
    else:
        return jsonify({
            "message": "Failed to send OTP email. Please check your email address and try again."
        }), 500

@app.route('/api/verify_mfa', methods=['POST'])
def api_verify_mfa():
    data = request.get_json()
    username = data.get('username')
    mfa_code = data.get('mfa_code')
    
    if not username or not mfa_code:
        return jsonify({"message": "Username and MFA code are required"}), 400
    
    # Find user
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Check OTP
    if user.get('otp') != mfa_code:
        return jsonify({"message": "Invalid MFA code"}), 401
    
    # Check if OTP is expired
    if datetime.utcnow() > user.get('otp_expiry', datetime.min):
        return jsonify({"message": "MFA code has expired"}), 401
    
    # Clear OTP and set session
    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {"$unset": {"otp": "", "otp_expiry": ""}}
    )
    
    session['user_id'] = str(user['_id'])
    session['username'] = user['username']
    
    return jsonify({"message": "MFA verification successful"}), 200

@app.route('/api/detect', methods=['POST'])
def api_detect():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    
    data = request.get_json()
    email_text = data.get('emailText', '')
    url = data.get('url', '')
    
    if not email_text:
        return jsonify({"message": "Email content is required"}), 400
    
    # Analyze email for phishing using comprehensive analysis
    analysis_result = comprehensive_analyzer.analyze_email_comprehensive(email_text, url)
    
    # Store detection result in database
    detection_record = {
        "user_id": session['user_id'],
        "email_content": email_text,
        "url": url,
        "result": analysis_result["result"],
        "confidence": analysis_result["confidence"],
        "indicators": analysis_result["indicators"],
        "timestamp": datetime.utcnow()
    }
    
    mongo.db.detections.insert_one(detection_record)
    
    return jsonify(analysis_result), 200

@app.route('/api/resend_otp', methods=['POST'])
def api_resend_otp():
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({"message": "Username is required"}), 400
    
    # Find user
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Generate new OTP
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    # Update OTP in database
    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"otp": otp, "otp_expiry": otp_expiry}}
    )
    
    # Send OTP email
    if send_otp_email(user['email'], otp):
        return jsonify({"message": "New OTP sent to your email"}), 200
    else:
        return jsonify({
            "message": "Failed to send OTP email. Please check your email address and try again."
        }), 500

@app.route('/api/user_info')
def api_user_info():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    
    # Get user info from database
    user = mongo.db.users.find_one({"_id": ObjectId(session['user_id'])})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "username": user['username'],
        "email": user['email']
    }), 200

@app.route('/api/analysis_history')
def api_analysis_history():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    
    try:
        # Get analysis history for the current user
        history = list(mongo.db.detections.find(
            {"user_id": session['user_id']},
            {
                "email_content": 1,
                "url": 1,
                "result": 1,
                "confidence": 1,
                "indicators": 1,
                "timestamp": 1,
                "_id": 0
            }
        ).sort("timestamp", -1).limit(10))  # Get last 10 analyses
        
        # Format the history data
        formatted_history = []
        for item in history:
            # Create email preview (first 100 characters)
            email_preview = item.get('email_content', '')[:100]
            if len(item.get('email_content', '')) > 100:
                email_preview += "..."
            
            # Format timestamp
            timestamp = item.get('timestamp', datetime.utcnow())
            if isinstance(timestamp, datetime):
                formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M")
            else:
                formatted_timestamp = str(timestamp)
            
            formatted_history.append({
                "email_preview": email_preview,
                "url": item.get('url', ''),
                "result": item.get('result', ''),
                "confidence": item.get('confidence', 0),
                "indicators": item.get('indicators', []),
                "timestamp": formatted_timestamp
            })
        
        return jsonify({
            "history": formatted_history
        }), 200
        
    except Exception as e:
        print(f"Error fetching analysis history: {e}")
        return jsonify({"message": "Error fetching history"}), 500

@app.route('/api/logout')
def api_logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

# Initialize comprehensive analyzer
comprehensive_analyzer = ComprehensiveEmailAnalyzer(HUGGINGFACE_API_KEY, HUGGINGFACE_API_URL)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
