##KS test, PSI
import json
import os
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from backend.src.config import settings
from backend.src.preprocess import NUM_COLS, CAT_COLS


def _load_baseline() -> dict:
    if not os.path.exists(settings.BASELINE_PATH):
        raise FileNotFoundError(f"Baseline not found at {settings.BASELINE_PATH}. Run training first.")
    with open(settings.BASELINE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def psi(expected: np.ndarray, actual: np.ndarray, quantiles: list[float]) -> float:
    # bucket by baseline quantiles
    if len(expected) == 0 or len(actual) == 0:
        return 0.0
    bins = np.array(quantiles, dtype=float)
    bins[0] = -np.inf
    bins[-1] = np.inf

    e_counts, _ = np.histogram(expected, bins=bins)
    a_counts, _ = np.histogram(actual, bins=bins)

    e_perc = e_counts / max(e_counts.sum(), 1)
    a_perc = a_counts / max(a_counts.sum(), 1)

    eps = 1e-6
    e_perc = np.clip(e_perc, eps, None)
    a_perc = np.clip(a_perc, eps, None)

    return float(np.sum((a_perc - e_perc) * np.log(a_perc / e_perc)))

def drift_report(new_df: pd.DataFrame) -> dict:
    baseline = _load_baseline()
    report = {"numeric": {}, "categorical": {}, "drift_detected": False}

    # numeric drift: KS p-value + PSI
    for c, b in baseline.get("numeric", {}).items():
        if c not in new_df.columns:
            continue
        x = pd.to_numeric(new_df[c], errors="coerce").dropna().to_numpy()
        if len(x) < 50:
            report["numeric"][c] = {"ks_pvalue": None, "psi": None, "drift": False}
            continue

        # create synthetic expected distribution from baseline stats not stored as full data:
        # we approximate expected with normal(mean,std) for KS; PSI uses baseline quantiles
        mean = float(b["mean"])
        std = float(b["std"])
        expected = np.random.normal(loc=mean, scale=std, size=min(2000, len(x)))

        ks = ks_2samp(expected, x)
        psi_val = psi(expected, x, b["quantiles"])

        drift = (ks.pvalue < 0.05) or (psi_val >= 0.2)
        report["numeric"][c] = {"ks_pvalue": float(ks.pvalue), "psi": float(psi_val), "drift": bool(drift)}

    # categorical drift: L1 distance on top categories
    for c, bdist in baseline.get("categorical", {}).items():
        if c not in new_df.columns:
            continue
        new = new_df[c].fillna("unknown").astype(str)
        new_dist = new.value_counts(normalize=True)

        cats = set(bdist.keys()) | set(new_dist.index)
        l1 = 0.0
        for cat in cats:
            l1 += abs(float(bdist.get(cat, 0.0)) - float(new_dist.get(cat, 0.0)))

        drift = l1 >= 0.3
        report["categorical"][c] = {"l1_distance": float(l1), "drift": bool(drift)}

    report["drift_detected"] = any(v.get("drift") for v in report["numeric"].values()) or any(v.get("drift") for v in report["categorical"].values())
    return report
