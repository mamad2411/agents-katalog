---
description: Agent workflow — rules, skills, verification, and task routing
alwaysApply: true
---

# Agent Workflow

## Context layers (read in order)

1. **Always-on rules** — `project-core`, `tech-stack`, this file
2. **File rules** — auto-attach when editing matching paths (see table below)
3. **Task skills** — `.cursor/skills/*/SKILL.md`; read the matching skill **before** implementing

Manually attached skills override generic routing.

## Task routing

| User intent | Skill | File rules (when editing) |
|-------------|-------|---------------------------|
| New feature, CLI, config knob | `feature-generation` | `architecture`, `config-toml` |
| Train, resume, tune, `metrics.jsonl` | `training-workflow` | `training-pipeline`, `config-toml` |
| Wrong fitness, train/eval mismatch | `debug-simulation` | `architecture`, `physics-simulation` |
| Server, WebSocket, `web/dist/` | `viz-studio` | `server-viz-studio`, `architecture` |
| Tests, coverage, regression | `add-tests` | `testing` |
| Refactor without behavior change | `refactoring-code` | `architecture` |
| NEAT genome / speciation / crossover | — | `neat-algorithm` |
| Physics / RK4 / observations | — | `physics-simulation` |

## File rules reference

| Rule | Globs |
|------|-------|
| `architecture` | `pendulum_neat/**`, `neat/**`, `physics/**`, `viz/**`, `server/**`, `training/**` |
| `training-pipeline` | `pendulum_neat/training/**`, `training/**`, `evaluator.py`, `checkpoints.py` |
| `neat-algorithm` | `neat/**` |
| `physics-simulation` | `physics/**` |
| `config-toml` | `**/*.toml`, `config.py` |
| `testing` | `tests/**` |
| `server-viz-studio` | `server/**`, `web/**` |

## Default loop

1. **Scope** — smallest correct diff; no drive-by refactors
2. **Read** — target module, peers, and relevant tests
3. **Skill + rules** — open matching skill; file rules apply automatically when editing
4. **Implement** — one fitness path (`Evaluator`), config via TOML, match existing style
5. **Verify** — `pytest tests/ -v`; smoke `configs/demo.toml` when training/viz touched
6. **Commit** — only when the user explicitly asks

## Hard stops (ask first)

- Renaming WebSocket `frame_dict` keys or public CLI flags
- Changing `EpisodeResult` semantics or NEAT compatibility distance
- Adding npm/webpack, PyTorch, or JAX
- Multi-minute training runs in tests or CI

## Commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
pendulum-neat train --config configs/demo.toml
pendulum-neat eval --checkpoint output/runs/<run>/best_genome.pkl
pendulum-neat serve --open
```
