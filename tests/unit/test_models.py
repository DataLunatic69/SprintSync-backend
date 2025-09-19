def test_user_creation(db):
    from app.models import User
    from app.auth import get_password_hash
    
    user = User(
        id="test-id",
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        is_admin=False
    )
    
    db.add(user)
    db.commit()
    
    retrieved_user = db.query(User).filter(User.username == "testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"

def test_task_creation(db):
    from app.models import Task, TaskStatus
    
    task = Task(
        id="test-task-id",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.TODO,
        user_id="test-user-id",
        assigned_by="test-admin-id"
    )
    
    db.add(task)
    db.commit()
    
    retrieved_task = db.query(Task).filter(Task.id == "test-task-id").first()
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.assigned_by == "test-admin-id"