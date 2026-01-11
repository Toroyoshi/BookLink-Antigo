from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from shared.db import Base

class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    copy_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(30), default="ACTIVE", index=True)  # ACTIVE | RETURNED
    loaned_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    due_at: Mapped[object] = mapped_column(DateTime(timezone=True))
    returned_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Fine(Base):
    __tablename__ = "fines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.id"), index=True)
    amount_eur: Mapped[float] = mapped_column(Numeric(10, 2))
    reason: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="OPEN", index=True)  # OPEN | PAID | WAIVED
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
