---
name: sklearn-pipelines
description: Use when building scikit-learn models that must not leak preprocessing. Covers Pipeline, ColumnTransformer, custom transformers, and combining preprocessing with cross-validation correctly.
---

# scikit-learn Pipelines

## Overview

A `Pipeline` chains preprocessing and the estimator into one object so that **every fit happens on training folds only**. This makes leakage structurally impossible and makes the model trivially serializable for serving. If you remember one thing from this pack: *wrap preprocessing in a Pipeline.*

## When to use

- Any sklearn model with preprocessing (scaling, encoding, imputing).
- You need cross-validation that includes preprocessing.
- You want one artifact to save and serve.

## Canonical pattern

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import HistGradientBoostingClassifier

num = ["age", "income", "tenure"]
cat = ["country", "plan"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), num),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore")),
    ]), cat),
])

model = Pipeline([
    ("prep", preprocess),
    ("clf", HistGradientBoostingClassifier(random_state=42)),
])

model.fit(X_train, y_train)        # all preprocessing fit on train only
preds = model.predict(X_test)      # preprocessing reused, no leakage
```

## Cross-validation the right way

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc")
# preprocessing is re-fit inside each fold automatically
```

Pair this with the `hyperparameter-tuning` skill — pass the whole pipeline to the search and tune with `clf__` / `prep__` prefixes.

## Custom transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin

class LogTransform(BaseEstimator, TransformerMixin):
    def __init__(self, cols): self.cols = cols
    def fit(self, X, y=None): return self
    def transform(self, X):
        X = X.copy()
        X[self.cols] = np.log1p(X[self.cols])
        return X
```

## Pitfalls

- **`scaler.fit_transform(X)` before `train_test_split`** — the #1 leakage bug. Fit inside the pipeline instead.
- **`OneHotEncoder` without `handle_unknown="ignore"`** crashes on unseen test categories.
- **Imputing the target** — pipelines transform `X`, never `y`; impute/clean targets separately and deliberately.
- **Tuning preprocessing outside CV** — keep it in the pipeline so search respects fold boundaries.

## Hand-off

A single fitted `Pipeline` artifact that the model-evaluation, hyperparameter-tuning, and model-serving skills all consume directly (`joblib.dump(model, "model.joblib")`).
