from fastapi import FastAPI
from shared.db import Base, engine
from app.routers import loans, fines, internal

app = FastAPI(title="bookLink - loan-service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(loans.router, prefix="/loans", tags=["loans"])
app.include_router(fines.router, prefix="/fines", tags=["fines"])
app.include_router(internal.router, prefix="/internal", tags=["internal"])
