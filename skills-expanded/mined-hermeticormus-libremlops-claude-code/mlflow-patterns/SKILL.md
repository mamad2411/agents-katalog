---
name: "mlflow-patterns"
description: "MLflow patterns with code: a production tracking server setup, model signatures and registration, MLproject files, custom pyfunc flavors, and registry webhooks for CI/CD. Use when running MLflow for a team."
---

# MLflow Patterns

Expert patterns for MLflow tracking server, model registry, custom flavors, and deployment.

## Pattern 1: Production MLflow Server Setup

PostgreSQL backend + S3 artifact store for team deployment.

```bash
# Infrastructure
# PostgreSQL for run metadata (reliable, concurrent, queryable)
# S3 for artifacts (scalable, durable, cheap)

# 1. Create PostgreSQL database
psql -c "CREATE DATABASE mlflow; CREATE USER mlflow_user WITH PASSWORD 'secure_password'; GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow_user;"

# 2. Start MLflow server
mlflow server \
  --backend-store-uri postgresql://mlflow_user:secure_password@localhost:5432/mlflow \
  --default-artifact-root s3://my-mlflow-bucket/artifacts \
  --host 0.0.0.0 \
  --port 5000 \
  --serve-artifacts  # proxy artifact requests through server (hides S3 creds from clients)

# 3. Configure clients
export MLFLOW_TRACKING_URI=http://mlflow-server:5000
export AWS_DEFAULT_REGION=us-east-1
# OR in Python:
import mlflow
mlflow.set_tracking_uri("http://mlflow-server:5000")

# Docker deployment
# docker run -p 5000:5000 \
#   -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
#   -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
#   ghcr.io/mlflow/mlflow:latest \
#   mlflow server --backend-store-uri postgresql://... --default-artifact-root s3://...
```

## Pattern 2: Model Signature and Registry

Register model with schema, input example, and stage transition.

```python
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
import numpy as np

client = MlflowClient()
model_name = "fraud-detection-lgbm"

with mlflow.start_run(run_name="lgbm-v2-features") as run:
    # Train
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    proba = model.predict_proba(X_val)

    # Signature: documents expected input/output schema
    signature = infer_signature(
        model_input=X_train,      # DataFrame or numpy array
        model_output=proba         # Use probabilities, not class labels
    )

    # Input example: shows serving endpoint what a valid request looks like
    input_example = X_train.iloc[:3].to_dict('list')

    # Log model with all metadata
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        signature=signature,
        input_example=input_example,
        registered_model_name=model_name,  # auto-registers to registry
        extra_pip_requirements=["lightgbm>=4.0", "pandas>=2.0"]
    )

    # Log evaluation metrics
    mlflow.log_metrics({
        "val_auc": roc_auc_score(y_val, proba[:, 1]),
        "val_f1": f1_score(y_val, y_pred, average="weighted"),
        "val_ks": ks_stat,  # KS statistic for credit scoring
    })

# Transition to Staging
latest = client.get_latest_versions(model_name, stages=["None"])
for version in latest:
    client.transition_model_version_stage(
        name=model_name,
        version=version.version,
        stage="Staging",
        archive_existing_versions=False
    )
    client.update_model_version(
        name=model_name,
        version=version.version,
        description=f"LightGBM with v2 feature set. AUC={0.934:.3f}. Trained on data-v3."
    )
    # Set named alias for flexible routing
    client.set_registered_model_alias(model_name, "challenger", version.version)

print(f"Registered {model_name} v{version.version} → Staging")
```

## Pattern 3: MLproject File for Reproducible Training

Define project entry points for reproducible CI/CD execution.

```yaml
# MLproject
name: fraud_detection

docker_env:
  image: my-registry/ml-training:1.2.3
  # OR for conda:
  # conda_env: conda.yaml

entry_points:
  preprocess:
    parameters:
      data_path: {type: str}
      output_path: {type: str, default: "data/processed/"}
      test_size: {type: float, default: 0.2}
    command: "python src/preprocess.py --data {data_path} --output {output_path} --test-size {test_size}"

  train:
    parameters:
      data_path: {type: str, default: "data/processed/"}
      learning_rate: {type: float, default: 0.05}
      n_estimators: {type: int, default: 200}
      max_depth: {type: int, default: 6}
      experiment_name: {type: str, default: "fraud-detection"}
    command: "python src/train.py --data {data_path} --lr {learning_rate} --n-estimators {n_estimators} --max-depth {max_depth} --experiment {experiment_name}"

  evaluate:
    parameters:
      model_uri: {type: str}
      test_data: {type: str, default: "data/processed/test.parquet"}
    command: "python src/evaluate.py --model {model_uri} --test {test_data}"
```

```bash
# Run training pipeline
mlflow run . -e train -P learning_rate=0.03 -P n_estimators=300

# Run from Git
mlflow run https://github.com/org/repo.git -e train -P learning_rate=0.03 \
  --version v1.2.3  # specific git tag

# Run on remote cluster
mlflow run . -e train -b databricks \
  --backend-config '{"cluster_spec": {"num_workers": 4, "spark_version": "12.2.x-cpu-ml-scala2.12"}}'
```

## Pattern 4: Custom Python Function Flavor

Register models that don't fit standard MLflow flavors.

```python
import mlflow.pyfunc
import mlflow
import pandas as pd
import numpy as np
import joblib
import os

class EnsembleModel(mlflow.pyfunc.PythonModel):
    """Ensemble of multiple models with preprocessing pipeline."""

    def load_context(self, context):
        """Load artifacts referenced in mlflow.pyfunc.log_model(artifacts=...)."""
        self.preprocessor = joblib.load(context.artifacts["preprocessor"])
        self.model_1 = joblib.load(context.artifacts["model_1"])
        self.model_2 = joblib.load(context.artifacts["model_2"])
        self.weights = np.array([0.6, 0.4])

    def predict(self, context, model_input: pd.DataFrame) -> np.ndarray:
        """Called by mlflow models serve and pyfunc.load_model().predict()."""
        X = self.preprocessor.transform(model_input)
        proba_1 = self.model_1.predict_proba(X)[:, 1]
        proba_2 = self.model_2.predict_proba(X)[:, 1]
        return self.weights[0] * proba_1 + self.weights[1] * proba_2

# Log the ensemble model
with mlflow.start_run(run_name="ensemble-v1"):
    # Save artifacts to temp files
    joblib.dump(preprocessor, "/tmp/preprocessor.pkl")
    joblib.dump(model_1, "/tmp/model_1.pkl")
    joblib.dump(model_2, "/tmp/model_2.pkl")

    mlflow.pyfunc.log_model(
        artifact_path="ensemble_model",
        python_model=EnsembleModel(),
        artifacts={
            "preprocessor": "/tmp/preprocessor.pkl",
            "model_1": "/tmp/model_1.pkl",
            "model_2": "/tmp/model_2.pkl",
        },
        signature=infer_signature(X_sample, y_sample),
        input_example=X_sample[:3],
        registered_model_name="fraud-ensemble",
        conda_env={
            "channels": ["defaults", "conda-forge"],
            "dependencies": ["python=3.10", "scikit-learn=1.3", "lightgbm=4.0", {"pip": ["mlflow>=2.8"]}]
        }
    )
```

## Pattern 5: Registry Webhook for CI/CD

Trigger deployment pipeline when a model transitions to Production.

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Create webhook: POST to CI/CD endpoint on Production transition
webhook = client.create_registry_webhook(
    events=["MODEL_VERSION_TRANSITIONED_TO_PRODUCTION"],
    http_url_spec={
        "url": "https://jenkins.internal/job/deploy-model/build",
        "authorization": f"Bearer {os.environ['JENKINS_TOKEN']}",
        "enable_ssl_verification": True,
    },
    model_name="fraud-detection-lgbm",
    description="Trigger deployment pipeline on Production promotion"
)

# The webhook POST body includes:
# {
#   "event": "MODEL_VERSION_TRANSITIONED_TO_PRODUCTION",
#   "model_name": "fraud-detection-lgbm",
#   "version": "7",
#   "to_stage": "Production",
#   "run_id": "abc123..."
# }

# List existing webhooks
webhooks = client.list_registry_webhooks(model_name="fraud-detection-lgbm")
for wh in webhooks:
    print(f"ID: {wh.id} | URL: {wh.http_url_spec.url} | Events: {wh.events}")
```

## Anti-Patterns

### Anti-Pattern 1: Using SQLite in Production
SQLite has no concurrent write support. Multiple training jobs writing to the same SQLite file cause corruption or lock errors. Use PostgreSQL for any shared team deployment.

### Anti-Pattern 2: Logging Models Without Signatures
Models without signatures can't be validated at serving time. A schema mismatch between training features and serving features causes silent wrong predictions, not an error. Always log with `signature=infer_signature(X_train, predictions)`.

### Anti-Pattern 3: Promoting Without a Gate
Transitioning models to Production manually without evaluation criteria leads to model quality regression. Always require: (1) evaluation metrics above threshold, (2) comparison against current Production model, (3) human approval or automated gate.

### Anti-Pattern 4: Storing Artifacts in the Backend Store
The backend store (PostgreSQL) is for metadata only — run IDs, params, metrics, tags. Large files (models, datasets) belong in the artifact store (S3). Storing binary blobs in PostgreSQL is slow and expensive.
