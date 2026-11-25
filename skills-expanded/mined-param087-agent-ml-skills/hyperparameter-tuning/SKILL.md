---
name: hyperparameter-tuning
description: Use when optimizing model hyperparameters. Covers search strategy (random vs Bayesian/Optuna), leakage-safe tuning inside CV, search-space design, early stopping, and budget management.
---

# Hyperparameter Tuning

## Overview

Tuning squeezes the last 5-15% out of a model — but done carelessly it overfits the validation set and leaks preprocessing. The rules: tune the **whole pipeline** inside cross-validation, search smart (not grid), and keep a final untouched test set.

## When to use

- A reasonable baseline exists and you want to improve it.
- You need to pick model complexity (depth, regularization, lr).

## Strategy selection

| Situation | Method |
|-----------|--------|
| Few params, cheap model | `GridSearchCV` |
| Many params / continuous | `RandomizedSearchCV` (often beats grid per compute) |
| Expensive model, want efficiency | **Bayesian / Optuna** (TPE) |
| Neural nets | Optuna + early stopping + pruning |

## Optuna pattern (leakage-safe, prunes bad trials)

```python
import optuna
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(5, shuffle=True, random_state=42)

def objective(trial):
    params = {
        "clf__learning_rate": trial.suggest_float("lr", 1e-3, 0.3, log=True),
        "clf__max_depth": trial.suggest_int("max_depth", 3, 12),
        "clf__l2_regularization": trial.suggest_float("l2", 1e-3, 10, log=True),
    }
    model.set_params(**params)
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")
    return scores.mean()

study = optuna.create_study(direction="maximize",
                            sampler=optuna.samplers.TPESampler(seed=42))
study.optimize(objective, n_trials=50, timeout=1800)
print(study.best_params, study.best_value)
```

Note the `clf__` prefix — you're tuning the estimator **inside** the pipeline, so preprocessing re-fits per fold.

## Search-space design

- Sample learning rates and regularization on a **log scale**.
- Start wide, then **narrow** around the best region in a second study.
- Tie `n_estimators` to **early stopping** rather than tuning it directly.
- Fix the seed in the sampler for reproducible studies.

## Budget management

- Set `timeout` and `n_trials` ceilings; use Optuna **pruning** to kill hopeless trials early.
- Tune on a representative **subsample** first to find the region, then refine on full data.
- Don't tune dozens of params — pick the 3-5 that matter for your model family.

## Pitfalls

- **Nested leakage:** preprocessing fit outside CV, then tuned — inflates scores. Tune the pipeline.
- **Tuning on the test set** — only ever touch train/validation; report final number on the holdout once.
- **Over-tuning** to a tiny validation set → great CV, worse production. Prefer simpler models + regularization.
- **Comparing tuned-vs-untuned across different CV splits** — keep the split fixed.

## Hand-off

Best params + a refit pipeline, logged via experiment-tracking and scored once on the holdout via model-evaluation.
