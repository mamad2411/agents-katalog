---
name: follow-lang-python
description: Python project guidelines with best practices, ruff, pyright, and Clean Architecture
argument-hint: "[scope|setup-project]"
related:
  - follow-lang-javascript
  - follow-lang-kotlin
  - follow-best-practice
  - refactor
  - follow-tool-madge
  - follow-default-config
  - setup-cicd
  - use-scripts
  - deep-research
---

## Goal

Develop Python projects with best practices and Clean Architecture

## Scope

For projects developed with a modern Python 3 runtime. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time scaffold with venv, `pyproject.toml`, ruff, pyright); verify current Python/tool versions via `/deep-research` at use time (official docs: https://docs.python.org/3/)

## Execute

### 1. Check Version And Install

> Goal: install Python and dependencies with live-checked versions

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest stable Python, current Python practices, and the project's `requires-python` before installing
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): runtime pin, venv, scaffold, dev tools, first test, verify, git hygiene
3. Tool inventory (interpreter, pip, venv, ruff, pyright, runners) → `references/toolchain.md`
4. Install packages with `python -m pip install <pkg>` — always `python -m pip`, never bare `pip`; avoid floating/unbounded version ranges; pin to stable releases

### 2. Configuration

> Goal: keep `pyproject.toml` as the single source of truth

1. Dependencies in `[project.dependencies]`, dev tools in `[project.optional-dependencies] dev`
2. `[tool.ruff]` (with `target-version` matching the runtime) and `[tool.pyright]` (strict) configured with overrides only per `/follow-default-config` — concrete skeleton in `workflows/setup-project/SKILL.md`

### 3. Project Structure

> Goal: organize code per Clean Architecture

1. Split into `domain/`, `application/`, `adapters/`, `presentation/`
2. `domain/` holds pure business logic without side effects; `application/` orchestrates use cases
3. `adapters/` owns I/O (DB, HTTP, filesystem); `presentation/` owns entry points (CLI/API/UI)
4. Every package has `__init__.py`; tests live in `tests/`; run `/follow-architecture` for the pattern choice

### 4. Core Principles

> Goal: write Python per best practices

1. Type-hint every function; use `from __future__ import annotations` for forward references
2. Use `@dataclass(frozen=True)` or `pydantic` models for immutable data
3. Use `ruff check .` + `ruff format .` and `pyright` in CI before merge
4. Prefer `pathlib`, context managers, and async (`async def`) for I/O-bound work

### 5. Import Rules

> Goal: keep imports deterministic and sorted

1. Order: stdlib → third-party → local, separated by blank lines (enforced by `ruff` `I` rules)
2. No unused imports (`F401`); no circular imports — check with `/follow-tool-madge` if suspected

## Rules

### 1. Toolchain

- Use the project's `requires-python` (never a stale hardcoded version); `ruff` for lint/format, `pyright` strict for types
- Use `pyproject.toml` as the single source of truth; no secrets in config

### 2. Code Standard

- Type hints on every public function; `dataclass`/`pydantic` for data models
- Clean Architecture layering; side effects only in `adapters/`

### 3. Live Checks

- Verify current Python/ruff/pyright behavior and new stdlib features via `/deep-research` at use time, not from memory

- Use /follow-lang-javascript if needed
- Use /follow-lang-kotlin if needed
- Use /follow-best-practice if needed
- Use /refactor if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- Python project following Clean Architecture
- `pyproject.toml` with ruff and pyright config
- Every function typed; code passes `ruff check` and `pyright` strict
