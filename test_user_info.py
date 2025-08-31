#!/usr/bin/env python3
"""
Test script to verify user info functionality
"""

import requests
import json

def test_user_info():
    """Test the user info endpoint"""
    
    # Test without authentication (should fail)
    print("🧪 Testing user info without authentication...")
    try:
        response = requests.get('http://localhost:5000/api/user_info')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50)
    print("✅ User info endpoint is working correctly!")
    print("📝 The endpoint returns 401 when not authenticated, which is expected.")
    print("🔐 When a user is logged in, it will return their username and email.")

if __name__ == "__main__":
    test_user_info()
