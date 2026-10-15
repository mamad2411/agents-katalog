---
name: compute-budget-planner
description: Estimate GPU compute budget before running ML experiments. Use when planning how much compute an experiment, ablation matrix, or sweep will cost, sizing smoke tests, finding cheaper alternatives, or deciding whether a planned run fits available resources.
argument-hint: "[project-dir] [--mode estimate|smoke|ablation|compare] [--model <model-size>]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Compute Budget Planner

Estimate and control compute spend before jobs are submitted. This skill prevents GPU-hour waste from under-scoped smoke tests, over-specified ablations, and jobs that could have been half the cost with a smarter design.

Use this skill when:

- a planned training run's cost is unknown before submission
- a smoke test needs to be sized to give signal without wasting a full GPU-day
- an ablation matrix needs to be costed before scheduling all variants
- a cheaper model variant, shorter sequence, or smaller dataset could answer the same question
- available compute is limited and job priority needs to be set
- a paper's experimental budget needs to be disclosed or defended to reviewers

Do not use this skill to submit jobs — use `run-experiment` after sizing is done. Do not use this skill for experiment design — use `experiment-design-planner` first.

Pair this skill with:

- `experiment-design-planner` to align experiment scope with compute budget before design is locked
- `run-experiment` to submit the sized job with the correct resource spec
- `baseline-selection-audit` when baseline replication costs need to be included in the total budget
- `research-project-memory` to record compute decisions as evidence or risk items

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    └── estimation-guide.md
```

## Progressive Loading

- Always read `references/estimation-guide.md`.
- Read existing job configs in `jobs/`, `configs/`, or `experiments/` when a previous run exists.
- Read `memory/evidence-board.md` when the compute estimate is tied to a paper claim.

## Core Principles

- Estimate before submitting, not while waiting for the job to time out.
- A smoke test that uses less than 5% of the full job cost should be the default first step.
- Compute cost compounds: one model × one dataset × one seed is the atom; ablations multiply.
- Cheaper alternatives should always be explored before committing to expensive runs.
- Reviewer trust is higher when compute is disclosed and reproducibility is feasible on standard hardware.
- Underestimating compute is a submission risk: a result that cannot be reproduced because the hardware is unavailable is a reviewer concern.

## Step 1 — Gather Training Context

Collect:

- model name and parameter count (or approximate FLOPs if known)
- dataset size: number of training examples, sequence length or image size
- planned training duration: epochs or steps
- batch size and gradient accumulation steps
- hardware: GPU type (A100, H100, V100, RTX 3090), VRAM, number of GPUs
- framework and mixed precision: FP16, BF16, or FP32
- existing throughput: samples/second or tokens/second from a prior run (if available)

If no prior run exists, use `references/estimation-guide.md` to estimate throughput.

## Step 2 — Estimate Full Run Cost

Compute:

```
total_steps = ceil(dataset_size / batch_size) × epochs
             or planned_steps (if step-based)

gpu_hours = total_steps × seconds_per_step / 3600 × num_gpus
```

Report:

- estimated GPU-hours (single GPU equivalent)
- wall-clock time with the planned number of GPUs
- whether the run fits in the available time limit (e.g., SLURM 24h, RunAI policy)

If throughput is unknown, provide a range using the estimation guide's reference values for the model class and hardware.

## Step 3 — Size the Smoke Test

A smoke test should:

- use ≤ 5% of the full run's compute (ideally 1–2%)
- complete within 10–30 minutes on one GPU
- produce a loss curve with a clear downward trend (proves the code runs correctly)
- exercise the full data pipeline, model forward/backward, checkpointing, and logging

Recommend:

```
Smoke test steps: max(100, 0.01 × total_steps)
Smoke dataset: subsample 1% of training data, or use 1 batch per shard
Expected smoke wall-clock: < 30 min on 1× GPU
```

Flag if the smallest feasible smoke run exceeds 30 minutes. This is a sign the setup overhead is too high.

## Step 4 — Cost the Ablation Matrix

For each ablation dimension, record:

| Variant | Changed variable | Cost multiplier | GPU-hours | Priority |
|---|---|---|---|---|
| Baseline | — | 1× | | required |
| Ablation A | [removed component] | 1× | | required |
| Ablation B | [changed config] | 0.5× | | should-have |
| Sweep C | [hyperparameter] | 3× | | optional |

Classify each variant as:

- `required`: paper claim depends on this comparison
- `should-have`: reviewer will likely ask; defensible to omit with a reason
- `optional`: nice-to-have; drop first if compute is limited

Report:

- total required GPU-hours
- total should-have GPU-hours
- total optional GPU-hours
- recommended minimum run set

## Step 5 — Identify Cheaper Alternatives

Check whether any of the following can answer the same question at lower cost:

- **Smaller model / fewer parameters**: Can a 125M model prove the concept before scaling to 1B?
- **Shorter sequences / smaller images**: Does the method work at half resolution?
- **Fewer training steps**: Can early stopping or learning rate warmup give a valid comparison at 50% of steps?
- **Smaller dataset**: Can a 10% subsample reproduce the trend with ±5% relative error?
- **Lower-rank approximation**: Can LoRA or adapter training substitute for full fine-tuning for this ablation?
- **Faster hardware**: Can an A100 replace 4× V100s and finish in one-quarter the wall-clock time?

For each alternative, record the expected signal quality and the risk of a misleading result.

## Step 6 — Write the Budget Plan

Save to:

```text
code/.agent/compute-budget.md
```

The plan should include:

- full run estimate (GPU-hours and wall-clock)
- smoke test spec (steps, data fraction, expected wall-clock)
- ablation matrix with priority and cost
- cheaper alternatives considered and rejected or accepted
- available resource envelope and whether budget fits
- recommended submission order: smoke → required ablations → should-have → optional

## Memory Writeback

- If compute cost affects a paper claim's feasibility, add to `memory/risk-board.md`
- If a cheaper alternative is accepted and changes the experimental design, update `memory/decision-log.md`
- Update `memory/evidence-board.md` when compute details need to be cited in the paper (hardware, training duration, GPU-hours)

## Final Sanity Check

Before finalizing:

- smoke test spec is under 30 minutes on 1 GPU
- full run estimate fits available time limit
- ablation matrix has priorities assigned
- cheaper alternatives were considered
- required GPU-hours are within the available resource envelope or a risk entry is filed
