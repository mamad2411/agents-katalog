---
description: TOML configuration schema, validation, and preset conventions
globs: **/*.toml,**/config.py
alwaysApply: false
---

# Configuration

## Known sections

`neat`, `physics`, `simulation`, `curriculum`, `fitness`, `viz`, `web`, `training`

Unknown sections trigger warnings in `pendulum_neat.config._validate()`.

## Presets

| File | Purpose |
|------|---------|
| `config.toml` | Default / local dev |
| `configs/demo.toml` | Fast smoke: tiny pop, 1 gen, curriculum off |
| `configs/full.toml` | Full training: large pop, curriculum, parallel eval |

## Key defaults (set in `load_config`)

```python
neat.parallel_workers = 1
neat.fitness_metric = "time_above"
curriculum.advance_metric = "time_above"
curriculum.enabled = True  # overridden to false in demo.toml
```

## Rules when editing config

- Add new keys to `_validate()` defaults in `pendulum_neat/config.py` if they need project-wide fallbacks.
- Use `episode_max_steps(config)` for episode length — respects `curriculum.episode_seconds` when enabled.
- Mirror changes across `config.toml`, `configs/demo.toml`, and `configs/full.toml` only when the key applies to all presets.
- Training runs copy config into `output/runs/<timestamp>/config.toml` — runtime edits do not retroactively change old runs.

## Curriculum knobs

- `advance_metric`: usually `time_above` (seconds upright), not composite `score`.
- `advance_threshold`: metric value required for N consecutive generations before ramping gravity/friction.
