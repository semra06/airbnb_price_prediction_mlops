import json
import os
import numpy as np
import pandas as pd

TARGET = "price"

NUM_COLS = [
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365",
    "latitude",
    "longitude",
]

CAT_COLS = ["neighbourhood_group", "room_type"]

DROP_COLS = ["id", "name", "host_name", "last_review", "neighbourhood"]

def clean_airbnb(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # target cleaning
    df = df[df[TARGET].notna()]
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df[df[TARGET].notna()]
    df = df[df[TARGET] > 0]

    # trim extreme outliers (practical)
    q1, q99 = df[TARGET].quantile(0.01), df[TARGET].quantile(0.99)
    df = df[(df[TARGET] >= q1) & (df[TARGET] <= q99)]

    # drop unused
    for c in DROP_COLS:
        if c in df.columns:
            df.drop(columns=c, inplace=True)

    # keep only required columns (ignore if missing)
    keep = [TARGET]
    keep += [c for c in NUM_COLS if c in df.columns]
    keep += [c for c in CAT_COLS if c in df.columns]
    df = df[keep]

    # numeric fill
    for c in NUM_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            med = df[c].median()
            df[c] = df[c].fillna(med)

    # categorical fill
    for c in CAT_COLS:
        if c in df.columns:
            df[c] = df[c].astype("string").fillna("unknown")

    return df

def build_baseline(df: pd.DataFrame) -> dict:
    """
    Baseline stats for drift:
    - numeric: mean/std + quantile bins
    - cat: top categories distribution
    """
    baseline = {"numeric": {}, "categorical": {}}

    for c in NUM_COLS:
        if c not in df.columns:
            continue
        x = pd.to_numeric(df[c], errors="coerce").dropna().to_numpy()
        if len(x) == 0:
            continue
        qs = np.quantile(x, np.linspace(0, 1, 11)).tolist()  # 10 buckets
        baseline["numeric"][c] = {
            "mean": float(np.mean(x)),
            "std": float(np.std(x) + 1e-9),
            "quantiles": qs,
        }

    for c in CAT_COLS:
        if c not in df.columns:
            continue
        dist = df[c].astype(str).value_counts(normalize=True).head(30)  # top 30
        baseline["categorical"][c] = dist.to_dict()

    return baseline

def save_json(obj: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
