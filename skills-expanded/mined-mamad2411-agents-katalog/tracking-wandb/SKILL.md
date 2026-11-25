---
name: tracking-wandb
description: >
  Recording experiments with Weights & Biases — every train/eval run becomes a tracked, comparable,
  reproducible record. Carries: `wandb.init(project=...)` to open a run, `wandb.log({...}, step=)`
  for per-step curves, `wandb.config` for the resolved hyperparams, artifacts for
  checkpoints/plots/the composed config, tags + run names for organizing, and comparing runs in the
  W&B UI. Load when a train/eval loop needs to record what it did, when a past result can't be
  found, or when setting up tracking on a new box; `training`/`evaluation` call this to log; pair
  with `config-hydra` to log the composed config. Triggers: wandb, weights and biases, wandb.init,
  wandb.log, experiment tracking, track this run, log metrics/params/artifacts, compare runs, run
  name, where did that result go, WANDB_API_KEY, wandb offline.
---

# tracking-wandb — recording experiments so they're comparable & reproducible

**Pinned:** wandb — unpinned · authored against 0.x (2026-07) · run `/skill-update tracking-wandb` once the dep is installed

> On-demand: load this before adding tracking to a train/eval loop, or when you can't reconstruct what a
> past run did. A run is only worth logging if it's **reproducible** — the resolved config + code version
> must be in it (see the closing rule). Never hand-roll a CSV logger where a run belongs.

## When this applies
Instrumenting a train or eval loop to record params/metrics/artifacts, organizing runs into projects,
running on a box without egress (offline mode), or comparing runs to pick a winner. The `training` and
`evaluation` skills defer here for the *how* of logging; this skill owns it.

## Open a run
One `wandb.init` per run, as a context manager so it finishes and flushes on exit — including on
exception. Pass the **resolved** config at init; it becomes the run's searchable params:

```python
import wandb
from omegaconf import OmegaConf

with wandb.init(
    project="<PLACEHOLDER: project name, e.g. detector-baselines>",
    name=run_name,                                        # short human handle, not the random slug
    config=OmegaConf.to_container(cfg, resolve=True),     # the config as ACTUALLY used (see config-hydra)
) as run:
    ...  # everything below logs into this run
```
- **Name runs meaningfully** — a short, scannable handle (`r50-fpn-lr3e-4`, `sweep-trial-017`). The
  workspace run table is only as readable as your names.
- **One project per line of investigation** (a model family, a dataset, a paper); trials/sweeps are the
  runs inside it. `entity=` selects the team namespace; set it once via `WANDB_ENTITY` in `.env` rather
  than in code.

## What to log (and when)
- **Params — the resolved config, once, at init.** Passed via `config=` above: hyperparameters and paths
  as they were *actually* used (post-composition, post-override), not the defaults. Late additions:
  `run.config.update({...})`.
- **Metrics — per step, with `step=`.** `wandb.log({"train/loss": loss}, step=global_step)` and
  `wandb.log({"val/mAP": score}, step=epoch)`. Namespace with `train/` `val/` `test/` prefixes — the UI
  groups panels by prefix. Batch related scalars into one `wandb.log` call per step; each call is a row.
- **Artifacts — files worth keeping.** Checkpoints, PR/confusion-matrix plots, sample predictions, and
  **the composed config file**:
  ```python
  art = wandb.Artifact(f"{run.name}-model", type="model")
  art.add_file("models/best.pt")
  run.log_artifact(art)
  ```
  Artifacts are versioned (`:v0`, `:v1`, `:latest`) and deduplicated by content — logging the same bytes
  twice costs nothing.
- **Tags — searchable run metadata.** `wandb.init(tags=["smoke"])` or `run.tags += (...,)` — anything
  you'll later filter the run table on.

## Watch the model (the fast path)
`wandb.watch(model, log="all", log_freq=100)` after building the model logs gradient and parameter
histograms automatically. Call it once, then still **explicitly log the resolved config + git SHA**
(watch won't capture your Hydra composition or code version) and any custom metrics it doesn't know
about. `watch` and manual `wandb.log` coexist — watch for the boilerplate, manual for what's
project-specific.

## Where runs are stored (auth + offline)
- **Auth: `WANDB_API_KEY` in `.env`** — never in code, never committed (`.env` is gitignored and the
  settings deny-list blocks reading it). One-time interactive alternative: `uv run wandb login`.
- **No egress from the GPU box? `WANDB_MODE=offline`** (in `.env`) — runs record locally under `wandb/`
  and nothing is sent. Ship them later from a connected machine:
  `uv run wandb sync wandb/offline-run-*`. This is the normal mode for an airgapped or firewalled box.
- **`wandb/` is a local cache, not the record** — it's gitignored (already in this scaffold's
  `.gitignore`); the record of truth is the W&B server after sync. Version shareable artifacts via
  `data-dvc` if they must live with the repo.
- Read tracking settings from the config system, **not** `os.environ` mid-logic — per the *config over
  constants* always-on convention (see `config-hydra`); the config interpolates the env var in one place
  (`project: ${oc.env:WANDB_PROJECT}`), and `WANDB_MODE`/`WANDB_API_KEY` stay in `.env` where the
  `wandb` library reads them itself.

## Compare runs
- **The workspace** (wandb.ai → your entity → project): sort the run table by a metric, multi-select
  runs to overlay curves, diff their configs, build a report from the comparison.
- Programmatic: `wandb.Api().runs("entity/project")` returns run objects with `.config`, `.summary`,
  and `.history()` (a DataFrame) for scripted comparison and to feed the `eval-analyst` agent's error
  analysis.

## Gotcha
A run without the **resolved config + code version (git SHA)** isn't reproducible — it's a number you
can't regenerate. Log both every run: the composed config via `config=` at init (from `config-hydra`)
and the SHA as config/tag (`run.config.update({"git_sha": sha})`; note a dirty tree). W&B captures a
git SHA automatically when it detects a repo — **verify it did**, don't assume. And **never log secrets
or raw data** — tracking stores are broadly readable; config/tags/artifacts are the wrong place for
credentials, PII, or dataset contents. This is the reproducibility always-on convention made concrete;
the handling rules for sensitive data live in the `governance` skill (`.claude/memory/policy/`).
