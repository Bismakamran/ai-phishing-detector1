#!/usr/bin/env python3
"""
Script to view MongoDB database contents
"""

import os
from pymongo import MongoClient
from datetime import datetime
import json

def view_database():
    """View all data in the MongoDB database"""
    
    # Get MongoDB connection string from environment or use default
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        
        # List all databases
        print("📊 Available Databases:")
        print("=" * 50)
        for db_name in client.list_database_names():
            print(f"  - {db_name}")
        
        # Connect to the phishing detector database
        db_name = 'mailguard'  # Database name from app.py
        db = client[db_name]
        
        print(f"\n🔍 Database: {db_name}")
        print("=" * 50)
        
        # List all collections
        collections = db.list_collection_names()
        print(f"Collections found: {collections}")
        
        # View Users Collection
        if 'users' in collections:
            print(f"\n👥 Users Collection ({db.users.count_documents({})} documents):")
            print("-" * 50)
            users = list(db.users.find({}, {'password_hash': 0}))  # Exclude password hashes
            for i, user in enumerate(users, 1):
                print(f"\nUser {i}:")
                print(f"  ID: {user.get('_id')}")
                print(f"  Username: {user.get('username', 'N/A')}")
                print(f"  Email: {user.get('email', 'N/A')}")
                print(f"  Created: {user.get('created_at', 'N/A')}")
                if 'otp' in user:
                    print(f"  OTP: {user.get('otp', 'N/A')}")
                    print(f"  OTP Expiry: {user.get('otp_expiry', 'N/A')}")
        
        # View Detections Collection
        if 'detections' in collections:
            print(f"\n📧 Detections Collection ({db.detections.count_documents({})} documents):")
            print("-" * 50)
            detections = list(db.detections.find().sort('timestamp', -1).limit(10))  # Last 10 detections
            for i, detection in enumerate(detections, 1):
                print(f"\nDetection {i}:")
                print(f"  ID: {detection.get('_id')}")
                print(f"  User ID: {detection.get('user_id', 'N/A')}")
                print(f"  Email Content Preview: {detection.get('email_content', 'N/A')[:100]}...")
                print(f"  Confidence Score: {detection.get('confidence_score', 'N/A')}")
                print(f"  Result: {detection.get('result', 'N/A')}")
                print(f"  Timestamp: {detection.get('timestamp', 'N/A')}")
                
                # Show analysis breakdown if available
                if 'analysis_breakdown' in detection:
                    print(f"  Analysis Breakdown:")
                    breakdown = detection['analysis_breakdown']
                    for key, value in breakdown.items():
                        print(f"    {key}: {value}")
        
        # Show database statistics
        print(f"\n📈 Database Statistics:")
        print("-" * 50)
        print(f"Total Users: {db.users.count_documents({})}")
        print(f"Total Detections: {db.detections.count_documents({})}")
        
        # Show recent activity
        recent_detections = db.detections.find().sort('timestamp', -1).limit(5)
        print(f"\n🕒 Recent Activity (Last 5 detections):")
        print("-" * 50)
        for detection in recent_detections:
            timestamp = detection.get('timestamp', 'Unknown')
            if isinstance(timestamp, datetime):
                timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            print(f"  {timestamp} - Score: {detection.get('confidence_score', 'N/A')} - Result: {detection.get('result', 'N/A')}")
        
        client.close()
        print(f"\n✅ Database connection closed successfully!")
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MongoDB is running")
        print("2. Check your MONGO_URI environment variable")
        print("3. Verify the database name in your app.py file")

if __name__ == "__main__":
    view_database()
