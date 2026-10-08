---
name: ai-science-llm-training-systems
description: "Track LLM fine-tuning runs with pandas/dataclasses + W&B/MLflow/TensorBoard: log per-epoch loss, run one-factor ablations (LoRA rank, LR), build a run registry. Use for hyperparameter ablations or picking an early-stop epoch."
tool_type: python
primary_tool: pandas
---

# LLM Training Systems: Tracking, Epochs, and Ablations

## When to Use

- Setting up experiment tracking for an LLM fine-tuning/LoRA project before burning GPU hours
- Deciding which epoch/checkpoint to keep from a training run (early stopping)
- Designing an ablation matrix (LoRA rank, learning rate, sequence length, warmup) and comparing results without confounding factors
- Building a run registry so past experiments (config, commit, metrics) are queryable instead of scattered across notebooks
- Wiring up W&B, MLflow, or TensorBoard logging calls into a training loop

## Version Compatibility

- Python >= 3.10, pandas >= 2.0, numpy >= 1.24
- `transformers` >= 4.40, `trl` >= 0.9, `accelerate` >= 0.30 (for the real training loop this tracking layer wraps)
- `wandb` >= 0.17 or `mlflow` >= 2.10 (either optional, pick one tracker per project)

## Prerequisites

- `pip install pandas numpy` (required); `pip install wandb` or `pip install mlflow` (optional, for real logging)
- Familiarity with LoRA/PEFT fine-tuning concepts (see `huggingface-skills:huggingface-llm-trainer` / `huggingface-skills:trl-training`)
- A training loop that already emits `train_loss` / `eval_loss` per step or epoch — this skill covers what to do with those numbers, not the loop itself

**Key discipline rules:**
- Change one factor at a time — simultaneous changes make attribution impossible
- Fix seeds for dataset splits, weight init, and data shuffling before starting any run
- Pick one primary metric (e.g., `eval_loss`) before running — cherry-picking post-hoc is p-hacking

**Goal:** capture every hyperparameter for a run in one reproducible object before training starts.
**Approach:** use a `dataclass` as the single source of truth, then convert to a `pd.Series`/dict for logging to any tracker.

```python
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np

np.random.seed(42)

@dataclass
class TrainConfig:
    """Full hyperparameter set for one fine-tuning run. Log this object, not loose variables."""
    run_name: str
    model_name: str
    lora_rank: int
    learning_rate: float
    batch_size: int
    epochs: int
    warmup_ratio: float
    weight_decay: float
    max_seq_len: int
    seed: int

cfg = TrainConfig(
    run_name='baseline-lora-r16',
    model_name='mistral-7b-instruct',
    lora_rank=16,
    learning_rate=2e-4,
    batch_size=8,
    epochs=3,
    warmup_ratio=0.03,
    weight_decay=0.01,
    max_seq_len=2048,
    seed=42,
)

pd.Series(asdict(cfg))
```

**Goal:** track per-epoch train/eval loss and pick the checkpoint to keep.
**Approach:** append one row per epoch to a DataFrame, then select the epoch with minimum `eval_loss` (early stopping on a held-out metric, not train loss).

```python
def simulate_training(epochs=5, base_train=2.2, base_eval=2.4, noise=0.03):
    """Stand-in for a real training loop's per-epoch metrics (swap for actual logged values)."""
    rows = []
    train_loss = base_train
    eval_loss = base_eval
    for ep in range(1, epochs + 1):
        train_loss = train_loss * (0.86 + np.random.uniform(-0.02, 0.02))
        eval_loss = eval_loss * (0.90 + np.random.uniform(-0.03, 0.03)) + np.random.normal(0, noise)
        eval_acc = max(0.0, min(1.0, 1.35 - eval_loss / 2.0 + np.random.normal(0, 0.01)))
        rows.append({'epoch': ep, 'train_loss': train_loss, 'eval_loss': eval_loss, 'eval_acc': eval_acc})
    return pd.DataFrame(rows)

def best_epoch(df: pd.DataFrame):
    """Return (epoch, eval_loss, eval_acc) for the row with the lowest eval_loss."""
    i = df['eval_loss'].idxmin()
    return int(df.loc[i, 'epoch']), float(df.loc[i, 'eval_loss']), float(df.loc[i, 'eval_acc'])

history = simulate_training(epochs=8)
ep, loss, acc = best_epoch(history)
print(f'Best epoch = {ep}, eval_loss = {loss:.4f}, eval_acc = {acc:.4f}')
```

**Goal:** wire per-epoch metrics into a real tracker without hard-depending on it being installed.
**Approach:** guard the import so the tracking call is a no-op if the package isn't present — safe to leave in shared code.

```python
def log_metrics(cfg, step: int, metrics: dict, backend: str = 'wandb'):
    """Log a metrics dict for one step/epoch to W&B or MLflow. Falls back to print if unavailable."""
    if backend == 'wandb':
        try:
            import wandb
            if wandb.run is None:
                wandb.init(project='llm-finetuning', name=cfg.run_name, config=asdict(cfg))
            wandb.log(metrics, step=step)
            return
        except ImportError:
            pass
    elif backend == 'mlflow':
        try:
            import mlflow
            mlflow.log_metrics(metrics, step=step)
            return
        except ImportError:
            pass
    print(f'[step {step}] {metrics}')
```

## Ablation Study Design

Ablation factors (one at a time):
- LoRA rank: 8 vs 16 vs 32
- Learning rate: 1e-4 vs 2e-4 vs 5e-4
- Sequence length: 1024 vs 2048
- Warmup ratio: 0.01 vs 0.03 vs 0.1

**Goal:** compare a grid of hyperparameter combinations without confounding attribution.
**Approach:** sweep the factors in nested loops, record one row per run, then aggregate by factor to see main effects.

```python
def simulate_run(lora_rank, lr, seq_len):
    """Toy score surface: higher rank helps a bit, too-high lr hurts, longer seq helps slightly."""
    score = 0.64
    score += 0.015 * np.log2(lora_rank)
    score -= 0.10 * abs(np.log10(lr) - np.log10(2e-4))
    score += 0.01 if seq_len == 2048 else 0.0
    score += np.random.normal(0, 0.004)
    eval_loss = 1.4 - score + np.random.normal(0, 0.01)
    return score, eval_loss

rows = []
for r in [8, 16, 32]:
    for lr in [1e-4, 2e-4, 5e-4]:
        for s in [1024, 2048]:
            score, ev = simulate_run(r, lr, s)
            rows.append({'lora_rank': r, 'lr': lr, 'seq_len': s, 'eval_score': score, 'eval_loss': ev})

ablation_df = pd.DataFrame(rows).sort_values('eval_score', ascending=False)
summary = ablation_df.groupby('lora_rank', as_index=False)['eval_score'].mean().sort_values('eval_score', ascending=False)
```

## Run Registry

Minimum fields per run: `run_id`, date, git commit, dataset version, config values, best metrics, note on what changed.

```python
registry = pd.DataFrame([
    {'run_id': 'r001', 'commit': 'abc123', 'change': 'baseline r16', 'best_eval_loss': 0.694, 'best_eval_acc': 0.712},
    {'run_id': 'r002', 'commit': 'def456', 'change': 'rank 32',      'best_eval_loss': 0.681, 'best_eval_acc': 0.724},
    {'run_id': 'r003', 'commit': 'ghi789', 'change': 'lr 5e-4',      'best_eval_loss': 0.741, 'best_eval_acc': 0.689},
])
registry.sort_values('best_eval_loss')
```

## Pre/Post-Run Checklist

**Before launching:**
1. Freeze data splits and seed
2. Log full config + package versions
3. Define primary metric (e.g., `eval_loss`) and secondary metric (task F1/accuracy)
4. Set checkpoint cadence and early-stop policy
5. Predefine ablation matrix and stopping budget

**After run:**
1. Compare against best prior run
2. Record interpretation (why change helped/hurt)
3. Decide next run from evidence, not intuition alone

## Recommended Stack

- **Trainer/runtime**: HuggingFace `transformers` + `trl` + `accelerate`
- **Scaling**: DeepSpeed or FSDP for multi-GPU/multi-node
- **Tracking**: W&B or MLflow
- **Data/versioning**: DVC or immutable dataset snapshots
- **Orchestration**: Slurm/Kubernetes + reproducible launch scripts

## Pitfalls

- **Comparing across trackers/runs with different seeds**: a single-seed win can be noise — rerun the top 1-2 ablation candidates with 2-3 seeds before trusting the ranking
- **Early stopping on train loss**: always select the checkpoint by `eval_loss`/task metric, not train loss, which keeps decreasing even when the model overfits
- **Changing two factors at once** (e.g., rank and LR together): makes it impossible to attribute the outcome to either one — always hold all but one factor fixed
- **Silent tracker failures**: `wandb`/`mlflow` calls that fail mid-run (auth, network) can silently drop metrics — wrap logging calls and fall back to local CSV/DataFrame as done in `log_metrics` above

## See Also

- `huggingface-skills:huggingface-llm-trainer` — the actual fine-tuning/LoRA training loop this tracking layer wraps
- `huggingface-skills:trl-training` — SFT/DPO trainer setup with `trl`
- `huggingface-skills:huggingface-trackio` — lightweight run tracking alternative to W&B/MLflow
- `bio-experimental-design-power-analysis` — general experimental design discipline (one-factor-at-a-time, multiple testing) that applies equally to ablations
