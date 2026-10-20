# backend

FastAPI app. Python managed with uv.

## Commands

| Task | Command |
|---|---|
| Install deps | `uv sync` |
| Run dev server | `uv run uvicorn app.main:app --reload` |
| Run tests | `uv run pytest` |

## Environment variables

| Variable | Purpose |
|---|---|
| `R5PY_HELSINKI_ENGINE_URL` | Optional URL for the Helsinki r5py grid engine; defaults to the static development grid client |
| `DIGITRANSIT_API_KEY` | Optional Digitransit API key for live `/places/search`; defaults to the static development place provider when unset |
| `DIGITRANSIT_GEOCODING_URL` | Optional Digitransit Geocoding base URL; defaults to `https://api.digitransit.fi/geocoding` |

Set local secrets in `backend/.env`; shell environment variables override `.env` values.

## Time buckets

Six buckets map to representative arrival times (Helsinki tz):

| Bucket | Arrival |
|---|---|
| `weekday-morning` | Tuesday 08:30 |
| `weekday-midday` | Tuesday 12:00 |
| `weekday-evening` | Tuesday 17:30 |
| `weekday-night` | Tuesday 22:00 |
| `weekend-day` | Saturday 11:00 |
| `weekend-evening` | Saturday 19:00 |

## Grid engine

The public backend route is `POST /travel-time-grid`. Configure external engines in `app.main.build_grid_engine_clients()` and keep engine-specific contracts behind `GridEngineClient`.

The removed point-to-point `/durations` and `/route-detail` paths must not be reintroduced for the main map. Future route inspection belongs behind a sparse `POST /cell-route` endpoint; see ADR 0014.

## TDD

New code starts with a failing test. Use `/tdd` for any new feature area.
