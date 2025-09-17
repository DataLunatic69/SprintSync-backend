from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.database import get_db
from app import models, schemas
from app.auth import get_current_active_user
from app.exceptions import TaskNotFound, InsufficientPermission

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Users can only see their own tasks unless they're admin
    if current_user.is_admin:
        tasks = db.query(models.Task).offset(skip).limit(limit).all()
    else:
        tasks = db.query(models.Task).filter(
            models.Task.user_id == current_user.id
        ).offset(skip).limit(limit).all()
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_task = models.Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        status=models.TaskStatus.TODO,
        user_id=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise TaskNotFound()
    
    # Users can only see their own tasks unless they're admin
    if not current_user.is_admin and task.user_id != current_user.id:
        raise InsufficientPermission()
    
    return task

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: str,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise TaskNotFound()
    
    # Users can only update their own tasks unless they're admin
    if not current_user.is_admin and db_task.user_id != current_user.id:
        raise InsufficientPermission()
    
    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise TaskNotFound()
    
    # Users can only delete their own tasks unless they're admin
    if not current_user.is_admin and task.user_id != current_user.id:
        raise InsufficientPermission()
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/status", response_model=schemas.Task)
async def update_task_status(
    task_id: str,
    status: schemas.TaskStatus,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise TaskNotFound()
    
    # Users can only update their own tasks unless they're admin
    if not current_user.is_admin and task.user_id != current_user.id:
        raise InsufficientPermission()
    
    task.status = status
    db.commit()
    db.refresh(task)
    return task