import os
import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

from backend.src.config import settings
from backend.src.data_loader import load_csv
from backend.src.preprocess import (
    clean_airbnb,
    build_baseline,
    save_json,
    NUM_COLS,
    CAT_COLS,
)


def train():
    df = clean_airbnb(load_csv(settings.DATA_PATH))

    X = df[NUM_COLS + CAT_COLS]
    y = df["price"].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore"))
    ])

    pre = ColumnTransformer([
        ("num", num_pipe, NUM_COLS),
        ("cat", cat_pipe, CAT_COLS),
    ])

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    pipe = Pipeline([("pre", pre), ("model", model)])
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
    mae = float(mean_absolute_error(y_test, preds))

    # Save model + metrics
    os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
    joblib.dump(pipe, settings.MODEL_PATH)

    metrics_path = os.path.join(os.path.dirname(settings.MODEL_PATH), "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({"rmse": rmse, "mae": mae}, f, indent=2)

    # Save baseline for drift
    baseline = build_baseline(df)
    save_json(baseline, settings.BASELINE_PATH)

    print("✅ Training complete")
    print({"rmse": rmse, "mae": mae})
    print(f"Model: {settings.MODEL_PATH}")
    print(f"Baseline: {settings.BASELINE_PATH}")

if __name__ == "__main__":
    train()
