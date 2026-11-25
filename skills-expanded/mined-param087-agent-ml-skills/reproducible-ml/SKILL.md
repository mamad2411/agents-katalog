---
name: reproducible-ml
description: Use when an ML result must be reproducible — fixing seeds, pinning environments, versioning data, and structuring projects so runs can be exactly recreated. Covers determinism gotchas across NumPy, PyTorch, and CUDA.
---

# Reproducible ML

## Overview

Reproducibility means: same code + same data + same config → same result. It is a prerequisite for trusting comparisons, debugging regressions, and shipping. Three pillars: **seed everything, pin everything, version the data.**

## When to use

- Results vary run-to-run.
- Setting up a new project or research codebase.
- Preparing work others must reproduce (papers, audits, reviews).

## Pillar 1 — Seed everything

```python
import os, random, numpy as np, torch

def seed_everything(seed: int = 42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False  # disables nondeterministic autotuner
```

For DataLoaders, also set `worker_init_fn` and a `generator` so workers are deterministic.

## Pillar 2 — Pin the environment

- Pin exact versions: `requirements.txt` with `==`, or `uv.lock` / `poetry.lock` / `conda env export`.
- Record Python + CUDA + cuDNN versions in the run metadata.
- Containerize (Docker) for cross-machine reproducibility.

## Pillar 3 — Version the data

- Hash datasets (`sha256`) and log the hash with every run.
- Use **DVC** or dataset snapshots; never overwrite `data.csv` in place.
- Treat data as immutable inputs keyed by version (`data_v="2026-06-01"`).

## Project layout that supports reproducibility

```
project/
├── data/            # raw (immutable) + processed, both versioned
├── src/             # importable code, no notebooks doing real work
├── configs/         # YAML/Hydra configs, one per experiment
├── scripts/         # entrypoints: train.py, evaluate.py
├── requirements.txt # or uv.lock / poetry.lock (pinned)
└── README.md        # exact commands to reproduce
```

## Determinism gotchas

- GPU reductions can be nondeterministic even with seeds — use `torch.use_deterministic_algorithms(True)` and set `CUBLAS_WORKSPACE_CONFIG=:4096:8`.
- Parallel `groupby`/`apply` ordering can vary — sort before reducing.
- `set`/`dict` ordering across processes — set `PYTHONHASHSEED`.
- Non-pinned dependencies silently change behavior between installs.

## Pitfalls

- Seeding only NumPy but using PyTorch/CUDA RNGs.
- "Works on my machine" — unpinned env + unversioned data.
- Doing real computation in notebooks with hidden execution order — move logic to `src/`.

## Hand-off

A repo where `pip install -r requirements.txt && python scripts/train.py --config configs/exp.yaml` recreates the exact result that experiment-tracking logged.
