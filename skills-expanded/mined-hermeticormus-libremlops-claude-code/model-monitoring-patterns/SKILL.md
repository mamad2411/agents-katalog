---
name: "model-monitoring-patterns"
description: "Model monitoring patterns with code: PSI feature drift, Evidently drift reports and test suites, NannyML performance estimation without labels, whylogs profiles, and Prometheus metrics for model serving. Use when watching a production model for degradation."
---

# Model Monitoring Patterns

Expert patterns for data drift detection, concept drift, performance estimation without labels, and alert engineering.

## Pattern 1: PSI Feature Drift Monitor

Population Stability Index for continuous and categorical features.

```python
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, wasserstein_distance

def compute_psi(reference: np.ndarray, current: np.ndarray,
                n_bins: int = 10, epsilon: float = 1e-6) -> float:
    """
    PSI < 0.1: stable | 0.1-0.25: investigate | > 0.25: significant shift
    """
    # Create bins from reference distribution
    breakpoints = np.linspace(0, 100, n_bins + 1)
    ref_percentiles = np.percentile(reference, breakpoints)
    ref_percentiles = np.unique(ref_percentiles)  # remove duplicates

    ref_counts, _ = np.histogram(reference, bins=ref_percentiles)
    cur_counts, _ = np.histogram(current, bins=ref_percentiles)

    ref_pct = ref_counts / len(reference) + epsilon
    cur_pct = cur_counts / len(current) + epsilon

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return round(psi, 4)

def drift_report(reference_df: pd.DataFrame, current_df: pd.DataFrame,
                 numeric_cols: list, categorical_cols: list) -> pd.DataFrame:
    """Full drift report across all features."""
    records = []
    for col in numeric_cols:
        ref = reference_df[col].dropna().values
        cur = current_df[col].dropna().values
        psi = compute_psi(ref, cur)
        ks_stat, ks_p = ks_2samp(ref, cur)
        w_dist = wasserstein_distance(ref, cur)
        severity = "stable" if psi < 0.1 else ("investigate" if psi < 0.25 else "significant")
        records.append({"feature": col, "type": "numeric",
                        "psi": psi, "ks_stat": round(ks_stat, 4),
                        "ks_p": round(ks_p, 4), "wasserstein": round(w_dist, 4),
                        "severity": severity})

    for col in categorical_cols:
        ref_dist = reference_df[col].value_counts(normalize=True)
        cur_dist = current_df[col].value_counts(normalize=True)
        all_cats = set(ref_dist.index) | set(cur_dist.index)
        ref_arr = np.array([ref_dist.get(c, 1e-6) for c in all_cats])
        cur_arr = np.array([cur_dist.get(c, 1e-6) for c in all_cats])
        psi = float(np.sum((cur_arr - ref_arr) * np.log(cur_arr / ref_arr)))
        severity = "stable" if psi < 0.1 else ("investigate" if psi < 0.25 else "significant")
        records.append({"feature": col, "type": "categorical",
                        "psi": round(psi, 4), "ks_stat": None,
                        "ks_p": None, "wasserstein": None, "severity": severity})

    return pd.DataFrame(records).sort_values("psi", ascending=False)

# Usage
report = drift_report(reference_df, current_df,
                      numeric_cols=["age", "income", "score"],
                      categorical_cols=["country", "device_type"])
print(report[report["severity"] != "stable"].to_string(index=False))
```

## Pattern 2: Evidently Drift Report and TestSuite

Automated drift gate with Evidently.

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns, TestShareOfDriftedColumns
from evidently import ColumnMapping

column_mapping = ColumnMapping(
    target="label",
    prediction="predicted_label",
    numerical_features=["age", "income", "tenure_days"],
    categorical_features=["country", "device_type"],
)

# Visual report (HTML)
report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=reference_df, current_data=current_df,
           column_mapping=column_mapping)
report.save_html("drift_report.html")

# Automated test gate (CI-friendly)
suite = TestSuite(tests=[
    TestNumberOfDriftedColumns(lt=3),     # fail if > 2 features drift
    TestShareOfDriftedColumns(lt=0.3),    # fail if > 30% features drift
])
suite.run(reference_data=reference_df, current_data=current_df,
          column_mapping=column_mapping)

result = suite.as_dict()
if not result["summary"]["all_passed"]:
    failed = [t for t in result["tests"] if t["status"] == "FAIL"]
    for t in failed:
        print(f"FAIL: {t['name']} — {t['description']}")
    raise SystemExit(1)
```

## Pattern 3: NannyML Performance Estimation Without Labels

Estimate model performance when ground truth labels are delayed.

```python
import nannyml as nml
import pandas as pd

# CBPE: Confidence-Based Performance Estimation
# Requires calibrated predicted probabilities
estimator = nml.CBPE(
    y_pred_proba="y_pred_proba",
    y_pred="y_pred",
    y_true="label",
    timestamp_column_name="timestamp",
    metrics=["roc_auc", "f1", "precision", "recall"],
    chunk_size=500,               # events per monitoring window
    problem_type="binary_classification",
)

# Fit on reference (labeled) data
estimator.fit(reference_df)

# Estimate on production data (no labels needed)
estimated_performance = estimator.estimate(production_df)
fig = estimated_performance.plot()
fig.savefig("estimated_performance.png")

# Check for estimated degradation
results_df = estimated_performance.to_df()
latest = results_df.iloc[-1]
if latest["estimated_roc_auc"] < 0.75:
    print(f"ALERT: Estimated AUC dropped to {latest['estimated_roc_auc']:.4f}")

# Univariate feature drift
univariate_drift = nml.UnivariateDriftCalculator(
    column_names=["age", "income", "country"],
    timestamp_column_name="timestamp",
    chunk_size=500,
    continuous_methods=["kolmogorov_smirnov", "wasserstein"],
    categorical_methods=["chi2", "jensen_shannon"],
)
univariate_drift.fit(reference_df)
drift_results = univariate_drift.calculate(production_df)
drift_results.filter(period="analysis", alerts=True).to_df()
```

## Pattern 4: whylogs Distribution Profiles

Lightweight sketches for continuous monitoring with WhyLabs.

```python
import whylogs as why
from whylogs.core.constraints import ConstraintsBuilder
from whylogs.core.constraints.factories import (
    no_missing_values,
    is_in_range,
)

# Profile reference data
reference_profile = why.log(reference_df).profile()
reference_profile.set_dataset_timestamp(reference_start)

# Profile production batch
production_profile = why.log(production_df).profile()

# Extract summary stats
ref_view = reference_profile.view()
cur_view = production_profile.view()

# Constraints: validate schema + ranges
builder = ConstraintsBuilder(dataset_profile_view=cur_view)
builder.add_constraint(no_missing_values(column_name="user_id"))
builder.add_constraint(is_in_range(column_name="age", lower=18, upper=120))
constraints = builder.build()

valid = constraints.validate()
for name, result in constraints.report():
    if not result:
        print(f"CONSTRAINT FAIL: {name}")

# Upload to WhyLabs for trend tracking
import whylogs.api.writer.whylabs as whylabs_writer
writer = whylabs_writer.WhyLabsWriter()
writer.write(file=production_profile)
```

## Pattern 5: Prometheus Metrics for Model Serving

Instrument prediction service for Grafana dashboards.

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import numpy as np

# Metrics
prediction_counter = Counter("model_predictions_total",
                              "Total prediction requests",
                              ["model_version", "outcome"])
prediction_latency = Histogram("model_prediction_latency_seconds",
                                "Prediction latency",
                                buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0])
score_histogram = Histogram("model_prediction_score",
                             "Distribution of predicted probabilities",
                             buckets=[i/10 for i in range(11)])
drift_gauge = Gauge("feature_psi", "PSI score per feature", ["feature"])

# In serving code
start_http_server(8001)   # Prometheus scrapes :8001/metrics

def predict_with_instrumentation(features: dict, model_version: str):
    import time
    start = time.time()

    score = model.predict_proba(features)[1]
    outcome = "positive" if score > 0.5 else "negative"

    prediction_counter.labels(model_version=model_version, outcome=outcome).inc()
    prediction_latency.observe(time.time() - start)
    score_histogram.observe(score)

    return score

# Background job: compute and push PSI per feature
def update_drift_gauges(reference_df, current_window_df, numeric_cols):
    for col in numeric_cols:
        psi = compute_psi(reference_df[col].values, current_window_df[col].values)
        drift_gauge.labels(feature=col).set(psi)
```

## Anti-Patterns

### Anti-Pattern 1: Alerting on Every Metric Individually
Monitoring 50 features × 3 metrics = 150 time series. Individual alerts per metric at 0.05 significance → expect 7+ false alarms per monitoring window by chance alone. Use composite drift score or require multiple features drifting before alerting.

### Anti-Pattern 2: Using Training Data as Reference Forever
Training data from 18 months ago may not represent current production distribution even when the model is working correctly (product changes, user base expansion). Periodically re-anchor reference windows or use stratified production samples from stable periods.

### Anti-Pattern 3: Monitoring Only Aggregate Distributions
Overall feature distribution can be stable while a specific slice (mobile users, a new country) drifts severely. Always monitor per-segment distributions for high-traffic segments.

### Anti-Pattern 4: Confusing Data Drift with Concept Drift
A feature distribution shift (data drift) does not necessarily cause model degradation. A model can handle new distribution ranges correctly. Concept drift (P(Y|X) shift) does cause degradation. Distinguish before triggering retraining.
