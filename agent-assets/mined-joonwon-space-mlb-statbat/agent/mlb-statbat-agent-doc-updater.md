---
name: doc-updater
description: Sync all docs/ files with current codebase state. Extracts ground truth from code first, then diffs against docs, then updates. Never relies on AI memory.
model: sonnet
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Documentation Updater

**Core principle**: Extract facts from code first → diff against docs → update only what's wrong.
Never rely on AI memory. Always verify from source before writing.

---

## Phase 1: Extract Ground Truth from Code

Run ALL of the following before reading any docs.

### 1a. Backend routes

Routes are defined directly in `backend/app/main.py`:
```bash
grep -n "@app\." backend/app/main.py | grep -E '\.(get|post|patch|delete|put)\('
```

Build a canonical route list:
```
METHOD  /path               HANDLER
GET     /health             health
POST    /api/query          query
```

### 1b. Pydantic schemas (request/response shapes)

```bash
cat backend/app/schemas.py
```

### 1c. DB models

```bash
grep -n "^class " backend/app/models.py
```

For each model read the full file to extract table name and columns.

### 1d. text_to_sql pipeline

```bash
cat backend/app/text_to_sql.py
```

Note: which LLM is wired (Anthropic / OpenAI / stub), the DB_SCHEMA prompt, and both functions (`generate_sql`, `generate_answer`).

### 1e. Frontend pages

```bash
find frontend/src/app -name "page.tsx" | sed 's|frontend/src/app||; s|/page\.tsx$||; s|^$|/|' | sort
```

### 1f. Data pipeline

```bash
cat data_pipeline/ingest_batting.py
```

Note: data source (pybaseball / FanGraphs), CLI args, what it writes to DB.

### 1g. Environment variables

```bash
cat backend/app/config.py
```

### 1h. Recent changes

```bash
git log --oneline -20
```

### 1i. Build & lint status

```bash
cd frontend && npx tsc --noEmit 2>&1 | tail -5
```
```bash
cd backend && source venv/bin/activate && ruff check . 2>&1 | tail -5
```

---

## Phase 2: Read All Docs

Read every existing file under `docs/`:
```bash
find docs/ -name "*.md" 2>/dev/null | sort
```

If `docs/` doesn't exist yet, skip to Phase 5.

---

## Phase 3: Build Explicit Diffs

For each doc section, produce two lists before editing anything:

### API diff

**Missing from docs** (route in code, not in docs):
```
+ POST /api/query
```

**Stale in docs** (route in docs, not in code):
```
- GET /api/old-endpoint
```

### Pages diff

**Missing from docs**:
```
+ /stats
```

### Schema diff

For `QueryRequest` and `QueryResponse` — verify fields match `backend/app/schemas.py`.

### Models diff

For each SQLAlchemy model — verify columns match `backend/app/models.py`.

### text_to_sql diff

Check if `docs/architecture/overview.md` accurately describes the LLM integration status (stub vs wired).

If all diffs are empty → docs are in sync, skip to Phase 6.

---

## Phase 4: Update Docs

Apply only what the diff found. Do NOT rewrite sections that are already accurate.

### `docs/architecture/overview.md`

**Section: API Endpoints** — sync with canonical route list.
**Section: DB Models** — sync with models.py classes and columns.
**Section: LLM Pipeline** — sync with text_to_sql.py (stub or live, which provider).
**Section: Data Pipeline** — sync with ingest_batting.py (data source, CLI usage).

### `docs/architecture/api-reference.md`

For each **missing** endpoint, add:
```markdown
### METHOD /path
- **Request body**: `{ field: type }` (read schemas.py — do not guess)
- **Response** (status): shape
- **Description**: one sentence
```

For each **stale** endpoint, remove its section.

### `docs/architecture/frontend-guide.md`

- Sync the page routing map.
- Add sections for new pages.
- Remove sections for deleted pages.

---

## Phase 5: Create Missing Files

### If `docs/` doesn't exist

Create the directory and these files:

#### `docs/architecture/overview.md`

```markdown
# MLB StatBat — Architecture Overview

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python), SQLAlchemy async, PostgreSQL |
| Frontend | Next.js (TypeScript), Tailwind CSS, shadcn/ui |
| Data Pipeline | pybaseball, pandas, psycopg2 |
| LLM | Anthropic Claude (text-to-SQL) / OpenAI (fallback) |
| Infrastructure | Docker Compose |

## DB Models

(fill from Phase 1c extraction)

## API Endpoints

(fill from Phase 1a extraction)

## LLM Pipeline (`backend/app/text_to_sql.py`)

(fill from Phase 1d extraction — note if stub or live)

## Data Pipeline (`data_pipeline/ingest_batting.py`)

(fill from Phase 1f extraction)

## Environment Variables

(fill from Phase 1g extraction)
```

#### `docs/architecture/api-reference.md`

Generate from canonical route list. Read each handler and schema before writing shapes.

```markdown
# API Reference

Base URL: `http://localhost:8000`
Auth: None (public API)

---

## Health

### GET /health
- **Response** (200): `{ "status": "ok" }`

## Query

### POST /api/query
(fill from schemas.py)
```

#### `docs/architecture/frontend-guide.md`

```markdown
# Frontend Guide

## Page Routing Map

| Route | Description |
|-------|-------------|
| / | (fill from Phase 1e) |

## How to Add a New Page

1. Create `frontend/src/app/{name}/page.tsx`
2. Update this doc's routing map

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/app/layout.tsx` | Root layout |
| `frontend/src/app/page.tsx` | Home page |
| `frontend/src/app/globals.css` | Global styles |
```

---

## Phase 6: Commit

```bash
git add docs/
git commit -m "docs: sync documentation with current codebase state"
```

---

## Phase 7: Output Report

```
## Ground Truth (extracted from code)
- Backend routes: N total
- Frontend pages: N total
- DB models: N total (Players, BattingStats, ...)
- LLM status: stub / live (provider)

## Diffs Applied
### overview.md
  (list changes or "no changes needed")

### api-reference.md
  (list added/removed sections)

### frontend-guide.md
  (list changes)

## Unchanged (verified accurate)
  (list files with no changes)

## Build Status
  TypeScript: ✓ / ✗ (N errors)
  Ruff: ✓ / ✗ (N issues)

## Committed
  docs: sync documentation with current codebase state
```
