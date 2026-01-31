import os
from dotenv import load_dotenv

load_dotenv()  # loads from project root .env when run from repo root; also works in docker env vars

class Settings:
    API_TOKEN: str = os.getenv("API_TOKEN", "CHANGE_ME")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    DB_URL: str = os.getenv("DB_URL", "postgresql://train:Ankara06@localhost:5433/projectdb")

    MODEL_PATH: str = os.getenv("MODEL_PATH", "backend/saved_models/model.joblib")
    BASELINE_PATH: str = os.getenv("BASELINE_PATH", "backend/saved_models/baseline.json")
    DATA_PATH: str = os.getenv("DATA_PATH", "backend/data/AB_NYC_2019.csv")

    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8502"))

settings = Settings()
