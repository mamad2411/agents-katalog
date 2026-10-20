---
description: Sync all docs/ files with current codebase state. Extracts ground truth from code first, diffs against docs, then updates only what changed.
---

# Update Docs

Use the **doc-updater** agent for this task.

Delegate all work to the `doc-updater` agent now.

## What this command does

1. **Extracts ground truth from code** — never relies on AI memory:
   - All backend routes from `backend/app/main.py`
   - Request/response shapes from `backend/app/schemas.py`
   - DB models and columns from `backend/app/models.py`
   - LLM pipeline status from `backend/app/text_to_sql.py` (stub vs live)
   - Data pipeline details from `data_pipeline/ingest_batting.py`
   - Frontend pages from `frontend/src/app/**/page.tsx`
   - Recent git changes (`git log --oneline -20`)

2. **Reads all docs** in `docs/architecture/` and `docs/setup/`

3. **Builds an explicit diff** per doc section:
   - Items in code but missing from docs → add
   - Items in docs but not in code → remove

4. **Updates docs** based on the diff — does not rewrite sections that are already accurate

5. **Creates missing docs** if `docs/architecture/` doesn't exist yet

6. **Updates `README.md`** at the project root:
   - Project overview and tech stack
   - Quick start instructions (docker compose, local dev)
   - Project structure summary
   - Links to detailed docs in `docs/`
   - Does NOT overwrite manually-written sections marked with `<!-- manual -->`

7. **Commits** all doc changes

## What this command does NOT touch

- Source code — documentation only
- `.claude/` config files

## When to run

- After wiring up the LLM integration in `text_to_sql.py`
- After adding new API endpoints or frontend pages
- After running a new Alembic migration (schema changes)
- After ingesting new data with the data pipeline
- When docs feel stale or before a code review
