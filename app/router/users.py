from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_active_user, get_password_hash
from app.exceptions import UserNotFound, InsufficientPermission

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise InsufficientPermission()
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise InsufficientPermission()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFound()
    return user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: str,
    user_update: schemas.UserUpdate,  # You'll need to create this schema
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise InsufficientPermission()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserNotFound()
    
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        db_user.password_hash = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise InsufficientPermission()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFound()
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}