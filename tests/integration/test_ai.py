def test_ai_suggestion(client, auth_headers):
    suggestion_data = {
        "title": "Implement user authentication"
    }
    
    response = client.post("/ai/suggest", json=suggestion_data, headers=auth_headers)
    assert response.status_code == 200
    assert "description" in response.json()

