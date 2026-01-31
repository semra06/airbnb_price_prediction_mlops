from fastapi import FastAPI
from sqlmodel import SQLModel

from backend.src.db.session import engine
from backend.src.routers import health, predict, drift

app = FastAPI(title="Airbnb Price Prediction MLOps API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(drift.router)
