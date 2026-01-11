from fastapi import FastAPI
from shared.db import Base, engine
from app.routers import works, copies

app = FastAPI(title="bookLink - catalog-service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(works.router, prefix="/works", tags=["works"])
app.include_router(copies.router, prefix="/copies", tags=["copies"])
