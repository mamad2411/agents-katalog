---
name: mlflow-patterns
description: "When to activate: MLflow, experiment tracking, model registry, autologging, MLflow serving, artifact storage, model signatures, ML lifecycle"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# MLflow Patterns

## Experiment Tracking

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("churn-prediction-v2")

with mlflow.start_run(run_name="rf-baseline"):
    # Log parameters
    params = {"n_estimators": 200, "max_depth": 6, "random_state": 42}
    mlflow.log_params(params)

    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)

    # Log metrics
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_metric("train_auc", roc_auc_score(y_train, model.predict_proba(X_train)[:, 1]))

    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
    mlflow.log_dict({"features": list(X_train.columns)}, "features.json")

    # Log model with signature
    from mlflow.models.signature import infer_signature
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(model, "model", signature=signature)
```

## Autologging

```python
# One-line autologging — logs params, metrics, model automatically
mlflow.sklearn.autolog(log_input_examples=True, log_model_signatures=True)

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    # Automatically logs: n_estimators, max_depth, accuracy, f1, model artifact

# PyTorch autologging
mlflow.pytorch.autolog()

# XGBoost autologging
mlflow.xgboost.autolog()
```

## Model Registry

```python
# Register model
run_id = "abc123def456"
model_uri = f"runs:/{run_id}/model"
model_version = mlflow.register_model(model_uri, "ChurnPredictor")

# Transition to staging/production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="ChurnPredictor",
    version=model_version.version,
    stage="Production",
    archive_existing_versions=True,  # Archive old production versions
)

# Load production model
model = mlflow.sklearn.load_model("models:/ChurnPredictor/Production")
```

## Model Serving

```bash
# Serve via REST API
mlflow models serve -m "models:/ChurnPredictor/Production" -p 1234

# Docker deployment
mlflow models build-docker -m "models:/ChurnPredictor/Production" -n churn-predictor
docker run -p 1234:8080 churn-predictor

# Predict via API
curl -X POST http://localhost:1234/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_records": [{"age": 35, "tenure": 12, "plan": "premium"}]}'
```

## Projects (Reproducible Runs)

```yaml
# MLproject
name: churn-model
conda_env: conda.yaml

entry_points:
  train:
    parameters:
      n_estimators: {type: int, default: 100}
      max_depth: {type: int, default: 6}
      data_path: {type: str, default: "data/train.csv"}
    command: "python train.py --n-estimators {n_estimators} --max-depth {max_depth} --data {data_path}"
```

```bash
# Run project
mlflow run . -P n_estimators=200 -P max_depth=8
mlflow run git+https://github.com/org/churn-model -P n_estimators=200
```

## Comparing Runs

```python
client = mlflow.tracking.MlflowClient()

# Get all runs sorted by AUC
runs = client.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.roc_auc > 0.85",
    order_by=["metrics.roc_auc DESC"],
    max_results=10,
)

for run in runs:
    print(f"{run.info.run_id[:8]}: auc={run.data.metrics['roc_auc']:.4f} "
          f"params={run.data.params}")
```
