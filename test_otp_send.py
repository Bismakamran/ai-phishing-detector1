#!/usr/bin/env python3
"""
OTP Sending Test Script
This script tests the OTP sending functionality directly.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import secrets
import string

# Load environment variables
load_dotenv()

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'mailguard849@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'Mailguard123')

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def send_otp_email(email, otp):
    """Send OTP via email - same function as in app.py"""
    try:
        print(f"📧 Attempting to send OTP to: {email}")
        print(f"📧 Using email: {EMAIL_ADDRESS}")
        print(f"🔑 Password length: {len(EMAIL_PASSWORD)}")
        
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
        print("📡 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print(f"🔐 Attempting to login with email: {EMAIL_ADDRESS}")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        print("📤 Sending email...")
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
        print(f"❌ Error type: {type(e).__name__}")
        return False

def main():
    """Main function"""
    print("MailGuard OTP Sending Test")
    print("=" * 40)
    print()
    
    # Test email address (you can change this to your email)
    test_email = input("Enter email address to send test OTP: ").strip()
    
    if not test_email:
        test_email = "mailguard849@gmail.com"  # Default to sending to yourself
    
    print(f"📧 Sending test OTP to: {test_email}")
    print()
    
    # Generate OTP
    otp = generate_otp()
    print(f"🔢 Generated OTP: {otp}")
    print()
    
    # Send OTP
    success = send_otp_email(test_email, otp)
    
    print()
    print("=" * 40)
    if success:
        print("🎉 OTP sending test successful!")
        print(f"📧 Check your inbox at: {test_email}")
        print(f"🔢 OTP code: {otp}")
    else:
        print("❌ OTP sending test failed!")
        print("🔧 Please check the error messages above.")

if __name__ == "__main__":
    main()

