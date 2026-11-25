---
name: ml-training-experiments
description: "Plan or change ML training experiments, tracking, checkpoints, scaling, evals, or reproducibility."
---

# ML Training Experiments

Run ML experiments as reproducible engineering work: scoped hypotheses, pinned code/data/config, tracked results, resumable training, and clear promotion decisions.

## Trigger boundary

Use this skill when planning or changing ML training experiments, datasets/configuration, tracking, checkpoints/resume, scaling, evaluation, promotion, or reproducibility controls.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no training, dataset, experiment, checkpoint, evaluation, or promotion behavior impact; follow the repository's established convention directly.

## Process

1. Inspect repo-pinned Python version, package manager, lockfile, CUDA/driver notes, framework versions, configs, CI, experiment tracking, dataset/versioning, and hardware assumptions before choosing commands or tools.
2. For new-project or version-sensitive framework choices, use `itsol-current-tech-context`; avoid hardcoding fast-moving package versions in plans or skill output.
3. Start with a baseline and one written hypothesis. Keep one primary metric, explicit guardrails, fixed data/split/evaluator/budget, and a keep/discard/inconclusive/crash decision for every run.
4. Keep training code in importable modules with explicit configs. Notebooks may explore and report, but must not be the only implementation.
5. Record run metadata: code commit, dirty state, lockfile/container digest, dataset and split version, config, seed policy, hardware, metrics, resources, cost, artifacts, and decision rationale.
6. Before scaling training, prove the loop at small scale: forward/backward pass, overfit one batch, overfit a small subset, smoke eval, profiler, and cost estimate.
7. Treat checkpoints as resumable training state, not only model weights. Test resume and retention before long runs.
8. Add focused verification: lint/format/typecheck, unit/data-contract tests, smoke train, smoke inference, small golden eval, checkpoint resume, export compatibility, and dependency/security checks where applicable.

## Coordination

Use with `ml-data-evaluation` for datasets, splits, leakage, metrics, and error analysis; `ml-serving-mlops-review` for model promotion, registry, serving contracts, monitoring, and rollout; `itsol-current-tech-context` for current framework/package decisions; `security-*` skills when datasets, models, notebooks, tracking servers, or artifacts contain sensitive data. For Rust/Rig/Candle training or runtime code, route first to the existing `rust-ml-llm-*` skills and use this skill only for cross-cutting experiment discipline.

## Reference Routing

- Python environment policy, project layout, dependency boundaries, notebook rules, framework/tool selection, and algorithm starting points: read [01-python-framework-repo.md](./references/01-python-framework-repo.md).
- Experiment hypotheses, one-change discipline, run metadata, reproducibility, practical significance, autoresearch loops, and experiment templates: read [02-experiment-design-tracking.md](./references/02-experiment-design-tracking.md).
- Model parameters, hyperparameters, learning rate, batch size, optimizers, regularization, schedulers, precision, inference parameters, and config versioning: read [03-hyperparameters-config.md](./references/03-hyperparameters-config.md).
- Training smoke tests, profiling, dataloaders, mixed precision, accumulation, checkpointing, early stopping, distributed training, CI, training pipelines, and promotion gates: read [04-training-performance-distributed.md](./references/04-training-performance-distributed.md).

## Version Policy

- Existing repo: implement against pinned Python, package manager, lockfile, ML framework, CUDA/driver, model, dataset, and infrastructure versions.
- New project or upgrade: use `itsol-current-tech-context` and current official docs or package registries before recommending exact framework versions, base models, CUDA stacks, or training tools.
- Keep training, development, and serving dependencies separated when the repo supports it. Commit lockfiles and run CI in locked or frozen mode.
