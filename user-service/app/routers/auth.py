from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shared.db import get_db
from shared.settings import TOKEN_EXPIRE_MINUTES
from shared.auth import create_access_token

from app.models import User
from app.schemas import RegisterIn, LoginIn, TokenOut
from app.security import hash_password, verify_password

router = APIRouter()

@router.post("/register", response_model=TokenOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        role=data.role,
        password_hash=hash_password(data.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id), role=user.role, expires_minutes=TOKEN_EXPIRE_MINUTES)
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.is_active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id), role=user.role, expires_minutes=TOKEN_EXPIRE_MINUTES)
    return TokenOut(access_token=token)
