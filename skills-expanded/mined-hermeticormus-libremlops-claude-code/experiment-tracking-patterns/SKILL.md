---
name: "experiment-tracking-patterns"
description: "Experiment tracking patterns with code: MLflow manual logging and autologging, W&B sweeps with Bayesian search, Optuna with MLflow, run queries and comparison, and a team tagging strategy. Use when instrumenting or organizing ML experiments."
---

# Experiment Tracking Patterns

Expert patterns for MLflow, W&B, Optuna hyperparameter search, and experiment organization at scale.

## Pattern 1: MLflow Manual Logging

Complete MLflow run with params, metrics, artifacts, and model signature.

```python
import mlflow
import mlflow.pytorch
from mlflow.models import infer_signature
import torch
import numpy as np

# Set tracking URI (local or server)
mlflow.set_tracking_uri("http://mlflow-server:5000")  # or "mlite:///mlflow.db" for local SQLite

mlflow.set_experiment("sentiment-classification")

with mlflow.start_run(run_name="bert-base-lr3e4-ep10") as run:
    # Log hyperparameters (immutable)
    mlflow.log_params({
        "model_name": "bert-base-uncased",
        "learning_rate": 3e-4,
        "batch_size": 32,
        "epochs": 10,
        "warmup_ratio": 0.06,
        "weight_decay": 0.01,
        "max_seq_len": 512,
        "optimizer": "adamw",
        "scheduler": "linear_warmup",
    })

    # Log tags for filtering
    mlflow.set_tags({
        "model_family": "bert",
        "task": "sentiment",
        "status": "ablation",
        "dataset_version": "amazon-v2",
        "git_commit": get_git_commit(),
    })

    # Training loop with step-level metrics
    for epoch in range(10):
        train_loss = train_epoch(model, train_loader, optimizer)
        val_metrics = evaluate(model, val_loader)

        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_metrics["loss"],
            "val_accuracy": val_metrics["accuracy"],
            "val_f1_macro": val_metrics["f1_macro"],
            "val_f1_weighted": val_metrics["f1_weighted"],
        }, step=epoch)

    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("classification_report.txt")

    # Log model with signature
    X_sample = next(iter(val_loader))["input_ids"][:5].numpy()
    y_sample = model(torch.tensor(X_sample)).detach().numpy()
    signature = infer_signature(X_sample, y_sample)

    mlflow.pytorch.log_model(
        model,
        "model",
        signature=signature,
        input_example=X_sample[:2],
        registered_model_name="sentiment-bert"
    )

    print(f"Run ID: {run.info.run_id}")
```

## Pattern 2: MLflow Autologging

Minimal instrumentation — autolog handles params, metrics, and model.

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

mlflow.set_experiment("gbm-tabular")
mlflow.sklearn.autolog(log_input_examples=True, log_model_signatures=True)

with mlflow.start_run(run_name="gbm-baseline"):
    # Autolog captures: estimator params, CV metrics, feature importances, model artifact
    model = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
    )
    model.fit(X_train, y_train)
    # ^ autolog logs everything from fit()

    # Add manual tags on top of autolog
    mlflow.set_tag("feature_set", "v3_with_embeddings")
    mlflow.set_tag("status", "baseline")
```

## Pattern 3: W&B Sweeps with Bayesian Search

Define sweep configuration and run distributed hyperparameter search.

```yaml
# sweep_config.yaml
program: train.py
method: bayes
metric:
  goal: maximize
  name: val/f1_macro
parameters:
  learning_rate:
    distribution: log_uniform_values
    min: 1e-5
    max: 1e-3
  batch_size:
    values: [16, 32, 64]
  weight_decay:
    distribution: uniform
    min: 0.0
    max: 0.1
  warmup_ratio:
    values: [0.0, 0.06, 0.1]
  dropout:
    distribution: uniform
    min: 0.0
    max: 0.3
early_terminate:
  type: hyperband
  min_iter: 3
  eta: 3
```

```python
import wandb

# Create sweep
sweep_id = wandb.sweep(
    sweep=yaml.safe_load(open("sweep_config.yaml")),
    project="sentiment-sweep"
)

def train_with_wandb():
    with wandb.init() as run:
        config = wandb.config

        model = build_model(dropout=config.dropout)
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )

        for epoch in range(10):
            metrics = train_and_eval(model, optimizer, epoch)
            wandb.log(metrics, step=epoch)

            # Report for early termination
            run.log({"val/f1_macro": metrics["val/f1_macro"]})

# Run agent (can run multiple agents in parallel)
wandb.agent(sweep_id, function=train_with_wandb, count=50)

# View results
api = wandb.Api()
sweep = api.sweep(f"my-entity/sentiment-sweep/{sweep_id}")
best_run = sweep.best_run()
print(f"Best val/f1_macro: {best_run.summary['val/f1_macro']:.4f}")
print(f"Best config: {dict(best_run.config)}")
```

## Pattern 4: Optuna with MLflow Integration

Hyperparameter optimization with Optuna, logging each trial to MLflow.

```python
import optuna
import mlflow

mlflow.set_experiment("optuna-hpo")

def objective(trial: optuna.Trial) -> float:
    with mlflow.start_run(nested=True):
        params = {
            "lr": trial.suggest_float("lr", 1e-5, 1e-3, log=True),
            "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64]),
            "weight_decay": trial.suggest_float("weight_decay", 1e-4, 1e-1, log=True),
            "hidden_size": trial.suggest_categorical("hidden_size", [128, 256, 512]),
            "num_layers": trial.suggest_int("num_layers", 2, 6),
        }
        mlflow.log_params(params)

        model = build_model(**params)
        val_f1 = train_and_evaluate(model, params)

        mlflow.log_metric("val_f1", val_f1)
        mlflow.set_tag("trial_number", trial.number)

        # Pruning: report intermediate values and check if trial should stop
        trial.report(val_f1, step=0)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

        return val_f1

with mlflow.start_run(run_name="optuna-study"):
    study = optuna.create_study(
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner(n_warmup_steps=5)
    )
    study.optimize(objective, n_trials=100, n_jobs=4)

    mlflow.log_params({
        f"best_{k}": v for k, v in study.best_params.items()
    })
    mlflow.log_metric("best_val_f1", study.best_value)

    # Optuna visualization
    fig = optuna.visualization.plot_param_importances(study)
    fig.write_image("param_importances.png")
    mlflow.log_artifact("param_importances.png")
```

## Pattern 5: Experiment Query and Comparison

Programmatically find and compare experiments after many runs.

```python
import mlflow
import pandas as pd

# Query MLflow runs
runs = mlflow.search_runs(
    experiment_names=["sentiment-classification"],
    filter_string="metrics.val_f1_macro > 0.85 AND params.model_name = 'bert-base-uncased'",
    order_by=["metrics.val_f1_macro DESC"],
    max_results=20
)

# Runs is a DataFrame with params.*, metrics.*, tags.* columns
print(runs[["run_id", "params.learning_rate", "params.batch_size",
            "metrics.val_f1_macro", "metrics.val_loss", "tags.status"]])

# Find best run
best_run = runs.iloc[0]
print(f"Best run: {best_run['run_id']}")
print(f"Best F1: {best_run['metrics.val_f1_macro']:.4f}")

# Load best model
model = mlflow.pytorch.load_model(f"runs:/{best_run['run_id']}/model")

# W&B equivalent
import wandb
api = wandb.Api()
runs = api.runs(
    "my-entity/sentiment-classification",
    filters={"$and": [
        {"summary_metrics.val/f1_macro": {"$gt": 0.85}},
        {"config.model_name": "bert-base-uncased"},
        {"state": "finished"}
    ]},
    order="-summary_metrics.val/f1_macro"
)
for run in runs[:5]:
    print(f"{run.name}: {run.summary['val/f1_macro']:.4f} | lr={run.config['learning_rate']}")
```

## Pattern 6: Team Tagging Strategy

Consistent tagging enables filtering across hundreds of experiments.

```python
# Define tagging taxonomy as constants
TAGS = {
    # Required tags (enforced in training wrapper)
    "model_family": "bert|roberta|gpt|t5|custom",
    "task": "sentiment|ner|classification|generation",
    "status": "exploration|ablation|baseline|production-candidate|deprecated",
    "dataset_version": "v1|v2|...",

    # Tracking tags (auto-populated)
    "git_commit": "sha",
    "experimenter": "team member name",

    # Result tags (set after evaluation)
    "promoted_to_registry": "true|false",
}

def start_tracked_run(config: dict, run_name: str, tags: dict = None):
    """Wrapper that enforces required tags."""
    required = {"model_family", "task", "status", "dataset_version"}
    provided = set(tags.keys()) if tags else set()
    missing = required - provided
    if missing:
        raise ValueError(f"Missing required tags: {missing}")

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params(config)
        mlflow.set_tags({
            **tags,
            "git_commit": get_git_commit(),
            "experimenter": os.environ.get("USER", "unknown"),
        })
        return run
```

## Anti-Patterns

### Anti-Pattern 1: Logging Only the Final Metric
Log step-level metrics. Loss curves reveal training stability, overfitting onset, and learning rate issues. A final metric alone doesn't tell you if training was healthy.

### Anti-Pattern 2: Unnamed Runs
MLflow auto-generates run IDs like `adf3b2c1...`. Without `run_name` and tags, experiments are unqueryable after 20+ runs. Name every run and tag every experiment.

### Anti-Pattern 3: Deleting Failed Runs
Failed runs contain information: the hyperparameter region that doesn't work. Archive, don't delete. Tag with `status=failed` and add a note.

### Anti-Pattern 4: Not Logging the Dataset Version
A run is only reproducible if you know the exact dataset it used. Always log `dataset_version`, DVC commit, or data hash as a tag.

### Anti-Pattern 5: Running HPO Without a Baseline
If you don't know your baseline metric, you can't know if HPO improved anything. Always establish a baseline run before sweeping.
