# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Shared infra for the hasadna Open Bus hackathon. Each participant writes one
"analysis" function; every analysis shows up as a card on a shared React
dashboard for the final presentation. POCs proven here get consolidated
upstream into `open-bus-map-search`, `open-bus-stride-api`, and
`open-bus-pipelines`.

Everything runs inside the devcontainer (Python 3.12 via `uv`, Node 22) —
don't assume Python/Node are installed on the host.

## Commands

Everything goes through `./dev` (works in the devcontainer and on a bare
machine with `uv` installed):

```
./dev              start dashboard (5173) + API (8000) + JupyterLab (8888) together
./dev dash         dashboard (React/Vite) only
./dev api          analyses API (FastAPI, --reload) only
./dev lab          JupyterLab only, no token/password
./dev new <name>   scaffold analyses/<name>.py from analyses/_template.py.txt
./dev list         list every registered analysis (imports analyses/, no server needed)
./dev check        import every analysis and report breakage — run this before relying on a change
./dev save "msg"   git add -A && commit && push (this repo commits almost everything, including notebooks/workspace)
./dev setup        uv sync + npm install (auto-runs on first use of any other command)
```

There is no test suite and no configured linter invocation beyond `ruff`
(`[tool.ruff]` in `pyproject.toml`, line-length 100, target py312). Run
`ruff check .` directly if you need it. `./dev check` is the closest thing to
a test: it re-imports every module under `analyses/` and fails if any of them
raise on import.

To run/debug a single analysis without the server:

```python
from openbus_hack import discover, get, run, AnalysisRequest
discover()  # populates the registry by importing analyses/*
run("delay-by-hour", AnalysisRequest(lines=["480"]))
```

Frontend-only commands live in `frontend/` (`npm run dev`, `npm run build` —
`tsc -b && vite build`, `npm run preview`).

## Architecture

**Registry pattern, not a plugin system with manual wiring.** Adding a file
under `analyses/` and decorating one function with `@analysis(...)` is the
entire integration: `openbus_hack.registry.discover()` walks every module in
the `analyses` package and importing it is what registers it (side effect of
the decorator running at import time). The FastAPI server calls `discover()`
once at startup. A module that fails to import is caught, recorded in
`_IMPORT_PROBLEMS`, and surfaced to the dashboard as a broken-card notice —
it does not stop other analyses from loading or crash the server. Keep this
property in mind when touching `registry.py` or `server.py`: failures must
stay isolated per-module.

**The contract (`openbus_hack/contract.py`) is the shared vocabulary between
every author's analysis and the dashboard.** An analysis function takes an
`AnalysisRequest` (lines/operators/date range/free-form `options`, all with
sane defaults so it also runs standalone in a notebook) and returns something
renderable. Authors normally call a helper (`metrics`, `line_chart`,
`bar_chart`, `table`, `image`) rather than constructing `AnalysisResult`
directly. `registry.run()` also coerces "natural" return values it doesn't
recognize — a raw DataFrame, a matplotlib Figure, a pandas Series, a dict —
via `_coerce()`, and `run()` never raises: any exception is turned into an
`error()` result so one broken analysis renders as an error card instead of a
500 mid-demo. `AnalysisResult` is one flat Pydantic model (not a tagged
union) keyed by `kind`, deliberately, so the frontend has a single shape to
narrow on. `ensure_table()` auto-derives a table view from chart series if
the author didn't supply one — every chart is required to have a table
fallback ("relief view") because the palette has some sub-3:1-contrast slots
in light mode.

**Data access goes through `openbus_hack/stride.py`**, a thin, paginating,
disk-caching client over the public Open Bus Stride API
(https://open-bus-stride-api.hasadna.org.il/docs, overridable via
`STRIDE_API_URL`). Every call returns a DataFrame; responses are cached to
`.cache/stride/` keyed by path+params so repeated notebook cells hit disk,
not the shared community API. `gtfs_rides_agg`'s `group_by` only accepts the
fields in `AGG_GROUP_BY_FIELDS` (`gtfs_route_date`, `gtfs_route_hour`,
`operator_ref`, `day_of_week`, `line_ref`) — anything else 500s server-side,
so it's validated client-side first. Prefer `gtfs_rides_agg`/`siri_rides`
over paging raw endpoints when the shape fits. Known defects in the upstream
data — the stored SIRI→GTFS ride link is empty since 2024-10, `siri_ride` has
~2.6% duplicate journeys, `first_vehicle_location_id` is a processing-state
flag rather than a transmission signal, and five operators never reach the
feed at all — are documented in `docs/busanalysis.md`. Check it before
building an analysis that joins planned to actual or reads those columns.

**Styling is shared between Python and TypeScript by convention, not by
import**: `openbus_hack/theme.py`'s `SERIES_LIGHT`/`SERIES_DARK` palettes are
the same hex values as `frontend/src/theme.css`. If you change one, change
the other — they're validated for colorblind-safe adjacent-pair separation
and slots are assigned in fixed order (never reorder; fold overflow into
"Other" past 8 series). Structured results (`line_chart`, etc.) get this
styling for free from the frontend renderer; `theme.use_openbus_style()`
is only needed when returning a raw matplotlib PNG via `image()`.

**Frontend** (`frontend/`, React + Vite + TS): `api.ts` talks to the FastAPI
endpoints (`/api/analyses`, `/api/analyses/{name}/run`, `/api/agencies`,
`/api/lines`), `App.tsx` renders the card grid, `Chart.tsx` renders the
`AnalysisResult.kind`-tagged payload. CORS is wide open (`allow_origins=["*"]`)
since this is a local/Codespaces hackathon tool, not a deployed service.

**Per-person scratch space**: `workspace/<name>/` (notebooks, data, out,
NOTES.md) is gitignored-friendly scratch but *is* meant to be committed
(`./dev save`) — this repo intentionally ignores almost nothing, including
notebooks and intermediate results, on the principle that a half-finished
notebook in git beats a perfect one on a laptop. Only `analyses/*.py` is what
actually reaches the dashboard; `ruff` ignores unused-var/import lint in
`workspace/**` and `notebooks/**` since those are exploratory.

## Devcontainer notes

`.devcontainer/Dockerfile` builds on
`mcr.microsoft.com/devcontainers/python:1-3.12-bookworm`. That base image
ships a broken `dl.yarnpkg.com` apt source (no matching GPG key) — it's
removed before `apt-get update` runs. Hebrew font coverage (agency names
render in Hebrew) comes from `fonts-noto-core` (Debian has no standalone
`fonts-noto-hebrew` package). Claude Code itself runs inside the container
via the `ghcr.io/anthropics/devcontainer-features/claude-code` feature; its
login is persisted in a `claude-code-config-${devcontainerId}` Docker volume
via `CLAUDE_CONFIG_DIR`, so re-login isn't needed after a rebuild.
