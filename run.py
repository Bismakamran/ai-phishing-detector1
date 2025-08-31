#!/usr/bin/env python3
"""
MailGuard Startup Script
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("📝 Creating .env file from template...")
        
        try:
            with open('env_example.txt', 'r') as template:
                with open('.env', 'w') as env:
                    env.write(template.read())
            print("✅ .env file created from template")
            print("📋 Please edit .env file with your configuration")
            return False
        except FileNotFoundError:
            print("❌ env_example.txt not found")
            return False
    
    # Check if required environment variables are set
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['SECRET_KEY', 'MONGO_URI', 'HUGGINGFACE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your-'):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing or default environment variables: {', '.join(missing_vars)}")
        print("📋 Please update your .env file with proper values")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    print("📦 Checking dependencies...")
    
    try:
        import flask
        import flask_pymongo
        import werkzeug
        import requests
        import dotenv
        import pymongo
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_mongodb():
    """Check MongoDB connection"""
    print("🗄️  Checking MongoDB connection...")
    
    try:
        from app import mongo
        mongo.db.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("💡 Make sure MongoDB is running")
        return False

def main():
    """Main startup function"""
    print("🛡️  MailGuard - AI Phishing Email Detector")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment not properly configured")
        print("Please fix the issues above and try again")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies not installed")
        print("Please install dependencies and try again")
        sys.exit(1)
    
    # Check MongoDB
    if not check_mongodb():
        print("\n⚠️  MongoDB not available")
        print("The application may not work properly")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n🚀 Starting MailGuard...")
    print("=" * 50)
    
    try:
        from app import app
        print("✅ Application loaded successfully")
        print("🌐 Starting web server...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down MailGuard...")
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
