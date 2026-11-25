# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

The "arXiv Paper Curator" — a learner-focused, production-style RAG system built incrementally across a 7-week course. It fetches arXiv CS.AI papers, indexes them for keyword + hybrid search, and answers research questions via a LangGraph-based agentic RAG pipeline, exposed through a FastAPI backend, a Gradio UI, and a Telegram bot.

## Commands

```bash
# Setup
uv sync                          # Install Python dependencies
cp .env.example .env             # Configure environment (edit for JINA_API_KEY, TELEGRAM__BOT_TOKEN, LANGFUSE__* as needed)
codegraph init                   # Build the local CodeGraph index (.codegraph/, gitignored); `codegraph sync` after large edits

# Run the full stack (FastAPI, Postgres, OpenSearch, Airflow, Ollama, Redis, Langfuse)
make start                       # == docker compose up --build -d
make stop
make restart
make status
make logs
make health                      # curl health checks for API, OpenSearch, Airflow, Ollama

# Quality gate
make format                      # uv run ruff format
make lint                        # uv run ruff check --fix && uv run mypy src/
make test                        # uv run pytest
make test-cov                    # uv run pytest --cov=src --cov-report=html
make clean                       # docker compose down -v && docker system prune -f

# Single test
uv run pytest tests/unit/services/test_arxiv_client.py::test_name -v
uv run pytest tests/api/routers/test_ask.py -v

# Gradio UI standalone (requires stack running for backend calls)
uv run python gradio_launcher.py   # http://localhost:7861

# Weekly notebooks (primary learning path, also useful as executable docs of each layer)
uv run jupyter notebook notebooks/week1/week1_setup.ipynb   # through week7
```

Airflow UI credentials are in `airflow/simple_auth_manager_passwords.json.generated`.

Pre-commit hooks run `ruff --select=I --fix`, `ruff-format`, and `mypy`; `make lint` runs the equivalent manually.

## Architecture

### Layering

```
routers/  → services/  → repositories/ / db/  → models/
              ↑
         schemas/ (Pydantic I/O + per-domain config)
```

- **`src/routers/`** — FastAPI endpoint definitions only (`ping`, `hybrid_search`, `ask` + `stream` (SSE), `agentic_ask`). Delegate to services via `app.state`.
- **`src/services/`** — one subpackage per external integration or capability (`arxiv`, `pdf_parser`, `embeddings`, `opensearch`, `ollama`, `cache`, `langfuse`, `telegram`, `agents`, `indexing`). Each follows the same internal shape: `client.py` (the concrete implementation), `factory.py` (a `make_x_client()`/`make_x_service()` builder reading from `src/config.py`), and sometimes `prompts.py`/`prompts/`.
- **`src/db/`** — `interfaces/base.py` defines `BaseDatabase`; `interfaces/postgresql.py` implements it; `factory.py::make_database()` builds it from settings. Swappable-backend pattern — new backends implement `BaseDatabase`.
- **`src/repositories/`** — data-access layer over SQLAlchemy models (`paper.py`), used by services rather than routers touching the DB directly.
- **`src/models/`** — SQLAlchemy ORM models.
- **`src/schemas/`** — Pydantic models, split by concern (`api`, `arxiv`, `common`, `database`, `embeddings`, `indexing`, `pdf_parser`, `telegram`).
- **`src/config.py`** — single `Settings` (pydantic-settings) object composed of nested per-domain settings classes (`ArxivSettings`, `OpenSearchSettings`, `LangfuseSettings`, `RedisSettings`, `TelegramSettings`, etc.), each with its own `env_prefix` (e.g. `OPENSEARCH__`, `TELEGRAM__`) and `__`-nested env vars. `get_settings()` is the single entry point — don't read env vars directly elsewhere.
- **`src/main.py`** — FastAPI app + lifespan. All services are constructed once via their `factory.py::make_*()` in `lifespan()` and stashed on `app.state` (`app.state.opensearch_client`, `app.state.ollama_client`, etc.); routers/services pull dependencies from there rather than constructing their own clients. On startup it also verifies OpenSearch connectivity and calls `setup_indices(force=False)` to ensure the hybrid index exists, and conditionally starts the Telegram bot if `TELEGRAM__BOT_TOKEN` is configured.

### Search: keyword-first, then hybrid

Everything routes through a single hybrid OpenSearch index (`{index_name}-{chunk_index_suffix}`, see `OpenSearchSettings`). `src/services/opensearch/query_builder.py` builds BM25 and hybrid (RRF fusion of BM25 + vector) queries against `index_config_hybrid.py`'s mapping. `src/services/embeddings/` produces the vectors (Jina AI, 1024-dim) consumed by hybrid queries. `src/services/indexing/text_chunker.py` does section-aware chunking with overlap before indexing.

### Agentic RAG (LangGraph)

`src/services/agents/agentic_rag.py` wires a LangGraph state machine (`state.py` defines the shared state) from nodes in `src/services/agents/nodes/`: `guardrail_node` (in/out-of-domain check) → `retrieve_node` → `grade_documents_node` (relevance grading) → `rewrite_query_node` (adaptive re-query on poor results) → `generate_answer_node`, with `out_of_scope_node` short-circuiting guardrail failures. `agents/factory.py` assembles the graph from configured node functions; `agents/config.py` / `agents/prompts.py` hold graph-specific settings and prompt templates. Exposed via `src/routers/agentic_ask.py`, separate from the simpler non-agentic `ask`/`stream` endpoints.

### Ingestion pipeline

`src/services/metadata_fetcher.py` orchestrates: `services/arxiv/` (rate-limited arXiv API client) → `services/pdf_parser/` (Docling-based scientific PDF parsing) → Postgres (via `repositories/paper.py`) → OpenSearch indexing. `airflow/` DAGs schedule this as a recurring pipeline; the same services are also driven ad hoc from the week1–7 notebooks and directly from FastAPI routers.

### Cross-cutting services

- **Cache** (`services/cache/`): Redis, exact-match keys, TTL-based, used to short-circuit repeated `ask` queries. Per-request cache operations fail gracefully, but a Redis outage at boot currently crashes app startup — see ADR-0005's "Known gap".
- **Langfuse** (`services/langfuse/`): tracing wrapped around the RAG/agentic pipelines; toggled via `LANGFUSE__ENABLED`.
- **Telegram** (`services/telegram/`): thin bot layer over the same `opensearch_client`/`embeddings_client`/`ollama_client`/`cache_client` used by the HTTP API — constructed in `main.py` lifespan with those pre-built clients passed in, not built independently.

### Tests

`tests/unit/` (service- and schema-level, isolated), `tests/api/` (router-level via FastAPI test client, `tests/api/conftest.py` for fixtures), `tests/integration/` (`test_services.py`, exercises real service wiring — check for `testcontainers` usage before assuming a live stack is required). `.env.test` supplies test-time config (loaded via `pytest-dotenv`/`pytest-env`, configured in `pyproject.toml`).

**Run `uv sync --group dev` before testing.** Without it, `tests/api` and several `tests/unit` modules fail to collect (`ModuleNotFoundError: No module named 'langfuse'`, etc.) — `langfuse` and a few other main-dependency-group packages weren't locked in `uv.lock` until this was run.

**Patch factories where they're imported, not where they're defined.** `tests/api/conftest.py`'s `client` fixture patches `src.main.make_x_client` / `src.routers.ping.OllamaClient`, not `src.services.x.factory.make_x_client`. `main.py`/`ping.py` do `from src.services.x.factory import make_x_client`, which binds its own name into the importing module's namespace — patching the origin module leaves that reference untouched and the real (network-calling) factory still runs. Getting this wrong doesn't fail loudly for clients that don't eagerly connect (arXiv, PDF parser, Ollama) but does for ones that do (Redis/cache at construction, OpenSearch via the `/health` check) — this previously made every `tests/api` run take ~5 minutes retrying dead connections instead of ~1 second.

**Known gaps (found during #2, not fixed there):**
- `tests/unit/services/agents/` (`test_agentic_rag.py`, `test_nodes.py`, `test_tools.py` — 22 tests) has no `conftest.py`; all error with `fixture 'mock_opensearch_client' not found`. Needs its own conftest providing mocks for the agent nodes' dependencies.
- `tests/unit/services/test_pdf_parser.py::test_parse_pdf_success` / `test_parse_pdf_no_result` fail — the mocks still `await` `PDFParserService.parse_pdf`, which stopped being a coroutine after the async was removed from it.
- `tests/api/routers/test_agentic_ask.py::test_ask_agentic_with_rewritten_query` / `test_ask_agentic_custom_model` fail on assertions that don't match current response shape/kwargs.

## Agent skills

### Issue tracker

Issues live in GitHub Issues (pkuppens/production-agentic-rag-course), via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Related Projects

Sibling repo [pkuppens/on_prem_rag](https://github.com/pkuppens/on_prem_rag.git) is a separate on-premises RAG system (FastAPI, ChromaDB, Ollama) that is actively adopting lessons and techniques from this course; the reverse is not expected. When a technique here (hybrid search, agentic workflows, pipeline design, etc.) proves valuable, consider whether it's also worth porting to `on_prem_rag`.
