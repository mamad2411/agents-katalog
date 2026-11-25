---
name: optuna
description: Hyperparameter optimization framework (Optuna). Define-by-run API with automatic search space construction, state-of-the-art samplers (TPE, CMA-ES, NSGA-II, GPSampler), efficient pruning (Median, Hyperband, ASHA), multi-objective optimization, constrained optimization, distributed parallel execution, and visualization dashboard. Integrates with PyTorch, PyTorch Lightning, TensorFlow, Keras, XGBoost, LightGBM, CatBoost, MLflow, W&B, and scikit-learn.
license: MIT license
tags: [hyperparameter-optimization, pruning, multi-objective-optimization, experiment-search, optuna]
metadata:
    skill-author: K-Dense Inc.
------|----------|-------------|
| `TPESampler` | General ML tuning | Tree-structured Parzen Estimator; default, good for most cases |
| `CMAESSampler` | Continuous, low-dim (<100) | Covariance Matrix Adaptation; efficient for numeric params |
| `NSGAIISampler` | Multi-objective (2-3 objectives) | Pareto-front optimization |
| `GPSampler` | Expensive evaluations | Gaussian Process-based; sample-efficient |
| `RandomSampler` | Baseline, debugging | Uniform random sampling |
| `GridSampler` | Small discrete spaces | Exhaustive grid search |
| `QMCSampler` | Continuous spaces | Quasi-Monte Carlo, better coverage than random |

**Usage:**
```python
import optuna
sampler = optuna.samplers.TPESampler(seed=42, n_startup_trials=10)
study = optuna.create_study(sampler=sampler)
```

### 4. Pruning (Early Stopping)

Stop unpromising trials early to save compute:
```python
def objective(trial):
    for epoch in range(100):
        accuracy = train_and_evaluate(...)
        # Report intermediate value
        trial.report(accuracy, epoch)
        # Check if should prune
        if trial.should_prune():
            raise optuna.TrialPruned()
    return accuracy
```

**Pruner Selection:**
- `MedianPruner`: Prune if trial's intermediate value is below median at same step
- `HyperbandPruner`: Successive halving; efficient for large trial counts
- `SuccessiveHalvingPruner`: Similar to Hyperband, simpler configuration
- `ThresholdPruner`: Prune below absolute threshold
- `PatientPruner`: Prune after N epochs without improvement

**Integration with PyTorch Lightning:**
```python
from optuna.integration import PyTorchLightningPruningCallback

trainer = pl.Trainer(
    callbacks=[PyTorchLightningPruningCallback(trial, monitor="val_acc")],
    max_epochs=100,
)
```

### 5. Multi-Objective Optimization

```python
def objective(trial):
    accuracy = train_and_get_accuracy(trial)
    latency_ms = measure_latency(trial)
    return accuracy, latency_ms  # Return tuple

study = optuna.create_study(
    directions=["maximize", "minimize"],
    sampler=optuna.samplers.NSGAIISampler(),
)

study.optimize(objective, n_trials=200)

# Get Pareto front
best_trials = study.best_trials
for trial in best_trials:
    print(f"Params: {trial.params}, Values: {trial.values}")
```

### 6. Distributed / Parallel Execution

**Single-machine multi-process:**
```python
study.optimize(objective, n_trials=100, n_jobs=8)  # 8 parallel workers
```

**Multi-node via shared storage (SQLite):**
```python
# On all nodes, share the same study name and storage
study = optuna.create_study(
    study_name="distributed_study",
    storage="sqlite:///optuna_study.db",
    load_if_exists=True,
)
study.optimize(objective, n_trials=500)
```

**Multi-node via RDB (PostgreSQL/MySQL):**
```python
study = optuna.create_study(
    study_name="large_scale_study",
    storage="postgresql://user:pass@host:5432/optuna",
    load_if_exists=True,
)
```

### 7. Visualization

```python
from optuna.visualization import (
    plot_optimization_history,
    plot_param_importances,
    plot_parallel_coordinate,
    plot_contour,
    plot_slice,
)

# Optimization progress over trials
plot_optimization_history(study)

# Hyperparameter importance ranking
plot_param_importances(study)

# Parallel coordinate plot for high-dimensional analysis
plot_parallel_coordinate(study)

# Slice plot showing parameter-value relationship
plot_slice(study)

# Contour plot for pairwise parameter interactions
plot_contour(study, params=["learning_rate", "n_layers"])
```

**Web Dashboard (optuna-dashboard):**
```bash
pip install optuna-dashboard
optuna-dashboard sqlite:///optuna_study.db
# Opens at http://localhost:8080
```

### 8. PyTorch Lightning Integration

```python
import pytorch_lightning as pl
import optuna
from optuna.integration import PyTorchLightningPruningCallback

def objective(trial):
    # Suggest hyperparameters
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 128, 256])
    n_layers = trial.suggest_int("n_layers", 1, 6)

    model = MyLightningModule(lr=lr, n_layers=n_layers)
    trainer = pl.Trainer(
        max_epochs=50,
        callbacks=[PyTorchLightningPruningCallback(trial, monitor="val_loss")],
        logger=False,
    )
    trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader)

    return trainer.callback_metrics["val_loss"].item()

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=50)
```

### 9. HuggingFace Transformers Integration

```python
from transformers import Trainer, TrainingArguments
import optuna

def hp_space(trial):
    return {
        "learning_rate": trial.suggest_float("learning_rate", 1e-6, 1e-4, log=True),
        "per_device_train_batch_size": trial.suggest_categorical("batch_size", [8, 16, 32]),
        "num_train_epochs": trial.suggest_int("num_epochs", 1, 5),
        "warmup_ratio": trial.suggest_float("warmup_ratio", 0.0, 0.3),
    }

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

best_run = trainer.hyperparameter_search(
    hp_space=hp_space,
    n_trials=30,
    direction="minimize",
)
```

### 10. Artifact and Attribute Storage

```python
def objective(trial):
    model = train_model(trial)
    # Store arbitrary attributes
    trial.set_user_attr("model_architecture", str(model))
    trial.set_user_attr("training_time_seconds", 3600)
    return evaluate(model)

# Retrieve later
for trial in study.trials:
    print(trial.user_attrs.get("training_time_seconds"))
```

## Installation

```bash
pip install optuna
# Optional: dashboard
pip install optuna-dashboard
# Optional: OptunaHub features
pip install optunahub
```

## Key Patterns for ML Training

1. **Always use `log=True` for learning rates, batch sizes, and other scale-sensitive params**
2. **Set `n_startup_trials` to 10-20 for TPE to warm up with random exploration**
3. **Use pruning aggressively for expensive deep learning trials — saves 50-80% compute**
4. **For reproducibility, set `seed` on both sampler and `study.optimize()`**
5. **Store intermediate values with `trial.report()` even if not pruning — enables better analysis**

## References

- [Optuna Documentation](https://optuna.readthedocs.io/en/stable/)
- [Optuna Examples](https://github.com/optuna/optuna-examples)
- [OptunaHub](https://hub.optuna.org/) — community-contributed samplers, pruners, and visualization
- [Optuna Dashboard](https://github.com/optuna/optuna-dashboard)

See `scripts/optuna_lightning_template.py` for a complete PyTorch Lightning + Optuna training template.
See `references/advanced_samplers.md` for detailed sampler comparison and selection guidance.
