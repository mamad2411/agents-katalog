---
name: experiment-debugger
description: Use when training has engineering failures — NaN/gradient issues, GPU OOM, slow data loading, wrong metrics, reproducibility failures. Not for checking job queue/status (use run-status-monitor). Not for valid-but-surprising scientific results (use result-diagnosis). Not for confound or claim audit before writing (use research-results-auditor).
argument-hint: "[project-dir] [--run <run-id>] [--mode nan|oom|slow|metric|repro|crash]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Experiment Debugger

Fix engineering failures that prevent valid experiment results from being produced. This skill separates bugs from science: if the code is broken, wrong, or non-reproducible, fix the code first before interpreting results.

Use this skill when:

- training crashes or produces NaN loss, NaN gradients, or inf values
- GPU OOM errors block training or reduce batch size unexpectedly
- training is significantly slower than expected
- data loading is a bottleneck or produces corrupted batches
- metric values are impossible, unstable, or inconsistent across runs
- a run cannot be reproduced despite fixing the seed
- a config or checkpoint was changed silently between runs
- tensorboard, wandb, or logging output is missing or misaligned

Do not use this skill for interpreting surprising but valid results — use `result-diagnosis`. Do not use this skill for choosing baselines or experiment designs — use `baseline-selection-audit` and `experiment-design-planner`.

Pair this skill with:

- `result-diagnosis` after engineering issues are fixed and results are valid but still surprising
- `run-experiment` to resubmit a corrected job after the bug is resolved
- `run-status-monitor` to probe log artifacts and confirm whether the fix took effect
- `data-pipeline-manager` when the bug traces to a data loading, preprocessing, or split issue
- `research-project-memory` to record debugging decisions that affect experimental validity claims

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    └── failure-taxonomy.md
```

## Progressive Loading

- Always read `references/failure-taxonomy.md`.
- Read job logs, training logs, and config files before asking the user for information.
- Read `memory/risk-board.md` when the bug may recur or affect other runs.

## Core Principles

- Never modify config or model to silence a bug without understanding why it happened.
- Reproduce the bug in the smallest possible setting before fixing it.
- Distinguish numerical instability from code bugs from hardware issues from data bugs.
- Seed-related non-reproducibility is almost always a data-ordering, framework, or environment issue — not a random event.
- Metric bugs are often silent: a metric that computes without error may still be wrong.
- Engineering fixes should not change what the experiment was designed to test.

## Step 1 — Gather Run Context

Read:

- training log: `logs/`, `wandb/`, `runs/`, `output/`, or `docs/ops/runs/<run-id>-status.md`
- config file: `configs/`, `experiments/`, `jobs/<run-id>.yaml`, or equivalent
- error message or traceback: copy the exact error
- hardware context: GPU type, CUDA version, framework version
- git commit of the code being run

Record:

- failure mode: crash, NaN, OOM, slow, metric, repro, or silent error
- when in training the failure occurred: step 0, early training, mid-training, evaluation
- whether the failure is deterministic or intermittent

## Step 2 — Classify the Failure Mode

Read `references/failure-taxonomy.md`.

Choose one primary mode:

- `nan-gradient`: NaN or inf in loss or gradients
- `oom`: GPU out-of-memory
- `slow-training`: training throughput is below expected
- `slow-data`: data loading is the bottleneck
- `metric-error`: metric value is impossible, negative, > 1 for accuracy, wrong shape, or suspiciously round
- `repro-failure`: different results despite fixed seed
- `crash`: process exits with non-zero code, SIGKILL, or timeout without producing output
- `silent-error`: the run completes but results are clearly wrong or absent

If multiple modes apply, list them in priority order.

## Step 3 — NaN / Gradient Debugging

When `nan-gradient` is the mode:

1. Check whether NaN appears at step 0 or after many steps. Step-0 NaN almost always means a data or initialization bug; late NaN usually means instability.
2. Inspect the loss function for log(0), division by zero, or sqrt of negative values.
3. Check learning rate: very large LR can cause gradient explosion.
4. Check for mixed-precision errors: FP16 underflow/overflow is common. Try `torch.autocast` with `dtype=torch.float32` to isolate.
5. Add gradient norm logging: `torch.nn.utils.clip_grad_norm_` with `max_norm=1.0` can stabilize and surface the layer.
6. Check batch normalization with very small batch sizes (batch size 1 can produce NaN BN statistics).
7. Run `torch.autograd.set_detect_anomaly(True)` to find the exact operation.

Record which layer/operation produces NaN first.

## Step 4 — GPU OOM Debugging

When `oom` is the mode:

1. Identify total GPU memory and peak allocated memory from the error message.
2. Check whether OOM occurs at: model initialization, forward pass, backward pass, or evaluation.
3. Try: reduce batch size by 50%; if that resolves it, calculate the memory per sample.
4. Check for memory leaks: tensors retained in a Python list across steps, graph retained in loss variable.
5. Check for accidental double-size allocations: gradient checkpointing disabled, full sequence attention without flash attention.
6. Profile with `torch.cuda.memory_summary()` at the OOM step.
7. Check whether the job requested the correct GPU memory via SLURM `--mem-per-gpu` or RunAI resource spec.

## Step 5 — Slow Training / Slow Data Debugging

When `slow-training` or `slow-data` is the mode:

1. Get baseline throughput: samples/second or tokens/second from logs.
2. Check GPU utilization: `nvidia-smi` or `run-status-monitor` for GPU occupancy. If < 80%, training is data-starved or CPU-bound.
3. Check data loader workers: `num_workers=0` or low `num_workers` is a common bottleneck.
4. Check whether dataset is on a network filesystem vs local NVMe. Network I/O can dominate.
5. Check whether preprocessing happens online per batch vs cached offline.
6. Check whether data is being re-read from disk every epoch vs cached in memory or RAM disk.
7. Profile with `torch.profiler` for a few steps to find the dominant overhead.

## Step 6 — Metric Error Debugging

When `metric-error` is the mode:

1. Check metric reduction: is the metric averaged over samples or over batches? Unequal batch sizes break batch-mean metrics.
2. Check class label encoding: 0-indexed vs 1-indexed, one-hot vs integer.
3. Check whether evaluation uses the same preprocessing as training (tokenizer, normalization, augmentation).
4. Check for padding tokens included in loss or metric computation.
5. Check whether the metric is computed on the whole eval set at once vs accumulated from mini-batches.
6. Verify the metric against a tiny synthetic example where the expected value is known exactly.
7. For sequence metrics (BLEU, ROUGE, F1), check tokenization and normalization rules.

## Step 7 — Reproducibility Debugging

When `repro-failure` is the mode:

1. Check seed coverage: `torch.manual_seed`, `numpy.random.seed`, `random.seed`, and `torch.cuda.manual_seed_all`.
2. Check non-deterministic CUDA ops: `torch.backends.cudnn.deterministic = True` and `torch.backends.cudnn.benchmark = False`.
3. Check multi-worker data loading: shuffle + multiple workers + no `worker_init_fn` is a common source of order non-determinism.
4. Check floating-point accumulation order: multi-GPU reductions are not guaranteed deterministic across runs without explicit settings.
5. Check whether the environment is identical: CUDA version, cuDNN version, PyTorch version, Python version.
6. Check whether a checkpoint was loaded from a different step than expected.

If determinism cannot be achieved, document the expected variance and report mean ± std across seeds instead.

## Step 8 — Write Findings and Fix

After identifying the root cause:

1. Document the bug, root cause, and fix in `docs/ops/runs/<run-id>-debug.md`.
2. Update the config or code with the fix; do not rely on ad hoc command-line overrides.
3. Run a smoke test to confirm the fix (short run, small data).
4. Update `memory/risk-board.md` if the bug reveals a recurring risk to other runs.
5. Route to `run-experiment` to resubmit the corrected job.

## Final Sanity Check

Before declaring the bug fixed:

- smoke test passes without the failure mode
- fix is committed to code or config, not just a shell override
- the fix does not change what the experiment was designed to test
- memory writeback covers any new risks or data/environment findings
