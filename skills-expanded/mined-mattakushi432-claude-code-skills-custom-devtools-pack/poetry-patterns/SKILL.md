---
name: poetry-patterns
description: "When to activate: Poetry, pyproject.toml, dependency management, virtual environments, packaging, publishing"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Poetry Patterns

## Project Setup
```toml
# pyproject.toml
[tool.poetry]
name = "my-service"
version = "0.1.0"
description = "..."
authors = ["Team <team@example.com>"]
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110"
sqlalchemy = {version = "^2.0", extras = ["asyncio"]}
pydantic-settings = "^2.0"
alembic = "^1.13"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-asyncio = "^0.23"
httpx = "^0.27"
ruff = "^0.3"
mypy = "^1.9"

[tool.poetry.group.test.dependencies]
pytest-cov = "^5.0"
factory-boy = "^3.3"
```

## Common Commands
```bash
poetry new my-project             # create new project
poetry add fastapi                # add dependency
poetry add pytest --group dev    # add dev dependency
poetry add "sqlalchemy[asyncio]"  # add with extras
poetry install --no-root          # install deps (CI)
poetry install --with dev         # install with dev group
poetry update                    # update all deps within constraints
poetry lock --no-update          # regenerate lock without updating
poetry run pytest                 # run in venv
poetry shell                     # activate venv
poetry build                     # build wheel + sdist
poetry publish --repository pypi  # publish (set POETRY_PYPI_TOKEN_PYPI)
poetry export -f requirements.txt --output requirements.txt  # for Docker
```

## Dependency Groups Strategy
- `main`: runtime dependencies only (what ships in production)
- `dev`: development tools (ruff, mypy, ipdb)
- `test`: testing tools (pytest, factory-boy, faker)
- `docs`: documentation tools (mkdocs, sphinx)

## Docker Integration
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install poetry==1.8.2
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes > requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

## Ruff Configuration
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "C4", "SIM", "TCH"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]
```
