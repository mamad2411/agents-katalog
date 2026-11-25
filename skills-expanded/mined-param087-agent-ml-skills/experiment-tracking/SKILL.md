---
name: experiment-tracking
description: Use when running ML experiments that need to be compared, reproduced, or shared. Covers MLflow/Weights & Biases logging, what to track, run organization, and model registry basics.
---

# Experiment Tracking

## Overview

Untracked experiments are unreproducible experiments. If you can't answer "which data + code + hyperparameters produced this metric?", you don't have a result — you have a number. This skill standardizes what to log and how.

## When to use

- Running more than one model/config.
- Comparing experiments or sharing results with a team.
- Preparing a model for promotion to staging/production.

## What to always log

| Category | Examples |
|----------|----------|
| **Params** | hyperparameters, model arch, seed, data version/hash |
| **Metrics** | train/val loss per epoch, final test metrics, timing |
| **Artifacts** | model checkpoint, config file, plots, confusion matrix |
| **Code state** | git commit SHA, dirty flag, dependency lockfile |
| **Environment** | Python/CUDA version, hardware |

## MLflow pattern

```python
import mlflow, subprocess

mlflow.set_experiment("churn-classifier")
sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

with mlflow.start_run(run_name="hgb-baseline"):
    mlflow.log_params({"model": "HGB", "lr": 0.1, "seed": 42, "data_v": "2026-06-01"})
    mlflow.set_tag("git_sha", sha)
    for epoch, loss in enumerate(history):
        mlflow.log_metric("val_loss", loss, step=epoch)
    mlflow.log_metric("test_auc", test_auc)
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_artifact("confusion_matrix.png")
```

## Weights & Biases pattern

```python
import wandb
wandb.init(project="churn", config={"lr": 3e-4, "seed": 42})
for epoch in range(epochs):
    wandb.log({"val_loss": val_loss, "epoch": epoch})
wandb.log({"test_auc": test_auc})
wandb.finish()
```

## Run hygiene

- **One run = one config.** Don't mutate params mid-run.
- **Name runs meaningfully** (`hgb-lr0.1-seed42`), and tag by experiment goal.
- **Log the data version**, not just the code — data drift silently invalidates comparisons.
- Promote a vetted run to the **model registry** with a stage (`Staging`/`Production`) rather than copying files around.

## Pitfalls

- Logging only the final metric (no per-epoch curve) — you can't diagnose overfitting later.
- Forgetting the git SHA — "best model" becomes unreproducible.
- Tracking metrics but not the **exact dataset** used.
- Comparing runs with different seeds and calling a 0.1% delta "improvement" — see the `model-evaluation` skill on significance.

## Hand-off

A queryable run history + registered model that hyperparameter-tuning compares against and model-serving deploys from.
