---
description: Install Python packages, access Python CLI, run python code and scripts, execute Python commands, and manage Python environments. Use uv run for all Python execution instead of direct python commands.
alwaysApply: false
---
# Python Package Management with uv

Use uv exclusively for Python package management. Never use pip, pip-tools, poetry, or conda directly.

## Commands

- Install: `uv add <package>`
- Remove: `uv remove <package>`
- Sync: `uv sync`
- Run scripts/tools: `uv run <script>.py` or `uv run pytest`
- Python REPL: `uv run python`

## Monorepo Usage

**Always run commands from the repo root** (where `uv.lock` lives). Use path arguments to target services:

- Tests: `uv run pytest services/{name}/tests/`
- Linting: `uv run ruff check services/{name}/`