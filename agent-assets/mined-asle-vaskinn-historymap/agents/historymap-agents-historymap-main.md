# AGENTS.md — Codebase Guide for AI Coding Agents

Comprehensive map of the **Trondheim Historical Map** repository for LLM-based agentic coding.
`CLAUDE.md` holds the short rules loaded every session; this file is the deep reference —
read the relevant section before editing a subsystem.

**What this project does:** Interactive web map showing Trondheim's development 1700–present.
Building/road/water features carry temporal attributes (`sd`/`ed` = start/end year) so a year
slider filters the map. Features come from OSM, Norwegian registries (SEFRAK, Matrikkelen),
manual edits, and ML extraction (U-Net) from georeferenced historical Kartverket maps.

---

## 1. System Architecture

```
                       Browser (http://localhost:8080)
                                   │
                  ┌────────────────┴───────────────────┐
                  │  nginx (docker: historymap-web)    │
                  │  :80 in container → :8080 on host  │
                  └───┬──────────┬──────────┬──────────┘
        static files  │   /api/  │   /wms/  │  /data/
        frontend/ ────┘          │          │      └── data/ (GeoJSON, PMTiles, raster tiles)
                                 │          └── proxied WMS (Trondheim kommune, Geonorge)
                  ┌──────────────┴─────────────────┐
                  │ FastAPI backend (:5000, docker) │
                  │ backend/app.py + backend/jobs.py│
                  └──────────────┬─────────────────┘
                                 │ subprocess jobs (one at a time)
            ┌────────────────────┼─────────────────────┐
            │                    │                     │
     scripts/pipeline.py    ml/train.py           scripts/georeference_map.py
     (ingest→normalize→    ml/predict.py          scripts/align_to_osm.py
      merge→export)        ml/vectorize.py        scripts/verify_1937_buildings.py
```

**Ports** (memorize these — getting them wrong is the #1 source of confusion):

| Port | What | How it runs |
|------|------|-------------|
| 8080 | nginx → frontend + everything else | `docker compose up` (host port) |
| 5000 | FastAPI backend (`backend/app.py`) | Docker only; **not** published to host — reach it via nginx at `localhost:8080/api/` |

---

## 2. How to Run Things

```bash
# Full stack (frontend + backend + data serving)
docker compose up -d              # or: make deploy   → http://localhost:8080
docker compose restart            # after backend/nginx changes (volumes are mounted, no rebuild needed)
docker compose down               # or: make stop

# Frontend-only dev server (PMTiles needs HTTP Range support — python http.server does NOT work)
make serve                        # npx serve -l 8080 from frontend/

# Data pipeline (always from repo root, always with PYTHONPATH=scripts)
PYTHONPATH=scripts python3 scripts/pipeline.py --stage all          # ingest→normalize→merge→export
PYTHONPATH=scripts python3 scripts/pipeline.py --stage export       # just regenerate frontend data
PYTHONPATH=scripts python3 scripts/pipeline.py --stage all --feature-type water   # buildings|roads|water|all
PYTHONPATH=scripts python3 scripts/pipeline.py --list               # show sources + stage status

# ML
python ml/train.py --config ml/config.yaml
python ml/predict.py --checkpoint models/checkpoints/best_model.pth --input image.png --output mask.png
python ml/vectorize.py --input mask.png --output features.geojson --bounds "10.38,63.42,10.42,63.44"

# Tests / validation
PYTHONPATH=scripts python3 -m pytest tests/ -v   # unit tests (constants, Result type)
python3 scripts/test_pipeline_e2e.py             # end-to-end pipeline test (inject→run→verify→cleanup)
node --check frontend/app.js                     # JS syntax — run after EVERY frontend JS edit
make test                                        # frontend checks + python syntax compile checks
./scripts/validate_phase1.sh                     # artifact existence checks
```

Backend code is volume-mounted into the container (`docker-compose.yml`), so backend/script
edits only need `docker compose restart`, never an image rebuild. Rebuild the image only when
`backend/Dockerfile` or Python deps change: `docker compose build backend`.

---

## 3. Repository Map

| Path | What it is | Edit freely? |
|------|-----------|--------------|
| `frontend/` | Vanilla JS MapLibre app, no build step | Yes — run `node --check` after |
| `backend/` | FastAPI app (`app.py`, ~1400 lines) + async job queue (`jobs.py`) | Yes |
| `scripts/` | ~70 scripts; pipeline core + many one-offs (see §6 for which are load-bearing) | Core: carefully. One-offs: rarely needed |
| `scripts/{ingest,normalize,merge,export,ml,api}/` | Pipeline stage modules | Yes |
| `ml/` | PyTorch U-Net training/inference/vectorization | Yes |
| `data/` | All data (5+ GB). `sources/` (per-source raw+normalized), `merged/`, `export/`, `georeference/`, `training_*/`, `annotations/` | **Never** hand-edit generated files; manage via pipeline |
| `models/checkpoints/` | Trained weights (`best_model.pth`, 172 MB) | No |
| `synthetic/` | Synthetic training data generation (aged OSM renders + masks) | Rarely |
| `docs/` | Doc system: `need/` → `spec/` → `tech/` → `todo/` (see §9) | Yes |
| `tests/` | pytest unit tests + `conftest.py` fixtures | Per task |
| `production/` | Prod docker-compose (single nginx service, resource limits) | Rarely |
| `nginx.conf` | All routing: static, /api/ proxy, /wms/ proxies, PMTiles headers | Carefully (see §5) |
| Root `PHASE*_*.md`, `HISTORICAL_MAP_PROJECT_PLAN.md`, `PMTILES_IMPLEMENTATION.md`, `SOURCE_FILTER_FIX.md` | **Stale** historical phase reports — do not treat as current truth | Don't update; superseded by `docs/` |

**Authoritative status docs:** `docs/todo/current_work.md` (what's in flight) and
`docs/tech/IMPLEMENTATION_STATUS.md` (known loose ends). Root-level `PHASE*` files are archives.

---

## 4. Frontend

Stack: **MapLibre GL JS 4.0** + **PMTiles 3.0.6** via CDN (`unpkg.com`). Vanilla ES6, **no build
step, no framework, no npm install**. Leaflet 1.9.4 only in `source_manager.html`; Mapbox GL Draw
only in `feature_extraction.html`.

### Pages

| Page | Lines | Purpose | Backend deps |
|------|-------|---------|--------------|
| `index.html` + `app.js` (3.3k) + `style.css` | main | Map viewer: year slider 1700–2025, layer toggles, inspection mode, edit mode | Edit mode → Flask `:5001/api/manual`; otherwise static data only |
| `source_manager.html` (2.7k, **all JS inline**) | tool | Georeferencing UI: dual canvas (image px ↔ map coords), GCP placement, affine/TPS transform math, overlay preview, source catalog CRUD | FastAPI `/api/sources`, `/api/georef/*`, `/api/georeference` |
| `feature_extraction.html` + `feature_extraction.js` (3k) + `.css` | tool | ML pipeline control: training/verification jobs, annotation drawing, water editing, log streaming | FastAPI `/api/*` jobs + `WS /api/logs` |
| `about.html`, `1880_overlay.html`, `test_source_filter.html` | misc | Info page, demo, filter test page | none |

### app.js structure (the file you'll edit most)

- **Config** (top): map center `[10.39, 63.43]`, year range 1700–2025, historical-style threshold 1950.
- **Global state**: `currentYear`, `layerVisibility`, `dateSourceFilter` (sef/tk/mat/finn/osm/man),
  `snapshotFilter` (kv1880/kv1904/air1947), `inspectionMode`, `editMode`.
- **Temporal filtering** — the heart of the app:
  - `createTemporalFilter(year)`: `sd <= year AND (ed >= year OR ed == null)`.
  - `createBuildingFilter(year)`: dual mode — **Type A** sources (sef, mat, tk, man, finn, osm)
    are timeline-filtered; **Type B** ML snapshots (kv1880, kv1904, air1947) show all-or-nothing
    per `snapshotFilter`. Undated buildings fall back to appearing from **1960**; undated roads from **2000**.
  - `createRoadFilter(year)`: evidence-gated before 1900 (`ev == 'h'` only).
- **`updateLayerFilters(year)`**: updates filters in place on year change — never recreates the style.
  `createMapStyle(year)` builds the full style once at init/mode-switch.
- **Inspection mode**: overlays a historical raster + ML detections colored by confidence (`mlc`).
- **Edit mode**: click building → edit `sd`/`ed` form → POST `localhost:5001/api/manual`.

### Frontend rules

1. `node --check frontend/app.js` (and any edited .js) after every change — this is the only "compiler".
2. MapLibre **legacy filter syntax** is used throughout (`['==', 'prop', val]`, `['all', ...]`) — match it.
3. Data paths are relative to `frontend/` (e.g. `data/buildings_temporal.pmtiles`); in Docker,
   `data/` is the repo's `data/` dir mounted into nginx, and `frontend/data/` symlinks cover local dev.
4. Cache busting via `data/manifest.json` hashes (`getVersionedUrl()`) — don't invent new schemes.
5. Source colors are consistent across pages (tk=purple, finn=blue, sef=brown, osm=teal, man=green) — reuse.
6. Transform math (affine/TPS) is **duplicated** between `source_manager.html` and
   `feature_extraction.js` — a fix in one likely belongs in both. Flag it, don't silently fix one.
7. Test via HTTP (`make serve` or docker), never `file://` — PMTiles needs Range requests.

---

## 5. Backend & Serving

### FastAPI backend (`backend/app.py`, port 5000)

~34 endpoints under `/api`. Groups:

| Group | Endpoints | Notes |
|-------|-----------|-------|
| Health/status | `GET /api/health`, `GET /api/status` | status aggregates training/model/verification/job state |
| Jobs | `POST /api/generate-training`, `/api/train`, `/api/verify`, `/api/apply-annotations`, `/api/align`; `GET /api/jobs/{id}`; `WS /api/logs` | All return a `JobResponse`; logs stream over the WebSocket |
| Annotations | `GET/POST /api/annotations` | persists to `data/annotations/annotations_1937.json` |
| Source catalog | `GET/POST /api/sources`, `PUT/DELETE /api/sources/{id}` | persists to `data/sources/map_sources.json` |
| Georeferencing | `POST /api/georeference`, `GET /api/georef/images`, `POST /api/georef/upload`, `GET/POST /api/georef/gcps/{map_id}`, `POST /api/georef/run`, `GET /api/georef/manifest`, `GET /api/georef/output/{map_id}` | GCPs persist to `data/georeference/gcps/*.gcp.json`; output GeoTIFFs to `data/georeference/output/` |
| Alignment | `POST /api/align`, `GET /api/alignment-report/{source}` | wraps `scripts/align_to_osm.py` (IoU match + TPS/TIN/affine) |
| Water | `GET /api/water`, `POST /api/water/{add,update,delete}` | persists to `data/sources/manual/water.geojson` |

### Job system (`backend/jobs.py`)

- asyncio `JobManager`, **strictly sequential** — one subprocess job at a time, rest queue.
- Jobs run scripts with container paths (`/app/scripts/...`, `/app/ml/...`).
- **Jobs are in-memory only** — a backend restart loses job history (artifacts on disk survive).
- Output is streamed line-by-line to all WebSocket clients on `/api/logs`.

### nginx (`nginx.conf`)

- `/` → frontend static; `/api/` → `proxy_pass http://backend:5000` with WebSocket upgrade
  headers and 300s timeouts; `/data/` → repo `data/` dir.
- `/wms/trondheim/` and `/wms/geonorge/` proxy external WMS servers (CORS workaround for the browser).
- **PMTiles rules you must not break:** gzip **disabled** for `.pmtiles` and `/data/` (byte-range
  requests required), `Accept-Ranges` enabled, 30d immutable cache. CORS headers are set
  per-location — adding a global CORS header will duplicate them and break responses.
- `client_max_body_size 100M` for georef image uploads.

### Retired standalone servers (all consolidated into the FastAPI backend 2026-07-04)

- Flask manual-edit API (:5001) → `GET/POST /api/manual`, `POST /api/rebuild` in `backend/app.py`.
- Water editor (:5002) → `/api/water/*`; legacy georef server (:8082) → `/api/georef/*`.

---

## 6. Data Pipeline

### Stages & flow

```
data/sources/{src}/raw/  ──normalize──►  data/sources/{src}/normalized/*.geojson
                                                      │
                                                    merge          (merge_config.json: priorities, spatial matching)
                                                      ▼
                                         data/merged/{buildings,roads,water}_merged.geojson
                                                      │
                                                    export         (shortcodes, compaction, tippecanoe)
                                                      ▼
                                         data/export/*.geojson + *.pmtiles + manifest.json
```

Orchestrator: `scripts/pipeline.py` (stages: `ingest|normalize|merge|export|all`,
`--feature-type buildings|roads|water|all`, `--no-pmtiles`, `--list`).
Per-source completion is tracked in `data/sources/{src}/manifest.json` — completed stages are
skipped on re-run; invalidate with `scripts/pipeline_state.py`.

### Load-bearing modules (changes here ripple everywhere)

- `scripts/pipeline.py`, `pipeline_state.py`, `constants.py` (canonical paths/source enums/field maps),
  `config_schema.py`, `result.py` (Result type used by all pipeline functions — match this pattern).
- `scripts/ingest/base.py` (BaseIngestor) + per-source ingestors.
- `scripts/normalize/base.py` (BaseNormalizer — **enforces the schema**, see §8) + `normalize_*.py` per source.
- `scripts/merge/merge_sources.py` (buildings), `merge_roads.py`, `merge_water.py`, `match_roads.py`.
- `scripts/export/export_geojson.py` (compaction + source shortcodes), `export_pmtiles.py`
  (tippecanoe wrapper), `export_roads.py`, `export_water.py`, `export_manifest.py` (cache-bust hashes).
- Config: `data/merged/merge_config.json` (source priorities and matching rules).

Most of the other ~40 scripts in `scripts/` are one-off phase tools (annotation helpers,
extraction experiments, verification, fine-tuning). Check whether `pipeline.py` or `backend/app.py`
references a script before assuming it's live.

### Adding a new data source (established pattern — follow exactly)

1. `data/sources/{source_id}/manifest.json` with a `source_id` field (pipeline auto-discovers it).
2. `scripts/ingest/{source_id}.py` extending `BaseIngestor`.
3. `scripts/normalize/normalize_{source_id}.py` extending `BaseNormalizer`.
4. Add the source to `data/merged/merge_config.json` priorities.

### Tiles

- **Vector**: tippecanoe via `scripts/export/export_pmtiles.py` (zoom 10–16, attributes
  `sd,ed,ev,src,nm` typed as int where applicable). Install: `brew install tippecanoe`.
- **Raster** (historical map overlays): `./scripts/generate_raster_tiles.sh [map]` (GDAL/gdal2tiles)
  → XYZ pyramid in `data/export/tiles/{map}/z/x/y.png`. See `docs/tech/TILE_COMMANDS.md`.

---

## 7. ML Pipeline

U-Net semantic segmentation (`segmentation-models-pytorch`), encoder ResNet18/34/50 or
EfficientNet-b0. 5 classes: 0=background, 1=building, 2=road, 3=water, 4=forest.
Device auto-detect: CUDA → MPS (Apple Silicon) → CPU (`ml/utils.py`).

| File | Role |
|------|------|
| `ml/train.py` | YAML-config training loop: mixed precision, ReduceLROnPlateau, early stopping, checkpoints |
| `ml/predict.py` | Inference (single image or `--input-dir` batch) → grayscale PNG masks (pixel = class id) |
| `ml/vectorize.py` | Mask → GeoJSON: contours, simplification, buildings as polygons, roads skeletonized to lines; `--bounds` georeferences output |
| `ml/dataset.py`, `losses.py`, `evaluate.py` | Albumentations aug + ImageNet norm; Dice/Focal/Combined loss; IoU metrics |

Configs share one structure (`model`/`training`/`data`/`paths`/...): `config.yaml` (standard 5-class),
`config_quick.yaml` (fast smoke test), `config_water.yaml` (water-weighted classes),
`config_1904.yaml` (binary building detection, fine-tune LR), `config_1937.yaml` (used by backend
`POST /api/train` default). Image size 512×512 everywhere.

Checkpoints: `models/checkpoints/best_model.pth` exists (5-class, 172 MB);
`checkpoints_1904/` and `checkpoints_1937/` are empty (not yet trained to completion).
Training data lives in `data/training_*/` and `data/synthetic/`; `synthetic/` (repo root) holds
the generation code for synthetic training data.

---

## 8. Data Schemas

### Normalized schema (enforced by `scripts/normalize/base.py::validate_feature`)

Every feature in `data/sources/*/normalized/`:

| Field | Req | Meaning |
|-------|-----|---------|
| `_src` | ✓ | source id (`osm`, `sefrak`, `manual`, `ml_detected`, …) |
| `_src_id` | ✓ | id within source — never modified downstream |
| `_ingested` | ✓ | YYYY-MM-DD |
| `sd` / `ed` | – | start/end year (int; `ed` null = still standing) |
| `ev` | – | evidence: `h` / `m` / `l` (validated single char) |
| `bt`, `nm` | – | building type, name |
| `_raw` | – | original source properties, preserved for audit |

### Export/frontend schema (what the map reads from PMTiles/GeoJSON)

Source ids are **shortened** at export (`sefrak`→`sef`, etc. — mapping in `scripts/constants.py`
applied in `export_geojson.py`). Buildings: `bid`, `sd`, `ed`, `ev`, `src`, `nm`,
`sd_src` (date provenance: sef/tk/mat/finn/osm/man/inh/ml_*), `sd_method`
(direct/inferred/estimated/inherited), `mlc` (ML confidence 0–1), `donors` (ids that contributed
an inherited date). Roads add `ct` (change type: same/widened/rerouted/replaced/removed/new),
`rt` (road class), `ml_src`. Water: `wtype` (harbor/river/fjord/lake/canal) + `sd`/`ed`.

---

## 9. Documentation System & Workflow

Doc layers (every change should keep these aligned — `/sync` checks drift):

- `docs/need/` — WHY: problem statement, user needs, constraints, success criteria.
- `docs/spec/` — WHAT: `PRODUCT_SPEC.md`, `PIPELINE_DESIGN.md`, per-feature `feat_*/` dirs with status.
- `docs/tech/` — HOW: architecture (`DATA_PIPELINE_ARCHITECTURE.md`, `DATA_SCHEMA.md`),
  tile docs, georef analysis, `IMPLEMENTATION_STATUS.md` (loose-ends inventory; verify against
  code before acting on an entry — parts may pre-date recent work).
- `docs/todo/current_work.md` — what's in flight right now. **Read this first on any new task.**

Workflow commands in `.claude/commands/`: `/propose` → approve → `/implement` → `/test` → `/sync`,
plus `/status`, `/next`, `/doctor`, `/fix`, `/validate`, `/research`, `/arch-review`, `/parallel-impl`.
Specialized agents in `.claude/agents/` (data-pipeline, gis-architect, map-ux, plus arch/dev/review/utility sets).

Doc rules: never delete docs without approval — mark deprecated instead; add changelog entries;
cross-reference related docs.

---

## 10. Gotchas — Read Before Editing

1. **`PYTHONPATH=scripts` from repo root** for anything importing pipeline modules; otherwise
   `ModuleNotFoundError` on `from normalize.base import ...`.
2. **PMTiles need HTTP Range**: `python3 -m http.server` silently breaks the map. Use
   `make serve` or docker. Same reason gzip is off for `/data/` in nginx — keep it off.
3. **Backend is reached through nginx**: from the browser/host it's `localhost:8080/api/...`,
   never `localhost:5000`. Inside docker-compose it's `http://backend:5000`.
4. **Don't hand-edit `data/`** generated artifacts (`merged/`, `export/`, `normalized/`) — rerun
   the pipeline stage instead. `data/merged/` and `data/export/` are safe to delete to force
   regeneration; `data/sources/*/raw/` and the `manifest.json` state files are not.
5. **One job at a time** in the backend; jobs vanish from the API on restart (disk artifacts remain).
6. **No frontend fallback years** (removed 2026-07-04 per `docs/spec/feat_temporal_pipeline/SPEC.md`):
   every exported feature carries `sd`. Low-evidence (`ev='l'`) buildings render muted (0.35
   opacity); the "Estimated" toggle in the viewer hides them entirely.
7. **`frontend/legacy/` was removed 2026-07-04** (recover via git history); current tools are
   `source_manager.html` and `feature_extraction.{html,js,css}` (renamed from `source_viewer.*` —
   some docs still use the old name).
8. **Type A vs Type B sources** in the frontend filter logic (timeline-filtered vs all-or-nothing
   ML snapshots) interact; test both `dateSourceFilter` and `snapshotFilter` paths after touching filters.
9. **Stale docs exist**: root `PHASE*` files, parts of `IMPLEMENTATION_STATUS.md`, and older specs
   referencing `dataprep.*`. When a doc contradicts the code, trust the code and flag the doc.
10. **Shapely is optional but recommended** in merge — without it, spatial matching silently
    degrades to bbox matching.
11. Validate before claiming done: `node --check` for JS, `docker compose restart` + browser console
    for the app, `pytest tests/` + `scripts/test_pipeline_e2e.py` for the pipeline.

---

## 11. Pre-flight Checklist for Any Task

1. Read `docs/todo/current_work.md` — is your task related to in-flight work?
2. Find the relevant spec under `docs/spec/feat_*/` and tech doc under `docs/tech/`.
3. Locate the subsystem in this file (§4–§7); note its gotchas.
4. Read the existing code you're about to change — match its patterns (Result type in pipeline,
   legacy filter syntax in frontend, BaseNormalizer/BaseIngestor for sources).
5. After changes: run the validation for that subsystem (§2 test commands), restart docker if
   backend/nginx changed, check the browser console for MapLibre errors.
6. Update the docs that describe what you changed (spec status, current_work.md, changelog entries).
