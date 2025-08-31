#!/usr/bin/env python3
"""
Email Configuration Test Script
This script helps you test if your email configuration is working properly.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_configuration():
    """Test the email configuration"""
    
    # Get email configuration
    email_address = os.getenv('EMAIL_ADDRESS', 'mailguard849@gmail.com')
    email_password = os.getenv('EMAIL_PASSWORD', 'Mailguard123')
    
    print("🔧 Email Configuration Test")
    print("=" * 40)
    print(f"📧 Email Address: {email_address}")
    print(f"🔑 Password: {'*' * len(email_password)} ({len(email_password)} characters)")
    
    # Check if using default password
    if email_password == 'Mailguard123':
        print("⚠️  WARNING: Using default password!")
        print("   You need to set up Gmail App Password:")
        print("   1. Enable 2-factor authentication on your Gmail account")
        print("   2. Go to https://myaccount.google.com/apppasswords")
        print("   3. Generate a new app password for 'Mail'")
        print("   4. Update your .env file with the 16-character app password")
        print()
        return False
    
    # Test SMTP connection
    try:
        print("🔍 Testing SMTP connection...")
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = email_address  # Send to yourself for testing
        msg['Subject'] = "MailGuard - Email Configuration Test"
        
        body = """
        This is a test email from MailGuard.
        
        If you received this email, your email configuration is working correctly!
        
        Best regards,
        MailGuard Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP
        print("📡 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔐 Attempting to login...")
        server.login(email_address, email_password)
        
        print("📤 Sending test email...")
        text = msg.as_string()
        server.sendmail(email_address, email_address, text)
        server.quit()
        
        print("✅ SUCCESS: Email configuration is working!")
        print("📧 Check your inbox for a test email from yourself.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ AUTHENTICATION ERROR: {e}")
        print("   This usually means:")
        print("   - Wrong password")
        print("   - Using regular password instead of App Password")
        print("   - 2-factor authentication not enabled")
        return False
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ RECIPIENT ERROR: {e}")
        print("   The email address might be invalid.")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ SERVER ERROR: {e}")
        print("   Gmail server connection issue.")
        return False
        
    except Exception as e:
        print(f"❌ UNKNOWN ERROR: {e}")
        return False

def main():
    """Main function"""
    print("MailGuard Email Configuration Test")
    print("=" * 40)
    print()
    
    success = test_email_configuration()
    
    print()
    print("=" * 40)
    if success:
        print("🎉 Email configuration is ready!")
        print("   You can now run the main application.")
    else:
        print("🔧 Please fix the email configuration issues above.")
        print("   Then run this test again.")
    
    print()
    print("To run the main application:")
    print("   python app.py")

if __name__ == "__main__":
    main()
