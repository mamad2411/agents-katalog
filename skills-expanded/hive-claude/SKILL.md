# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project structure

Three-package Python monorepo:
- `packages/hive-engine/` — core game engine
- `packages/hive-agents/` — AI agents and search algorithms
- `services/hive-api/` — API service (early stage)

## Setup and commands

Dependency management uses `uv`. Python 3.13.x is required (no other minor versions).

```
make sync          # sync all packages (runs uv sync --all-groups --all-extras per package)
make format        # ruff format all packages
make lint          # ruff check --fix all packages
make type          # ty check all packages (ty, not mypy)
make check         # format + lint + type (no tests)
make test          # pytest all packages
```

Run these from the repo root to affect all packages, or from an individual package directory to target just that package.

## Code style

- Line length: 90 characters
- All public functions and methods require type annotations (enforced by `ANN` rules)
- All public classes and functions require docstrings (enforced by `D` rules)
- No `print` statements (enforced by `T20` — use logging instead)
- `notebooks/**` is excluded from ruff linting/formatting
- `uv.lock` files are intentionally committed — do not delete or gitignore them
- Use single backticks (`` `code` ``) for inline code in docstrings, not double backticks
- Reflow docstring text to fill up to the 90-character limit — do not wrap earlier

## Type checking

Uses `ty` (Astral-sh) — not mypy. Run via `make type`.

## Testing

Tests live in `tests/` within each package (not colocated with source). Run a single test with:
```
uv run pytest tests/path/to/test_file.py::test_name
```

## Git workflow

- Branch naming: `feature/`, `fix/`, `chore/` prefixes
- Commit messages must follow conventional commits format (enforced by commitizen pre-commit hook)
- Install pre-commit hooks once with `make install-pre-commit`
