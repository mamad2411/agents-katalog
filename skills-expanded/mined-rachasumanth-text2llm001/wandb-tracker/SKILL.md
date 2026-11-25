---
name: wandb-tracker
description: Integrate Weights & Biases tracking for training observability, artifact lineage, and experiment comparison.
---

# W&B Tracker

Use this skill to instrument and manage experiment tracking with Weights & Biases.

## Environment

Required:

- WANDB_API_KEY

## Run Initialization

Initialize each run with:

- project name
- entity/workspace
- run name
- tags (model scale, dataset version, phase, framework)
- config snapshot (hyperparameters + data/tokenizer/model ids)

Ensure runs are reproducible and easy to filter/compare.

## Metric Logging

Log metrics at consistent intervals:

- train loss
- eval/validation loss
- learning rate
- throughput (tokens/sec or samples/sec)
- grad norm (if available)
- GPU utilization and memory (if available)

Align metric names across runs for clean comparisons.

## Artifact Versioning

Track artifacts with explicit versions and lineage:

- model checkpoints
- tokenizer artifacts
- dataset manifests/snapshots
- evaluation reports

Include metadata linking artifacts to run id, step, and source config.

## Hyperparameter Tuning Comparison

Support side-by-side run comparison for tuning cycles:

- summarize best-performing runs by target metric
- identify stable vs unstable training regimes
- surface cost/performance tradeoffs for candidate configs

Output concise recommendation on next experiment set.

## Deliverables

1. `wandb_setup.md` (project/entity/tagging conventions)
2. `experiment_tracking_plan.md` (metrics + logging cadence)
3. `run_comparison.md` (tuning summary + recommended next run)

## Preflight Validation

Before initializing any W&B run, validate:

- `WANDB_API_KEY` is set and non-empty.
- W&B API is reachable (`wandb login --verify`).
- Project and entity exist or can be created.

Report clear error if credentials are missing, with guidance on where to set them.
