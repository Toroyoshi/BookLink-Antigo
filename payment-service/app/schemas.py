from pydantic import BaseModel, Field
from datetime import datetime

class PaymentCreate(BaseModel):
    fine_id: int = Field(gt=0)
    amount_eur: float = Field(gt=0)
    method: str = Field(pattern=r"^(card|mbway|cash)$")

class PaymentOut(BaseModel):
    id: int
    user_id: int
    fine_id: int
    amount_eur: float
    method: str
    status: str
    paid_at: datetime | None
