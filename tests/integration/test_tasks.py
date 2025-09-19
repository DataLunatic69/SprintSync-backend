def test_create_and_get_tasks(client, auth_headers):
    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }
    
    response = client.post("/tasks", json=task_data, headers=auth_headers)
    assert response.status_code == 200
    task_id = response.json()["id"]
    
    # Get all tasks
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Task"
    
    # Get specific task
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_update_task_status(client, auth_headers):
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }
    
    response = client.post("/tasks", json=task_data, headers=auth_headers)
    task_id = response.json()["id"]
    
    # Update task status
    response = client.patch(
        f"/tasks/{task_id}/status?status=in_progress",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"