# Agent instructions

NEAT neuroevolution for a double inverted pendulum on a cart. Python training + FastAPI Viz Studio.

## Start here

| Resource | Purpose |
|----------|---------|
| [`.cursor/rules/agent-workflow.mdc`](.cursor/rules/agent-workflow.mdc) | Task routing, verification loop, hard stops |
| [`.cursor/README.md`](.cursor/README.md) | Full index of rules and skills |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Data flow and module boundaries |

## Non-negotiables

- **One fitness path** — all simulation scoring through `pendulum_neat.evaluator.Evaluator`
- **Config-driven** — TOML keys in `config.toml` / `configs/`, not hard-coded constants
- **Minimize scope** — smallest correct diff; run `pytest tests/ -v` before finishing
- **No commits** unless the user explicitly asks

## Quick commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
pendulum-neat train --config configs/demo.toml
pendulum-neat eval --checkpoint output/runs/<run>/best_genome.pkl
pendulum-neat serve --open
```

## Task → skill

| Intent | Skill |
|--------|-------|
| New feature / CLI | `feature-generation` |
| Training / tuning | `training-workflow` |
| Fitness / physics bugs | `debug-simulation` |
| Viz Studio / server | `viz-studio` |
| Tests | `add-tests` |
| Refactoring | `refactoring-code` |

Skills live in `.cursor/skills/<name>/SKILL.md`.
