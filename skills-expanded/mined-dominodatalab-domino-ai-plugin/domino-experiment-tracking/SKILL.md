---
name: domino-experiment-tracking
description: Track traditional ML experiments in Domino's MLflow-based Experiment Manager. Covers unique experiment naming, auto-logging for scikit-learn, TensorFlow, PyTorch, XGBoost and LightGBM, manual logging of params, metrics and artifacts, Domino context tags, large-artifact multipart upload, comparing and exporting runs, and the Domino Model Registry (register from a run or by API, versions, aliases and tags, model cards, discoverability). Use when training ML models in Domino, logging metrics and parameters, comparing runs, or registering and versioning models. For GenAI tracing use domino-genai-tracing; to scaffold a helper module use domino-experiment-setup.
compatibility: Domino 6.3 and Domino Cloud. Runs in a Domino Workspace or Job where MLFLOW_TRACKING_URI is preconfigured; registry REST routes need DOMINO_API_HOST with DOMINO_API_PROXY or the localhost:8899 access token in a run, a Personal Access Token outside.
---

# Domino experiment tracking

Applies to Domino 6.3 and Domino Cloud.

Domino's Experiment Manager is MLflow Tracking with Domino's storage, access control and UI on top. In a Workspace or Job the `mlflow` package is installed (Domino Standard Environments) and `MLFLOW_TRACKING_URI` already points at Domino, so plain MLflow code works without configuration.

## What is Domino-specific

- **Experiments are created in code, not in the UI.** `mlflow.set_experiment(name)` creates it; it appears under **Experiments** only after the first run is logged.
- **Experiment names are unique across the whole deployment**, not per project. Always suffix with something unique, for example the project and the user: `f"churn-{os.environ['DOMINO_PROJECT_NAME']}-{os.environ['DOMINO_STARTING_USERNAME']}"`.
- **Access follows the project**: visibility (Private or Searchable; Domino 6.3 also has Public) and collaborator roles decide who sees runs. Results Consumers can view; Contributors and the owner can log and update; archiving another user's run needs the owner.
- Runs started from a Job are the reproducible ones (code commit, environment, hardware tier recorded). Workspace runs show the file name but are not re-versioned as you edit; finish in a Job.
- Give runs a `run_name`; otherwise MLflow generates one like `gifted-slug-123`.
- You cannot stop a run from the UI; call `mlflow.end_run()` in the Workspace or Job. Deleting a parent run does not delete its children.
- Compare up to four runs (select, **Compare**); export an experiment to CSV or a comparison to PDF from the three-dot menu.
- The Model Registry is Domino's (MLflow-backed, with model cards, role-based access and discoverability); R models are not supported.

## Reference files

| File | Use when |
|------|----------|
| [MLFLOW-BASICS.md](./MLFLOW-BASICS.md) | Auto-logging, manual logging, artifacts, tags, nested runs |
| [COMPARING-RUNS.md](./COMPARING-RUNS.md) | Searching, comparing, exporting and loading runs programmatically |
| [MODEL-REGISTRY.md](./MODEL-REGISTRY.md) | Registering, versioning with aliases and tags, model cards, registry REST routes |

## Quick start

```python
import os
import mlflow
from sklearn.ensemble import RandomForestClassifier

experiment = f"iris-{os.environ.get('DOMINO_PROJECT_NAME', 'local')}-{os.environ.get('DOMINO_STARTING_USERNAME', 'dev')}"
mlflow.set_experiment(experiment)
mlflow.autolog()                                   # sklearn, tensorflow, pytorch, xgboost, lightgbm ...

with mlflow.start_run(run_name="rf-baseline"):
    mlflow.set_tags({
        "domino.project": os.environ.get("DOMINO_PROJECT_NAME", ""),
        "domino.run_id": os.environ.get("DOMINO_RUN_ID", ""),
        "domino.hardware_tier": os.environ.get("DOMINO_HARDWARE_TIER_ID", ""),
    })
    model = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)
    mlflow.log_metric("test_accuracy", model.score(X_test, y_test))
```

Framework auto-logging: `mlflow.sklearn.autolog()`, `mlflow.tensorflow.autolog()`, `mlflow.pytorch.autolog()`, `mlflow.xgboost.autolog()`, `mlflow.lightgbm.autolog()`, or `mlflow.autolog()` for all.

## Domino variables worth tagging

| Variable | Value |
|----------|-------|
| `DOMINO_STARTING_USERNAME` | User who started the run |
| `DOMINO_PROJECT_NAME`, `DOMINO_PROJECT_OWNER`, `DOMINO_PROJECT_ID` | Project identity |
| `DOMINO_RUN_ID`, `DOMINO_RUN_NUMBER` | The Domino execution |
| `DOMINO_HARDWARE_TIER_ID` | Hardware tier id |
| `MLFLOW_TRACKING_URI` | Preconfigured; do not override |

Full list: https://docs.domino.ai/cloud/reference/environment-variables

## Large artifacts

Multi-GB artifacts (LLM weights, checkpoints) upload straight to blob storage with `MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD=true` (AWS and GCP deployments): [MLFLOW-BASICS.md](./MLFLOW-BASICS.md#large-artifact-upload).

## Registering a model

From a run in the UI: **Experiments** > run > **Register model from run**. In code: `mlflow.sklearn.log_model(model, "model", registered_model_name="churn-rf")` or `mlflow.register_model("runs:/<run_id>/model", "churn-rf")`. Promote with aliases (`client.set_registered_model_alias(name, "champion", version)`), not the deprecated MLflow stages. Details, Domino registry routes (`/api/registeredmodels/...`), model cards and discoverability: [MODEL-REGISTRY.md](./MODEL-REGISTRY.md). To serve a registered version as an endpoint see `domino-model-endpoints`.

## Documentation

- https://docs.domino.ai/cloud/platform-capabilities/features/development/track-monitor
- https://docs.domino.ai/cloud/platform-capabilities/features/models/register-and-govern/model-registry
