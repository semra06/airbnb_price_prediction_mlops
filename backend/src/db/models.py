from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class PredictionLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    input_json: str
    prediction: float

class DriftLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    drift_detected: bool
    report_json: str
