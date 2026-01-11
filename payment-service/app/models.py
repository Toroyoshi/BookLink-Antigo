from sqlalchemy import Integer, String, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from shared.db import Base

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    fine_id: Mapped[int] = mapped_column(Integer, index=True)
    amount_eur: Mapped[float] = mapped_column(Numeric(10, 2))
    method: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20), default="PENDING", index=True)  # PENDING | CONFIRMED | FAILED
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    paid_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)
