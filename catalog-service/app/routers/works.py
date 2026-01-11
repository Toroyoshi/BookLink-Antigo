from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from shared.db import get_db
from shared.auth import require_roles, get_current_user

from app.models import Work
from app.schemas import WorkCreate, WorkOut

router = APIRouter()

@router.get("", response_model=list[WorkOut])
def search_works(query: str | None = None, isbn: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Work)
    if query:
        like = f"%{query.lower()}%"
        q = q.filter(or_(Work.title.ilike(like), Work.subjects.ilike(like)))
    if isbn:
        q = q.filter(Work.isbn == isbn)
    return [WorkOut(id=w.id, title=w.title, isbn=w.isbn, year=w.year, language=w.language, subjects=w.subjects) for w in q.order_by(Work.id.desc()).limit(100).all()]

@router.post("", response_model=WorkOut)
def create_work(data: WorkCreate, _=Depends(require_roles("staff")), db: Session = Depends(get_db)):
    w = Work(**data.model_dump())
    db.add(w)
    db.commit()
    db.refresh(w)
    return WorkOut(id=w.id, title=w.title, isbn=w.isbn, year=w.year, language=w.language, subjects=w.subjects)

@router.get("/{work_id}", response_model=WorkOut)
def get_work(work_id: int, db: Session = Depends(get_db)):
    w = db.query(Work).get(work_id)
    return WorkOut(id=w.id, title=w.title, isbn=w.isbn, year=w.year, language=w.language, subjects=w.subjects)
