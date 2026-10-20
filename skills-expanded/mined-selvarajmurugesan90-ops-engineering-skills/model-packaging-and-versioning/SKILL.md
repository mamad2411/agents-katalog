---
name: model-packaging-and-versioning
description: >
  Guides packaging trained ML/LLM models into versioned, reproducible artifacts
  (model registry entries, container images, ONNX/TorchScript bundles) with a
  clear semantic versioning and promotion scheme (dev → staging → production).
  Use when the user asks to "register a model", "version a model", "promote a
  model to production", "package a model for serving", set up a model registry
  (MLflow, Vertex AI Model Registry, SageMaker Model Registry, Hugging Face
  Hub), or design a rollback strategy for a deployed model.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Model Packaging And Versioning

## Purpose

A trained model is not production-ready just because it produces good offline
metrics. It becomes production-ready when it is packaged into an immutable,
traceable artifact — with a fixed version identifier, a recorded lineage back
to the code/data/config that produced it, a declared runtime dependency set,
and a documented promotion state (dev/staging/production). Without this
discipline, teams end up unable to answer "which model is live right now,"
"what exactly changed between v12 and v13," or "can we roll back in the next
five minutes." Model packaging and versioning turns a model from a loose file
on someone's laptop into a governed, auditable release artifact that a serving
system, a compliance reviewer, and an on-call engineer can all reason about.

## When to use

- The user asks to set up or query a model registry (MLflow Model Registry,
  SageMaker Model Registry, Vertex AI Model Registry, Hugging Face Hub, a
  custom registry backed by S3/GCS + a metadata DB).
- The user wants to define a versioning scheme for models (semantic versioning
  variants, content-hash based versions, or registry auto-increment) and how
  it maps to git commits, training run IDs, and data snapshots.
- The user is designing a promotion workflow (dev → staging → canary →
  production) with approval gates.
- The user needs to package a model for a specific serving runtime (ONNX,
  TorchScript, TensorFlow SavedModel, a Docker/OCI image, a `.tar.gz` bundle
  for SageMaker/Vertex).
- The user asks how to roll back a bad model deployment quickly and safely.
- The user is building CI/CD for models and wants packaging to be a pipeline
  stage with build provenance and signing.

## Prerequisites & environment

- A model artifact produced by a training run (weights/checkpoint files,
  tokenizer/preprocessing artifacts, and a config file describing
  hyperparameters and framework versions).
- A model registry or artifact store: MLflow ≥ 2.x (Model Registry API),
  SageMaker Model Registry, Vertex AI Model Registry, or an internal registry
  backed by object storage (S3/GCS/Azure Blob) plus a metadata database.
- Framework export tooling as applicable: `torch.jit.trace`/`torch.onnx.export`
  (PyTorch ≥ 2.0), `tf.saved_model.save` (TensorFlow ≥ 2.x), `optimum`/`onnxruntime`
  for transformer export.
- Container tooling (Docker or equivalent OCI builder) if packaging as an
  image for serving.
- CI/CD system with the ability to run build steps, store artifacts, and gate
  promotions (GitHub Actions, GitLab CI, Jenkins, Argo Workflows).
- Read/write permissions to the registry's "staging" and "production" stages
  are usually separated — confirm who/what has production write access before
  designing the promotion workflow.

## Step-by-step guidance

1. **Define the version identifier scheme up front.** Recommended composite
   scheme: `<model-name>-v<major>.<minor>.<patch>+<short-git-sha>.<training-run-id>`.
   - `major`: incompatible input/output schema change (new feature set, new
     label space, new tokenizer).
   - `minor`: retrain on new data or materially changed hyperparameters,
     same schema.
   - `patch`: bug-fix retrain (e.g. fixed a data leak, no architecture change).
   - Example: `fraud-scorer-v2.3.1+a1b2c3d.run-8841`.
2. **Capture full lineage metadata at packaging time**, not after the fact:
   - Git commit SHA of the training code.
   - Training data snapshot ID/URI (e.g. a Delta Lake version or a dataset
     hash) — see
     [data-and-model-lineage](../data-and-model-lineage/SKILL.md) for how to
     wire this into a lineage graph.
   - Experiment tracking run ID and key metrics — see
     [experiment-tracking](../experiment-tracking/SKILL.md).
   - Exact framework/library versions (`pip freeze` or `conda env export`
     snapshot, or a locked `pyproject.toml`).
   - Input/output schema (feature names, dtypes, expected ranges; for LLMs,
     prompt template version and tokenizer version).
3. **Export to the target runtime format** and validate the export is
   numerically equivalent to the training-time model on a held-out sample:
   ```python
   import torch

   model.eval()
   example_input = torch.randn(1, 3, 224, 224)
   traced = torch.jit.trace(model, example_input)

   # Parity check before trusting the exported artifact
   with torch.no_grad():
       ref_out = model(example_input)
       traced_out = traced(example_input)
   assert torch.allclose(ref_out, traced_out, atol=1e-4), "export parity check failed"

   traced.save("fraud-scorer-v2.3.1.pt")
   ```
4. **Register the artifact** with its version, stage, and metadata:
   ```python
   import mlflow

   with mlflow.start_run(run_id="run-8841"):
       mlflow.pytorch.log_model(
           traced,
           artifact_path="model",
           registered_model_name="fraud-scorer",
       )

   client = mlflow.tracking.MlflowClient()
   client.update_model_version(
       name="fraud-scorer",
       version="14",
       description="v2.3.1+a1b2c3d.run-8841 — retrain on Q3 fraud labels, fixes leaky feature",
   )
   client.set_model_version_tag("fraud-scorer", "14", "semver", "2.3.1")
   client.set_model_version_tag("fraud-scorer", "14", "git_sha", "a1b2c3d")
   ```
5. **Promote through explicit stages with gates**, never straight to
   production:
   - `dev` → automated on every merge to main; no gate.
   - `staging` → requires passing offline eval thresholds and a schema
     compatibility check against the current production model.
   - `production` → requires a human approval or an automated canary result
     (see [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)
     for canary/shadow rollout mechanics) plus monitoring hooks already wired
     up (see
     [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)).
6. **Keep the previous production version pinned and retrievable.** Do not
   delete or overwrite the prior production registry entry when promoting a
   new one — archive it to an "Archived" stage instead so it is one click
   away for rollback.
7. **Wire rollback as a promotion, not a deploy hack**: rolling back means
   re-promoting the previously archived version through the same gated path
   used for forward promotion (possibly with an expedited/emergency approval
   track), so the audit trail stays intact.
8. **Sign and checksum production artifacts** (e.g. cosign for container
   images, SHA-256 manifest for tarballs) so the serving layer can verify it
   is running exactly the bits that were approved.

## Best practices

- Treat the model registry as the single source of truth for "what is
  running in production" — never let a serving deployment reference a raw
  file path that bypasses the registry.
- Version the *pipeline*, not just the *weights*: preprocessing code,
  tokenizer, feature transformations, and post-processing logic must be
  versioned together with the weights, because a mismatch between them is a
  common source of training/serving skew.
- Make promotion gates machine-checkable where possible (schema diff,
  min-accuracy threshold, latency budget on a sample batch) so promotion
  isn't a purely manual judgment call for routine retrains.
- Store a small "golden" evaluation batch with expected outputs alongside
  each registered version, so any future serving change can be regression
  tested against it.
- Prefer content-addressable storage (hash of the artifact) as an internal
  key even if a human-friendly semver is shown in UI — hashes catch silent
  artifact corruption or accidental overwrite.
- Record model card metadata (intended use, known limitations, training data
  summary, eval results) as part of the registered version, not a separate
  wiki page that drifts out of sync.

## Common pitfalls

- **Symptom:** Two engineers each retrain and register a model with the same
  version tag, and it's unclear which one is actually serving.
  **Fix:** Make version identifiers include an immutable, unique component
  (registry auto-increment ID or content hash) in addition to the
  human-assigned semver, and make the registry (not a spreadsheet or Slack
  message) the single source of truth.

- **Symptom:** A model scores well in offline evaluation but performs
  differently in production (training/serving skew) — often because the
  serving code reimplements feature preprocessing slightly differently than
  the training code.
  **Fix:** Package the preprocessing/feature transformation logic as part of
  the versioned artifact (e.g. a `sklearn.Pipeline`, a `transformers`
  tokenizer config, or an ONNX graph with preprocessing baked in) so training
  and serving execute the identical code path, not a reimplementation.

- **Symptom:** A bad model is promoted to production and the team spends
  30+ minutes locating the previous good artifact to roll back.
  **Fix:** Never delete or overwrite a previous production registry entry on
  promotion — archive it instead, and keep a documented one-command rollback
  procedure (e.g. `mlflow models transition-stage` back to `Production`) that
  has been tested, not just written down.

- **Symptom:** An exported ONNX/TorchScript model gives different predictions
  than the original PyTorch/TensorFlow model on the same input.
  **Fix:** Always run a numerical parity check (allclose on a batch of real
  or representative inputs) between the training-time model and the exported
  artifact as a required step before registering; treat a failed parity check
  as a blocking packaging failure, not a warning.

- **Symptom:** Someone runs a "cleanup" script that deletes registry versions
  older than N days, and it turns out a currently-serving canary was pointing
  at one of them.
  **Fix:** Never treat registry deletion as routine housekeeping. Warn
  explicitly before any deletion of registered model versions or their
  underlying artifacts; prefer archiving/soft-delete with a retention policy,
  and check active deployment references before any hard delete.

## Worked example

A team maintains a fraud-scoring model, `fraud-scorer`, retrained weekly.

1. Training run `run-8841` (tracked per
   [experiment-tracking](../experiment-tracking/SKILL.md)) completes with
   AUC 0.912 on the held-out set, git SHA `a1b2c3d`, trained on data snapshot
   `s3://data-lake/fraud/snapshots/2026-07-20`.
2. CI packaging job exports the model to TorchScript, runs the parity check,
   and registers it in MLflow as `fraud-scorer` version 14, tagged
   `semver=2.3.1`, `git_sha=a1b2c3d`, `data_snapshot=2026-07-20`, stage `None`.
3. An automated staging job promotes version 14 to `Staging` after confirming:
   AUC ≥ 0.90 (gate threshold), inference schema matches production's input
   contract, and p95 latency on a 1,000-row sample batch is ≤ 40 ms.
4. A human reviewer checks the model card diff against the current
   production version (13, AUC 0.905) and approves promotion.
5. Version 14 is promoted to `Production`; version 13 is moved to `Archived`
   (not deleted). The serving layer (see
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)) is
   configured to route 5% of traffic to version 14 as a canary for 24 hours
   before full cutover.
6. Two hours into the canary, monitoring
   ([model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md))
   flags a spike in the false-positive rate on version 14. On-call rolls back
   by re-promoting version 13 from `Archived` to `Production` — a two-minute
   action because the artifact and its metadata were never deleted.

## Cross-references

- [experiment-tracking](../experiment-tracking/SKILL.md)
- [data-and-model-lineage](../data-and-model-lineage/SKILL.md)
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
