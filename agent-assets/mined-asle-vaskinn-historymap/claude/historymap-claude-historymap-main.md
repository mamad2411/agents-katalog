# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

> **Deep reference:** `AGENTS.md` (repo root) is the full codebase map for agents —
> architecture, all servers/ports, pipeline internals, schemas, and gotchas.
> Read the relevant AGENTS.md section before editing a subsystem.

## Project Overview

**Trondheim Historical Map** - Interactive web application for exploring Trondheim's development from 1700 to present using ML-extracted features from historical Kartverket maps combined with modern OSM data. Buildings/roads/water carry temporal attributes (`sd`/`ed`) filtered by a year slider.

## Workflow tiers

> **This policy overrides any heavier plugin/skill workflow** (TDD-always skills,
> multi-agent orchestration, the `/propose → /implement → /test → /sync` cycle).
> Those are opt-in for Tier 2–3 work, not mandatory for every edit.

Default to the lowest tier that fits the change. Only escalate when the change crosses a module boundary or touches shared state, IO, migrations, auth, or a hot path. If I say "quick", force Tier 0–1.

**Tier 0 (trivial)** — typo, rename, comment, config value: make the change directly. No plan, no new tests. Run only a directly-touched test if one exists.

**Tier 1 (local)** — one function/module, no interface change: one-line plan inline, then edit. Run only the affected module's tests — prefer `python3 -m pytest --testmon` (testmon auto-selects the tests that exercise your change), or name the file directly, e.g. `python3 -m pytest tests/test_result.py`.

**Tier 2 (feature/interface)** — new public behavior or multi-module change: short plan first, TDD, run the affected modules plus their importers (e.g. `python3 -m pytest tests/test_result.py tests/test_constants.py`, or `--testmon` to follow the dependency graph).

**Tier 3 (risky)** — shared state, migrations, auth, hot path: full discipline — plan, tests-first, full suite, verification pass.

Do not run the full test suite or full rebuild for Tier 0–1 changes. Full suite runs once before commit/PR, not per edit.

**Repo-specific Tier 3 danger zones** (always escalate when touched):
- `scripts/pipeline.py`, `scripts/merge/` and `scripts/export/` — pipeline stages write shared generated data in `data/merged/` and `data/export/`; a regression corrupts every downstream layer. Re-run the affected stage + full `pytest tests/`.
- `backend/jobs.py` / `backend/app.py` — the sequential subprocess job queue (shared runtime state).
- Affine/TPS transform math duplicated across `frontend/source_manager.html` and `frontend/feature_extraction.js` (AGENTS.md gotcha #6) — a fix in one almost always belongs in both.
- `scripts/normalize/base.py` and the `sd`/`ed`/`ev` schema (`docs/tech/DATA_SCHEMA.md`) — schema changes ripple through normalize → merge → export.
- ML train/predict/vectorize (`ml/`) — model + inference contract.

### Incremental testing commands

| When | Command |
|------|---------|
| (a) Fast scoped run during iteration | `python3 -m pytest --testmon`  (or `python3 -m pytest --lf` for last-failed) |
| Watch loop (auto-runs affected tests on save) | `ptw`  (uses `--testmon` per `pytest.ini`) |
| (b) Full suite before commit/PR | `python3 -m pytest tests/` |

First `--testmon` run seeds its dependency DB (`.testmondata`, git-ignore it) by running everything once; subsequent runs are scoped to what changed.

## Workflow System

### Document-Driven Development

All changes follow a structured workflow through documentation layers:

```
docs/need/     → What we want to achieve (requirements, user stories)
docs/spec/     → Product specifications (features, acceptance criteria)
docs/tech/     → Technical decisions (architecture, schemas, instructions)
docs/todo/     → Task tracking (current work, backlog)
```

**Start any task by reading `docs/todo/current_work.md`** (authoritative in-flight status).
Root-level `PHASE*_*.md` files are stale archives — do not treat as current truth.

### Change Request Workflow

**Every request MUST follow this process:**

1. **PROPOSE** (`/propose`) - Analyze request, propose doc changes
2. **APPROVE** - User reviews and approves high-level changes
3. **IMPLEMENT** (`/implement`) - Agents execute approved work
4. **TEST** (`/test`) - Run tests, fix issues
5. **SYNC** (`/sync`) - Ensure docs are aligned with code

### Commands

| Command | Purpose |
|---------|---------|
| `/propose <request>` | Analyze request, show doc changes needed |
| `/implement` | Execute approved changes using agents |
| `/test` | Run tests and fix failures |
| `/sync` | Check doc/code alignment, fix drift |
| `/status` | Show project status |
| `/doctor` | Health check |

### Agent Strategy

Work is split across specialized agents:

- **Research agents** - Explore codebase, gather context
- **Implementation agents** - Write code in parallel
- **Test agents** - Run tests, verify changes
- **Doc agents** - Update documentation

User discusses high-level decisions while agents handle execution.

## Auto-Approval Rules

The following are auto-approved (git protects us):

### Always Approved
- Read operations (Glob, Grep, Read)
- Git operations (status, diff, log, add, commit)
- Docker operations (build, up, down, restart)
- Python/Node execution
- Test running
- Documentation edits in `docs/`

### Require Approval
- New file creation outside established patterns
- Destructive operations (rm, reset --hard)
- External network calls to new domains
- Schema changes

## Architecture

```
Browser → nginx :8080 (docker "web")
            ├─ /        frontend/ (vanilla JS, MapLibre GL 4 + PMTiles, NO build step)
            ├─ /data/   data/ (GeoJSON + PMTiles + raster tiles)
            ├─ /wms/    proxied external WMS (Trondheim kommune, Geonorge)
            └─ /api/  → FastAPI backend :5000 (docker "backend", backend/app.py)
                          └─ sequential subprocess jobs (backend/jobs.py):
                             pipeline, ML train/verify, georeferencing, alignment

Data pipeline: data/sources/*/raw → normalize → data/merged/ → export → data/export/ (PMTiles via tippecanoe)
ML: U-Net (segmentation-models-pytorch) — ml/train.py → predict.py → vectorize.py
```

Ports: **8080** nginx (only host-published port; backend reached via `/api/`).
All APIs — including manual edits (`/api/manual`) and rebuild (`/api/rebuild`) —
live in the FastAPI backend behind nginx. See AGENTS.md §1.

## Data Schema

Two layers (see `docs/tech/DATA_SCHEMA.md` and AGENTS.md §8):

**Normalized** (`data/sources/*/normalized/`, enforced by `scripts/normalize/base.py`):
required `_src`, `_src_id`, `_ingested`; optional `sd`, `ed`, `ev`, `bt`, `nm`, `_raw`.

**Export/frontend** (PMTiles/GeoJSON in `data/export/`, source ids shortened):

| Field | Type | Description |
|-------|------|-------------|
| `src` | string | Source: osm, sef, ml, man, tk, mat |
| `sd` | int | Start date (construction year) |
| `ed` | int/null | End date (demolition year) |
| `ev` | string | Evidence: h (high), m (medium), l (low) |
| `nm` | string | Building name |
| `sd_src` / `sd_method` | string | Date provenance and method (direct/inferred/estimated/inherited) |
| `mlc` | float | ML confidence (0–1) |

## Key Paths

| Path | Purpose |
|------|---------|
| `frontend/` | MapLibre app: `index.html`+`app.js` (viewer), `source_manager.html` (georef tool), `feature_extraction.*` (ML/annotation tool) |
| `backend/` | FastAPI app (`app.py`) + job queue (`jobs.py`) |
| `ml/` | PyTorch U-Net training/inference/vectorization |
| `scripts/` | Pipeline core (`pipeline.py`, `constants.py`, `result.py`) + stage modules (`ingest/`, `normalize/`, `merge/`, `export/`) + many one-off tools |
| `data/sources/` | Per-source raw + normalized data (+ `manifest.json` state files — don't delete) |
| `data/merged/`, `data/export/` | Generated — never hand-edit; rerun pipeline stage instead |
| `docs/` | All documentation |
| `.claude/commands/` | Workflow commands |
| `AGENTS.md` | Full codebase guide for agents |

## Common Commands

```bash
# Development (backend/scripts are volume-mounted — restart suffices, no image rebuild)
docker compose up -d                 # Full stack at http://localhost:8080
docker compose restart               # After backend/nginx changes
make serve                           # Frontend-only dev server (npx serve — python http.server breaks PMTiles)

# Data Pipeline (always from repo root with PYTHONPATH=scripts)
PYTHONPATH=scripts python3 scripts/pipeline.py --stage all      # ingest→normalize→merge→export
PYTHONPATH=scripts python3 scripts/pipeline.py --stage export   # regenerate frontend data only
PYTHONPATH=scripts python3 scripts/pipeline.py --list           # sources + stage status

# Testing
PYTHONPATH=scripts python3 -m pytest tests/ -v   # unit tests
python3 scripts/test_pipeline_e2e.py             # end-to-end pipeline test
node --check frontend/app.js                     # Validate JS syntax (after every JS edit)
./scripts/validate_phase1.sh                     # artifact checks

# ML
python ml/train.py --config ml/config.yaml
python ml/predict.py --checkpoint models/checkpoints/best_model.pth --input image.png
python ml/vectorize.py --input mask.png --output features.geojson
```

## Testing Requirements

Before any PR/commit:
1. `node --check frontend/app.js` - JavaScript syntax (plus any other edited .js)
2. `docker compose restart` - Server still works
3. Browser console - No MapLibre errors
4. Relevant validation script / `pytest tests/`

## Critical Gotchas

(Full list: AGENTS.md §10)

1. `PYTHONPATH=scripts` from repo root for all pipeline scripts — sibling-module imports fail otherwise.
2. PMTiles require HTTP Range requests: never `python3 -m http.server`, never enable gzip for `/data/` in nginx.
3. Backend API from browser/host is `localhost:8080/api/` (via nginx), not `:5000`.
4. Match existing patterns: Result type (`scripts/result.py`) in pipeline code, MapLibre *legacy* filter syntax in frontend, `BaseIngestor`/`BaseNormalizer` for new sources.
5. No fallback years: every exported feature carries `sd` (spec: `feat_temporal_pipeline/SPEC.md`).
   Low-evidence (`ev='l'`) buildings render muted; the "Estimated" toggle hides them.
6. Affine/TPS transform math is duplicated between `source_manager.html` and `feature_extraction.js` — fixes likely belong in both; flag it.

## Documentation Rules

### When Updating Docs

1. **Never delete** without explicit user approval
2. **Mark deprecated** instead of removing
3. **Add changelog** entries for significant changes
4. **Cross-reference** related docs

### Document Types

- `need/*.md` - User-facing requirements (WHY)
- `spec/*.md` - Product specifications (WHAT)
- `spec/feat_*/` - Feature specifications
- `tech/*.md` - Technical architecture (HOW)
- `todo/*.md` - Task tracking

## Git Safety

- All changes protected by git
- Commit frequently with descriptive messages
- Never force push to main
- Use branches for risky changes
