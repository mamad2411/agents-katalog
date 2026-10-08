# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A **prompt database and runtime delivery package** for LangChain/LangGraph apps. Prompts are versioned in a relational DB (Postgres or SQLite), aliased (`production`, `staging`, `latest`), and optionally exported to blob storage (local filesystem or MinIO). Accessible via Python client, FastAPI API, Rich CLI, or Streamlit dashboard.

## Development commands

```bash
# Install all dependency groups
make install                    # or: pdm install -G dev -G test -G docs -G dashboard -G observability -G minio -G redis

# Run all tests
make test                       # or: PYTHONPATH=src pdm run pytest -q

# Run tests by marker
make unit                       # pdm run pytest -m unit -q
make integration                # pdm run pytest -m integration -q
make e2e                        # pdm run pytest -m e2e -q

# Run a single test file or test
PYTHONPATH=src pdm run pytest tests/unit/test_domain.py -q
PYTHONPATH=src pdm run pytest tests/unit/test_domain.py::test_string_prompt_rendering -q

# Coverage
make cov                        # pdm run pytest --cov=src/promptdb --cov-report=term-missing --cov-report=xml

# Lint and format
make lint                       # pdm run ruff check .
make format                     # pdm run ruff format .
pdm run ruff check --fix .      # auto-fix lint issues

# Type checking
make typecheck                  # PYTHONPATH=src pdm run mypy src

# Docs
make docs                       # sphinx-build -W --keep-going -b html docs/source docs/build/html

# Run the API server
make api                        # pdm run uvicorn promptdb.api:app --reload

# Run the Streamlit dashboard
make dashboard

# Run everything (lint + typecheck + test + docs)
make all
```

## Architecture

```text
files / CLI / API / dashboard
          |
      PromptClient (client.py)  -- ergonomic facade
          |
      PromptService (service.py) -- orchestrates workflows
       /          \
  PromptRepository   BlobStore adapters
  (db.py)            (storage.py)
  SQLAlchemy ORM     LocalBlobStore | MinioBlobStore
```

### Key modules

- **`domain.py`** — Core Pydantic models: `PromptSpec`, `PromptRef`, `PromptVersionView`, `ResolvedPrompt`, `PromptRenderResult`. All rendering logic lives here. Supports f-string, Jinja2, and mustache template formats.
- **`db.py`** — SQLAlchemy ORM tables (`prompts`, `prompt_versions`, `prompt_aliases`, `prompt_assets`) and `PromptRepository` for persistence + resolution. Resolution order: version ID → `rev:N` → alias → user_version → `latest` fallback.
- **`service.py`** — `PromptService` coordinates registration, alias movement, resolution, rendering, and export. Shared by API and CLI.
- **`client.py`** — `PromptClient` facade. `PromptClient.from_env()` creates a fully wired instance from env vars.
- **`api.py`** — FastAPI app factory (`create_app`). Routes under `/api/v1/`. Module-level `app = create_app()` for uvicorn.
- **`storage.py`** — `LocalBlobStore` (filesystem) and `MinioBlobStore` (S3-compatible). Both expose `put_text`/`get_text`/`presign_upload`.
- **`files.py`** — Load prompts from `.yaml`/`.json`/`.txt`/`.md` files; write specs and version bundles back.
- **`cli.py`** — Rich-powered CLI (`promptdb init|list|register-file|resolve|render|export-file`).
- **`settings.py`** — `AppSettings` reads `PROMPTDB_*` env vars. Defaults to SQLite + local blob storage.

### Prompt references

Compact `namespace/name:selector` format: `support/triage:production`, `research/answerer:latest`, `support/triage:rev:2`.

### Persistence split

- **Database**: prompt identities, versions, aliases, relational asset metadata
- **Blob store**: exported bundles and larger artifacts

### Test structure

Tests are split into `tests/unit/`, `tests/integration/`, `tests/e2e/` with markers `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`. Shared fixtures in `tests/conftest.py` provide `app_settings`, `client`, `service`, and `prompt_registration`.

## Conventions

- Python `>=3.13`, Pydantic v2 idioms, Google-style docstrings.
- Ruff for lint+format (line length 100, rules: E, F, I, UP, B, N, D).
- mypy with `disallow_untyped_defs = true` and pydantic plugin.
- File-native authoring is first-class: prompts can come from YAML/JSON/text files.
- Blob artifacts should always have matching relational metadata in `prompt_assets`.
- Schema changes require: ORM model update → Alembic migration → tests → docs.
- Uses PDM for packaging. CLI entry point: `promptdb = promptdb.cli:main`.

## Good next-step areas

1. Deeper LangChain prompt round-tripping across more prompt classes
2. Stronger Streamlit dashboard UX
3. FastAPI lifespan migration to remove deprecated `on_event` startup hooks
4. Richer observability and asset workflows
5. Broader docs and tutorials
