#!/usr/bin/env python3
"""
Test MongoDB Atlas connection
"""

import os
from pymongo import MongoClient
from datetime import datetime

def test_mongodb_atlas():
    """Test connection to MongoDB Atlas"""
    
    print("🗄️ Testing MongoDB Atlas Connection")
    print("=" * 50)
    
    # Get connection string from environment or user input
    mongo_uri = os.getenv('MONGO_URI')
    
    if not mongo_uri:
        print("❌ MONGO_URI environment variable not found")
        print("\n📝 Please set your MongoDB Atlas connection string:")
        print("1. Go to MongoDB Atlas dashboard")
        print("2. Click 'Connect' on your cluster")
        print("3. Choose 'Connect your application'")
        print("4. Copy the connection string")
        print("5. Replace <password> with your database user password")
        print("6. Add /mailguard at the end of the URI")
        print("\nExample:")
        print("mongodb+srv://phishing_detector_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/mailguard?retryWrites=true&w=majority")
        
        # Ask user to input connection string
        mongo_uri = input("\n🔗 Enter your MongoDB Atlas connection string: ").strip()
        
        if not mongo_uri:
            print("❌ No connection string provided. Exiting.")
            return
    
    try:
        print("🔌 Attempting to connect to MongoDB Atlas...")
        
        # Connect to MongoDB Atlas
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get database info
        db = client.get_database()
        print(f"📊 Database name: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📁 Collections: {collections}")
        
        # Test basic operations
        print("\n🧪 Testing basic operations...")
        
        # Test insert
        test_collection = db.test_connection
        test_doc = {
            "test": True,
            "timestamp": datetime.now(),
            "message": "MongoDB Atlas connection test"
        }
        
        result = test_collection.insert_one(test_doc)
        print(f"✅ Insert test: Document ID {result.inserted_id}")
        
        # Test find
        found_doc = test_collection.find_one({"test": True})
        print(f"✅ Find test: Found document with ID {found_doc['_id']}")
        
        # Test delete
        delete_result = test_collection.delete_one({"test": True})
        print(f"✅ Delete test: Deleted {delete_result.deleted_count} document")
        
        # Test with your actual collections
        print("\n📧 Testing with your application collections...")
        
        if 'users' in collections:
            user_count = db.users.count_documents({})
            print(f"👥 Users collection: {user_count} documents")
        
        if 'detections' in collections:
            detection_count = db.detections.count_documents({})
            print(f"📧 Detections collection: {detection_count} documents")
        
        # Get cluster info
        print("\n📊 Cluster Information:")
        cluster_info = client.admin.command('serverStatus')
        print(f"   MongoDB version: {cluster_info.get('version', 'Unknown')}")
        print(f"   Uptime: {cluster_info.get('uptime', 0)} seconds")
        
        client.close()
        print("\n✅ MongoDB Atlas connection test completed successfully!")
        print("\n🎯 Your cluster is ready for deployment!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your connection string format")
        print("2. Verify username and password")
        print("3. Ensure network access allows all IPs (0.0.0.0/0)")
        print("4. Check if cluster is active")
        print("5. Verify database user has correct permissions")

if __name__ == "__main__":
    test_mongodb_atlas()
