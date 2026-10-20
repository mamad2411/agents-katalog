---
name: experiment-registry-standard
description: Define and enforce MLflow experiment and registry standards, including mandatory run metadata, naming and tags, promotion criteria, rollback, and a scalable tracking-server architecture. Use for experiment tracking, model registration or promotion, run comparison, artifact logging, reproducibility, MLflow deployment, or policies that prevent models and results from being copied around by hand.
---

# Experiment & Registry Standard

## Purpose
Make every model in the org reproducible and every promotion auditable. An experiment is code + data + model; if any leg is untracked, the run is folklore. This skill turns MLflow from "installed" into a *standard*: a mandatory logging contract per run, naming/tagging conventions, a registry stage workflow with written promotion criteria, and a rollback procedure — on the org's OSS stack (MLflow on Lambda managed K8s, Postgres backend, S3-compatible artifact store; no managed tracking service).

## Core model to hold in your head

### The four MLflow components and their jobs
- **Tracking** — records *runs* (single executions) grouped into *experiments*: params, metrics, tags, artifacts, source version, start/end time. API/UI/CLI.
- **Projects** — packaging format (directory/repo + MLproject descriptor + environment spec: venv, conda, Docker, system) so a run is re-executable anywhere.
- **Models** — model packaging in *flavors* (e.g., `python_function`, framework flavors); the output directory (MLmodel file, conda.yaml, model binary, params/metrics/tags subdirs) is itself the reproducibility record.
- **Model Registry** — central store of *registered model versions* with lineage back to the producing run, stage per version, annotations, and APIs the CI/CD layer listens to.

Two things MLflow does **not** do — say so explicitly: **data version control** (pair with lakeFS/DVC or immutable versioned prefixes in object storage; MLflow only *records* the version you tell it) and **model monitoring** (that's the pipeline's feedback/skew step).

### The logging contract — what every run MUST log
Reject runs missing any of these at review time:

| Field | How | Why |
|---|---|---|
| Hyperparameters (all of them, incl. frozen ones) | `log_params` batch call | Comparability; warm-starting later HPO |
| Objective + secondary metrics | `log_metric` per epoch/step where meaningful | Curves distinguish "converged" from "lucky last epoch" |
| **Dataset path AND version** | `log_params`/tags: `dataset_name`, `dataset_version`, URI | The most-skipped, most-regretted field: same algorithm + different data version = different model. Enables exact retraining |
| Git SHA + entry point | Auto-captured when run from a Project/repo; else tag `git_sha` | Code leg of the triangle |
| Environment | Model flavor's conda.yaml/requirements; container image tag as a tag | Same code, different CUDA/lib = different model |
| Seed(s) | param `seed` | Separates variance from improvement |
| Model artifact | `log_model` (framework flavor) | Registry registration needs it |
| Eval artifacts | confusion matrix, sample outputs, evaluation.json | The promotion gate reads these |

Rules of thumb:
- Prefer **explicit logging over autolog** — autolog coverage is incomplete/experimental for several frameworks in OSS MLflow; treat it as a supplement, and verify what it actually captured.
- Batch-log related params in one `log_params` call (dataset params together, model params together) — simpler to query later.
- **Never log large datasets as artifacts** — artifacts are for models/plots/small eval files; data lives in object storage under its own access control, and the run logs its *reference* (URI + version). Small (~100 MB) research sets in git are tolerable in the lab; the habit doesn't survive contact with privacy/access-control requirements.
- Avoid `log_artifacts(local_dir)` bulk-copies of working directories — you'll copy data you didn't mean to.

### Naming & tagging standard
- **Experiment** = one problem, long-lived: `<team>/<project>/<task>` (e.g., `perception/reranker/train`). Never one experiment per day or per person.
- **Run name** = auto or `<purpose>-<date>`; purpose ∈ {baseline, hpo, ablation, retrain, candidate}.
- **Mandatory tags**: `owner`, `dataset_name`, `dataset_version`, `trigger` (manual|schedule|new-data|drift|commit), `pipeline_run_id` (when launched by Argo/Kubeflow), `git_sha`.
- HPO sweeps: one parent run per sweep, child runs per trial (Ray Tune/Optuna integrations do this — keep it).

### Registry stage workflow

```
None (dev) → Staging → Production → Archived
```

- **Register** from a run: `log_model(..., registered_model_name=X)` or `register_model(run_id, X)` — new name ⇒ version 1; existing name ⇒ next version. Registered model name = deployable unit, versions immutable.
- **Transitions** via `MlflowClient.transition_model_version_stage(name, version, stage)`. Stage-change events drive CI/CD: a listener/webhook triggers the staging deploy or production rollout — humans change *stage*, automation does the plumbing. (Newer MLflow deprecates stages for **aliases + tags**, e.g. alias `champion`; the workflow maps 1:1 — flag which API the installed version uses.)
- **Promotion criteria — written, per model, checked before each transition**:
  - → *Staging*: logging contract complete; eval metrics ≥ threshold on held-out test split; beats or matches current Production version on the same eval set; model loads and serves in a scratch namespace.
  - → *Production*: passed integration/load tests in staging; segment-level checks (no regression on key slices); approver sign-off recorded (description/annotation on the version: what changed, eval evidence link); monitoring baseline captured.
  - → *Archived*: superseded or failed; never delete — archive keeps rollback and audit possible.

### Rollback procedure
Rollback is a registry operation, not a rebuild:
1. Transition the previous good version back to Production (alias flip where supported) — no retraining, no artifact hunt.
2. Archive/demote the bad version with a `rollback_reason` tag; keep it for the postmortem.
3. Redeploy pins the model by **version, never "latest"** — a rollback that races a new registration is a second incident.
4. Open an issue linking the offending run (params, dataset version, eval artifacts) for diagnosis.
5. Verify the monitoring baseline in use matches the rolled-back version, or drift alerts will fire on the wrong reference.

This only works if old versions and their environments remain in the registry/artifact store — hence archive-don't-delete and pinned environment specs. Why registries earn their keep: reproducibility, governance (tags/descriptions/access control), a central deployment source across teams, and version-controlled rollback that minimizes downtime.

### Deployment at scale
Local `mlruns/` directories are for laptops only. Org standard: **remote tracking server** (K8s Deployment, ≥2 replicas behind ingress with SSO/auth) + **backend store** = PostgreSQL (runs/params/metrics/tags) + **artifact store** = S3-compatible object storage bucket with lifecycle rules. All researchers point `MLFLOW_TRACKING_URI` at it — including notebook sessions and Ray/Argo pods (inject via ConfigMap/Secret). The registry is only useful if it's the *single* one.

### Anti-patterns (name them in review)
- **Unlogged data version** — run reproducible in code only; retrain silently differs.
- **Manual model copies** — model.pt passed via shared drive/Slack/scp; provenance gone, registry bypassed.
- **Latest-tag deployments** — serving "whatever registered last"; rollback becomes archaeology.
- **Results in spreadsheets/READMEs** — metrics detached from params and artifacts; comparisons unverifiable.
- **Per-person experiments** — fragmentation kills comparability.
- **Data blobs as artifacts** — bloated artifact store, access control bypassed.
- **Stage change without criteria** — promotion by enthusiasm; the registry degrades to a folder.
- **Local tracking in production pipelines** — pipeline pods logging to their own filesystems; runs vanish with the pod.

## Workflow
1. **Audit current practice.** Sample recent "models in use": can you walk each back to run → params → dataset version → git SHA → environment? Score the gaps against the logging contract and anti-pattern list.
2. **Stand up / verify the shared server** (K8s deployment, Postgres, object-store artifact root, auth). Confirm researchers and pipeline pods share one `MLFLOW_TRACKING_URI`.
3. **Write the org standard doc**: logging contract table, naming/tagging scheme, experiment map for existing projects.
4. **Codify it**: a small internal helper (`init_run(...)` that enforces mandatory tags/params) or a run-linter script CI runs against new experiments; templates for the training entry point.
5. **Define the registry workflow** per model family: promotion criteria checklists, who approves each transition, the CI/CD listener that reacts to stage/alias changes.
6. **Write the rollback runbook** (steps above, with the actual commands) and rehearse it once on a dummy model.
7. **Integrate siblings**: pipeline steps from `ml-pipeline-architect` call the helper; Ray Tune trials log via the MLflow integration (`ray-on-k8s-engineer`); fine-tune evals (`finetuning-strategy-advisor`) log ROUGE/semantic-sim + expert-review verdicts as metrics/tags.
8. **Output**: the standard doc, the helper/linter, registry criteria checklists, rollback runbook, and a migration list of currently-untracked models to backfill or grandfather.

## Guardrails
- No dataset version, no merge: refuse to bless runs that log metrics without `dataset_name`+`dataset_version`.
- MLflow is not a data-versioning tool — always name the companion mechanism (lakeFS/DVC/immutable prefixes) rather than implying MLflow covers it.
- Prefer explicit logging; if autolog is used, verify what it actually captured for that framework version before trusting it.
- Never deploy by "latest" or by stage-string lookup alone — pin model *version* at deploy time.
- Archive, never delete, superseded versions; rollback depends on it.
- Promotion criteria are written artifacts; a transition without its checklist is a finding, not a convenience.
- Keep secrets (DB creds, object-store keys) in K8s Secrets, not tracking URIs pasted into notebooks.

## Suggested effort
Medium — one session for audit + standard doc; a second for the helper/linter and registry criteria; rollback rehearsal ~1 hour. Ongoing: run-linter in CI keeps the standard alive.
