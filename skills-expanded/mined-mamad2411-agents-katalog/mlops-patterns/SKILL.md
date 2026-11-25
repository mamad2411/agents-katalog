---
name: mlops-patterns
description: "When to activate: MLOps, DVC, model versioning, drift detection, Evidently, WhyLogs, retraining, ML CI/CD, model monitoring"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# MLOps Patterns

## DVC Pipeline

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python src/prepare.py --date ${date}
    deps: [src/prepare.py, data/raw/]
    params: [params.yaml:prepare]
    outs: [data/processed/]

  featurize:
    cmd: python src/featurize.py
    deps: [src/featurize.py, data/processed/]
    outs: [data/features/]

  train:
    cmd: python src/train.py
    deps: [src/train.py, data/features/]
    params: [params.yaml:train]
    outs: [models/model.pkl]
    metrics: [metrics/train.json]

  evaluate:
    cmd: python src/evaluate.py
    deps: [src/evaluate.py, models/model.pkl, data/features/]
    metrics: [metrics/eval.json:
        cache: false]
```

```bash
dvc repro                    # run changed stages only
dvc params diff HEAD~1       # compare params to previous commit
dvc metrics diff HEAD~1      # compare metrics
dvc push                     # push artifacts to remote
```

## Model Versioning with MLflow Registry

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promote model to staging after validation
client.transition_model_version_stage(
    name="FraudClassifier",
    version=5,
    stage="Staging",
    archive_existing_versions=False,
)

# After A/B test: promote to production
client.transition_model_version_stage(
    name="FraudClassifier",
    version=5,
    stage="Production",
    archive_existing_versions=True,  # demote old prod version
)

# Load production model
model = mlflow.sklearn.load_model("models:/FraudClassifier/Production")
```

## Data & Prediction Drift (Evidently)

```python
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.tests import TestNumberOfDriftedColumns, TestShareOfDriftedColumns

# Scheduled monitoring report
report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=ref_df, current_data=weekly_df)
report.save_html(f"reports/drift_{week}.html")

# Alerting via test suite
tests = TestSuite(tests=[
    TestShareOfDriftedColumns(lt=0.3),  # fail if >30% features drift
    TestNumberOfDriftedColumns(lt=5),
])
tests.run(reference_data=ref_df, current_data=weekly_df)
if not tests.as_dict()["summary"]["all_passed"]:
    trigger_retraining_pipeline()
```

## WhyLogs Profiling

```python
import whylogs as why
from whylogs.core.constraints import ConstraintsBuilder, MetricConstraint
from whylogs.core.metrics.condition_count_metric import Condition

# Profile production data
with why.logger() as logger:
    for batch in production_batches:
        logger.log(batch)
    profile = logger.get_profile()

profile.writer("whylabs").write()  # send to WhyLabs platform

# Local constraint checks
builder = ConstraintsBuilder(dataset_profile_view=profile.view())
builder.add_constraint(
    MetricConstraint(name="amount non-negative", condition=Condition(ge=0), metric_selector=...)
)
constraints = builder.build()
report = constraints.generate_constraints_report()
```

## Retraining Trigger Pattern

```python
from datetime import datetime, timedelta

class RetrainingTrigger:
    def __init__(self, psi_threshold=0.2, performance_drop=0.05, max_age_days=30):
        self.psi_threshold = psi_threshold
        self.performance_drop = performance_drop
        self.max_age_days = max_age_days

    def should_retrain(self, current_metrics: dict, baseline_metrics: dict,
                       model_trained_at: datetime) -> tuple[bool, str]:
        age = (datetime.utcnow() - model_trained_at).days
        if age > self.max_age_days:
            return True, f"Model age {age}d exceeds limit"
        if current_metrics["psi"] > self.psi_threshold:
            return True, f"PSI={current_metrics['psi']:.3f} exceeds threshold"
        perf_drop = baseline_metrics["auc"] - current_metrics["auc"]
        if perf_drop > self.performance_drop:
            return True, f"AUC dropped by {perf_drop:.3f}"
        return False, "No retraining needed"
```

## ML CI/CD (GitHub Actions)

```yaml
# .github/workflows/ml-ci.yml
name: ML Pipeline
on:
  push:
    paths: ["src/**", "params.yaml"]

jobs:
  train-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: iterative/setup-dvc@v1
      - name: Pull data
        run: dvc pull data/features/
      - name: Train
        run: dvc repro train evaluate
      - name: Compare metrics
        run: dvc metrics diff main
      - name: Register model if better
        run: python scripts/register_if_better.py
```

## Key Patterns

- **Reproducibility triad**: pin data version (DVC), code version (git SHA), env version (requirements.lock)
- Retrain triggers: PSI > 0.2 (significant shift), performance drop > 5%, or time-based (30 days)
- Shadow models: run new model in parallel for 1-2 weeks before promoting to production
- Store training data + features in versioned artifacts, not just final model
