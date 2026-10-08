---
name: domain-tabular
description: "Use for structured/tabular data prediction: churn, fraud, credit/risk scoring, price/demand regression, conversion, recommendation features, any CSV/database ML. Picks gradient boosting vs deep tabular, robust feature engineering, correct CV, calibration, and imbalance handling. Triggers on 'predict churn/fraud/price/risk', 'classify this CSV/table', 'tabular', 'XGBoost/LightGBM', 'feature engineering'."
---

# Tabular ML - Method Selection

For most tabular problems, **gradient-boosted trees beat deep learning** - start there.

## Decision table
| Situation | Recommended | Notes |
|---|---|---|
| Default (any size, mixed types) | **LightGBM / XGBoost / CatBoost** | CatBoost handles categoricals natively; LightGBM is fast; XGBoost robust. Tune with Optuna. |
| Strong baseline / linear signal | **Regularized Linear/Logistic, ElasticNet** | Fast sanity baseline; interpretable. |
| Very large + rich, or embeddings needed | **Deep tabular (FT-Transformer / TabNet)** | Only when GBTs plateau and data is large. |
| Tiny data | **Linear / simple trees + heavy regularization** | Avoid overfitting; strong CV. |
| Ensembling | **Blend/stack GBTs + linear** | Usually the last real gain. |

## Feature engineering & correctness
- **Target leakage is the #1 killer**: drop features known only *after* the outcome or that encode the label. Audit each feature's availability at prediction time.
- Fit encoders/scalers/imputers/target-encoding **inside CV folds** (on train only) - fitting on the full set leaks (`data-rigor-and-leakage`).
- Handle categoricals (native/CatBoost, or target/one-hot with fold-safe encoding), missing values, and skew deliberately.
- Time-aware data needs a **time-based split** (train earlier than test), never random.

## Evaluation & imbalance
- **CV**: StratifiedKFold (classification), GroupKFold if entities repeat, TimeSeriesSplit if temporal.
- **Imbalanced** (fraud/churn): PR-AUC, recall at a fixed precision, class weights or focal/`scale_pos_weight` - not raw accuracy.
- **Calibrate** probabilities (Platt/isotonic) if scores drive decisions/thresholds.
- **Explainability**: SHAP for global + per-prediction attribution (great for stakeholder trust).
- Improve: use `accuracy-improvement-loop` (feature engineering usually beats model swaps; then tuning, then stacking).
