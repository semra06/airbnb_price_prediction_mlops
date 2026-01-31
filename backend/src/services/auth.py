##token kontrolü
from fastapi import HTTPException
from backend.src.config import settings


def require_token(x_token: str | None):
    if not x_token:
        raise HTTPException(status_code=401, detail="Missing X-Token")
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
