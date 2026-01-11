from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from shared.db import get_db
from shared.auth import get_current_user

from app.models import Payment
from app.schemas import PaymentCreate, PaymentOut
from app.clients import mark_fine_paid

router = APIRouter()

@router.post("", response_model=PaymentOut)
def create_payment(data: PaymentCreate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    p = Payment(
        user_id=current["user_id"],
        fine_id=data.fine_id,
        amount_eur=data.amount_eur,
        method=data.method,
        status="PENDING",
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return PaymentOut(id=p.id, user_id=p.user_id, fine_id=p.fine_id, amount_eur=float(p.amount_eur), method=p.method, status=p.status, paid_at=p.paid_at)

@router.get("", response_model=list[PaymentOut])
def my_payments(current=Depends(get_current_user), db: Session = Depends(get_db)):
    pays = db.query(Payment).filter(Payment.user_id == current["user_id"]).order_by(Payment.id.desc()).limit(200).all()
    return [PaymentOut(id=p.id, user_id=p.user_id, fine_id=p.fine_id, amount_eur=float(p.amount_eur), method=p.method, status=p.status, paid_at=p.paid_at) for p in pays]

@router.post("/{payment_id}/confirm", response_model=PaymentOut)
async def confirm_payment(payment_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(Payment).get(payment_id)
    if not p or p.user_id != current["user_id"]:
        raise HTTPException(status_code=404, detail="Payment not found")
    if p.status != "PENDING":
        raise HTTPException(status_code=409, detail="Payment is not pending")

    # Simula confirmação (em produção: gateway externo)
    p.status = "CONFIRMED"
    p.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(p)

    resp = await mark_fine_paid(p.fine_id)
    if resp.status_code != 200:
        # Em produção: compensação / re-tentativa
        raise HTTPException(status_code=502, detail="Could not mark fine as paid in loan-service")

    return PaymentOut(id=p.id, user_id=p.user_id, fine_id=p.fine_id, amount_eur=float(p.amount_eur), method=p.method, status=p.status, paid_at=p.paid_at)
