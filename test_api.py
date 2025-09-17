import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Testing SprintSync API Endpoints\n")
    print("=" * 50)
    
    # Test data
    timestamp = int(time.time())
    test_user = {
        "username": f"testuser_{timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "password123"
    }
    
    test_task = {
        "title": "Test Task",
        "description": "This is a test task created by API test"
    }
    
    access_token = None
    task_id = None
    
    try:
        # 1. Test user registration
        print("1. Testing user registration...")
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user
        )
        
        if response.status_code == 200:
            print("✓ User registration successful")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
        else:
            print(f"✗ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # 2. Test user login
        print("\n2. Testing user login...")
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={
                "grant_type": "password",
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        
        if response.status_code == 200:
            print("✓ User login successful")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   Access token: {access_token[:20]}...")
        else:
            print(f"✗ User login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 3. Test task creation
        print("\n3. Testing task creation...")
        response = requests.post(
            f"{BASE_URL}/tasks",
            headers=headers,
            json=test_task
        )
        
        if response.status_code == 200:
            print("✓ Task creation successful")
            task_data = response.json()
            task_id = task_data["id"]
            print(f"   Task ID: {task_id}")
        else:
            print(f"✗ Task creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # 4. Test getting all tasks
        print("\n4. Testing get all tasks...")
        response = requests.get(
            f"{BASE_URL}/tasks",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Get tasks successful")
            tasks = response.json()
            print(f"   Found {len(tasks)} tasks")
        else:
            print(f"✗ Get tasks failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # 5. Test getting a specific task
        print("\n5. Testing get specific task...")
        response = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Get specific task successful")
            task = response.json()
            print(f"   Task title: {task['title']}")
        else:
            print(f"✗ Get specific task failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # 6. Test updating a task
        print("\n6. Testing task update...")
        updated_task = {
            "title": "Updated Test Task",
            "description": "This task has been updated"
        }
        
        response = requests.put(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers,
            json=updated_task
        )
        
        if response.status_code == 200:
            print("✓ Task update successful")
            updated_task_data = response.json()
            print(f"   Updated title: {updated_task_data['title']}")
        else:
            print(f"✗ Task update failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # 7. Test updating task status - FIXED
        print("\n7. Testing task status update...")
        # Use lowercase status values as expected by the API
        response = requests.patch(
            f"{BASE_URL}/tasks/{task_id}/status?status=in_progress",  # Use lowercase
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Task status update successful")
            status_data = response.json()
            print(f"   New status: {status_data['status']}")
        else:
            print(f"✗ Task status update failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # 8. Test AI suggestion endpoint
        print("\n8. Testing AI suggestion...")
        ai_request = {
            "title": "Implement user authentication"
        }
        
        response = requests.post(
            f"{BASE_URL}/ai/suggest",
            headers=headers,
            json=ai_request
        )
        
        if response.status_code == 200:
            print("✓ AI suggestion successful")
            ai_data = response.json()
            print(f"   AI response: {ai_data['description'][:50]}...")
        else:
            print(f"✗ AI suggestion failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # 9. Test deleting a task
        print("\n9. Testing task deletion...")
        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Task deletion successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"✗ Task deletion failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        print("\n" + "=" * 50)
        print("API Testing Complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)