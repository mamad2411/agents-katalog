---
description: Core project conventions for pendulum-neat — scope, imports, and agent behavior
alwaysApply: true
---

# Project Core

## What this repo is

NEAT neuroevolution trains controllers for a **double inverted pendulum on a cart**. Python drives training, physics, and the FastAPI server; `web/dist/` is a prebuilt Three.js Viz Studio frontend.

## Agent principles

- **Minimize scope**: smallest correct diff; no drive-by refactors or unrelated formatting.
- **Match existing style**: `from __future__ import annotations`, type hints, module docstrings where peers have them.
- **One fitness path**: all simulation scoring goes through `pendulum_neat.evaluator.Evaluator` — never duplicate episode loops.
- **Config-driven behavior**: prefer TOML keys in `config.toml` / `configs/` over hard-coded constants.
- **Do not commit** `output/`, `.venv/`, or generated run artifacts.

For task routing, skills, and verification steps see `agent-workflow.mdc`.

## Package layout (canonical)

| Package | Role |
|---------|------|
| `pendulum_neat/` | CLI, config, evaluator, checkpoints, training runner |
| `neat/` | NEAT algorithm (genome, population, speciation) |
| `physics/` | RK4 double-pendulum simulation + fitness helpers |
| `training/` | `CurriculumManager` — canonical import: `from training.curriculum import ...` |
| `viz/` | Trajectory recorder, network graph JSON |
| `server/` | FastAPI + WebSocket Viz Studio backend |
| `web/dist/` | Static frontend (no build step in CI) |

Note: `pendulum_neat/training/curriculum.py` re-exports `training.curriculum`; follow imports used by `runner.py`.

## When changing behavior

1. Read surrounding module and its tests first.
2. Update or add tests in `tests/` for non-trivial logic.
3. Run `pytest tests/ -v` before finishing.
4. Only create git commits when the user explicitly asks.
