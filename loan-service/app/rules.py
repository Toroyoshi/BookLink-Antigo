import os
from datetime import datetime, timedelta, timezone

FINE_PER_DAY_EUR = float(os.getenv("FINE_PER_DAY_EUR", "0.50"))
LOAN_DAYS_STUDENT = int(os.getenv("LOAN_DAYS_STUDENT", "14"))
LOAN_DAYS_DOCENTE = int(os.getenv("LOAN_DAYS_DOCENTE", "30"))
LOAN_DAYS_STAFF = int(os.getenv("LOAN_DAYS_STAFF", "30"))

def loan_days_for_role(role: str) -> int:
    return {
        "student": LOAN_DAYS_STUDENT,
        "docente": LOAN_DAYS_DOCENTE,
        "staff": LOAN_DAYS_STAFF,
    }.get(role, LOAN_DAYS_STUDENT)

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def compute_due_at(role: str) -> datetime:
    return now_utc() + timedelta(days=loan_days_for_role(role))

def compute_fine_amount(due_at: datetime, returned_at: datetime) -> float:
    if returned_at <= due_at:
        return 0.0
    days = (returned_at.date() - due_at.date()).days
    if days <= 0:
        return 0.0
    return round(days * FINE_PER_DAY_EUR, 2)
