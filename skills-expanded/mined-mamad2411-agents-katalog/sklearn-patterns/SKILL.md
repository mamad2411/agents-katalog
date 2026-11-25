---
name: sklearn-patterns
description: "When to activate: scikit-learn, sklearn, Pipeline, ColumnTransformer, GridSearchCV, cross-validation, custom transformers, feature importance, classification, regression"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# scikit-learn Patterns

## Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer

numeric_features = ["age", "income", "tenure"]
categorical_features = ["plan", "region"]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", GradientBoostingClassifier(n_estimators=200, max_depth=4)),
])
```

## Cross-Validation

```python
from sklearn.model_selection import StratifiedKFold, cross_validate
import numpy as np

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = cross_validate(
    pipeline, X, y,
    cv=cv,
    scoring=["accuracy", "roc_auc", "f1_weighted"],
    return_train_score=True,
    n_jobs=-1,
)

print(f"Val AUC: {results['test_roc_auc'].mean():.3f} ± {results['test_roc_auc'].std():.3f}")
print(f"Train AUC: {results['train_roc_auc'].mean():.3f}")   # Check for overfitting
```

## Hyperparameter Search with Optuna

```python
import optuna
from sklearn.model_selection import cross_val_score

def objective(trial):
    params = {
        "classifier__n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "classifier__max_depth": trial.suggest_int("max_depth", 2, 8),
        "classifier__learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "classifier__min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
    }
    pipeline.set_params(**params)
    return cross_val_score(pipeline, X_train, y_train, cv=3, scoring="roc_auc").mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100, n_jobs=4)

best_pipeline = pipeline.set_params(**study.best_params)
best_pipeline.fit(X_train, y_train)
```

## Custom Transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin

class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, date_column: str):
        self.date_column = date_column

    def fit(self, X, y=None):
        return self  # Stateless — nothing to fit

    def transform(self, X):
        X = X.copy()
        col = pd.to_datetime(X[self.date_column])
        X["day_of_week"] = col.dt.dayofweek
        X["month"] = col.dt.month
        X["is_weekend"] = col.dt.dayofweek.isin([5, 6]).astype(int)
        X["days_since_epoch"] = (col - pd.Timestamp("2020-01-01")).dt.days
        return X.drop(columns=[self.date_column])
```

## Feature Importance

```python
import pandas as pd
import matplotlib.pyplot as plt

# After fitting pipeline
feature_names = (
    pipeline.named_steps["preprocessor"]
    .get_feature_names_out()
)
importances = pipeline.named_steps["classifier"].feature_importances_

importance_df = (
    pd.DataFrame({"feature": feature_names, "importance": importances})
    .sort_values("importance", ascending=False)
    .head(20)
)

importance_df.plot(kind="barh", x="feature", y="importance", legend=False)
plt.title("Feature Importances")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
```

## Model Persistence

```python
import joblib

# Save
joblib.dump(pipeline, "model.joblib")

# Load
pipeline = joblib.load("model.joblib")
predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)[:, 1]
```

## Evaluation

```python
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")

# Calibration check
from sklearn.calibration import calibration_curve
fraction_pos, mean_pred = calibration_curve(y_test, y_prob, n_bins=10)
```
