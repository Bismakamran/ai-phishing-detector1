#!/usr/bin/env python3
"""
Detailed Email Debugging Script
This script helps identify the exact issue with Gmail authentication.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_email_configuration():
    """Debug the email configuration step by step"""
    
    # Get email configuration
    email_address = os.getenv('EMAIL_ADDRESS', 'mailguard849@gmail.com')
    email_password = os.getenv('EMAIL_PASSWORD', 'Mailguard123')
    
    print("🔧 Detailed Email Configuration Debug")
    print("=" * 50)
    print(f"📧 Email Address: {email_address}")
    print(f"🔑 Password Length: {len(email_password)} characters")
    print(f"🔑 Password (first 4 chars): {email_password[:4]}...")
    print(f"🔑 Password contains spaces: {'Yes' if ' ' in email_password else 'No'}")
    
    # Check if using default password
    if email_password == 'Mailguard123':
        print("⚠️  WARNING: Using default password!")
        print("   This will not work with Gmail SMTP.")
        return False
    
    # Check password format
    if len(email_password) != 16:
        print(f"⚠️  WARNING: App Password should be 16 characters, got {len(email_password)}")
        print("   Make sure you're using the correct App Password format.")
    
    if ' ' in email_password:
        print("⚠️  WARNING: App Password contains spaces!")
        print("   Remove all spaces from the App Password.")
        # Try without spaces
        email_password = email_password.replace(' ', '')
        print(f"   Trying without spaces: {email_password}")
    
    # Test SMTP connection step by step
    try:
        print("\n🔍 Step 1: Testing SMTP connection...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("✅ SMTP connection established")
        
        print("\n🔍 Step 2: Starting TLS...")
        server.starttls()
        print("✅ TLS started successfully")
        
        print("\n🔍 Step 3: Attempting login...")
        print(f"   Username: {email_address}")
        print(f"   Password: {email_password[:4]}...")
        
        server.login(email_address, email_password)
        print("✅ Login successful!")
        
        # Test sending a simple email
        print("\n🔍 Step 4: Testing email sending...")
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = email_address
        msg['Subject'] = "MailGuard - Email Test"
        
        body = "This is a test email from MailGuard."
        msg.attach(MIMEText(body, 'plain'))
        
        text = msg.as_string()
        server.sendmail(email_address, email_address, text)
        print("✅ Test email sent successfully!")
        
        server.quit()
        print("\n🎉 SUCCESS: Email configuration is working perfectly!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure 2-Factor Authentication is enabled on your Gmail account")
        print("2. Go to https://myaccount.google.com/apppasswords")
        print("3. Generate a new App Password for 'Mail'")
        print("4. Copy the 16-character password (without spaces)")
        print("5. Update your .env file with the new password")
        return False
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"\n❌ RECIPIENT ERROR: {e}")
        print("   The email address might be invalid or blocked.")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"\n❌ SERVER ERROR: {e}")
        print("   Gmail server connection issue.")
        return False
        
    except Exception as e:
        print(f"\n❌ UNKNOWN ERROR: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    """Main function"""
    print("MailGuard Email Debugging Tool")
    print("=" * 50)
    print()
    
    success = debug_email_configuration()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 Email configuration is ready!")
        print("   You can now run the main application.")
    else:
        print("🔧 Please follow the troubleshooting steps above.")
        print("   Then run this debug script again.")
    
    print()
    print("To run the main application:")
    print("   python app.py")

if __name__ == "__main__":
    main()

