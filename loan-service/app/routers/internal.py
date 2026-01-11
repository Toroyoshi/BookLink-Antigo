from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from shared.db import get_db
from shared.auth import require_internal_token

from app.models import Fine
from app.schemas import FineOut

router = APIRouter()

@router.post("/fines/{fine_id}/mark-paid", response_model=FineOut)
def mark_fine_paid(
    fine_id: int,
    x_internal_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    require_internal_token(x_internal_token)
    fine = db.query(Fine).get(fine_id)
    fine.status = "PAID"
    db.commit()
    db.refresh(fine)
    return FineOut(id=fine.id, user_id=fine.user_id, loan_id=fine.loan_id, amount_eur=float(fine.amount_eur), reason=fine.reason, status=fine.status)
