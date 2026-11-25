---
name: ml-experiment-tracking
version: 1.0.0
description: Set up reproducible experiment tracking for runs, params, metrics, artifacts, and seeds so any result can be regenerated.
author: matrixx0070
tags: [ml, tracking, reproducibility, mlflow, seeds]
capabilities: []
---

## When to use

Use this at the start of an ML project or the moment you run a second experiment, so every run is logged with enough context (code, data, params, seeds, artifacts) to reproduce or compare it later.

**Not for:** LLM prompt/version logging or eval-run comparison (see `ai-eval-harness`). Not for BI/report versioning or dashboard change history (see `data-build-dashboard`).

## Method

1. Choose a tracker: MLflow / Weights & Biases / a structured runs table. Any is fine; the discipline matters more than the tool.
2. Define a run as one training execution. Log at minimum: git commit, data version/hash, all hyperparameters, metrics, and the environment (package versions).
3. Set and log ALL seeds — numpy, framework, data-shuffle, CV split seed. Decision point: nondeterministic GPU ops → log the flag and accept bounded variance, or force deterministic mode.
4. Version the data, not just the code: a snapshot path, hash, or DVC/table pointer. A run irreproducible without its exact data is not tracked.
5. Log artifacts: the fitted model, the feature/transform pipeline, and the evaluation plots/report.
6. Use consistent naming/tags (experiment, dataset, model family) so runs are queryable and comparable.
7. Record the winning run explicitly and link the artifact that will be promoted to `ml-deployment`.

## Example

```python
import mlflow, numpy as np, random
SEED = 42
random.seed(SEED); np.random.seed(SEED)
with mlflow.start_run(run_name="lgbm_churn_v3"):
    mlflow.set_tags({"dataset": "churn_2026q2", "data_hash": DATA_SHA})
    mlflow.log_params({"seed": SEED, "num_leaves": 64, "lr": 0.05})
    model = train(X, y, seed=SEED)
    mlflow.log_metric("pr_auc_cv", 0.63)
    mlflow.sklearn.log_model(pipeline, "model")   # includes transforms
```
Six weeks later the same commit + data_hash + seed reproduces PR-AUC 0.63 exactly.

## Pitfalls

- **Metrics in a notebook cell.** Results vanish on restart. Log to a persistent tracker every run.
- **Unseeded runs.** Score swings look like real gains but are just RNG noise. Seed and log everything.
- **Code versioned, data not.** Same commit + different data = irreproducible. Version both.
- **Model logged without its pipeline.** The transforms drift and serving breaks. Log the full pipeline as one artifact.

## Output format

```
# Experiment Tracking: <name>
TRACKER: <mlflow|wandb|table>
RUN = <one training execution>
LOGGED: git=<sha> | data=<version/hash> | env=<lockfile>
PARAMS: <all hyperparameters>
SEEDS: numpy=<> framework=<> split=<> | deterministic=<y/n>
METRICS: <name: value>
ARTIFACTS: model, pipeline, eval report
PROMOTED RUN: <run_id> -> deployment
```
