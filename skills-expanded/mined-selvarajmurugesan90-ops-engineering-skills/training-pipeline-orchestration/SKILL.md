---
name: training-pipeline-orchestration
description: >
  Guides designing reproducible, orchestrated ML training pipelines (DAGs)
  covering data ingestion, feature computation, training, evaluation, and
  conditional registration/promotion steps. Use when the user asks to
  "orchestrate a training pipeline", set up Airflow/Kubeflow Pipelines/Argo
  Workflows/Vertex AI Pipelines/SageMaker Pipelines/Metaflow, schedule
  retraining jobs, add pipeline gates before model registration, or make a
  training run reproducible.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Training Pipeline Orchestration

## Purpose

Ad hoc "run a notebook, save a pickle" training does not scale past a single
model or a single person, and it cannot be safely automated for recurring
retraining. Training pipeline orchestration turns the sequence of data
ingestion → validation → feature computation → training → evaluation →
conditional registration into an explicit, versioned DAG that runs
identically whether triggered by a schedule, an event (new data landed), or a
human. This matters operationally because it is what makes retraining
repeatable, auditable, resumable after failure, and safe to gate — instead of
a fragile script that only the original author can rerun correctly.

## When to use

- The user wants to design or implement an ML training pipeline as a DAG with
  discrete, dependency-ordered steps.
- The user is choosing or configuring an orchestrator: Airflow ≥ 2.x, Kubeflow
  Pipelines, Argo Workflows, Vertex AI Pipelines, SageMaker Pipelines,
  Metaflow, or Dagster.
- The user wants scheduled or event-triggered retraining (e.g. "retrain
  weekly" or "retrain when data drift is detected").
- The user needs to add automated gates between pipeline stages (e.g. don't
  register a model unless evaluation metrics clear a threshold).
- The user is debugging a non-reproducible training run or wants to make
  training runs reproducible.
- The user needs to parallelize or checkpoint long-running training jobs
  across a pipeline.

## Prerequisites & environment

- An orchestrator installed and accessible: Airflow ≥ 2.5 (TaskFlow API),
  Kubeflow Pipelines ≥ 2.0 (KFP SDK v2, component-based), Argo Workflows
  ≥ 3.4, or a managed equivalent (Vertex AI Pipelines, SageMaker Pipelines).
- Containerized or environment-pinned execution for each pipeline step so
  "works on my machine" doesn't leak into the DAG (Docker images or a locked
  dependency file per step).
- Access to the data source(s), feature store (see
  [feature-store-design](../feature-store-design/SKILL.md)), and experiment
  tracking backend (see [experiment-tracking](../experiment-tracking/SKILL.md)).
- Compute resources for training steps (GPU/CPU pool, autoscaling cluster, or
  managed training jobs) provisioned or requestable by the pipeline.
- A model registry endpoint to register the pipeline's output (see
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)).
- Deterministic seeding support in the training framework (e.g.
  `torch.manual_seed`, `numpy.random.seed`) if bit-for-bit reproducibility is
  a goal — note full determinism is not always achievable with GPU
  non-determinism in some CUDA kernels; document this limitation rather than
  promising exact reproducibility you can't guarantee.

## Step-by-step guidance

1. **Sketch the DAG stages before writing orchestrator code.** A typical
   supervised-learning retraining DAG:
   ```
   ingest_raw_data
        │
   validate_data_schema  ──(fail)──> alert + halt
        │
   compute_features  (calls feature store materialization)
        │
   split_train_val_test  (time-based split, not random, for temporal data)
        │
   train_model
        │
   evaluate_model
        │
   ├──(metrics below threshold)──> alert + halt, do not register
   │
   register_model_candidate  (registers to "staging", not "production")
        │
   notify_for_promotion_review
   ```
2. **Pin every step's environment.** Each DAG node should run in a container
   or environment with a locked dependency set; do not rely on a shared
   mutable environment across steps that could drift between runs.
3. **Implement the DAG** (Airflow TaskFlow example):
   ```python
   from airflow.decorators import dag, task
   from datetime import datetime

   @dag(schedule="@weekly", start_date=datetime(2026, 1, 1), catchup=False)
   def fraud_scorer_retrain():

       @task
       def validate_data_schema(snapshot_uri: str) -> str:
           # raises on schema mismatch; return validated snapshot_uri
           ...

       @task
       def compute_features(snapshot_uri: str) -> str:
           # materializes feature view, returns training dataset URI
           ...

       @task
       def train_model(dataset_uri: str) -> str:
           # trains, logs to experiment tracker, returns run_id
           ...

       @task
       def evaluate_model(run_id: str) -> dict:
           # returns metrics dict; raises AirflowSkipException if below gate
           ...

       @task
       def register_candidate(run_id: str, metrics: dict) -> str:
           # registers to model registry stage "Staging" only if metrics pass
           ...

       snapshot = validate_data_schema("s3://data-lake/fraud/latest")
       dataset = compute_features(snapshot)
       run_id = train_model(dataset)
       metrics = evaluate_model(run_id)
       register_candidate(run_id, metrics)

   fraud_scorer_retrain()
   ```
4. **Use time-based (not random) splits for temporally ordered data** to
   avoid leaking future information into training — train on data before
   cutoff T, validate/test on data after T, mirroring how the model will
   actually be used in production.
5. **Add explicit gates as pipeline logic, not tribal knowledge**: a failed
   data validation step or a below-threshold evaluation metric should halt
   the DAG and alert, not silently continue to registration.
6. **Log every step's inputs/outputs and parameters** to the experiment
   tracker so a given pipeline run's full lineage (data snapshot → features →
   model → metrics) is reconstructable later (see
   [data-and-model-lineage](../data-and-model-lineage/SKILL.md)).
7. **Make retries idempotent.** A step re-run after a transient failure
   (e.g. a spot instance preemption) should not double-write data or corrupt
   partial outputs — write to a new versioned path/partition per run rather
   than mutating a shared location in place.
8. **Trigger retraining on both schedule and drift signal** where
   appropriate: a weekly schedule as a baseline, plus an event-driven trigger
   from a drift alert (see
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md))
   for faster response to real distribution shifts.
9. **Never let a training pipeline auto-promote to production.** The DAG's
   output should land in a "candidate"/"staging" state; the actual
   production promotion is a separate, explicitly gated step (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)).

## Best practices

- Version the pipeline definition itself (in git) alongside the code it
  orchestrates — a DAG change is a code change and should go through the
  same review process.
- Parameterize DAGs (data window, hyperparameter overrides) rather than
  hardcoding values, so ad hoc runs and scheduled runs share one definition.
- Fail fast and loud on data validation — a schema or distribution check at
  the top of the DAG is far cheaper than discovering bad data after a
  multi-hour training job completes.
- Keep training steps stateless with respect to prior runs unless
  intentionally doing incremental/warm-start training; make warm-starts
  explicit and versioned (which checkpoint was resumed from).
- Emit structured, queryable run metadata (start/end time, git SHA, data
  snapshot, resulting metrics) for every run, not just logs — this is what
  makes "why did last Tuesday's run behave differently" answerable months
  later.
- Set resource requests/limits per step deliberately (especially GPU steps)
  so one runaway training job doesn't starve the rest of the shared cluster.

## Common pitfalls

- **Symptom:** The same training pipeline produces meaningfully different
  metrics run-to-run with identical inputs, and no one can tell if a change
  is a real improvement or noise.
  **Fix:** Fix random seeds across all relevant libraries, pin dependency
  versions per step, and document any known sources of nondeterminism (e.g.
  certain GPU ops); treat a materially non-reproducible pipeline as a bug to
  investigate, not an accepted cost of doing ML.

- **Symptom:** A retraining run uses a random train/test split on
  time-ordered data, and offline metrics look great, but the deployed model
  underperforms because it was implicitly evaluated on data "from the
  future" relative to some training rows.
  **Fix:** Always use time-based splits for temporally ordered data —
  train strictly before a cutoff, validate/test strictly after it — and add
  an automated check that flags any label timestamp in the training split
  that is later than a corresponding timestamp in the validation split.

- **Symptom:** A transient failure mid-pipeline (e.g. spot instance
  preemption during training) is retried, but the retry appends to the same
  output file/table that the failed run partially wrote, producing corrupted
  or duplicated training data on the next attempt.
  **Fix:** Design every step to write to a fresh, uniquely versioned output
  location per run (partitioned by run ID or timestamp) rather than mutating
  a shared path in place, so retries are safe by construction.

- **Symptom:** A pipeline's evaluation step logs a low AUC, but the
  registration step runs anyway and registers (and later gets manually
  promoted) a materially worse model because the gate was only a dashboard
  a human was supposed to check.
  **Fix:** Encode gates as pipeline control flow (raise/skip on failed
  threshold) rather than relying on a human noticing a metric in a
  dashboard after the fact.

## Worked example

A weekly retraining pipeline for `fraud-scorer`, orchestrated in Airflow:

1. **Trigger:** scheduled weekly, plus an event-driven trigger fired by a
   drift alert from
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
   if population stability index on a key feature exceeds 0.25 mid-week.
2. **validate_data_schema:** checks the latest data snapshot against the
   expected schema (column names, types, null-rate bounds); raises and pages
   on-call if a required column is missing.
3. **compute_features:** calls the `driver_stats`-style feature view
   materialization from
   [feature-store-design](../feature-store-design/SKILL.md) to produce a
   point-in-time-correct training dataset at
   `s3://data-lake/fraud/training/run-8841/`.
4. **split_train_val_test:** splits by time — train on data through
   2026-07-13, validate on 2026-07-14 to 2026-07-20 — never a random split,
   since fraud patterns are temporally correlated.
5. **train_model:** trains a gradient-boosted model, logs params/metrics/
   artifacts to the experiment tracker as run `run-8841`.
6. **evaluate_model:** computes AUC = 0.912 on the validation window; gate
   requires AUC ≥ 0.90 and false-positive rate ≤ 2% — both pass.
7. **register_candidate:** registers the model to the registry's `Staging`
   stage as version 14 (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)),
   with full lineage tags (data snapshot, feature view version, git SHA, run
   ID).
8. **notify_for_promotion_review:** posts a summary to the ML team's review
   channel; a human approves promotion to `Production` the next business day
   following the packaging skill's gated promotion process.

## Cross-references

- [feature-store-design](../feature-store-design/SKILL.md)
- [experiment-tracking](../experiment-tracking/SKILL.md)
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
