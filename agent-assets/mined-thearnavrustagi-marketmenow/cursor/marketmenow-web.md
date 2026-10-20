---
description: Conventions for the FastAPI web dashboard
globs: src/web/**
alwaysApply: false
---

# Web Dashboard Rules

## Architecture

The web app spawns `mmn` CLI commands as subprocesses — it does not call the
Python pipeline directly. `cli_runner.py` handles subprocess execution and
progress parsing. Real-time updates flow through `EventHub` → WebSocket.

Adapter CLIs are mounted as **hidden groups** in `marketmenow/cli.py`
(`hidden=True`). They don't appear in `mmn --help` but remain callable by the
web frontend. New workflows (like `reddit-launch`) use `mmn run <name>` directly.

## Key Modules

- `app.py` — FastAPI app with lifespan (DB pool + queue worker), WebSocket at
  `/ws/content/{item_id}`, route registration, static/output mounts.
- `cli_runner.py` — `run_cli()` and `run_cli_streaming()`. Defines `PLATFORM_META`
  (JSON params) and `BUILDERS` (command constructors). Progress parsed via regex.
- `queue_worker.py` — `run_queue_loop()` background task. Polls DB queue, checks
  per-platform rate limits, calls `run_cli_streaming` for each job.
- `events.py` — `EventHub` pub/sub per content-item UUID. `ProgressEvent` types:
  `phase`, `progress`, `wait`, `log`, `stderr`, `done`, `error`.
- `db.py` — asyncpg pool, all DB operations (content, queue, rate limits, post log).

## Patterns

- Routes live in `routes/` as separate `APIRouter` instances.
- Templates are Jinja2 in `templates/`.
- Static assets in `static/` (CSS, JS).
- Generated output mounted at `/output` from `settings.output_dir`.

## Adding a Platform to the Dashboard

1. Add an entry to `PLATFORM_META` in `cli_runner.py` (label, modality, params).
2. Write generate and publish `CommandBuilder` functions.
3. Register them in the `BUILDERS` dict.
4. No route changes needed — the generate page auto-discovers from `PLATFORM_META`.

## Database

PostgreSQL via asyncpg. Pool initialized in lifespan, closed on shutdown.
`MMN_WEB_DATABASE_URL` env var required.
