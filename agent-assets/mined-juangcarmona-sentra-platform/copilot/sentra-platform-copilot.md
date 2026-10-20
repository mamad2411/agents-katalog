# Copilot Coding Agent – Onboarding Instructions for `sentra-brain`

---

## High-Level Overview

**Sentra Brain** is a modular, private AI server platform designed for professional environments needing compliance, privacy, and control. It delivers a full-stack AI solution with LLM serving (via llama.cpp), a private RAG engine (ChromaDB or Qdrant), and an orchestrator layer (MCP Server).  
The system supports both community (up to 3 users/devices, AGPLv3) and commercial (licensed) deployments, with additional features for monitoring, user/agent management, and regulatory compliance (GDPR, HIPAA, ISO/IEC 27001, etc).

**Core Technologies:**
- **Python:** FastAPI, llama-index, SQLAlchemy, Pydantic, ChromaDB, Alembic (migrations).
- **TypeScript/React:** Frontend (Admin Panel) with Tailwind CSS, shadcn/ui, lucide-react.
- **C#:** Optional for MCP Server.
- **ChromaDB/Qdrant:** Private vector database for RAG.
- **llama.cpp:** LLM engine, always exposed over HTTP (never included in Docker Compose by default).
- **Database:** Postgres (default).

**Folder Layout:**
- `core/sentra-core/` – Shared backend logic (Domain, Infra, Core, Model, Tests).
- `apps/` – Application entrypoints (APIs, Admin UI, MCP Server, etc.).
- `services/` – Service modules, agent infrastructure.
- `deploy/` – Deployment scripts, Docker Compose, cloud infra.
- `docs/` – Documentation, regulatory, and API specs.
- `website/` – Public marketing site and documentation.

---

## Build & Validation Instructions

### Environment Setup

- **Python 3.10+** is required. Use `pyenv` or similar to manage versions.
- **Node.js 18+** for frontend/admin panel.
- **PostgreSQL 14+** for persistence.
- You may need `poetry` or `pip` for Python dependency management.

### Backend (Python)

#### 1. Install dependencies:
```bash
cd core/sentra-core
pip install -r requirements.txt
# or, if using poetry
poetry install
```

#### 2. Set up environment variables:
- Copy `.env.example` to `.env` and fill in secrets (DB, API keys, etc).

#### 3. Initialize & apply Alembic migrations:
```bash
cd sentra_core/infra/sql/alembic
# Set DATABASE_URL or ensure .env is loaded
alembic upgrade head
```
- Ensure `alembic.ini` uses `sqlalchemy.url = env:DATABASE_URL`.

#### 4. Run tests:
```bash
cd core/sentra-core
pytest
```

#### 5. Lint (if configured):
```bash
ruff check .
black --check .
```
- See `pyproject.toml` for tool config.

### Frontend (Admin Panel)

#### 1. Install dependencies:
```bash
cd apps/admin-ui
npm install
```

#### 2. Build:
```bash
npm run build
```

#### 3. Run locally:
```bash
npm run dev
```

#### 4. Lint/test (if configured):
```bash
npm run lint
npm run test
```

### Running the System

- **llama.cpp** must be running and accessible over HTTP as configured in environment.
- Use Docker Compose for all services except llama.cpp, unless otherwise documented.
- Always run DB migrations before starting services after a code change that affects the schema.

### CI/CD & Validation

- PRs are validated by GitHub Actions workflows (see `.github/workflows/`).
- Checks include: lint, type-check, backend tests (pytest), frontend build and lint, DB migrations.
- All tests must pass locally before PR.
- No code should be checked in without running the full test suite and migrations.

---

## Project Layout & Architectural Guidance

- **Domain-driven design:**  
  Business logic and entities in `sentra_core/domain/`  
  Infrastructure in `sentra_core/infra/`  
  Core models, logging in `sentra_core/core/`
- **Tests:**  
  In `core/sentra-core/tests/`
- **Migration scripts:**  
  In `core/sentra-core/sentra_core/infra/sql/alembic/`
- **Frontend:**  
  In `apps/admin-ui/`
- **Deployment:**  
  Compose files in `deploy/`

**Config Files:**
- `pyproject.toml`: Python tool config (black, ruff, pytest, etc.)
- `alembic.ini`: DB migration config (must use env:DATABASE_URL)
- `.env`, `.env.example`: Environment config
- `package.json`: Frontend dependencies/scripts
- `.github/workflows/`: CI/CD pipelines

---

## Essential Commands (Summary)

- `pip install -r requirements.txt` or `poetry install`
- `alembic upgrade head`
- `pytest`
- `ruff check .`
- `black --check .`
- `npm install`
- `npm run build`
- `npm run dev`
- `docker compose up` (from `deploy/`, *excluding* llama.cpp unless noted)

---

## Troubleshooting & Workarounds

- Always check `.env` variables are set and correct.
- If Alembic fails, check DB connectivity and env vars.
- Build errors in admin panel: ensure Node.js version matches and dependencies are installed.
- If test or lint fails, check `pyproject.toml` and `package.json` for versions and tool configs.

---

## Agent Guidance

**Trust these instructions and only perform a search if required information is missing or found to be in error.**  
Follow the documented build, test, and validation steps exactly.  
If you encounter undocumented issues, record them and update these instructions for future use.

---
