---
name: python-quality-gate
description: Python code quality enforcement with Ruff, pyright, Vulture, and deptry for linting, formatting, type checking, dead code, and dependency hygiene
triggers:
  - python quality
  - code quality
  - ruff
  - pyright
  - dead code
  - vulture
  - type check
  - lint
---

# Python Quality Gate

Enforces code quality for Python 3.10+ projects using Ruff (lint+format), pyright (types), Vulture (dead code), and deptry (deps).

## One-Command Quality Check

```bash
# Run all quality checks
just check  # or manually:
ruff check --fix src/ tests/ && ruff format src/ tests/
pyright src/
vulture src/ --min-confidence 80
deptry src/
```

## Ruff (Linter + Formatter)

Ruff replaces flake8, isort, black, pyupgrade, and bandit. It's 100x faster.

```bash
# Auto-fix and format
ruff check --fix src/ tests/
ruff format src/ tests/

# Check without fixing
ruff check src/ tests/

# Show what would change
ruff format --diff src/ tests/
```

Key rules enabled: E/W (pycodestyle), F (pyflakes), I (isort), UP (pyupgrade), B (bugbear), S (bandit security), SIM (simplify), RUF (ruff-specific).

## pyright (Type Checker)

```bash
# Standard mode (recommended starting point)
pyright src/

# Strict mode (aspirational)
pyright src/ --pythonversion 3.10 --level strict
```

Common fixes:
- Add return type annotations to all public functions
- Use `Optional[X]` or `X | None` for nullable params
- Use `TypeVar` for generic functions
- Add `py.typed` marker file for library packages

## Vulture (Dead Code Detection)

```bash
# Find unused code (80% confidence threshold)
vulture src/ --min-confidence 80

# Whitelist known false positives
vulture src/ vulture_whitelist.py --min-confidence 80
```

Create `vulture_whitelist.py` for false positives:
```python
# vulture_whitelist.py - known used code that Vulture can't detect
from coremind.api.main import app  # Used by uvicorn
from coremind.core.types import *  # Re-exported for public API
```

## deptry (Dependency Hygiene)

```bash
# Find unused, missing, and transitive dependencies
deptry src/

# Ignore known false positives
deptry src/ --ignore DEP002 --per-rule-ignores "DEP001=uvicorn"
```

## Pre-commit Integration

All tools run automatically via pre-commit hooks (see .pre-commit-config.yaml). Manual full check: `pre-commit run --all-files`.

## Quality Targets

| Metric | Target | Tool |
|--------|--------|------|
| Lint errors | 0 | Ruff |
| Type coverage | >80% public APIs | pyright |
| Dead code | <5 findings | Vulture |
| Unused deps | 0 | deptry |
| Security findings | 0 HIGH/CRITICAL | Ruff S rules + Bandit |
