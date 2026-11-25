---
name: python-conventions
description: >-
  Enforce Python tooling conventions for uv, ty, Ruff, pytest, and
  pyproject.toml. Use when working on .py files or Python project config.
  NOT for JS/TS, shell scripts, CI design, profiling, or test architecture.
user-invocable: false
disable-model-invocation: false
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Python Conventions

Apply these conventions when Python work is the primary workstream.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Active (auto-invoked when Python work is primary) | Apply the operator contract below |
| Empty | Display the convention summary and routing guidance |
| `check` | Verify tooling compliance only |

## Reference File Index

| File | Purpose |
|------|---------|
| `references/tooling-contract.md` | Required command sequence for install, run, lint, type-check, and test flows |
| `references/redirection-boundaries.md` | When Python conventions should yield to shell, JS/TS, or domain-specific skills |
| `references/exceptions.md` | When to break conventions (legacy, corporate) |
| `references/library-preferences.md` | Guided library defaults for new Python work |
| `references/performance-tips.md` | Profiling tools, optimization patterns quick-reference |
| `references/testing-patterns.md` | Fixture scopes, markers, conftest skeleton |

## Operator Contract

### Active

1. Apply this skill only when Python files, Python tooling, or `pyproject.toml` are the primary surface of the task.
2. Read `references/redirection-boundaries.md` when Python appears alongside shell, JS/TS, or other dominant workstreams.
3. Enforce the hard requirements in `references/tooling-contract.md` for package management, command execution, linting, type checking, and tests.
4. Check `references/exceptions.md` before recommending any legacy or constrained-environment deviation.
5. Read `references/library-preferences.md` only when choosing libraries for new Python work.

### Empty / Help

1. Summarize the hard requirements: `uv`, `uv run`, `uv add`, `ty`, `ruff`, `pytest`, and `pyproject.toml`.
2. Show the difference between hard requirements and guided preferences.
3. Point to the exact reference files for tooling, exceptions, libraries, testing, performance, and mixed-language routing.

### `check`

1. Verify tooling compliance only; do not widen into full implementation advice unless the user asks.
2. Report whether the project uses `uv`, `uv run`, `ty`, `ruff`, `pytest`, and `pyproject.toml` in the expected ways.
3. Flag legacy or exception-path deviations and require the reason to match `references/exceptions.md`.
4. Reject recommendations that replace repo-required tooling with `mypy`, `pip install`, or bare `python`.

## Hard Requirements

- **Package manager**: use `uv` for all Python package operations
- **Dependencies**: use `uv add`, `uv add --group dev`, `uv remove`, and `uv lock --upgrade-package <pkg>` as appropriate
- **Reproducible installs**: use `uv sync --locked` when validating an existing lockfile workflow
- **Project config**: keep Python project configuration in `pyproject.toml`
- **Type checking**: use `uv run ty check`, not `mypy`
- **Linting**: use `uv run ruff check` and `uv run ruff format`
- **Testing**: use `uv run pytest`
- **Task running**: use `uv run <command>` for Python command execution

### Virtual Environments

- Let `uv` manage virtual environments automatically
- Never manually create or activate `.venv` directories
- Use `uv run` to execute within the project environment

## Guided Preferences

Guided library preferences apply only when starting new Python work and no stronger local constraint already exists. Read `references/library-preferences.md` before recommending replacements for an established stack.

## Project Structure

- Use `pyproject.toml` for all project metadata and dependencies
- Place source code in a package directory matching the project name
- Use `uv` workspace members for monorepo sub-packages
- Run the required lint, format, type-check, and test sequence from `references/tooling-contract.md` before considering Python work complete

## Performance Conventions

1. Profile before optimizing.
2. Use `references/performance-tips.md` for quick Python profiling and optimization patterns.
3. Route broad profiling, regression analysis, or performance investigation to `performance-profiler`.

## Testing Conventions

1. Use pytest for Python tests and configure project test defaults in `pyproject.toml`.
2. Use `references/testing-patterns.md` for fixtures, markers, `tmp_path`, `monkeypatch`, parametrization, and coverage policy.
3. Route test strategy, suite design, fixture architecture, or cross-language test plans to `test-architect`.

## Validation Contract

Run from this skill directory before declaring changes complete:

```bash
python scripts/check.py
git diff --check
```

Completion criteria:

1. `scripts/check.py` exits 0.
2. `git diff --check` exits 0.
3. No portable-CLI violations remain under this skill directory.

After changing skill definitions, public descriptions, reference files, or eval behavior, invoke `docs-steward` if available.

## Critical Rules

1. Reject Python setup advice that uses `pip install`, `uv pip install`, or bare `python` when the task is not explicitly on an approved exception path.
2. Require `uv add` for runtime dependencies and `uv add --group dev` for development-only dependencies unless `references/exceptions.md` justifies a legacy or constrained-environment deviation.
3. Require `uv run ty check` for type checking; do not recommend `mypy` or bare `ty check` as the default path in this repo.
4. Treat `uv run ruff check`, `uv run ruff format`, `uv run ty check`, and `uv run pytest` as the default completion gate for Python changes unless an exception is documented.
5. Do not edit `uv.lock` by hand; use `uv lock`, `uv sync`, or dependency commands.
6. Do not present guided library preferences as mandatory replacements for an already-established local stack.
7. Read `references/exceptions.md` before approving a legacy toolchain, alternate environment manager, or alternate library path.
8. Redirect mixed-language or non-Python-primary work through `references/redirection-boundaries.md` instead of force-fitting this skill onto the whole task.

**Canonical terms** (use these exactly):
- `uv` -- the required package manager and task runner
- `ty` -- the required type checker (not mypy)
- `uv run ty check` -- the required type-check command
- `ruff` -- the required linter and formatter
- `pyproject.toml` -- the single source of project configuration
- `uv run` -- prefix for all Python command execution
- `uv sync --locked` -- default reproducible install check for lockfile-backed workflows

## Scaling Strategy

- Incidental Python file in a broader non-Python task: enforce only the hard requirements that touch the Python-owned surface, then route mixed-workflow questions through `references/redirection-boundaries.md`.
- Python-primary feature or refactor work: apply the full operator contract, including tooling, testing, and guided preferences where relevant.
- Repo-wide Python tooling or migration work: use `check`, `references/tooling-contract.md`, and `references/exceptions.md` to separate hard violations from documented transition paths.

## Progressive Disclosure

- Do not load every reference by default.
- Read `references/tooling-contract.md` first for command-sequence questions.
- Read `references/redirection-boundaries.md` when shell, JS/TS, CI, or framework-specific work is mixed into the request.
- Read `references/exceptions.md` only when the task appears to require legacy, corporate, or constrained-environment exceptions.
- Read `references/library-preferences.md` only when selecting libraries for new Python work.
- Read performance or testing references only when the active task actually touches those areas.

## Scope Boundaries

**IS for:** Python tooling conventions, command selection, dependency-management rules, type/lint/test gates, and exception-aware repo guidance.

**NOT for:** JS/TS conventions, shell conventions, CI pipeline design, profiling investigations, test architecture, or framework/domain-specific implementation strategy.
