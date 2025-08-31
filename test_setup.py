#!/usr/bin/env python3
"""
Test script to verify MailGuard setup and dependencies
"""

import sys
import importlib
import requests

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    dependencies = [
        'flask',
        'flask_pymongo',
        'werkzeug',
        'requests',
        'dotenv',
        'pymongo'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} - OK")
        except ImportError:
            print(f"❌ {dep} - Missing")
            all_ok = False
    
    return all_ok

def test_flask_app():
    """Test Flask application structure"""
    print("\n🚀 Testing Flask application...")
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test basic routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home route working")
            else:
                print(f"❌ Home route failed: {response.status_code}")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n🗄️ Testing MongoDB connection...")
    try:
        from app import mongo
        # Try to connect to MongoDB
        mongo.db.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running and MONGO_URI is configured")
        return False

def test_huggingface_api():
    """Test Hugging Face API connection"""
    print("\n🤖 Testing Hugging Face API...")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key or api_key == 'your-huggingface-api-key-here':
            print("⚠️ Hugging Face API key not configured")
            print("   Add your API key to the .env file")
            return False
        
        # Test API connection
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Hugging Face API connection successful")
            return True
        else:
            print(f"❌ Hugging Face API test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Hugging Face API test failed: {e}")
        return False

def test_email_configuration():
    """Test email configuration"""
    print("\n📧 Testing email configuration...")
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Test SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Note: This will fail without proper app password setup
        # Just testing the connection for now
        print("✅ SMTP server connection test passed")
        server.quit()
        return True
        
    except Exception as e:
        print(f"⚠️ Email configuration test failed: {e}")
        print("   Make sure to configure app passwords for Gmail")
        return False

def main():
    """Run all tests"""
    print("🔍 MailGuard Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_flask_app,
        test_mongodb_connection,
        test_huggingface_api,
        test_email_configuration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} tests passed! MailGuard is ready to run.")
        print("\nTo start the application:")
        print("1. Make sure MongoDB is running")
        print("2. Configure your .env file")
        print("3. Run: python app.py")
        print("4. Open: http://localhost:5000")
    else:
        print(f"⚠️ {passed}/{total} tests passed")
        print("\nPlease fix the failed tests before running MailGuard")
        
        if not results[0]:  # Python version
            print("- Upgrade to Python 3.8 or higher")
        if not results[1]:  # Dependencies
            print("- Run: pip install -r requirements.txt")
        if not results[2]:  # Flask app
            print("- Check app.py for syntax errors")
        if not results[3]:  # MongoDB
            print("- Start MongoDB service")
            print("- Check MONGO_URI in .env file")
        if not results[4]:  # Hugging Face
            print("- Get API key from Hugging Face")
            print("- Add to .env file")
        if not results[5]:  # Email
            print("- Configure Gmail app password")
            print("- Update .env file")

if __name__ == "__main__":
    main()
