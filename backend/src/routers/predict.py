import json
import pandas as pd
from fastapi import APIRouter, Header, Depends, Request
from sqlmodel import Session

from backend.src.services.auth import require_token
from backend.src.db.session import get_session
from backend.src.db.models import PredictionLog

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/")
def predict(
    payload: dict,
    request: Request,
    x_token: str | None = Header(None, alias="X-Token"),
    session: Session = Depends(get_session),
):
    # 🔐 Auth
    require_token(x_token)

    # 📊 Input
    df = pd.DataFrame([payload])

    # 🤖 Get model loaded at startup
    model = request.app.state.model

    # 🔮 Predict
    pred = model.predict(df)[0]

    # 🧾 Log to DB
    row = PredictionLog(
        input_json=json.dumps(payload, ensure_ascii=False),
        prediction=float(pred),
    )
    session.add(row)
    session.commit()

    return {"prediction": float(pred)}
