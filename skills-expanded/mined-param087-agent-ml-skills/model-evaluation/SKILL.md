---
name: model-evaluation
description: Use when choosing metrics, validating models, or interpreting results. Covers metric selection by problem type, cross-validation strategy, calibration, confusion-matrix analysis, and avoiding misleading scores.
---

# Model Evaluation

## Overview

The wrong metric on the wrong split produces confident, wrong conclusions. Evaluation is about choosing a metric that matches the business cost, validating it on a split that mirrors production, and reporting it honestly with uncertainty.

## When to use

- Selecting how to score a model.
- A model "looks great" but you're unsure it's real.
- Comparing candidate models for promotion.

## Metric selection

| Problem | Default metric | Use when |
|---------|---------------|----------|
| Balanced classification | ROC-AUC, accuracy | classes ~balanced |
| Imbalanced classification | PR-AUC, F1, recall@k | rare positives (fraud, disease) |
| Probabilistic output | Log loss, Brier, calibration | you need trustworthy probabilities |
| Ranking | NDCG, MAP, MRR | recommendation/search |
| Regression | MAE (robust), RMSE (penalize big errors) | match error cost |
| Regression, multiplicative | MAPE / RMSLE | errors scale with magnitude |

## Cross-validation strategy

- **Default:** `StratifiedKFold` for classification.
- **Time series:** `TimeSeriesSplit` — never shuffle; train on past, validate on future.
- **Grouped data** (multiple rows per user): `GroupKFold` so the same group never spans train and test.
- **Small data:** repeated CV; report mean ± std.

## Honest reporting

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold
import numpy as np

cv = StratifiedKFold(5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="average_precision")
print(f"PR-AUC: {scores.mean():.3f} ± {scores.std():.3f}")  # always report spread
```

## Beyond a single number

- **Confusion matrix / classification report** at the chosen threshold — accuracy hides per-class failure.
- **Threshold tuning** — default 0.5 is rarely optimal; pick it from the PR curve to match precision/recall needs.
- **Calibration** — `CalibratedClassifierCV` or reliability curves when probabilities feed decisions.
- **Slice metrics** — evaluate on subgroups to catch fairness/robustness gaps.

## Pitfalls

- **Accuracy on imbalanced data** — 99% accuracy by predicting the majority class. Use PR-AUC/recall.
- **Tuning the threshold on the test set** — do it on validation.
- **Shuffling time-series CV** — leaks the future, inflates scores, collapses in production.
- **Reporting a point estimate** with no variance — a 0.2% gain inside ±1.5% noise is not a gain.
- **Evaluating on the data you tuned on** — keep a final untouched test set.

## Hand-off

A defensible metric + validated score with uncertainty, plus a chosen decision threshold, for experiment-tracking to log and stakeholders to trust.
