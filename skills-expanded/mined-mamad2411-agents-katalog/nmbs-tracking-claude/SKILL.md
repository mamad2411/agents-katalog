# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static dashboard set + automated daily delay log for the **direct** (0-transfer)
NMBS/SNCB trains across a small monitored network, built entirely on the open
[iRail API](https://docs.irail.be/). No build step, no server framework — plain
HTML files served from GitHub Pages (https://thbraet.github.io/nmbs_tracking/)
plus a single Python script run by a daily cron.

### The monitored network and the anchor rule

Six **monitored stations** are watched: `Diest`, `Halle`, `Leuven`,
`Brussels-North`, `Brussels-Central`, `Brussels-South/Brussels-Midi` (iRail names).
Of these, three are **anchors**: `Diest`, `Halle`, `Leuven`. The Brussels trio is
pass-through.

A train is tracked **iff its trajectory visits ≥1 anchor AND ≥2 monitored stations.**
This is the core domain rule. It keeps anchored trajectories (e.g. a Knokke→Liège
IC that passes Brussels-South → -Central → -North → Leuven is kept for its
Brussels⇄Leuven segment) and drops the firehose of trains that merely clip two
Brussels stations with no anchor — pure Brussels↔Brussels has no anchor, so it's
excluded.

Each kept train is sliced to its **segment**: the span from its first to its last
monitored stop (inclusive — intermediary non-monitored stops like Aarschot or
Brussels Airport are kept so delay evolution along the trajectory is visible).
The segment is labelled `origin → dest` by the first/last monitored stop.

## Commands

```bash
# Run the daily collector locally (upserts log/trips_history.csv + log/stops_history.csv)
pip install certifi
python fetch_log.py

# Serve the dashboards locally — segment-explorer.html fetches log/stops_history.csv,
# which fails under file:// (CORS), so it MUST be served over http:
python -m http.server 8000     # then open http://localhost:8000/
```

There are no tests, linters, or package manifests. `fetch_log.py` uses only the
standard library plus optional `certifi`. `migrate_logs.py` is a one-shot that
already converted the old per-route logs to the current schema — keep it for
record, but it no-ops once the CSVs are in the new schema.

> Corporate-proxy caveat (see user memory): local Python HTTPS may fail with a cert
> error behind the corporate TLS proxy. If `fetch_log.py` can't reach iRail locally,
> that's the environment, not the code — the GitHub Actions run is the source of
> truth. To exercise parsing/slicing logic locally, fetch sample JSON with `curl`
> and feed it through `fetch_log.extract_segment`.

## Architecture

Three pieces share two contracts: the **MONITORED/ANCHORS station sets** and the
**iRail station names**.

1. **`fetch_log.py`** — the collector. Two phases:
   - *Discover*: sweep iRail `/connections` for every ordered monitored pair with at
     least one anchor endpoint (`DISCOVERY_PAIRS`, ~24 sweeps — everything except
     Brussels→Brussels), paginating each across the whole day, to build the set of
     unique direct vehicle IDs touching the network.
   - *Collect*: fetch each vehicle's full stop list from `/vehicle`, run
     `extract_segment` (the anchor rule above), and log the per-stop delays of the
     qualifying ones.
   Run by the daily workflow.

2. **`.github/workflows/daily.yml`** — GitHub Actions cron. GitHub cron is UTC-only
   but we want 23:45 *Brussels* time year-round, so it fires at **both** 21:45 and
   22:45 UTC and a DST-aware gate step proceeds only on the trigger that lands on the
   23:00 Brussels hour (manual `workflow_dispatch` runs always proceed). 23:45 is
   late enough to capture a full day yet still "today" in Brussels, which matters
   because **iRail only exposes real-time delays for the current day** — that's the
   whole reason this must run late each evening. Needs `contents: write` to commit
   the log back.

3. **The HTML dashboards** (`index.html` landing → `live-board.html`,
   `segment-explorer.html`) — self-contained, no dependencies.
   - `live-board.html` calls `/liveboard` for all six stations directly from the
     browser.
   - `segment-explorer.html` fetches `log/stops_history.csv` for past days and
     computes *today* live in-browser: it enumerates today's direct trains for the
     selected segment via `/connections`, fetches each `/vehicle` (concurrency capped
     at 3), and runs the **same `extractSegment` logic as the collector** so live and
     logged data match.

### Data outputs (under `log/`, both idempotent per day)
- `log/trips_history.csv` — one row per train per day. Schema `TRIPS_CSV_COLS`
  (`date, origin, dest, train, dep_time, dep_delay_min, arr_delay_min,
  arr_delay_sec, canceled`). Compact long-term overview / export.
- `log/stops_history.csv` — one row per train **per stop** per day along the segment.
  Schema `STOPS_CSV_COLS`; carries `origin`/`dest` (the segment endpoints),
  `monitored` (0/1), and `seq` (0-based stop index). This is the source of truth the
  explorer reads. **Idempotent per day**: a run drops all existing rows for today's
  date and re-writes them, so re-running never duplicates.

## Conventions that matter

- **MONITORED / ANCHORS are the cross-file contract.** `MONITORED` and `ANCHORS` in
  `fetch_log.py` must mirror the `MONITORED`/`ANCHORS` sets in `segment-explorer.html`
  (and the station list in `live-board.html`). The two must agree on the exact iRail
  station names (e.g. `Brussels-South/Brussels-Midi`) or live and logged data diverge.
  `extract_segment` (Python) and `extractSegment` (JS) implement the **same** anchor
  rule; change them together.
- **`origin`/`dest` replace the old `route` slug.** A train's segment is identified by
  its first/last monitored stop, not a hardcoded route. There is no fixed route list
  any more — segments are discovered from the data. `segment-explorer.html` populates
  its picker from the distinct `(origin, dest)` pairs in `stops_history.csv`.
- **Times are Brussels-local.** The collector works in `Europe/Brussels` (`zoneinfo`);
  the workflow gate uses `TZ=Europe/Brussels`. Don't introduce naive/UTC timestamps.
- **iRail politeness is deliberate.** All requests go through `_get_json()`, which
  throttles to ~1.4 req/s (`MIN_REQUEST_INTERVAL`), sends a descriptive `User-Agent`,
  and backs off on 429/5xx/network errors honoring `Retry-After`. A full run is ~24
  connection sweeps plus one `/vehicle` fetch per unique vehicle (a few hundred all
  told) — sustained ~1.4 req/s stays well under iRail's ~3 req/s cap. Preserve the
  throttle/backoff when editing fetch logic. The browser-side live fetch in
  `segment-explorer.html` caps `/vehicle` concurrency at 3 for the same reason.
- **CSV upsert** is `_upsert_csv` in `fetch_log.py`: it keeps every row whose `date`
  differs from today and re-appends today's fresh rows. Both CSVs share it.
