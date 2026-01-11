from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timezone

from shared.db import get_db
from shared.auth import get_current_user

from app.models import Loan, Fine
from app.schemas import LoanCreate, LoanOut
from app.rules import compute_due_at, compute_fine_amount, now_utc
from app.clients import claim_copy, release_copy

router = APIRouter()

@router.post("", response_model=LoanOut)
async def create_loan(data: LoanCreate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    # 1) claim copy no catalog-service (atómico: AVAILABLE -> LOANED)
    resp = await claim_copy(data.copy_id)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", "Could not claim copy"))

    due_at = compute_due_at(current["role"])
    loan = Loan(user_id=current["user_id"], copy_id=data.copy_id, due_at=due_at, status="ACTIVE")
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return LoanOut(id=loan.id, user_id=loan.user_id, copy_id=loan.copy_id, status=loan.status, due_at=loan.due_at, returned_at=loan.returned_at)

@router.get("", response_model=list[LoanOut])
def list_my_loans(current=Depends(get_current_user), db: Session = Depends(get_db)):
    loans = db.query(Loan).filter(Loan.user_id == current["user_id"]).order_by(Loan.id.desc()).limit(200).all()
    return [LoanOut(id=l.id, user_id=l.user_id, copy_id=l.copy_id, status=l.status, due_at=l.due_at, returned_at=l.returned_at) for l in loans]

@router.post("/{loan_id}/return", response_model=LoanOut)
async def return_loan(loan_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    loan = db.query(Loan).get(loan_id)
    if not loan or loan.user_id != current["user_id"]:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "ACTIVE":
        raise HTTPException(status_code=409, detail="Loan is not active")

    returned_at = now_utc()
    loan.returned_at = returned_at
    loan.status = "RETURNED"
    db.commit()
    db.refresh(loan)

    # 2) libera cópia no catalog
    resp = await release_copy(loan.copy_id)
    if resp.status_code != 200:
        # não falha o retorno, mas deixa alerta (em produção: compensação)
        pass

    # 3) cria multa se houver atraso
    amount = compute_fine_amount(loan.due_at, returned_at)
    if amount > 0:
        fine = Fine(user_id=loan.user_id, loan_id=loan.id, amount_eur=amount, reason="Atraso na devolução", status="OPEN")
        db.add(fine)
        db.commit()

    return LoanOut(id=loan.id, user_id=loan.user_id, copy_id=loan.copy_id, status=loan.status, due_at=loan.due_at, returned_at=loan.returned_at)
