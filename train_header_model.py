#!/usr/bin/env python3
"""
Header Model Training Script
Trains the Random Forest model for email header analysis.
"""

import pandas as pd
import numpy as np
import os
import sys
from header_ml_model import HeaderMLModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_kaggle_dataset():
    """Download phishing email dataset from Kaggle"""
    try:
        import kagglehub
        
        print("📥 Downloading phishing email dataset from Kaggle...")
        
        # Download a popular phishing email dataset
        # You can replace this with your specific dataset
        dataset_path = kagglehub.model_download('phishing-email-dataset')
        
        print(f"✅ Dataset downloaded to: {dataset_path}")
        return dataset_path
        
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        print("❌ Failed to download dataset from Kaggle")
        print("Please manually download a phishing email dataset and place it in the project directory")
        return None

def prepare_sample_dataset():
    """Create a sample dataset for testing if no Kaggle dataset is available"""
    print("📝 Creating sample dataset for testing...")
    
    # Sample phishing emails with headers
    phishing_emails = [
        {
            "email_content": """From: security@paypal-security.com
Subject: URGENT: Your PayPal account has been suspended
Date: Mon, 30 Aug 2025 10:00:00 +0000
Message-ID: <123456@paypal-security.com>
Return-Path: <security@paypal-security.com>
Reply-To: <support@paypal-verify.com>

Dear Customer,
Your PayPal account has been suspended due to suspicious activity.
Click here to verify your account: http://paypal-verify.com/login
""",
            "label": "phishing"
        },
        {
            "email_content": """From: noreply@bankofamerica.com
Subject: Security Alert: Unusual Login Detected
Date: Mon, 30 Aug 2025 11:00:00 +0000
Message-ID: <789012@bankofamerica.com>
Return-Path: <noreply@bankofamerica.com>
Reply-To: <security@bankofamerica.com>

We detected an unusual login to your account.
Please verify your identity: https://bankofamerica.com/verify
""",
            "label": "phishing"
        },
        {
            "email_content": """From: support@microsoft.com
Subject: Your Microsoft account needs attention
Date: Mon, 30 Aug 2025 12:00:00 +0000
Message-ID: <345678@microsoft.com>
Return-Path: <support@microsoft.com>
Reply-To: <support@microsoft.com>

Your Microsoft account requires immediate attention.
Please click here to resolve: http://microsoft-verify.com/account
""",
            "label": "phishing"
        }
    ]
    
    # Sample legitimate emails with headers
    legitimate_emails = [
        {
            "email_content": """From: noreply@github.com
Subject: [GitHub] Your repository has been updated
Date: Mon, 30 Aug 2025 13:00:00 +0000
Message-ID: <abc123@github.com>
Return-Path: <noreply@github.com>
Reply-To: <support@github.com>

Your repository "my-project" has been updated.
View the changes: https://github.com/user/my-project
""",
            "label": "legitimate"
        },
        {
            "email_content": """From: notifications@linkedin.com
Subject: You have 3 new messages on LinkedIn
Date: Mon, 30 Aug 2025 14:00:00 +0000
Message-ID: <def456@linkedin.com>
Return-Path: <notifications@linkedin.com>
Reply-To: <support@linkedin.com>

You have 3 new messages waiting for you.
View messages: https://linkedin.com/messages
""",
            "label": "legitimate"
        },
        {
            "email_content": """From: hello@slack.com
Subject: New message in #general
Date: Mon, 30 Aug 2025 15:00:00 +0000
Message-ID: <ghi789@slack.com>
Return-Path: <hello@slack.com>
Reply-To: <support@slack.com>

You have a new message in the #general channel.
View message: https://slack.com/app
""",
            "label": "legitimate"
        }
    ]
    
    # Combine all emails
    all_emails = phishing_emails + legitimate_emails
    
    # Create DataFrame
    df = pd.DataFrame(all_emails)
    
    # Save to CSV
    dataset_path = "sample_phishing_dataset.csv"
    df.to_csv(dataset_path, index=False)
    
    print(f"✅ Sample dataset created: {dataset_path}")
    return dataset_path

def train_model(dataset_path: str):
    """Train the header analysis model"""
    try:
        print("🤖 Training header analysis model...")
        
        # Initialize model
        model = HeaderMLModel()
        
        # Train model
        training_result = model.train(dataset_path)
        
        if training_result["success"]:
            print("✅ Model training completed successfully!")
            print(f"📊 Accuracy: {training_result['accuracy']:.2%}")
            print("\n📋 Classification Report:")
            print(training_result["classification_report"])
            
            print("\n🔍 Feature Importance:")
            feature_importance = training_result["feature_importance"]
            for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
                print(f"  {feature}: {importance:.4f}")
            
            # Save model
            model_path = "header_analysis_model.pkl"
            model.save_model(model_path)
            print(f"\n💾 Model saved to: {model_path}")
            
            return True
        else:
            print(f"❌ Model training failed: {training_result['error']}")
            return False
            
    except Exception as e:
        logger.error(f"Error training model: {e}")
        print(f"❌ Error during training: {e}")
        return False

def test_model():
    """Test the trained model with sample data"""
    try:
        print("\n🧪 Testing trained model...")
        
        # Load model
        model = HeaderMLModel()
        model.load_model("header_analysis_model.pkl")
        
        # Test with sample phishing email
        test_email = """From: security@paypal-security.com
Subject: URGENT: Your account has been suspended
Date: Mon, 30 Aug 2025 10:00:00 +0000
Message-ID: <test123@paypal-security.com>
Return-Path: <security@paypal-security.com>
Reply-To: <support@paypal-verify.com>

Your account has been suspended. Click here to verify.
"""
        
        # Parse headers
        from email import message_from_string
        email_message = message_from_string(test_email)
        headers = dict(email_message.items())
        
        # Make prediction
        prediction = model.predict(headers)
        
        print("📧 Test Email Headers:")
        for key, value in headers.items():
            print(f"  {key}: {value}")
        
        print(f"\n🔮 Prediction: {prediction['prediction']}")
        print(f"📊 Probabilities: {prediction['probability']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing model: {e}")
        print(f"❌ Error during testing: {e}")
        return False

def main():
    """Main training function"""
    print("🚀 Starting Header Analysis Model Training")
    print("=" * 50)
    
    # Try to download dataset from Kaggle
    dataset_path = download_kaggle_dataset()
    
    # If Kaggle download fails, create sample dataset
    if not dataset_path:
        dataset_path = prepare_sample_dataset()
    
    if not dataset_path or not os.path.exists(dataset_path):
        print("❌ No dataset available for training")
        return
    
    # Train model
    success = train_model(dataset_path)
    
    if success:
        # Test model
        test_model()
        print("\n🎉 Training and testing completed successfully!")
        print("The model is ready to use in the MailGuard application.")
    else:
        print("\n❌ Training failed. Please check the error messages above.")

if __name__ == "__main__":
    main()

