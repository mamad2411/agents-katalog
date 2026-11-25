---
name: feature-engineering
description: Use when creating, encoding, scaling, or selecting features for ML models. Covers categorical encoding, numeric transforms, datetime/text/aggregation features, and leakage-safe target encoding.
---

# Feature Engineering

## Overview

Feature engineering is where most model performance is won or lost. The aim is to express the signal in a form the model can use, while never letting information from the target or the test set leak into a feature.

## When to use

- After cleaning, before/iterating with modeling.
- A model plateaus and you suspect under-expressed signal.
- You have raw datetime, text, or relational data to turn into columns.

## Encoding categoricals

| Cardinality | Encoder | Notes |
|-------------|---------|-------|
| Low (<15), tree model | One-hot or native categorical | LightGBM/CatBoost handle natively |
| Low, linear model | One-hot | Drop-first to avoid collinearity |
| High (>15) | Target/leave-one-out encoding | **Must** be cross-fitted to avoid leakage |
| Ordinal meaning | Ordinal map | Preserve order (low<med<high) |

## Numeric transforms

- **Skewed positive values** → `log1p` or Box-Cox/Yeo-Johnson.
- **Scaling** → `StandardScaler` for linear/NN, none needed for trees.
- **Binning** → only when the relationship is genuinely non-monotonic.
- **Interactions** → products/ratios of features with domain meaning (e.g., `price / sqft`).

## Datetime features

```python
ts = df["event_time"]
df["hour"] = ts.dt.hour
df["dayofweek"] = ts.dt.dayofweek
df["is_weekend"] = ts.dt.dayofweek.ge(5).astype(int)
df["month"] = ts.dt.month
# Cyclical encoding so 23:00 and 00:00 are close
import numpy as np
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
```

## Leakage-safe target encoding

Target encoding must be fit out-of-fold, never on the rows it encodes:

```python
from sklearn.model_selection import KFold
import numpy as np

def target_encode_oof(train, col, target, n_splits=5, smoothing=10):
    oof = np.zeros(len(train))
    prior = train[target].mean()
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    for tr_idx, val_idx in kf.split(train):
        agg = train.iloc[tr_idx].groupby(col)[target].agg(["mean", "count"])
        smooth = (agg["mean"] * agg["count"] + prior * smoothing) / (agg["count"] + smoothing)
        oof[val_idx] = train.iloc[val_idx][col].map(smooth).fillna(prior).values
    return oof
```

## Pitfalls

- **Target encoding fit on all rows** → severe leakage, inflated CV, collapse in production.
- **Scaling fit on full data** → use `Pipeline` so scaler fits on train folds only.
- **Aggregations over the whole timeline** in time-series → only use past data (rolling windows with proper shift).
- **Creating thousands of features** then trusting noisy importance — prefer a few well-motivated features + regularization.

## Hand-off

Deliver a documented feature set (name, source, rationale) and ensure all transforms are wrapped in a fitted `Pipeline` for the model-evaluation and model-serving skills to reuse.
