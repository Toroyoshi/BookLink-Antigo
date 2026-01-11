from pydantic import BaseModel, Field
from datetime import datetime

class LoanCreate(BaseModel):
    copy_id: int = Field(gt=0)

class LoanOut(BaseModel):
    id: int
    user_id: int
    copy_id: int
    status: str
    due_at: datetime
    returned_at: datetime | None

class FineOut(BaseModel):
    id: int
    user_id: int
    loan_id: int
    amount_eur: float
    reason: str
    status: str
