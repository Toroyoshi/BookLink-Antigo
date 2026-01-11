from fastapi import FastAPI
from shared.db import Base, engine
from app.routers import payments

app = FastAPI(title="bookLink - payment-service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(payments.router, prefix="/payments", tags=["payments"])
