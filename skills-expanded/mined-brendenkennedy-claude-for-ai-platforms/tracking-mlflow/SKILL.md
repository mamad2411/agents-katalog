---
name: tracking-mlflow
description: >
  Recording experiments with MLflow — every train/eval run becomes a tracked, comparable,
  reproducible record. Carries: `mlflow.set_experiment` + `start_run`, `log_param(s)` for the
  resolved hyperparams, `log_metric(..., step=)` for curves, `log_artifact(s)` for
  checkpoints/plots/the composed config, `set_tag`, `mlflow.pytorch.autolog()`, the tracking URI
  (MLflow 3.x needs a database URI, not `./mlruns`), and comparing runs in `mlflow ui`. Load when a
  train/eval loop needs to record what it did, when a past result can't be found, or when setting up
  tracking on a new box; `training`/`evaluation` call this to log; pair with `config-hydra` to log
  the composed config. Triggers: mlflow, experiment tracking, track this run, log metrics,
  log_param, log_metric, log_artifact, start_run, autolog, mlruns, mlflow ui, MLFLOW_TRACKING_URI,
  compare runs, where did that result go, record hyperparameters.
---

# tracking-mlflow — recording experiments so they're comparable & reproducible

**Pinned:** mlflow — unpinned · authored against 3.x · run `/skill-update tracking-mlflow` once the dep is installed

> On-demand: load this before adding tracking to a train/eval loop, or when you can't reconstruct what a
> past run did. A run is only worth logging if it's **reproducible** — the resolved config + code version
> must be in it (see the closing rule). Never hand-roll a CSV logger where a run belongs.

## When this applies
Instrumenting a train or eval loop to record params/metrics/artifacts, organizing runs into experiments,
pointing at a local vs remote tracking store, or comparing runs to pick a winner. The `training` and
`evaluation` skills defer here for the *how* of logging; this skill owns it.

## Open a run
Set the experiment (a named bucket of runs) once, then open a run as a context manager so it closes and
flushes on exit — including on exception:

```python
import mlflow

mlflow.set_experiment("<PLACEHOLDER: experiment name, e.g. detector-baselines>")
with mlflow.start_run(run_name="<PLACEHOLDER: short human run name>") as run:
    ...  # everything below logs into this run
```
- **Name runs meaningfully** — a short, scannable handle (`r50-fpn-lr3e-4`, `sweep-trial-017`), not the
  default random slug. The `mlflow ui` run table is only as readable as your names.
- **One experiment per line of investigation** (a model family, a dataset, a paper); trials/sweeps are the
  runs inside it. Keep the taxonomy shallow.

## What to log (and when)
- **Params — the resolved config, once, at run start.** Hyperparameters and paths as they were *actually*
  used (post-composition, post-override), not the defaults. `mlflow.log_params(cfg_dict)` for a flat dict,
  `mlflow.log_param(k, v)` one at a time. Params are immutable per run — log the final values.
- **Metrics — per step, with `step=`.** `mlflow.log_metric("train/loss", loss, step=global_step)` and
  `mlflow.log_metric("val/mAP", score, step=epoch)`. Passing `step=` is what makes MLflow draw a curve
  instead of a single point — always pass it. Namespace with `train/` `val/` `test/` prefixes.
- **Artifacts — files worth keeping.** `mlflow.log_artifact(path)` (single) / `log_artifacts(dir)` (tree):
  checkpoints, PR/confusion-matrix plots, sample predictions, and **the composed config file**. Group with
  `artifact_path=` (e.g. `"checkpoints"`, `"plots"`).
- **Tags — searchable run metadata.** `mlflow.set_tag("stage", "smoke")`, `set_tag("dataset_version", ...)`
  — anything you'll later filter the run table on.

## Autolog for PyTorch (the fast path)
`mlflow.pytorch.autolog()` before the loop captures params, metrics, and the model automatically for
PyTorch Lightning trainers. Call it once, then still **explicitly log the resolved config + git SHA**
(autolog won't capture your Hydra composition or code version) and any custom metrics it doesn't know about.
Autolog and manual `log_*` coexist — autolog for the boilerplate, manual for what's project-specific.

## Where runs are stored (tracking URI)
> **The `./mlruns/` file store is DEAD on MLflow 3.x.** Every tutorial says runs land in `./mlruns/` by
> default. On 3.x that raises `MlflowException` on the **first** `set_experiment` call: *"The filesystem
> tracking backend is in maintenance mode."* Don't burn an hour on this, and don't reach for the
> `MLFLOW_ALLOW_FILE_STORE=true` escape hatch — it only forces the corpse to move. Use a database backend.

- **Local default: `MLFLOW_TRACKING_URI=sqlite:///mlflow.db`** — a local SQLite file, no server to run, and
  a real DB backend, so 3.x is happy. Set it in `.env`.
- **Where artifacts actually land — the confusing part.** With that URI set in-process (no `mlflow server`),
  *metadata* goes to `mlflow.db` but *artifacts* still go to **`./mlruns/<exp_id>/<run_id>/artifacts/`**.
  So `mlruns/` reappears on disk even though the file-store *backend* is gone — it is now just an artifact
  directory. (`./mlartifacts/` is the default only under a standalone `mlflow server`.) Gitignore
  `mlflow.db`, `mlruns/`, and `mlartifacts/`; version artifacts via `data-dvc` if they must be shared.
- **Remote server:** point at a shared tracking server (`http://<host>:5000`); the code does not change.
- Read the URI from the config system, **not** `os.environ` mid-logic — per the *config over constants*
  always-on convention (see `config-hydra`). The config interpolates the env var in one place:
  ```python
  mlflow.set_tracking_uri(cfg.tracking.uri)   # conf/config.yaml: uri: ${oc.env:MLFLOW_TRACKING_URI}
  ```

## Model Registry — from "a good run" to "the model we serve"
The registry is the named, versioned lineage layer on top of runs — use it when a model outlives
its experiment (gets deployed, shared, or compared across time), not for every checkpoint:
- **Register from a run:** `mlflow.register_model(f"runs:/{run.info.run_id}/model", "<model name>")`,
  or log-and-register in one step via `log_model(..., registered_model_name=...)`. Each register
  bumps an auto-incremented **version**; the link back to the source run (and thus its config + git
  SHA) is the provenance chain — never register a model whose run lacks them.
- **Aliases, not stages.** Mutable stages (`Staging`/`Production`) are deprecated; use **aliases**:
  `MlflowClient().set_registered_model_alias("<name>", "champion", version)` and load with
  `mlflow.pyfunc.load_model("models:/<name>@champion")`. Promotion = moving the alias — which is a
  governed act: consult `governance` → `model-governance` (model card, eval evidence) before moving
  `@champion`, and record the decision.
- **Division of labor with DVC:** the registry tracks *which model is which* (lineage, aliases);
  `data-dvc` versions *bytes* (raw checkpoints, datasets). A served model lives in the registry;
  its training artifacts stay DVC-tracked.

## Compare runs
- **`mlflow ui --backend-store-uri sqlite:///mlflow.db`** (add `--host`/`--port` as needed) — opens the UI.
  A bare `mlflow ui` assumes the dead file store and shows you nothing. Then:
  sort the run table by a metric, multi-select runs to overlay metric curves, diff their params.
- Programmatic: `mlflow.search_runs(experiment_names=[...])` returns a DataFrame for scripted comparison
  and to feed the `eval-analyst` agent's error analysis.

## Gotcha
A run without the **resolved config + code version (git SHA)** isn't reproducible — it's a number you can't
regenerate. Log both every run: the composed config as an artifact (from `config-hydra`) and the SHA as a
param/tag (`mlflow.set_tag("git_sha", <sha>)`; note a dirty tree). And **never log secrets or raw data** —
tracking stores are broadly readable; params/tags/artifacts are the wrong place for credentials, PII, or
dataset contents. This is the reproducibility always-on convention made concrete; the handling rules for
sensitive data live in the `governance` skill (`.claude/memory/policy/`).
