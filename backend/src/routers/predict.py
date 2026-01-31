import json
import pandas as pd
from fastapi import APIRouter, Header, Depends
from sqlmodel import Session

from backend.src.services.auth import require_token
from backend.src.services.model_service import predict_df
from backend.src.db.session import get_session
from backend.src.db.models import PredictionLog


router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/")
def predict(payload: dict, x_token: str | None = Header(None, alias="X-Token"), session: Session = Depends(get_session)):
    require_token(x_token)

    df = pd.DataFrame([payload])
    pred = predict_df(df)

    row = PredictionLog(input_json=json.dumps(payload, ensure_ascii=False), prediction=float(pred))
    session.add(row)
    session.commit()

    return {"prediction": float(pred)}
