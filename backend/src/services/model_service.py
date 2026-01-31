## model load / predict
import os
import joblib
import pandas as pd
from backend.src.config import settings


_model = None

def load_model():
    global _model
    if _model is None:
        if not os.path.exists(settings.MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {settings.MODEL_PATH}. Run training first.")
        _model = joblib.load(settings.MODEL_PATH)
    return _model

def predict_df(df: pd.DataFrame) -> float:
    model = load_model()
    pred = float(model.predict(df)[0])
    return pred
