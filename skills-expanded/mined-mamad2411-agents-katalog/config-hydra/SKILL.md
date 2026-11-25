---
name: config-hydra
description: >
  Run configuration with Hydra (on OmegaConf) — the `conf/` tree of config groups, `@hydra.main`,
  the defaults list, CLI overrides, and multirun sweeps. Carries the commands that work today: `uv
  run python train.py optimizer=adamw optimizer.lr=3e-4` to override, `-m optimizer.lr=1e-3,3e-4` to
  sweep, structured/typed configs via dataclasses, `${...}` interpolation, the per-run output dir,
  and `OmegaConf.to_container(cfg, resolve=True)` to snapshot the exact config that ran so it can be
  logged. Load when adding a hyperparameter, wiring a new config group, running a sweep, or asking
  where a value comes from. Triggers: hydra, omegaconf, config, conf/, config group, defaults list,
  @hydra.main, override, multirun, sweep, structured config, interpolation, MISSING, hydra output
  dir, resolve config, hyperparameter, where does this value come from.
---

# config-hydra — composing run config with Hydra

**Pinned:** hydra-core, omegaconf — unpinned · authored against hydra-core 1.3 · run `/skill-update config-hydra` once the dep is installed

> On-demand: load this before adding a hyperparameter, wiring a config group, running a sweep, or when
> tracing where a value came from. Hydra **composes** the config that runs from many small files plus CLI
> overrides — the composed object is the source of truth, so resolve and log it (see `tracking-mlflow`).
> This backs the always-on **config-over-constants** convention; policy detail lives in `governance`.

## When this applies
Adding or moving a hyperparameter/path into config, creating a new config group (optimizer, model,
dataset, …), running or sweeping over overrides, typing a config with dataclasses, or debugging why a
value resolved the way it did.

## The `conf/` layout (config groups)
Each subdirectory is a **config group**; each `.yaml` inside is one selectable option for that group.

```
conf/
  config.yaml            # top-level: the defaults list + run-wide values
  model/
    resnet50.yaml
    vit_b16.yaml
  optimizer/
    adamw.yaml
    sgd.yaml
  dataset/
    <PLACEHOLDER: your_dataset>.yaml
```

The top-level `config.yaml` picks one option per group via the **defaults list**:

```yaml
# conf/config.yaml
defaults:
  - model: resnet50
  - optimizer: adamw
  - dataset: <PLACEHOLDER: your_dataset>
  - _self_            # _self_ placement decides whether this file's keys win over the groups

seed: 42
epochs: 90
optimizer:
  lr: 3e-4            # a value a group file may also set; last writer in the list wins
```

## The entry point (`@hydra.main`)
The train/eval entry points are decorated with Hydra; see the `training` skill for the loop itself.

```python
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    ...

if __name__ == "__main__":
    main()   # Hydra parses argv, composes cfg, and creates the per-run output dir
```

- `version_base=None` opts into current-Hydra behavior (no legacy compatibility shims).
- `config_path` is relative to the file the decorator lives in; `config_name` drops the `.yaml`.

## CLI overrides & multirun sweeps
Everything is overridable from the command line — no code edit to change a run:

```bash
# swap a whole group option, then tweak one field inside it
uv run python train.py optimizer=adamw optimizer.lr=3e-4 epochs=50

# add a key not in the config: +key=val   remove one: ~key
uv run python train.py +trainer.grad_clip=1.0

# multirun (-m / --multirun): the comma list is a sweep, one run per combination
uv run python train.py -m optimizer.lr=1e-3,3e-4 model=resnet50,vit_b16
```

> **Struct mode: you can only override a key the config already declares.** `key=val` on a key that isn't
> in the composed config fails with `ConfigCompositionException: Could not override 'key' ... use +key=`.
> The `+` exists for genuine one-offs — it is **not** the fix for a key your entry point always needs.
> Declare those in `config.yaml` with a `null` default. The two that bite every project:
> `ckpt: null` (so `eval.py ckpt=models/best.pt` works) and `resume: null` (so `train.py
> resume=models/last.pt` works). Miss `resume` and everything passes until the day you need to resume.

The last line launches 4 runs (2 lrs × 2 models). Log each one with `tracking-mlflow` so the sweep is
comparable.

## Structured (typed) configs
Back the config with dataclasses to get type-checking and fail-fast on unknown/missing keys:

```python
from dataclasses import dataclass, field
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING

@dataclass
class OptimizerConf:
    name: str = "adamw"
    lr: float = 3e-4

@dataclass
class TrainConf:
    seed: int = 42
    epochs: int = 90
    optimizer: OptimizerConf = field(default_factory=OptimizerConf)
    dataset: str = MISSING          # no default → must be supplied, else Hydra errors at compose

cs = ConfigStore.instance()
cs.store(name="base_config", node=TrainConf)
```

`MISSING` makes an omitted required value a loud compose-time error, not a silent `None`.

## Interpolation (`${...}`)
Reference other config values instead of repeating them — resolved lazily at access:

```yaml
run_name: ${model.name}_lr${optimizer.lr}      # e.g. resnet50_lr0.0003
data_dir: ${oc.env:DATA_ROOT}/<PLACEHOLDER: dataset>   # env read stays in config, not business logic
```

Keep `${oc.env:...}` reads **in the config layer** — never `os.environ` in the middle of a train loop
(config-over-constants; see `governance`).

## Per-run output dir
Hydra creates a fresh working dir per run (default `outputs/YYYY-MM-DD/HH-MM-SS/`, or a sweep dir under
`multirun/` with `-m`) and `chdir`s into it, writing the composed config to `.hydra/config.yaml`. Resolve
paths against the **original** cwd via `hydra.utils.get_original_cwd()` or use absolute paths, or a
relative `open(...)`/`load(...)` will silently look inside the run dir.

**Where things go** (Hydra's docs say "keep everything in the run dir"; that conflicts with `data-dvc`,
which needs one *stable* path to track — resolve it like this):
- **Data in, checkpoints out, at the *original* cwd** — `Path(get_original_cwd()) / "models" / "best.pt"`.
  DVC cannot track a path with a timestamp in it.
- **Everything else in the run dir** — logs, plots, the resolved `.hydra/config.yaml`. Per-run, disposable.

The tracker is what reconciles the two: log the checkpoint as a run artifact, so the *run* keeps its own
copy even though the file on disk lives at a stable path.

## Snapshot the config that actually ran (log it)
The composed `cfg` — not the source YAML — is what ran. Resolve interpolations and hand a plain container
to your tracker:

```python
cfg_snapshot = OmegaConf.to_container(cfg, resolve=True)   # dict with all ${...} expanded
mlflow.log_params(flatten(cfg_snapshot))                   # or log the yaml as an artifact
```

`tracking-mlflow` covers the logging side. `resolve=True` is the point: it freezes the interpolated
values so the record matches the run, even if a referenced default later changes.

## Gotcha
The composed config that Hydra built for **this** run is the single source of truth — resolve it with
`OmegaConf.to_container(cfg, resolve=True)` and log it. Don't reconstruct "what config ran" from the
source YAML (overrides and interpolation make them differ), don't read `os.environ` or hardcode constants
inside business logic, and remember `-m` changes cwd to a sweep dir — resolve input paths against the
original cwd or they'll silently miss.
