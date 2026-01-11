from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update

from shared.db import get_db
from shared.auth import require_roles

from app.models import Copy, Work
from app.schemas import CopyCreate, CopyOut

router = APIRouter()

@router.get("", response_model=list[CopyOut])
def list_copies(work_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Copy)
    if work_id is not None:
        q = q.filter(Copy.work_id == work_id)
    copies = q.order_by(Copy.id.asc()).limit(200).all()
    return [CopyOut(id=c.id, work_id=c.work_id, barcode=c.barcode, status=c.status, location=c.location) for c in copies]

@router.post("/work/{work_id}", response_model=CopyOut)
def add_copy(work_id: int, data: CopyCreate, _=Depends(require_roles("staff")), db: Session = Depends(get_db)):
    if not db.query(Work).get(work_id):
        raise HTTPException(status_code=404, detail="Work not found")
    c = Copy(work_id=work_id, barcode=data.barcode, location=data.location, status="AVAILABLE")
    db.add(c)
    db.commit()
    db.refresh(c)
    return CopyOut(id=c.id, work_id=c.work_id, barcode=c.barcode, status=c.status, location=c.location)

@router.post("/{copy_id}/claim", response_model=CopyOut)
def claim_copy(copy_id: int, purpose: str = "LOAN", db: Session = Depends(get_db)):
    # Atualiza apenas se estiver AVAILABLE (operação atómica no DB)
    res = db.execute(
        update(Copy)
        .where(Copy.id == copy_id)
        .where(Copy.status == "AVAILABLE")
        .values(status="LOANED" if purpose == "LOAN" else "RESERVED")
        .returning(Copy.id, Copy.work_id, Copy.barcode, Copy.status, Copy.location)
    ).first()
    if not res:
        raise HTTPException(status_code=409, detail="Copy not available")
    db.commit()
    return CopyOut(id=res.id, work_id=res.work_id, barcode=res.barcode, status=res.status, location=res.location)

@router.post("/{copy_id}/release", response_model=CopyOut)
def release_copy(copy_id: int, db: Session = Depends(get_db)):
    c = db.query(Copy).get(copy_id)
    if not c:
        raise HTTPException(status_code=404, detail="Copy not found")
    c.status = "AVAILABLE"
    db.commit()
    db.refresh(c)
    return CopyOut(id=c.id, work_id=c.work_id, barcode=c.barcode, status=c.status, location=c.location)
