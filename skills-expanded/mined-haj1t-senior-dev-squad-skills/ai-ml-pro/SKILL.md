---
name: ai-ml-pro
description: "ML workflows, training pipelines, model evaluation, deployment, experiment tracking. Use when building or reviewing ML systems."
---

# AI/ML Pro

## Purpose

Build production ML systems: data pipelines, training, evaluation, model serving, experiment tracking, and MLOps. Treat models as software — versioned, tested, monitored, and reproducible.

## When to Use

**Use this when:**
- Building or reviewing training pipelines, feature engineering, or model evaluation workflows
- Designing a model serving endpoint or inference API
- Setting up experiment tracking, model registry, or MLOps CI/CD for a project

**Use this ESPECIALLY when:**
- Your model is going to production and needs monitoring for data drift or concept drift
- You need reproducibility guarantees across environments (seed management, DVC, artifact versioning)
- You are establishing an A/B testing or shadow-deployment strategy for a new model version

**Don't skip when:**
- The dataset contains PII that must be redacted before training or evaluation
- A prior model is already in production and any regression in metrics would have business impact
- The team lacks a baseline evaluation framework and acceptance criteria are undefined

## Core Patterns

### 1. Project Structure

```
project/
  data/
    raw/
    processed/
    features/
  notebooks/
    01_eda.ipynb
    02_feature_engineering.ipynb
  src/
    features/
      build_features.py
    models/
      train.py
      predict.py
      evaluate.py
    pipelines/
      training_pipeline.py
      inference_pipeline.py
  tests/
    test_features.py
    test_model.py
  configs/
    experiment_001.yaml
    experiment_002.yaml
  models/              ← Trained artifacts (gitignored)
  reports/
    figures/
  pyproject.toml
  requirements.txt
  Dockerfile
  .dvc/config         ← Data version control
```

### 2. Experiment Tracking

```python
# Weights & Biases / MLflow
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("project-name")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("model_type", "random_forest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)

    # Log metrics
    mlflow.log_metric("accuracy", 0.94)
    mlflow.log_metric("f1_score", 0.92)
    mlflow.log_metric("latency_ms", 45)

    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("feature_importance.png")

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

### 3. Training Pipeline

```python
# src/pipelines/training_pipeline.py
from pathlib import Path
import yaml

class TrainingPipeline:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def run(self):
        # 1. Load and validate data
        data = self.load_data()
        self.validate_data(data)

        # 2. Feature engineering
        features = self.build_features(data)

        # 3. Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            features, data.target,
            test_size=self.config['data']['test_size'],
            random_state=self.config['data']['seed'],
        )

        # 4. Train model
        model = self.train_model(X_train, y_train)

        # 5. Evaluate
        metrics = self.evaluate(model, X_test, y_test)

        # 6. Save artifacts
        self.save_model(model)
        self.save_metrics(metrics)

        return model, metrics
```

### 4. Model Evaluation

```python
# src/models/evaluate.py
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
)

def evaluate_classification(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1': f1_score(y_test, y_pred, average='weighted'),
    }

    if y_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_test, y_proba)

    return metrics

    # Test: Model metrics must exceed baseline
    assert metrics['f1'] > BASELINE_F1, f"F1 {metrics['f1']} below baseline {BASELINE_F1}"
    # Test: No data leakage (time-based split for time series)
    # Test: Reproducibility (same seed → same results)
```

### 5. Model Serving

```python
# FastAPI inference endpoint
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
model = load_model("models/production/model.pkl")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    probability: float | None
    model_version: str
    latency_ms: float

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    import time
    start = time.time()

    if len(request.features) != EXPECTED_FEATURES:
        raise HTTPException(400, f"Expected {EXPECTED_FEATURES} features")

    prediction = model.predict([request.features])[0]
    probability = model.predict_proba([request.features])[0].max() if hasattr(model, 'predict_proba') else None

    latency = (time.time() - start) * 1000

    return PredictionResponse(
        prediction=prediction,
        probability=probability,
        model_version=MODEL_VERSION,
        latency_ms=round(latency, 2),
    )
```

### 6. Data Validation

```python
# Great Expectations / Pandas profiling
import pandera as pa

class InputSchema(pa.DataFrameModel):
    age: int = pa.Field(ge=0, le=120)
    income: float = pa.Field(ge=0)
    education_years: int = pa.Field(ge=0, le=30)
    employment_status: str = pa.Field(isin=['employed', 'unemployed', 'student', 'retired'])

@pa.check_types
def validate_input(df: pd.DataFrame) -> pd.DataFrame:
    InputSchema.validate(df)
    # Domain-specific checks
    assert df['age'].notna().all(), "Missing age values"
    assert (df['income'] > 0).all(), "Negative income values"
    return df
```

### 7. A/B Testing Framework

```python
# Model comparison in production
class ModelRouter:
    def __init__(self):
        self.control_model = load_model("v1")
        self.treatment_model = load_model("v2")
        self.traffic_split = 0.1  # 10% to v2

    def predict(self, features, user_id: str):
        # Consistent routing (same user → same model)
        if hash(user_id) % 100 < self.traffic_split * 100:
            model = self.treatment_model
            variant = 'treatment'
        else:
            model = self.control_model
            variant = 'control'

        result = model.predict([features])[0]
        self.log_prediction(user_id, variant, result)
        return result
```

### Checklist

- [ ] Data versioned (DVC / Quilt / LakeFS)
- [ ] Experiments tracked (MLflow / W&B)
- [ ] Training reproducible (fixed seed, deterministic algorithms)
- [ ] Data validation (schema, ranges, distributions)
- [ ] Model evaluation > baseline before deployment
- [ ] Feature store for production features
- [ ] Model monitoring (data drift, concept drift)
- [ ] A/B testing framework ready
- [ ] Inference endpoint has latency + input validation
- [ ] Model registry (versioned, staged: staging→production)
- [ ] CI/CD pipeline trains + evaluates on every PR

## Related Skills

- **data-engineering-pro** — upstream ETL, feature store construction, and data quality contracts that feed your training pipeline
- **ai-app-security-pro** — LLM-specific threats when the model you serve accepts user-supplied prompts
- **backend-senior-engineer** — FastAPI / REST serving layer, auth, and rate limiting around your inference endpoint
- **observability-pro** — production monitoring for model latency, error rates, and drift alerting
- **test-engineer** — evaluation harnesses, baseline regression tests, and property-based tests for feature transforms
- **performance-engineer** — inference latency optimization, batching strategies, and GPU/CPU profiling
- **devops-release-engineer** — CI/CD pipeline that trains, evaluates, and promotes models through staging to production
- **cloud-security-auditor** — IAM policies and storage security for model artifacts, datasets, and feature stores
