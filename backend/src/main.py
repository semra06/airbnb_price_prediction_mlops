import os
import joblib
from fastapi import FastAPI
from sqlmodel import SQLModel

from minio import Minio

from backend.src.db.session import engine
from backend.src.routers import health, predict, drift
from backend.src.config import settings


app = FastAPI(title="Airbnb Price Prediction MLOps API")

MODEL_PATH = settings.MODEL_PATH  # örn: /app/backend/saved_models/model.joblib


def download_model_from_minio():
    minio_endpoint = os.getenv("MINIO_ENDPOINT")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY")
    minio_bucket = os.getenv("MINIO_BUCKET", "ml-models")

    if not all([minio_endpoint, minio_access_key, minio_secret_key]):
        raise RuntimeError("❌ MinIO environment variables are missing")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    client = Minio(
        minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False,
    )

    if not client.bucket_exists(minio_bucket):
        raise RuntimeError(f"❌ MinIO bucket not found: {minio_bucket}")

    client.fget_object(
        minio_bucket,
        "airbnb/model.joblib",
        MODEL_PATH,
    )

    print("✅ Model downloaded from MinIO")


@app.on_event("startup")
def on_startup():
    # 1️⃣ DB init
    SQLModel.metadata.create_all(engine)

    # 2️⃣ Model init
    if not os.path.exists(MODEL_PATH):
        print("ℹ️ Model not found locally, downloading from MinIO...")
        download_model_from_minio()
    else:
        print("✅ Model already exists locally")

    # 3️⃣ Load model once
    model = joblib.load(MODEL_PATH)

    # 4️⃣ Make model accessible globally (routers use this)
    app.state.model = model

    print("🚀 Model loaded and API is ready")


# Routers
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(drift.router)
