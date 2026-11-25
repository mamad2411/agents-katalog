---
name: config-omegaconf
description: >
  Run configuration with plain OmegaConf (no Hydra) — YAML files merged with CLI dotlist
  overrides, by hand but leakage-free. Carries: `OmegaConf.load` + `OmegaConf.merge(base,
  exp_file, OmegaConf.from_cli())` as the composition order, structured configs (dataclass
  schema merged first so typos and wrong types fail fast), `${...}` interpolation +
  `${oc.env:VAR}`, `MISSING` for required fields, and `OmegaConf.to_container(cfg,
  resolve=True)` to snapshot the exact config for logging. Load when adding a hyperparameter,
  wiring config, or overriding from the CLI in a non-Hydra project. Triggers: omegaconf, config
  without hydra, OmegaConf.load, OmegaConf.merge, from_cli, dotlist, structured config,
  interpolation, oc.env, MISSING, resolve, to_container, config yaml, override from CLI,
  hyperparameter.
---

# config-omegaconf — composed config without the Hydra framework

**Pinned:** omegaconf — unpinned · authored against 2.3 · run `/skill-update config-omegaconf`
once the dep is installed

> On-demand: the config system when `/intake` chose plain OmegaConf over Hydra — same
> config-over-constants convention, same "log the composed config" contract with the tracker
> skills, but composition is explicit in your entry point instead of `@hydra.main`. **Note:**
> `/bootstrap`'s skeleton is Hydra-shaped — with this choice, adapt the entry points to the
> pattern below (no decorator, no auto output dir; you own both).

## The composition pattern (the whole trick)
One explicit merge, least→most specific, in every entry point:

```python
from dataclasses import dataclass, field
from omegaconf import OmegaConf, MISSING

@dataclass
class TrainConfig:                      # the schema — typos fail here, not mid-run
    seed: int = 42
    epochs: int = MISSING               # MISSING = required; raises on first access if unset
    lr: float = 3e-4
    data_dir: str = "${oc.env:DATA_ROOT}/${dataset}"
    dataset: str = MISSING

def load_config(argv_overrides=True) -> TrainConfig:
    cfg = OmegaConf.merge(
        OmegaConf.structured(TrainConfig),          # 1. typed schema (defaults + required)
        OmegaConf.load("conf/config.yaml"),         # 2. base file
        *(OmegaConf.load(p) for p in exp_files),    # 3. optional experiment file(s)
        OmegaConf.from_cli() if argv_overrides else {},  # 4. CLI dotlist: lr=1e-4 dataset=widgets
    )
    return cfg
```

- **Merge order is precedence** — later wins. Keep it identical in `train.py` and `eval.py`
  (one shared `load_config`), or the two compose different configs from the same files.
- **Schema first** buys struct-mode safety: merging a YAML/CLI key the dataclass doesn't
  declare raises instead of silently adding it — the same typo protection Hydra gives.
- **CLI overrides are dotlist**: `uv run python train.py lr=1e-4 model.depth=50`. No `--`
  flags, no argparse needed; if you must mix argparse (e.g. `--config-file`), parse yours
  first and pass the remainder to `OmegaConf.from_dotlist()`.

## Interpolation + environment
`${other.key}` cross-references; `${oc.env:DATA_ROOT}` reads the **process** environment — it
does not read `.env`, so entry points call `load_env()` first (the load-order rule `/bootstrap` wires into every entry point;
`/bootstrap` emits `src/<pkg>/env.py`). Fail-fast alternative with a default:
`${oc.env:DATA_ROOT,./data}`.

## The logging contract (unchanged from Hydra)
Before training starts, snapshot what actually ran:
```python
resolved = OmegaConf.to_container(cfg, resolve=True)   # plain dict, interpolations resolved
```
Log `resolved` as params + save `OmegaConf.to_yaml(cfg)` as an artifact via the active tracker
skill. A run without its composed config is unreproducible — same rule, no framework.

## What you gave up vs Hydra (own these by hand)
- **No per-run output dir** — create one (`runs/{time.strftime(...)}-{run_name}/`) and write
  the composed config into it.
- **No `-m` multirun** — sweep with a shell loop over dotlist overrides, or graduate to
  `hpo-optuna` when the space outgrows loops.
- **No config groups / defaults list** — emulate with experiment files
  (`conf/exp/baseline.yaml`) merged in step 3; keep them small diffs against the base, not
  forks of it.
