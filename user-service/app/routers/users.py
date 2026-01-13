from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db import get_db
from shared.auth import get_current_user, require_roles

from app.models import User
from app.schemas import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).get(current["user_id"])
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, _=Depends(require_roles("staff")), db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    return user
