# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multimodal Retrieval Assistant for AI Challenge 2026. Ingests video/image/audio/text data and supports three retrieval modes:
- **KIS** – Keyframe Image Search
- **QA** – Question Answering
- **TRAKE** – Temporal Ranking of Key Events

Stack: FastAPI (Python 3.11) backend + React/TypeScript/Vite frontend, with PostgreSQL, Milvus (vector), Elasticsearch, Redis, and MinIO.

## Commands

### Full Stack (Docker)
```bash
docker compose up -d --build       # Start all services
docker compose logs -f backend     # Tail backend logs
docker compose down                # Stop all services
```

### Backend (local dev)
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend runs with SQLite in dev mode by default; no external services needed locally.

### Frontend (local dev)
```bash
cd apps/web
npm install
npm run dev        # Vite dev server
npm run build      # Production build (TypeScript check included)
npm run preview    # Preview production build
```

### Validation
```bash
# Backend syntax check (no bytecode)
python -m py_compile apps/backend/app/main.py

# Swagger UI smoke test (after starting backend)
open http://localhost:8000/docs
```

### Scripts
```bash
python scripts/ingest_video.py     # Ingest video into the pipeline
python scripts/export_results.py   # Export retrieval results
python scripts/benchmark.py        # Run benchmarks
```

## Architecture

### Backend (`apps/backend/`)

Module layout — each module follows `router.py / service.py / schemas.py`:

```
app/
├── main.py              # FastAPI app, router registration, CORS
├── core/
│   ├── config.py        # Settings via pydantic-settings
│   ├── database.py      # SQLAlchemy engine + session
│   └── bootstrap.py     # Mock data seeding on startup
├── modules/
│   ├── datasets/        # Dataset CRUD
│   ├── ingest/          # Video ingest pipeline
│   ├── jobs/            # Background job tracking
│   ├── media/           # Frame/media serving
│   ├── models/          # Model registry API
│   ├── retrieval/       # Hybrid retrieval engine (KIS/QA/TRAKE)
│   ├── submissions/      # AIC submission export & validation
│   └── temporal/        # ATS temporal search
└── adapters/
    ├── vector_db.py     # Milvus adapter
    ├── text_search.py   # Elasticsearch adapter
    └── model_runtime.py # Mock / Hugging Face model adapter
```

**Database models:** Dataset → Video → Frame → Annotation, plus QueryRun and RetrievalResult.

**Retrieval pipeline:** hybrid ranking combining semantic (vector), metadata (ES), and temporal signals with RRF fusion. Weights are controlled per-profile in `configs/retrieval_profiles.yaml`.

**Model runtime** defaults to mock adapters for local dev. Toggle real models in `configs/model_registry.yaml` (CLIP, PE Core, BeiT3, PaddleOCR, WhisperX, Qwen).

### Frontend (`apps/web/src/`)

Single-workspace UI, no routing:

- `App.tsx` – root component; owns query panel, result grid, context viewer, selected tray
- `api/client.ts` – centralized fetch wrapper for all backend endpoints
- `types.ts` – shared contracts: `SearchResult`, `FrameContext`, `SubmissionRow`
- `styles.css` – global styles; icons via Lucide React

**Rule:** Any backend API contract change must update both `apps/backend/README.md` and `src/types.ts`.

### Configuration

| File | Purpose |
|------|---------|
| `configs/model_registry.yaml` | Enable/disable individual models |
| `configs/retrieval_profiles.yaml` | Ranking weight profiles (semantic/metadata/temporal/RRF) |
| `.env` (from `.env.example`) | Secrets and service URLs — never commit |

### Key Conventions

- Results must carry a **score breakdown** (semantic, metadata, temporal components) for debugging and tuning.
- Index versioning is built in — rebuilds create a new index version, enabling rollback.
- Mock mode is on by default; the backend seeds mock data on startup via `bootstrap.py`.
- Models, raw datasets, `.env`, and submission files are excluded from git (see `.gitignore`).
