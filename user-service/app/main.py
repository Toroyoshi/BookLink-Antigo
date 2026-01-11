from fastapi import FastAPI
from shared.db import Base, engine
from app.routers import auth, users

app = FastAPI(title="bookLink - user-service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
