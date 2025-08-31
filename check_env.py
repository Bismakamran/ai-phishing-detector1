#!/usr/bin/env python3
"""
Environment Variables Check Script
This script checks what environment variables are currently loaded.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check the current environment variables"""
    
    print("🔍 Environment Variables Check")
    print("=" * 40)
    
    # Check email configuration
    email_address = os.getenv('EMAIL_ADDRESS', 'mailguard849@gmail.com')
    email_password = os.getenv('EMAIL_PASSWORD', 'Mailguard123')
    
    print(f"📧 EMAIL_ADDRESS: {email_address}")
    print(f"🔑 EMAIL_PASSWORD: {email_password[:4]}... (length: {len(email_password)})")
    
    # Check if using default password
    if email_password == 'Mailguard123':
        print("⚠️  WARNING: Using default password!")
    elif len(email_password) == 16:
        print("✅ App Password format looks correct")
    else:
        print(f"⚠️  WARNING: Unexpected password length: {len(email_password)}")
    
    # Check other important variables
    secret_key = os.getenv('SECRET_KEY', 'not-set')
    mongo_uri = os.getenv('MONGO_URI', 'not-set')
    huggingface_key = os.getenv('HUGGINGFACE_API_KEY', 'not-set')
    
    print(f"🔐 SECRET_KEY: {secret_key[:10]}... (length: {len(secret_key)})")
    print(f"🗄️  MONGO_URI: {mongo_uri}")
    print(f"🤖 HUGGINGFACE_API_KEY: {huggingface_key[:10]}... (length: {len(huggingface_key)})")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            print(f"📄 .env file size: {len(content)} characters")
    else:
        print("❌ .env file not found")

if __name__ == "__main__":
    check_environment()

