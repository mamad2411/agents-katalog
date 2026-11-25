---
name: "feature-engineering-patterns"
description: "Feature engineering patterns with code: Feast feature store setup, sklearn pipelines with ColumnTransformer, time-series features, K-fold target encoding that avoids leakage, SHAP-based selection, and PSI drift monitoring. Use when building or reviewing model features."
---

# Feature Engineering Patterns

Expert patterns for feature stores, sklearn pipelines, time-series features, and drift detection.

## Pattern 1: Feast Feature Store Setup

Define entity, feature view, and feature service; retrieve point-in-time correct training data.

```python
from feast import FeatureStore, Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from datetime import timedelta

# feature_repo/feature_store.yaml
# project: my_ml_project
# registry: data/registry.db
# provider: local
# online_store: redis

# Define entity (the join key)
user = Entity(
    name="user_id",
    description="User identifier",
    value_type=String
)

# Define data source
purchase_source = FileSource(
    path="s3://features/user_purchases/",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

# Define feature view
user_purchase_fv = FeatureView(
    name="user_purchase_features",
    entities=[user],
    ttl=timedelta(days=90),
    schema=[
        Field(name="purchase_count_30d", dtype=Float32),
        Field(name="total_spend_30d", dtype=Float32),
        Field(name="avg_order_value_30d", dtype=Float32),
        Field(name="days_since_last_purchase", dtype=Float32),
        Field(name="category_diversity_30d", dtype=Int64),
    ],
    online=True,
    source=purchase_source,
    tags={"team": "ml-platform", "version": "v2"},
)

# Define feature service (group features for a model)
recommendation_fs = FeatureService(
    name="recommendation_model_v1",
    features=[
        user_purchase_fv[["purchase_count_30d", "total_spend_30d", "avg_order_value_30d"]],
    ]
)
```

```python
# Retrieve historical (training) features — point-in-time correct
import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Entity dataframe: user_id + event_timestamp (label timestamp)
entity_df = pd.DataFrame({
    "user_id": ["user_1", "user_2", "user_3"],
    "event_timestamp": pd.to_datetime(["2024-01-15", "2024-01-20", "2024-01-25"]),
    "label": [1, 0, 1],
})

# Feast joins features as-of each row's event_timestamp (no leakage)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["user_purchase_features:purchase_count_30d",
               "user_purchase_features:total_spend_30d",
               "user_purchase_features:avg_order_value_30d"],
).to_df()

# Online retrieval (serving)
feature_vector = store.get_online_features(
    features=["user_purchase_features:purchase_count_30d"],
    entity_rows=[{"user_id": "user_42"}]
).to_dict()
```

## Pattern 2: sklearn Pipeline with ColumnTransformer

Prevent leakage by fitting all transforms inside a pipeline.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

# Separate column groups
numeric_features = ['age', 'income', 'purchase_count_30d', 'avg_order_value_30d']
low_card_cat = ['country', 'device_type']   # < 20 categories
high_card_cat = ['product_category']        # many categories

# Numeric: impute then scale
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
])

# Low-cardinality: OHE
low_card_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')),
])

# High-cardinality: ordinal (for tree models)
high_card_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)),
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_features),
    ('low_cat', low_card_pipeline, low_card_cat),
    ('high_cat', high_card_pipeline, high_card_cat),
], remainder='drop')

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(n_estimators=200, max_depth=4))
])

# Fit ONLY on training data
full_pipeline.fit(X_train, y_train)

# Transform test data (never fit on test)
y_pred = full_pipeline.predict(X_test)

# Save pipeline (includes fitted transformers)
import joblib
joblib.dump(full_pipeline, 'pipeline_v1.joblib')
```

## Pattern 3: Time-Series Feature Engineering

Rolling, lag, and cyclical features for temporal ML tasks.

```python
import pandas as pd
import numpy as np

def compute_time_series_features(df: pd.DataFrame,
                                  entity_col: str,
                                  value_col: str,
                                  timestamp_col: str) -> pd.DataFrame:
    """
    Compute lag, rolling, and recency features.
    df must be sorted by (entity_col, timestamp_col).
    """
    df = df.sort_values([entity_col, timestamp_col])
    g = df.groupby(entity_col)[value_col]

    # Lag features (shift within entity group)
    df[f'{value_col}_lag_1'] = g.shift(1)
    df[f'{value_col}_lag_7'] = g.shift(7)
    df[f'{value_col}_lag_30'] = g.shift(30)

    # Rolling statistics
    for window in [7, 14, 30, 90]:
        rolled = g.transform(lambda x: x.rolling(window, min_periods=1))
        df[f'{value_col}_rolling_mean_{window}d'] = rolled.mean()
        df[f'{value_col}_rolling_std_{window}d'] = rolled.std().fillna(0)
        df[f'{value_col}_rolling_max_{window}d'] = rolled.max()

    # Trend: ratio of recent to older period
    df[f'{value_col}_trend_7d_vs_30d'] = (
        df[f'{value_col}_rolling_mean_7d'] /
        df[f'{value_col}_rolling_mean_30d'].replace(0, np.nan)
    ).fillna(1.0)

    # Cyclical time encoding (hour, day-of-week)
    ts = pd.to_datetime(df[timestamp_col])
    df['hour_sin'] = np.sin(2 * np.pi * ts.dt.hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * ts.dt.hour / 24)
    df['dow_sin'] = np.sin(2 * np.pi * ts.dt.dayofweek / 7)
    df['dow_cos'] = np.cos(2 * np.pi * ts.dt.dayofweek / 7)
    df['month_sin'] = np.sin(2 * np.pi * ts.dt.month / 12)
    df['month_cos'] = np.cos(2 * np.pi * ts.dt.month / 12)

    return df
```

## Pattern 4: Target Encoding with K-Fold to Prevent Leakage

Target encoding encodes high-cardinality categories with their mean target. Naive implementation leaks.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

def target_encode_kfold(X_train: pd.DataFrame, y_train: pd.Series,
                         X_test: pd.DataFrame, col: str,
                         n_splits: int = 5, smoothing: float = 1.0) -> tuple:
    """
    K-fold target encoding to prevent leakage.
    For each fold, encode using out-of-fold examples only.
    """
    X_train = X_train.copy()
    X_test = X_test.copy()

    global_mean = y_train.mean()
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    train_encoded = np.full(len(X_train), np.nan)

    for train_idx, val_idx in kf.split(X_train):
        # Compute target stats on train fold only
        stats = (y_train.iloc[train_idx]
                 .groupby(X_train[col].iloc[train_idx])
                 .agg(['mean', 'count']))
        stats.columns = ['mean', 'count']
        # Smoothed encoding: blend category mean with global mean
        stats['encoded'] = (
            (stats['count'] * stats['mean'] + smoothing * global_mean) /
            (stats['count'] + smoothing)
        )
        # Apply to validation fold
        val_cats = X_train[col].iloc[val_idx]
        train_encoded[val_idx] = val_cats.map(stats['encoded']).fillna(global_mean)

    # For test: use all training data
    stats_full = (y_train.groupby(X_train[col])
                  .agg(['mean', 'count']))
    stats_full.columns = ['mean', 'count']
    stats_full['encoded'] = (
        (stats_full['count'] * stats_full['mean'] + smoothing * global_mean) /
        (stats_full['count'] + smoothing)
    )
    test_encoded = X_test[col].map(stats_full['encoded']).fillna(global_mean)

    X_train[f'{col}_target_enc'] = train_encoded
    X_test[f'{col}_target_enc'] = test_encoded
    return X_train, X_test
```

## Pattern 5: SHAP-Based Feature Selection

Remove features that don't contribute to model decisions.

```python
import shap
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def select_features_by_shap(X_train: pd.DataFrame, y_train: pd.Series,
                              threshold_percentile: float = 10) -> list[str]:
    """
    Train a model, compute SHAP values, return features above threshold.
    threshold_percentile: remove features below this percentile of mean |SHAP|.
    """
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)

    # For multi-class: average across classes
    if isinstance(shap_values, list):
        mean_shap = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
    else:
        mean_shap = np.abs(shap_values).mean(axis=0)

    shap_df = pd.DataFrame({
        'feature': X_train.columns,
        'mean_abs_shap': mean_shap
    }).sort_values('mean_abs_shap', ascending=False)

    threshold = np.percentile(mean_shap, threshold_percentile)
    selected = shap_df[shap_df['mean_abs_shap'] > threshold]['feature'].tolist()
    removed = shap_df[shap_df['mean_abs_shap'] <= threshold]['feature'].tolist()

    print(f"Selected: {len(selected)} features | Removed: {len(removed)} features")
    print(f"Removed: {removed}")
    return selected
```

## Pattern 6: PSI Feature Drift Monitoring

Detect when production feature distributions diverge from training.

```python
import numpy as np
import pandas as pd

def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """
    Population Stability Index.
    PSI < 0.1: stable | 0.1-0.25: slight shift | > 0.25: significant drift
    """
    def scale_range(arr):
        return (arr - arr.min()) / (arr.max() - arr.min() + 1e-10)

    expected_scaled = scale_range(expected)
    actual_scaled = scale_range(actual)

    breakpoints = np.linspace(0, 1, buckets + 1)
    expected_counts, _ = np.histogram(expected_scaled, bins=breakpoints)
    actual_counts, _ = np.histogram(actual_scaled, bins=breakpoints)

    # Convert to proportions, add small value to avoid log(0)
    expected_pct = expected_counts / len(expected) + 1e-6
    actual_pct = actual_counts / len(actual) + 1e-6

    psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return psi

def drift_report(train_df: pd.DataFrame, prod_df: pd.DataFrame,
                  numeric_cols: list[str]) -> pd.DataFrame:
    records = []
    for col in numeric_cols:
        psi = calculate_psi(train_df[col].dropna().values, prod_df[col].dropna().values)
        status = "stable" if psi < 0.1 else "slight" if psi < 0.25 else "DRIFT"
        records.append({"feature": col, "psi": round(psi, 4), "status": status})
    return pd.DataFrame(records).sort_values("psi", ascending=False)
```

## Anti-Patterns

### Anti-Pattern 1: Fitting Transformers on the Full Dataset
`scaler.fit(X)` before train/test split means test statistics contaminate training. Always `fit` on train only, `transform` both. Use sklearn `Pipeline` to enforce this automatically.

### Anti-Pattern 2: Time-Series Features Without Entity Grouping
`df['lag_1'] = df['value'].shift(1)` without groupby by entity creates cross-entity contamination. User A's lag-1 becomes User B's current value if data is sorted by timestamp only.

### Anti-Pattern 3: Training Features That Aren't Available at Serving Time
Build a feature that uses `user.age` at training time but the serving API doesn't provide it. The model is undeployable. Map every feature to its serving source before finalizing the feature set.

### Anti-Pattern 4: Online/Offline Skew
Computing features differently in the training pipeline vs the serving pipeline. Classic example: different NULL handling, different rounding, different timezone. Test serving feature values against offline values for a sample of entities.

### Anti-Pattern 5: Naive Target Encoding
`df['cat_encoded'] = df.groupby('category')['label'].transform('mean')` leaks target information for training examples. Use K-fold or leave-one-out target encoding.
