---
name: tpl-ai-ml-ml-training-pipeline
description: Template do pack (ai-ml/09-ml-training-pipeline.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/09-ml-training-pipeline.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: ML Training Pipeline (PyTorch + MLflow + DVC + GitHub Actions)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/09-ml-training-pipeline.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Training:** PyTorch 2.2+ + CUDA 12.1
- **Experiment Tracking:** MLflow 2.11+ (local or Databricks)
- **Data Versioning:** DVC 3.x + S3 (remote storage)
- **CI/CD:** GitHub Actions (automated training + evaluation)
- **Model Registry:** MLflow Model Registry (staging → production lifecycle)
- **Environment:** conda / virtualenv, requirements.txt pinned

---

## PROJECT STRUCTURE
```
ml-project/
├── data/
│   ├── raw/                  # DVC-tracked (not in git)
│   ├── processed/            # DVC-tracked
│   └── .gitignore
├── src/
│   ├── data/
│   │   ├── preprocessing.py
│   │   └── dataset.py        # PyTorch Dataset class
│   ├── models/
│   │   ├── architecture.py   # Model class
│   │   └── train.py          # Training loop
│   ├── evaluation/
│   │   └── metrics.py
│   └── config.py             # Hydra / dataclasses config
├── experiments/
│   └── configs/
│       ├── baseline.yaml
│       └── experiment_01.yaml
├── dvc.yaml                  # DVC pipeline stages
├── params.yaml               # Tunable params (tracked by DVC)
├── .github/
│   └── workflows/
│       └── training_ci.yml
├── MLproject                 # MLflow project definition
└── requirements.txt
```

---

## ARCHITECTURE RULES
1. **Every experiment is tracked** — no training run without MLflow. Metrics, params, artifacts all logged.
2. **Experiment naming convention** — `{task}_{model_arch}_{date}_{run_id}`, e.g., `classification_resnet50_20240315_abc123`.
3. **Data versions match model versions** — every registered model has a DVC commit ref in its tags.
4. **Model registry stages** — None → Staging → Production. Never deploy without explicit promotion.
5. **Reproducibility requires code + data + params** — DVC pipeline (`dvc repro`) must produce identical results.
6. **Training CI does not auto-promote** — CI trains and evaluates; human approves promotion to production.
7. **Log everything, prune nothing during training** — log at every epoch; disk is cheap, missing data is not.
8. **Pin all dependencies** — `requirements.txt` with exact versions (`==`); no `>=` in production training.

---

## DVCYAML — PIPELINE DEFINITION

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python src/data/preprocessing.py
    deps:
      - src/data/preprocessing.py
      - data/raw/
    params:
      - params.yaml:
          - preprocessing.test_size
          - preprocessing.random_seed
    outs:
      - data/processed/

  train:
    cmd: python src/models/train.py
    deps:
      - src/models/train.py
      - src/models/architecture.py
      - data/processed/
    params:
      - params.yaml:
          - training.epochs
          - training.lr
          - training.batch_size
          - model.hidden_size
    metrics:
      - metrics/train_metrics.json:
          cache: false
    outs:
      - models/best_model.pt

  evaluate:
    cmd: python src/evaluation/metrics.py
    deps:
      - src/evaluation/metrics.py
      - models/best_model.pt
      - data/processed/test/
    metrics:
      - metrics/eval_metrics.json:
          cache: false
```

---

## PARAMS.YAML

```yaml
# params.yaml — DVC tracks changes here
preprocessing:
  test_size: 0.2
  val_size: 0.1
  random_seed: 42
  normalize: true

training:
  epochs: 50
  lr: 0.001
  lr_scheduler: cosine
  batch_size: 64
  early_stopping_patience: 5
  gradient_clip: 1.0

model:
  architecture: resnet50
  num_classes: 10
  dropout: 0.3
  hidden_size: 512
  pretrained: true

evaluation:
  metrics: [accuracy, f1_macro, roc_auc]
  threshold: 0.5
```

---

## TRAINING SCRIPT WITH MLFLOW

```python
# src/models/train.py
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import yaml
from pathlib import Path
from datetime import datetime

# Load params from DVC params.yaml
with open("params.yaml") as f:
    params = yaml.safe_load(f)

EXPERIMENT_NAME = "image-classification"
RUN_NAME = f"resnet50_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def train():
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=RUN_NAME) as run:
        # Log ALL params upfront
        mlflow.log_params({
            **params["training"],
            **params["model"],
        })
        mlflow.log_param("git_commit", os.popen("git rev-parse HEAD").read().strip())
        mlflow.log_param("dvc_stage", "train")

        # Build model
        model = build_model(params["model"])
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=params["training"]["lr"],
            weight_decay=1e-4,
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=params["training"]["epochs"]
        )

        # Training loop
        best_val_loss = float("inf")
        patience_counter = 0

        for epoch in range(params["training"]["epochs"]):
            train_loss, train_acc = train_epoch(model, train_loader, optimizer)
            val_loss, val_acc = validate(model, val_loader)
            scheduler.step()

            # Log every epoch (don't skip — disk is cheap)
            mlflow.log_metrics({
                "train_loss":    train_loss,
                "train_acc":     train_acc,
                "val_loss":      val_loss,
                "val_acc":       val_acc,
                "learning_rate": scheduler.get_last_lr()[0],
            }, step=epoch)

            # Best model checkpoint
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                torch.save(model.state_dict(), "models/best_model.pt")
                mlflow.log_artifact("models/best_model.pt")
            else:
                patience_counter += 1
                if patience_counter >= params["training"]["early_stopping_patience"]:
                    mlflow.log_param("early_stopped_at_epoch", epoch)
                    break

        # Log final model
        mlflow.pytorch.log_model(model, "model")

        # Write DVC metrics file (for dvc metrics show)
        import json
        with open("metrics/train_metrics.json", "w") as f:
            json.dump({"best_val_loss": best_val_loss, "final_epoch": epoch}, f)

        print(f"Training complete. Run ID: {run.info.run_id}")
        return run.info.run_id
```

---

## MODEL REGISTRY — STAGING TO PRODUCTION

```python
# src/registry/promote.py
from mlflow.tracking import MlflowClient
import os

client = MlflowClient(tracking_uri=os.environ["MLFLOW_TRACKING_URI"])
MODEL_NAME = "image-classifier"

def register_model(run_id: str, model_name: str = MODEL_NAME) -> str:
    """Register trained model to Model Registry in Staging."""
    result = mlflow.register_model(
        f"runs:/{run_id}/model",
        model_name,
    )

    # Add metadata tags
    client.set_model_version_tag(model_name, result.version, "dvc_commit",
                                  os.popen("git rev-parse HEAD").read().strip())
    client.set_model_version_tag(model_name, result.version, "trained_by", "training_ci")

    # Transition to staging (automatic after CI)
    client.transition_model_version_stage(model_name, result.version, "Staging")
    print(f"Model v{result.version} in Staging")
    return result.version

def promote_to_production(version: str, model_name: str = MODEL_NAME):
    """Human-triggered: promote staging model to production."""
    # Archive current production model
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for v in prod_versions:
        client.transition_model_version_stage(model_name, v.version, "Archived")

    client.transition_model_version_stage(model_name, version, "Production")
    print(f"Model v{version} promoted to Production")
```

---

## DVC DATA VERSIONING

```bash
# One-time setup
dvc init
dvc remote add -d s3remote s3://my-bucket/dvc-store
dvc remote modify s3remote region us-east-1

# Track dataset
dvc add data/raw/dataset.csv
git add data/raw/dataset.csv.dvc data/raw/.gitignore
git commit -m "data: add raw dataset v1.0"
git tag "data-v1.0"

# Run pipeline
dvc repro           # Runs only changed stages
dvc repro --force   # Force re-run all stages

# Push data to S3
dvc push

# Switch dataset version
git checkout data-v0.9
dvc checkout   # Swaps data/raw/dataset.csv to the v0.9 version
```

---

## GITHUB ACTIONS TRAINING CI

```yaml
# .github/workflows/training_ci.yml
name: Training CI

on:
  push:
    paths:
      - 'params.yaml'
      - 'src/**'
      - 'dvc.yaml'

jobs:
  train-and-evaluate:
    runs-on: [self-hosted, gpu]   # Requires GPU runner
    steps:
      - uses: actions/checkout@v4

      - name: Setup DVC
        run: |
          pip install dvc[s3] mlflow
          dvc remote modify s3remote access_key_id ${{ secrets.AWS_ACCESS_KEY_ID }}
          dvc remote modify s3remote secret_access_key ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Pull data
        run: dvc pull

      - name: Run pipeline
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
        run: dvc repro

      - name: Check metrics
        run: |
          VAL_ACC=$(python -c "import json; d=json.load(open('metrics/eval_metrics.json')); print(d['val_accuracy'])")
          python -c "
          acc = float('$VAL_ACC')
          assert acc >= 0.85, f'Accuracy {acc} below 0.85 threshold'
          print(f'Quality gate passed: accuracy={acc}')
          "

      - name: Register to staging
        run: python src/registry/promote.py
```

---

## EXPERIMENT NAMING CONVENTIONS
```
Format: {task}_{model}_{variant}_{YYYYMMDD}

Examples:
  classification_resnet50_baseline_20240315
  ner_deberta_v2_augmented_20240318
  regression_lgbm_feature_v4_20240320

MLflow tags (always set):
  - "git_commit": SHA
  - "dvc_commit": data version SHA
  - "trained_by": "ci" | "manual" | "scheduled"
  - "dataset_version": "v1.2"
```
