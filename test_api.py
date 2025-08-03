"""
Simple test script for the User Management API
Run this to make sure everything works after the fixes
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_create_user():
    print("Testing: Create User")
    data = {
        "name": "John Doe",
        "email": "john@example.com", 
        "password": "mypassword123"
    }
    response = requests.post(f"{BASE_URL}/users", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_users():
    print("Testing: Get All Users")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_user_by_id():
    print("Testing: Get User by ID")
    response = requests.get(f"{BASE_URL}/user/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login():
    print("Testing: User Login")
    data = {
        "email": "john@example.com",
        "password": "mypassword123"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search():
    print("Testing: Search Users")
    response = requests.get(f"{BASE_URL}/search?name=John")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_update_user():
    print("Testing: Update User")
    data = {
        "name": "John Updated",
        "email": "john.updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/user/1", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("🧪 Testing User Management API")
    print("Make sure the Flask app is running first!\n")
    
    try:
        # Test home page
        print("Testing: Home Page")
        response = requests.get(BASE_URL)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Run tests
        test_create_user()
        test_get_users()
        test_get_user_by_id()
        test_login()
        test_search()
        test_update_user()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Can't connect to the server.")
        print("Make sure you run 'python app.py' first!")
    except Exception as e:
        print(f"❌ Error: {e}")
