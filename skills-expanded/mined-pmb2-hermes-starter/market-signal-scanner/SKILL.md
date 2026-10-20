---
name: market-signal-scanner
description: Use when building multi-source market signal scanners.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [market-data, signal-scanners, pipelines, trading, cron]
    triggers: [market signal scanner, multi-source scanner, signal scanner, symbol extraction, watchlist generator, picks engine, stock scanner]
    related_skills: [sports-data-pipeline, scheduled-scanner-scanner]
---

# Market Signal Scanner

Build and operate multi-source signal scanners (stock sniffer, picks engines, watchlist generators): ingest social + editorial + media sources → normalize → extract symbols → score for a strategy → confirm with market data → persist ledger → deliver scheduled reports.

## Architecture (7 stages)

1. **Sources** → `RawItem` (source, source_id, title, body, author, created_at, score, comments, meta)
2. **Symbol extraction** — cashtags first (`$NVDA`), then standalone uppercase with blocklist + min-length; per-source mode: YouTube = cashtag + 3-char min standalone, StockTwits = cashtags only (+ meta symbol), Reddit/RSS = standalone 2-char min
3. **Per-ticker aggregation buckets** — items, source-set, texts, engagement, fit, recency
4. **Score 0-100** — engagement×w + recency×w + multi-source-confirm×w + strategy-fit×w − risk×w; multi-source bonus; challenge/priority bonus (e.g. "30 day challenge" videos)
5. **Confirmation layer** — keyless quotes/earnings for top N signals (cached 15 min); context only, never alters social score
6. **Ledger** — SQLite runs + signals + per-ticker day table for mention streaks (🔥Nd in reports)
7. **Report + cron** — Discord-compact house style; `[SILENT]` exact match when nothing actionable

## Keyless source playbook
See `references/financial-data-sources.md` — verified endpoints for Reddit (browser UA required), StockTwits trending/streams, working vs dead RSS feeds, yfinance quote/earnings quirks, OmniRoute LLM gating.

## Pressure tests (fully offline)
- **Determinism**: same input twice → identical signal list (guards time/order nondeterminism)
- **Noise robustness**: 300 random capslock-word posts → ≤8 signals (blocklist must hold)
- **Multi-source ranking**: cross-source confirmation must outscore a single loud mention
- **Scale budget**: 500 mixed items score in <2s
- **Offline parser fixtures** for every source adapter (canned JSON/XML, no network in CI)

## Pitfalls
- **YAML bool trap**: unquoted `ON/OFF/NO/YES` in YAML parse as Python booleans → `AttributeError: 'bool' object has no attribute 'upper'` in ticker blocklists. Quote them in YAML AND coerce `str()` with a bool guard in code.
- **StockTwits crypto pollution**: symbols ending `.X` (CRO.X) are crypto — filter out of equity watchlists.
- **Reddit public JSON**: 403 without a browser-like UA; keep multi-host fallback chain (www.reddit.com → old.reddit.com → api.reddit.com) and per-host try/except.
- **Single-source YouTube noise**: standalone caps from transcripts are spam; require cashtags, challenge-tagged titles, or multi-mention to pass the floor.
- **Cron Guardian auto-pause**: the guardian pauses ALL jobs on the box (not just the broken one) during model-unavailable events. After any infra event, check `cronjob list` for `state: paused` and `cronjob action=resume job_id=...` — then re-verify `state: scheduled`.
- **Cron job shape**: set `workdir` to the repo, toolsets `["terminal","file"]`, prompt says "deliver the report only", script prints report to stdout; empty results emit the exact string `[SILENT]` so cron stays quiet.
- **Feed drift**: RSS/news endpoints die silently (empty body or HTML). Verify feeds with a curl probe before wiring, and treat feeds as non-critical (surface errors in report notes, don't fail the scan).

## Verification
1. `python -m pytest -q` — all offline tests green
2. Live smoke: run the real scan (`scan --mode morning`) and confirm every source name appears in the "Checked: sources ..." footer line
3. Spot-check that market/earnings context renders on watchlist rows
4. `cronjob list` → jobs show `state: scheduled` with correct `next_run_at`
5. Commit + push; cron prompts only change when schedule/prompt semantics change
