---
description: pytest conventions, test layout, and verification workflow
globs: tests/**/*.py
alwaysApply: false
---

# Testing

## Runner

```bash
pytest tests/ -v
```

Config in `pyproject.toml`: `testpaths = ["tests"]`.

## Test modules

| File | Focus |
|------|-------|
| `test_smoke.py` | End-to-end one-generation training with `configs/demo.toml` |
| `test_pendulum.py` | Physics / RK4 correctness |
| `test_fitness.py` | Fitness scoring |
| `test_neat_*.py` | Speciation, crossover, cycle detection, population |
| `test_curriculum_checkpoints.py` | Curriculum advancement, checkpoint round-trips |
| `test_viz_recorder.py` | Trajectory JSON export |

## Conventions

- Use `configs/demo.toml` or inline TOML for fast tests — never `configs/full.toml` in unit tests.
- Prefer `tempfile.TemporaryDirectory()` for run dirs; never write to `output/` in tests.
- Seed RNGs when determinism matters (`training.seed`, `DoublePendulumCart(..., seed=42)`).
- Name tests `test_<behavior>()` with docstrings only when the behavior is non-obvious.

## What to test

- **Do**: algorithm invariants, physics edge cases, evaluator scoring, checkpoint round-trips.
- **Don't**: full 200-generation training runs, matplotlib pixel output, browser UI.

## After code changes

1. Run affected tests: `pytest tests/test_<area>.py -v`
2. Run full suite before marking work complete.
3. CI must pass — no skipped hooks or `--no-verify` unless the user requests it.
