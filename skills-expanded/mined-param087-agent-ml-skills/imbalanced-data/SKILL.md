---
name: imbalanced-data
description: Use when the target is rare (fraud, churn, disease, anomalies). Covers correct metrics, resampling (SMOTE/undersampling), class weights, threshold tuning, and avoiding the accuracy trap and resampling leakage.
---

# Imbalanced Data

## Overview

When positives are rare, naive training and naive metrics both mislead. A model that always predicts "negative" can score 99% accuracy and catch zero fraud. Handle imbalance at three levels: **metric, algorithm, and threshold** — and resample *inside* cross-validation, never before.

## When to use

- Class ratio is skewed (e.g., 95/5 or worse).
- Catching the rare class matters (fraud, defaults, rare disease, defects).

## Step 1 — Fix the metric first

Drop accuracy and ROC-AUC-as-sole-metric. Prefer:

- **PR-AUC (average precision)** — most informative for rare positives.
- **Recall @ fixed precision** — "catch X% of fraud while keeping false alarms tolerable."
- **F1 / Fβ** — β>1 weights recall when misses are costly.

## Step 2 — Algorithm-level handling

| Technique | How | When |
|-----------|-----|------|
| **Class weights** | `class_weight="balanced"` / `scale_pos_weight` | First choice — no data duplication |
| **Undersample majority** | `RandomUnderSampler` | Lots of data, majority redundant |
| **Oversample minority** | `SMOTE` / `ADASYN` | Limited minority samples |
| **Combine** | SMOTE + Tomek/ENN | Noisy boundaries |

Class weights are the cheapest, leak-free first move:

```python
# sklearn
LogisticRegression(class_weight="balanced")
# XGBoost / LightGBM
scale_pos_weight = n_negative / n_positive
```

## Step 3 — Resample INSIDE the pipeline (no leakage)

Resampling before CV leaks synthetic neighbors across the split and inflates scores. Use `imblearn`'s pipeline so SMOTE fits on training folds only:

```python
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

pipe = ImbPipeline([
    ("smote", SMOTE(random_state=42)),   # applied to train fold only
    ("clf", HistGradientBoostingClassifier(random_state=42)),
])
cv = StratifiedKFold(5, shuffle=True, random_state=42)
print(cross_val_score(pipe, X, y, cv=cv, scoring="average_precision").mean())
```

## Step 4 — Tune the decision threshold

Default 0.5 is almost always wrong for imbalanced problems. Pick the threshold from the validation PR curve to hit your precision/recall target:

```python
from sklearn.metrics import precision_recall_curve
import numpy as np

prec, rec, thr = precision_recall_curve(y_val, val_scores)
# smallest threshold achieving >= 0.90 precision
ok = np.where(prec[:-1] >= 0.90)[0]
chosen = thr[ok[0]] if len(ok) else 0.5
```

## Pitfalls

- **Accuracy as the metric** — the central trap.
- **SMOTE before train/test split** — leaks synthetic points; scores look great, production fails.
- **Resampling the test set** — evaluate on the real (imbalanced) distribution.
- **Oversampling then ignoring the threshold** — probabilities shift; recalibrate/tune the cut.
- **Synthetic samples on categorical/high-dim data** — SMOTE assumes meaningful interpolation; use SMOTENC or class weights instead.

## Hand-off

A model trained with leak-free resampling/weights, scored with PR-AUC and a tuned threshold via model-evaluation, ready for model-serving.
