---
name: ci-cd-python
description: "Applies when creating or modifying CI/CD pipelines for Python projects. Covers pip/pipenv/poetry/uv caching, pytest-cov coverage, ruff linting, mypy type checking, and pip-audit."
---

# Python CI/CD

## Setup and caching

Use `actions/setup-python@v5` with the `cache` parameter:

| Manager | `cache:` value | Lockfile for key |
|---------|---------------|-----------------|
| pip | `'pip'` | `requirements*.txt` |
| pipenv | `'pipenv'` | `Pipfile.lock` |
| poetry | `'poetry'` | `poetry.lock` |

For uv, use `astral-sh/setup-uv` with `cache: true` (keys on `uv.lock`).

## Install commands (frozen)

```bash
pip install -r requirements.txt --no-deps       # pip-tools
pipenv install --deploy                          # pipenv
poetry install --no-interaction                  # poetry
uv sync --frozen                                 # uv
```

## Coverage

```bash
pytest --cov=src --cov-report=xml:coverage.xml --cov-fail-under=80
```

Tool: `pytest-cov`. Output: Cobertura XML for Codecov/Coveralls upload.

## Linting and type checking

```bash
ruff check .
ruff format --check .
mypy src/           # or: pyright src/
```

Run lint and type check as separate parallel jobs before the test job.

## Dependency audit

```bash
pip-audit -r requirements.txt
# or: safety check
```

## Python-specific gotchas

1. Always set `PYTHONDONTWRITEBYTECODE=1` in CI to avoid `.pyc` file pollution.
2. Use `python -m pytest` (not bare `pytest`) to ensure the correct interpreter.
3. For monorepos, cache per-project by specifying `cache-dependency-path`.
4. `tox` and `nox` manage their own virtualenvs — cache `~/.cache/pip`, not `.tox/`.

## Sources

- https://github.com/actions/setup-python
- https://docs.astral.sh/uv/guides/integration/github/
