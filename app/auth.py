from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.config import config
from app.exceptions import InvalidCredentials, InvalidToken, UserNotFound

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise UserNotFound()
    return user

def authenticate_user(db: Session, username: str, password: str):
    try:
        user = get_user(db, username)
        print(f"User found: {user.username}")
        print(f"Stored hash: {user.password_hash}")
        print(f"Password verification: {verify_password(password, user.password_hash)}")
        if not verify_password(password, user.password_hash):
            raise InvalidCredentials()
        return user
    except UserNotFound:
        raise InvalidCredentials()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidToken()
        token_data = {"sub": username}
    except JWTError:
        raise InvalidToken()
    
    user = get_user(db, username=token_data["sub"])
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):

    return current_user