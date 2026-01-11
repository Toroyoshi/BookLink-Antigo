from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db import get_db
from shared.auth import get_current_user

from app.models import Fine
from app.schemas import FineOut

router = APIRouter()

@router.get("", response_model=list[FineOut])
def my_fines(current=Depends(get_current_user), db: Session = Depends(get_db)):
    fines = db.query(Fine).filter(Fine.user_id == current["user_id"]).order_by(Fine.id.desc()).limit(200).all()
    return [FineOut(id=f.id, user_id=f.user_id, loan_id=f.loan_id, amount_eur=float(f.amount_eur), reason=f.reason, status=f.status) for f in fines]
