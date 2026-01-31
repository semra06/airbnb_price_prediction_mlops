import pandas as pd
from backend.src.config import settings


def load_csv(path: str | None = None) -> pd.DataFrame:
    return pd.read_csv(path or settings.DATA_PATH)
