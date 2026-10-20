# Python Poetry Setup

## Summary

**One-sentence:** Produces a reproducible Poetry setup — poetry.lock committed, --sync install in CI, dep groups (main/dev/test/docs), tight Python constraint, builder-stage Docker, snok install action + .venv cache.

**One-paragraph:** Poetry is the standard for Python dependency management: deterministic builds via poetry.lock, isolated virtual environments, streamlined PyPI publishing. Always commit `poetry.lock`. Use `poetry install --sync --no-interaction` in CI (the `--sync` removes packages that left the lockfile, preventing zombies). Never run bare `poetry update` in a shared repo — bump per-package only. Split deps into groups: main, dev, test, docs (docs `optional = true`). Tight Python constraints (`python = "^3.11"`, not `>=3.8`). Docker: builder stage runs `poetry export`, final stage runs `pip install -r requirements.txt` so Poetry doesn't ship into production. CI uses `snok/install-poetry@v1` + cache `.venv` by `poetry.lock` hash.

**Ефективно для:** new Python projects, services migrating from requirements.txt + pip-tools, Docker images bloated with Poetry runtime, CI suites with slow install times.

## Applies If (ALL must hold)

- Python project on 3.11+.
- Team accepts Poetry as dep manager (or willing to adopt).
- CI can install Poetry and cache .venv.
- Docker builds (if any) can use multi-stage.

## Skip If (ANY kills it)

- Project on uv / hatch / Rye — different tool family.
- requirements.txt-only legacy with no migration mandate.
- Pure pip-installable library where Poetry overhead exceeds value.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python version | semver | tech stack |
| Dep list (current) | requirements.txt or Pipfile | repo |
| CI provider | string | infra ADR |
| Docker target | image base | infra ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[python]]` | Broader Python conventions; this file is the dep-manager focus. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: commit lockfile, --sync in CI, no bare update, dep groups, tight Python, poetry check --lock, Docker multi-stage, snok+cache, env var for PyPI token | ~800 |
| `content/02-output-contract.xml` | essential | Required pyproject + CI + Dockerfile invariants | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: missing lockfile, bare update, Poetry in final Docker stage, broad Python constraint | ~600 |
| `content/06-decision-tree.xml` | essential | Root: "Python project where Poetry is acceptable?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Migration from requirements.txt | sonnet | Dep parsing + pyproject generation. |
| Docker multi-stage rewrite | sonnet | Template. |
| CI cache config | haiku | YAML boilerplate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Poetry pyproject with groups + ruff + mypy config. |
| `templates/Dockerfile` | Multi-stage Dockerfile (builder + final). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-poetry-setup.py` | Verifies poetry.lock presence, --sync in CI, Python tight pin, no `poetry install` in final Dockerfile stage. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[python]]` — broader Python rules

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: Python project, Poetry acceptable, CI can cache .venv.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pyproject.toml`

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Production-ready Python project"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "my_project", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
pydantic = "^2.6.0"
sqlalchemy = {extras = ["asyncio"], version = "^2.0.25"}

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^4.1.0"
ruff = "^0.5.0"
mypy = "^1.8.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.5.0"
mkdocs-material = "^9.5.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "T20"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"
```

### `templates/Dockerfile`

```text
# Multi-stage Dockerfile for Poetry projects.
# Builder: export requirements.txt. Final: pip install only.
# Never run poetry install in the final stage.

FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install poetry==1.8.5

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "my_project.main"]
```
