import json
import pandas as pd
from fastapi import APIRouter, Header, Depends
from sqlmodel import Session

from backend.src.services.auth import require_token
from backend.src.services.drift_service import drift_report
from backend.src.db.session import get_session
from backend.src.db.models import DriftLog


router = APIRouter(prefix="/drift", tags=["Drift"])

@router.post("/")
def drift(payload: list[dict], x_token: str | None = Header(None, alias="X-Token"), session: Session = Depends(get_session)):
    """
    payload: list of records (same feature keys as predict)
    """
    require_token(x_token)

    df = pd.DataFrame(payload)
    rep = drift_report(df)

    row = DriftLog(drift_detected=bool(rep["drift_detected"]), report_json=json.dumps(rep, ensure_ascii=False))
    session.add(row)
    session.commit()

    return rep
