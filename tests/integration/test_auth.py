def test_register_and_login(client):
    # Test registration
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    
    # Test login
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_endpoint(client, auth_headers):
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200