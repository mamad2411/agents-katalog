---
name: "model-registry-patterns"
description: "Model registry patterns with code: MLflow registration with signature and lineage, staging gates and production promotion, champion and challenger with MLflow aliases, model card generation, and webhook-triggered promotion pipelines. Use when governing model releases."
---

# Model Registry Patterns

Expert patterns for model registration, versioning, champion/challenger promotion, model cards, and webhook-driven CI/CD.

## Pattern 1: MLflow Registration with Signature and Lineage

Register a model with full metadata: signature, metrics, dataset reference.

```python
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import pandas as pd

mlflow.set_tracking_uri("http://mlflow-server:5000")

with mlflow.start_run(run_name="churn-model-v2.1.0") as run:
    # Train model
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    # Log evaluation metrics
    mlflow.log_metrics({
        "val_auc_roc": roc_auc_score(y_val, y_proba),
        "val_f1": f1_score(y_val, y_pred),
        "val_mcc": matthews_corrcoef(y_val, y_pred),
    })

    # Log dataset lineage
    mlflow.log_params({
        "train_dataset_version": "s3://data/processed/v20240315/train.parquet",
        "train_dataset_sha256": "abc123def456",
        "train_size": len(X_train),
        "val_size": len(X_val),
        "git_commit": "d4e5f6a",
    })

    # Infer and log signature (enforces schema at serving time)
    signature = infer_signature(X_val, y_proba)
    input_example = X_val.iloc[:3]

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        signature=signature,
        input_example=input_example,
        registered_model_name="churn-model",
    )

# Retrieve the version just registered
client = mlflow.tracking.MlflowClient()
latest = client.get_latest_versions("churn-model", stages=["None"])[0]
print(f"Registered: churn-model v{latest.version} (run_id={latest.run_id})")
```

## Pattern 2: Staging Gate and Production Promotion

Automated evaluation gate before promotion to Production.

```python
from mlflow.tracking import MlflowClient
from sklearn.metrics import roc_auc_score, f1_score
import mlflow.pyfunc

client = MlflowClient()
MODEL_NAME = "churn-model"
AUC_THRESHOLD = 0.82
F1_THRESHOLD = 0.70

def evaluate_and_promote(candidate_version: str, X_holdout, y_holdout):
    """Evaluate a Staging model and promote to Production if gates pass."""
    # Load Staging model
    model_uri = f"models:/{MODEL_NAME}/{candidate_version}"
    model = mlflow.pyfunc.load_model(model_uri)

    y_proba = model.predict(X_holdout)
    y_pred = (y_proba > 0.5).astype(int)

    auc = roc_auc_score(y_holdout, y_proba)
    f1 = f1_score(y_holdout, y_pred)

    print(f"Holdout AUC: {auc:.4f} (threshold: {AUC_THRESHOLD})")
    print(f"Holdout F1:  {f1:.4f} (threshold: {F1_THRESHOLD})")

    if auc < AUC_THRESHOLD or f1 < F1_THRESHOLD:
        print("Gate FAILED — archiving candidate")
        client.transition_model_version_stage(MODEL_NAME, candidate_version, "Archived")
        return False

    # Promote to Production, archive current champion
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=candidate_version,
        stage="Production",
        archive_existing_versions=True,  # previous Production → Archived
    )
    # Set semantic alias
    client.set_registered_model_alias(MODEL_NAME, "champion", candidate_version)
    print(f"Promoted churn-model v{candidate_version} to Production")
    return True

# Usage in CI
staging_versions = client.get_latest_versions(MODEL_NAME, stages=["Staging"])
if staging_versions:
    success = evaluate_and_promote(staging_versions[0].version, X_holdout, y_holdout)
```

## Pattern 3: Champion/Challenger with MLflow Aliases

Track champion and challenger with semantic aliases.

```python
from mlflow.tracking import MlflowClient
import mlflow.pyfunc

client = MlflowClient()
MODEL_NAME = "fraud-detector"

# Set up champion/challenger aliases
def register_challenger(run_id: str, model_artifact_path: str = "model") -> str:
    """Register a new model version as challenger."""
    model_uri = f"runs:/{run_id}/{model_artifact_path}"
    result = mlflow.register_model(model_uri, MODEL_NAME)
    client.set_registered_model_alias(MODEL_NAME, "challenger", result.version)
    client.transition_model_version_stage(MODEL_NAME, result.version, "Staging")
    print(f"Challenger: {MODEL_NAME} v{result.version}")
    return result.version

# Load by alias
champion = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}@champion")
challenger = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}@challenger")

# Shadow evaluation: compare outputs on live traffic sample
def shadow_compare(X_sample, threshold: float = 0.5) -> dict:
    champ_proba = champion.predict(X_sample)
    chall_proba = challenger.predict(X_sample)

    agreement = (
        ((champ_proba > threshold) == (chall_proba > threshold)).mean()
    )
    champ_auc = roc_auc_score(y_sample, champ_proba)
    chall_auc = roc_auc_score(y_sample, chall_proba)

    return {
        "champion_auc": round(champ_auc, 4),
        "challenger_auc": round(chall_auc, 4),
        "prediction_agreement": round(agreement, 4),
        "promote": chall_auc > champ_auc + 0.005,  # epsilon threshold
    }
```

## Pattern 4: Model Card Generation

Structured model documentation per Hugging Face / Google standard.

```python
from huggingface_hub import ModelCard, ModelCardData

def generate_model_card(
    model_name: str,
    version: str,
    metrics: dict,
    sliced_metrics: dict,
    training_data_ref: str,
    intended_use: str,
    out_of_scope: str,
    known_limitations: str,
) -> str:
    card_data = ModelCardData(
        language="en",
        license="apache-2.0",
        model_name=model_name,
        tags=["classification", "tabular"],
        metrics=["roc_auc", "f1", "mcc"],
    )

    card_content = f"""---
{card_data.to_yaml()}
---

# {model_name} v{version}

## Model Details
- **Architecture**: LightGBM binary classifier
- **Version**: {version}
- **Training date**: {metrics.get('training_date', 'unknown')}

## Intended Use
{intended_use}

**Out of scope**: {out_of_scope}

## Evaluation Results

| Metric | Value |
|--------|-------|
| AUC-ROC | {metrics.get('auc_roc', 'N/A'):.4f} |
| F1 | {metrics.get('f1', 'N/A'):.4f} |
| MCC | {metrics.get('mcc', 'N/A'):.4f} |

### Performance by Subgroup
{_format_sliced_metrics(sliced_metrics)}

## Training Data
{training_data_ref}

## Known Limitations
{known_limitations}
"""
    return card_content

def _format_sliced_metrics(sliced: dict) -> str:
    rows = ["| Slice | AUC | F1 |", "|-------|-----|-----|"]
    for slice_name, vals in sliced.items():
        rows.append(f"| {slice_name} | {vals.get('auc', 'N/A'):.4f} | {vals.get('f1', 'N/A'):.4f} |")
    return "\n".join(rows)
```

## Pattern 5: Webhook-Triggered CI Promotion Pipeline

Automate evaluation when a model transitions to Staging.

```python
# fastapi webhook receiver — receives MLflow registry events
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/webhooks/mlflow-registry")
async def handle_registry_event(request: Request):
    event = await request.json()

    model_name = event.get("model_name")
    version = event.get("version")
    new_stage = event.get("to_stage")

    if new_stage == "Staging":
        # Trigger GitHub Actions evaluation workflow
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.github.com/repos/org/repo/actions/workflows/evaluate-model.yml/dispatches",
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
                json={
                    "ref": "main",
                    "inputs": {
                        "model_name": model_name,
                        "model_version": str(version),
                    }
                }
            )
        return {"status": "CI triggered", "model": model_name, "version": version}

    return {"status": "ignored", "stage": new_stage}
```

## Anti-Patterns

### Anti-Pattern 1: Promoting Models Without Model Cards
A model in Production with no documentation of training data, evaluation results, or known limitations is a governance liability. Any model in Production must have a model card before promotion.

### Anti-Pattern 2: Deleting Old Registry Versions
Never delete registry entries — archive them. Deleted versions break audit trails and rollback capability. The archive stage exists precisely to retire models while preserving history.

### Anti-Pattern 3: Using Only Version Numbers Without Aliases
`models:/churn-model/15` hardcoded in serving code breaks when v16 is promoted. Use semantic aliases (`@champion`) so deployment code never needs to change when models are promoted.

### Anti-Pattern 4: Registering Without Dataset Lineage
A model registered without a reference to the training dataset version cannot be reproduced, audited, or investigated when failures occur. Always log the dataset URI, version hash, and git commit in the run parameters before registering.
