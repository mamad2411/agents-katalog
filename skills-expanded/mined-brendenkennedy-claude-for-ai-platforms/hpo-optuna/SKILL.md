---
name: hpo-optuna
description: >
  Hyperparameter optimization with Optuna — studies, trials, pruning, and the leakage-safe
  protocol. Carries: `create_study(direction=..., sampler=TPESampler(seed=...),
  pruner=MedianPruner())`, `trial.suggest_float/int/categorical` (log=True for learning rates),
  mid-training `trial.report` + `should_prune` to kill bad trials early, `storage=
  "sqlite:///optuna.db"` for resume + parallel workers, and the discipline: tune on VAL only
  (test stays untouched), seed every trial, log every trial to the tracker, then retrain the best
  config and evaluate ONCE on test. Load when a search outgrows Hydra multirun grids or needs
  pruning/resume. Triggers: optuna, hyperparameter search, HPO, tune hyperparameters, sweep,
  trial, study, TPE, pruner, prune trials, suggest_float, best_trial, bayesian optimization,
  random search, search space.
---

# hpo-optuna — hyperparameter search that doesn't cheat

**Pinned:** optuna — unpinned · authored against 4.x · run `/skill-update hpo-optuna` once the
dep is installed

> On-demand: load this when grid sweeps (`config-hydra` multirun) stop being enough — large
> spaces, expensive trials worth pruning, or resumable/parallel search. The non-negotiable it
> exists to protect: **HPO is model selection, so it runs on validation only** — a search that
> ever reads the test metric has spent the test set.

## When this applies — and when multirun is enough
A handful of discrete combos → `uv run python train.py -m optimizer.lr=1e-3,3e-4` and read the
tracker; done. Reach for Optuna when the space is continuous/conditional, trials are costly
enough that pruning pays, or the search must survive restarts and share workers.

## The canonical shape
```python
import optuna
from optuna.samplers import TPESampler
from optuna.pruners import MedianPruner

def objective(trial: optuna.Trial) -> float:
    lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)      # log=True for rates/weight decay
    wd = trial.suggest_float("weight_decay", 1e-6, 1e-2, log=True)
    overrides = {"optimizer.lr": lr, "optimizer.weight_decay": wd, "seed": cfg.seed}
    for epoch, val_metric in train_epochs(overrides):          # your train entry, VAL metric out
        trial.report(val_metric, step=epoch)
        if trial.should_prune():
            raise optuna.TrialPruned()
    return val_metric                                          # VALIDATION metric. Never test.

study = optuna.create_study(
    study_name=cfg.hpo.study_name,
    direction="maximize",
    sampler=TPESampler(seed=cfg.seed),                         # seeded sampler = reproducible search
    pruner=MedianPruner(n_warmup_steps=2),
    storage="sqlite:///optuna.db", load_if_exists=True,        # resume + parallel workers
)
study.optimize(objective, n_trials=cfg.hpo.n_trials)
```
Parallelize by running the same script on N workers against the same storage; SQLite handles a
single box, use a real DB across machines.

## The protocol around the loop
1. Search space + budget are **written before the search** (PROCESS.md §3.6 — a question and a
   compute budget, in `conf/` not code; the space is config like everything else).
2. **Every trial is a tracked run** — log trial params + VAL metric to the active tracker
   (`mlflow` nested runs or a `trial=<n>` tag) so the search is auditable; `optuna.db` is search
   state, not the record.
3. **After the search:** take `study.best_trial.params`, retrain on train (fresh seed, full
   schedule), evaluate **once** on test, and log that run as the candidate. The best-trial VAL
   number is not the reported number — selection bias inflates it (that's *why* test exists).
4. Best params + the decision to adopt them → decision log; the config change lands in `conf/`.

## Gotchas
- **Pruning + noisy first epochs kill good trials** — set `n_warmup_steps` past the noise.
- **A seeded sampler is not a deterministic search** when trials run in parallel (completion
  order feeds TPE) — reproducibility of the *winner's retrain* is what matters; that's why step 3
  retrains from config + seed.
- Conditional spaces (`suggest_categorical("scheduler", ...)` then per-branch params) are fine —
  but keep the space in config so the study is re-runnable from the repo alone.
