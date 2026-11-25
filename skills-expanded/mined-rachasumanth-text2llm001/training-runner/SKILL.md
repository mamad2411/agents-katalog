---
name: training-runner
description: Generate and run robust pretraining pipelines with background execution, live monitoring, and checkpoint-safe recovery.
---

# Training Runner

Use this skill for end-to-end model training execution, optimized for from-scratch pretraining.

## Framework Support

Generate/adapt training workflows for:

- NanoGPT
- LitGPT
- Hugging Face Trainer

## Script Generation Defaults

Training scripts should include at minimum:

- cosine learning rate schedule
- gradient clipping
- mixed precision (bf16/fp16 based on hardware)
- deterministic seeds where feasible
- structured logging for losses and throughput

## Execution Patterns

### 1. SSH / Remote Execution (RunPod/Vast/Lambda)

- Use `ssh` to run training commands on provisioned instances.
- Use `screen` or `tmux` to keep processes alive.
- Stream logs back via `tail -f`.

### 2. Kaggle Kernels

- Prepare a `kernel-metadata.json` with `enable_gpu: true` and `enable_internet: true`.
- Use `kaggle kernels push -p <path>` to start training.
- Monitor with `kaggle kernels status <user>/<kernel>`.
- Retrieve logs/outputs via `kaggle kernels output <user>/<kernel>`.

### 3. Background Terminal Execution

For long runs, prefer background terminal execution:

- start via `exec`
- set `background: true`
- set `pty: true` for interactive-safe output

This keeps the agent responsive while training proceeds asynchronously.

## Live Monitoring

Use `process:log` to stream and inspect ongoing training output.
Parse and report key metrics:

- train loss
- eval/validation loss
- learning rate
- tokens/sec or samples/sec
- checkpoint save events

If divergence appears (NaN, exploding loss, repeated OOM), propose immediate mitigation and recovery.

## Multi-Phase Training Strategy

Support staged curricula:

1. broad pretraining phase
2. curated high-quality phase
3. domain-specific phase
4. cooldown/anneal phase

For each phase, define target steps/tokens, LR policy, and success criteria.

## Checkpoint Management

- Save checkpoints on predictable intervals and key milestones.
- Keep latest + best + periodic snapshots.
- Validate checkpoint integrity after save.
- Support clean resume from last good checkpoint after interruption.
- Maintain a concise checkpoint index with timestamp/step/metrics.

## Cost Tracking

Append compute cost entries to the project-level `cost_ledger.json`:

- Track GPU-hours consumed per training phase.
- Estimate cost based on provider hourly rate × elapsed time.
- Write cost entries at checkpoint intervals and on training completion.
- Include cost-per-token-trained metric for efficiency comparison across runs.

## Run Outputs

1. `train.sh` or equivalent launcher script
2. `training_config.yaml` (or framework-native config)
3. `training_status.md` (current metrics + risk notes)
4. `checkpoints_index.json`
