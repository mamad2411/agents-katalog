---
name: ml-experiment-tracking
description: Set up ML experiment tracking with MLflow or Weights & Biases. Outputs experiment logging code, model registry integration, hyperparameter tracking, artifact management, and reproducibility configuration.
argument-hint: [ML framework, experiment type, team size, deployment target]
allowed-tools: Read, Write, Bash
---

# ML Experiment Tracking

Track every experiment — parameters, metrics, artifacts, and environment — so you can reproduce any result, compare runs systematically, and promote the right model to production with confidence.

## Process

1. **Choose tracking backend** — MLflow (self-hosted), W&B (managed), or Neptune.
2. **Instrument training code** — log params, metrics at each epoch, artifacts.
3. **Set up experiment organization** — experiments > runs > nested runs.
4. **Configure artifact storage** — model weights, datasets, feature importance plots.
5. **Register successful models** — model registry with staging/production stages.
6. **Automate comparison** — scripts to compare runs, find best model.
7. **Reproduce any run** — env capture, seed logging, code versioning.

## Output Format

### MLflow Experiment Tracking

```python
# train.py — full MLflow instrumentation
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import numpy as np
import pandas as pd
from datetime import datetime
import os
import json
import hashlib
import subprocess

# Configure tracking server
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000"))

class ExperimentTracker:
    def __init__(self, experiment_name: str, tags: dict = None):
        self.experiment_name = experiment_name
        self.tags = tags or {}
        
        # Create or get experiment
        mlflow.set_experiment(experiment_name)
        self.experiment = mlflow.get_experiment_by_name(experiment_name)
    
    def start_run(self, run_name: str = None, nested: bool = False):
        """Context manager for a tracked run."""
        return mlflow.start_run(
            run_name=run_name or f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            tags={
                **self.tags,
                "git_commit": self._get_git_commit(),
                "git_branch": self._get_git_branch(),
                "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}",
            },
            nested=nested
        )
    
    def log_dataset(self, df: pd.DataFrame, name: str, context: str = "training"):
        """Log dataset metadata and hash for reproducibility."""
        dataset_hash = hashlib.md5(
            pd.util.hash_pandas_object(df).values
        ).hexdigest()
        
        mlflow.log_params({
            f"dataset_{name}_rows": len(df),
            f"dataset_{name}_cols": len(df.columns),
            f"dataset_{name}_hash": dataset_hash[:8],
        })
        
        # Log dataset as artifact
        dataset_info = {
            "name": name,
            "context": context,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "hash": dataset_hash,
        }
        mlflow.log_dict(dataset_info, f"datasets/{name}_metadata.json")
        
        return dataset_hash
    
    def _get_git_commit(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"]
            ).decode().strip()
        except Exception:
            return "unknown"
    
    def _get_git_branch(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"]
            ).decode().strip()
        except Exception:
            return "unknown"


def train_and_track(config: dict):
    tracker = ExperimentTracker(
        experiment_name="order-propensity-model",
        tags={"team": "ml-platform", "project": "recommendations"}
    )
    
    with tracker.start_run(run_name=f"xgb-{config['max_depth']}-{config['learning_rate']}"):
        
        # ── Log configuration ─────────────────────────────
        mlflow.log_params({
            # Model hyperparameters
            "model_type": "xgboost",
            "max_depth": config["max_depth"],
            "learning_rate": config["learning_rate"],
            "n_estimators": config["n_estimators"],
            "subsample": config["subsample"],
            "colsample_bytree": config["colsample_bytree"],
            
            # Training config
            "train_size": config["train_size"],
            "random_seed": config["random_seed"],
            "early_stopping_rounds": config.get("early_stopping_rounds", 50),
        })
        
        # Set environment tags
        mlflow.set_tags({
            "framework": "xgboost",
            "task": "binary_classification",
            "feature_set": config["feature_set_version"],
        })
        
        # ── Load and log data ─────────────────────────────
        X_train, X_val, y_train, y_val = load_data(config)
        tracker.log_dataset(pd.DataFrame(X_train), "train")
        tracker.log_dataset(pd.DataFrame(X_val), "validation")
        
        # ── Train with epoch logging ──────────────────────
        import xgboost as xgb
        
        evals_result = {}
        model = xgb.XGBClassifier(
            max_depth=config["max_depth"],
            learning_rate=config["learning_rate"],
            n_estimators=config["n_estimators"],
            random_state=config["random_seed"],
            eval_metric=["logloss", "auc"],
            callbacks=[
                xgb.callback.EarlyStopping(
                    rounds=config.get("early_stopping_rounds", 50)
                )
            ]
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_val, y_val)],
            evals_result=evals_result,
            verbose=False
        )
        
        # Log training curve (per-epoch metrics)
        for epoch, (train_loss, val_loss) in enumerate(zip(
            evals_result["validation_0"]["logloss"],
            evals_result["validation_1"]["logloss"]
        )):
            mlflow.log_metrics({
                "train_logloss": train_loss,
                "val_logloss": val_loss,
            }, step=epoch)
        
        # ── Log evaluation metrics ────────────────────────
        from sklearn.metrics import (
            roc_auc_score, average_precision_score,
            f1_score, precision_score, recall_score
        )
        
        y_prob = model.predict_proba(X_val)[:, 1]
        y_pred = (y_prob > 0.5).astype(int)
        
        metrics = {
            "val_auc": roc_auc_score(y_val, y_prob),
            "val_avg_precision": average_precision_score(y_val, y_prob),
            "val_f1": f1_score(y_val, y_pred),
            "val_precision": precision_score(y_val, y_pred),
            "val_recall": recall_score(y_val, y_pred),
            "best_iteration": model.best_iteration,
        }
        mlflow.log_metrics(metrics)
        
        # ── Log artifacts ────────────────────────────────
        # Feature importance
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 8))
        xgb.plot_importance(model, ax=ax, max_num_features=20)
        mlflow.log_figure(fig, "feature_importance.png")
        plt.close()
        
        # Model signature (input/output schema)
        from mlflow.models.signature import infer_signature
        signature = infer_signature(X_val, y_prob)
        
        # Log model
        mlflow.xgboost.log_model(
            model,
            "model",
            signature=signature,
            input_example=X_val[:5],
            registered_model_name="order-propensity"  # Auto-register
        )
        
        # Requirements file for reproducibility
        mlflow.log_artifact("requirements.txt")
        
        return mlflow.active_run().info.run_id, metrics


# Model registry operations
def promote_to_staging(run_id: str, model_name: str = "order-propensity"):
    client = mlflow.tracking.MlflowClient()
    
    # Find the model version from the run
    model_uri = f"runs:/{run_id}/model"
    result = mlflow.register_model(model_uri, model_name)
    
    # Transition to staging after validation
    client.transition_model_version_stage(
        name=model_name,
        version=result.version,
        stage="Staging",
        archive_existing_versions=False
    )
    
    # Add description with validation metrics
    run = mlflow.get_run(run_id)
    metrics = run.data.metrics
    
    client.update_model_version(
        name=model_name,
        version=result.version,
        description=(
            f"AUC: {metrics.get('val_auc', 0):.4f} | "
            f"F1: {metrics.get('val_f1', 0):.4f} | "
            f"Promoted by: {os.environ.get('CI_USER', 'unknown')}"
        )
    )
    
    return result.version


def compare_runs(experiment_name: str, metric: str = "val_auc", n_top: int = 5):
    """Find the best runs for a given metric."""
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="status = 'FINISHED'",
        order_by=[f"metrics.{metric} DESC"],
        max_results=n_top
    )
    
    comparison = []
    for run in runs:
        comparison.append({
            "run_id": run.info.run_id[:8],
            "name": run.info.run_name,
            metric: run.data.metrics.get(metric),
            "params": {k: v for k, v in run.data.params.items() 
                      if k in ["max_depth", "learning_rate", "n_estimators"]},
        })
    
    return pd.DataFrame(comparison)
```

### Weights & Biases Alternative

```python
# train_wandb.py
import wandb
import numpy as np

def train_with_wandb(config: dict):
    # Initialize run
    run = wandb.init(
        project="order-propensity",
        entity="ml-team",
        name=f"xgb-{config['max_depth']}-lr{config['learning_rate']}",
        config=config,
        tags=["xgboost", "binary-classification"],
        notes="Experimenting with deeper trees after feature engineering v3"
    )
    
    # Log dataset as artifact
    dataset_artifact = wandb.Artifact(
        name="training-data",
        type="dataset",
        description="Order propensity training dataset v2.3"
    )
    dataset_artifact.add_file("data/train.parquet")
    run.log_artifact(dataset_artifact)
    
    # Training loop with logging
    for epoch in range(config["n_estimators"]):
        train_metrics = train_one_epoch(epoch)
        
        wandb.log({
            "epoch": epoch,
            "train/loss": train_metrics["loss"],
            "train/auc": train_metrics["auc"],
            "val/loss": train_metrics["val_loss"],
            "val/auc": train_metrics["val_auc"],
            "learning_rate": get_lr(epoch),
        })
    
    # Log final model
    model_artifact = wandb.Artifact(
        name="order-propensity-model",
        type="model",
        metadata={"val_auc": final_auc, "framework": "xgboost"}
    )
    model_artifact.add_file("model.xgb")
    run.log_artifact(model_artifact)
    
    # Finish run
    wandb.finish()
```

### Experiment Config Management

```yaml
# configs/experiment_001.yaml — version-controlled experiment config
name: order-propensity-v2
experiment: order-propensity
created_at: 2024-01-15
created_by: ml-team@example.com

model:
  type: xgboost
  hyperparameters:
    max_depth: 6
    learning_rate: 0.05
    n_estimators: 500
    subsample: 0.8
    colsample_bytree: 0.8
    min_child_weight: 1
    gamma: 0.1

data:
  feature_set_version: v3.2
  train_start_date: "2023-01-01"
  train_end_date: "2023-12-01"
  val_start_date: "2023-12-01"
  val_end_date: "2024-01-01"
  target_column: will_purchase_30d
  
training:
  random_seed: 42
  early_stopping_rounds: 50
  train_size: 0.8
  
evaluation:
  primary_metric: val_auc
  thresholds:
    val_auc: 0.75
    val_f1: 0.60
```

## Rules

- **Log before training, not after** — log params at run start so failed runs are still recorded.
- **Version datasets, not just models** — log dataset hash for exact reproducibility.
- **Log git commit + branch** — always know which code produced which run.
- **Fix random seeds** — set `numpy.random.seed`, `torch.manual_seed`, `random.seed`.
- **Log training curves per epoch** — not just final metrics; identify overfitting early.
- **Use model registry stages** — None → Staging → Production, never push direct to Production.
- **Archive superseded production models** — don't delete, archive for rollback.
- **Store `requirements.txt` as artifact** — reproduce exact environment months later.
- **Meaningful run names** — `xgb-depth6-lr0.05` beats `run-20240115-142301`.
- **Compare before promoting** — always compare candidate vs. current production on held-out test set.
