---
name: wreck-load
description: Page speed and load testing for a local web app with the wreck-it CLI. It measures each page with Lighthouse on a simulated phone (LCP, CLS, TBT), diagnoses slow pages with Chrome DevTools performance traces when available, runs ramp, spike and soak load profiles (p50/p90/p99 latency, error rate, breaking point, memory trend), then traces slow endpoints to causes such as N+1 queries, missing indexes or blocking work. Use as stage 7 of a wreck-it run, or when the user asks to "stress test my API", "load test", "how many users can my app handle", "find slow endpoints", "check page speed", or "run Lighthouse".
---

# wreck-load

`WRECK` means `npx @miyanishar/wreck-it`.

`WRECK run stage load running`

## Safety

- GET/HEAD only. Mutating load needs `"allowMutatingLoad": true`, which only the user sets.
- A hosted (remote) database: ask before any load test; load on a production database hurts real users.
- The CLI refuses endpoints that call AI, email, SMS or payments (thousands of real calls) unless the user allowed them.
- Prefer a production build (`npm run build && npm start`) when the user agrees; dev servers give misleading numbers. Say which you tested.

## 0. Page speed (Lighthouse)

```bash
WRECK perf --record                 # discovered pages on a simulated mid-range phone, slow 4G
WRECK perf / /products --device desktop --record   # optional: key pages on desktop
```

- Each page gets a Lighthouse score plus **LCP** (largest paint), **CLS** (layout shift) and **TBT** (main-thread blocking); reports go to `.wreck-it/perf/*.html`. With `--record`, metrics in Google's "poor" range become `performance` findings when a second run agrees.
- On a **dev server** only CLS is recorded (LCP/TBT there reflect unminified code): tell the user and offer a production-build re-run.
- Its "to judge yourself" list (best practices, SEO): mention notable ones; record only what affects users (e.g. a page without a `<title>`).
- **Diagnose slow pages** with Chrome DevTools MCP (`wreck-devtools` in the plugin), if available: `new_page` (keep its `pageId`), `emulate` `{"networkConditions": "Slow 4G", "cpuThrottlingRate": 4}`, `performance_start_trace` `{"reload": true, "autoStop": true}`, then `performance_analyze_insight`. Use what it names (LCP element, blocking script, long task) for the finding's `source`.

## 1. Choose 3–6 targets

Pick them from `.wreck-it/discovery.json` and what you've seen while exploring:
- The home page and the main list page
- GET API endpoints that return collections: lists, search, feeds, dashboards, stats
- Anything that felt slow in the browser (check `browser_network_requests` timings)
- Endpoints with query params (search, filter, pagination). Load-test with a realistic param, e.g. `/api/search?q=phone`.

Skip auth-only endpoints unless you can pass a session cookie with `--header "cookie: …"`.

## 2. Find the server PID (for memory trend)

The CLI tries `lsof` on the URL's port automatically. If that finds nothing, pass `--pid <n>` (from `lsof -ti tcp:3000 -sTCP:LISTEN` or `pgrep -f "next start"`).

## 3. Run profiles

```bash
WRECK load http://localhost:3000/api/products --profile ramp     # 10→500 connections until thresholds break
WRECK load http://localhost:3000/api/products --profile spike    # 10 → 100 → 10
WRECK load http://localhost:3000/api/stats --profile soak --soak-duration 180   # memory trend / leaks
```

- Run **ramp** on every target.
- Run **spike** on the 1–2 most important targets.
- Run **soak** (`--soak-duration 180`) on at least one target. Pick, in order of preference:
  1. an endpoint the UI calls repeatedly or on every page (polling, analytics, counters, "who's online"); look for repeats in `browser_network_requests`
  2. an endpoint that keeps state in memory
  3. the busiest list endpoint

Results are written to `.wreck-it/load/*.json`, and the report renders their charts.

## 4. Interpret and record

The CLI records server crashes itself as `critical` findings.

You **must** record a `performance` finding for each of these:
- p99 > 500 ms at 10 connections (a simple GET should be far faster; this usually means N+1 queries or sequential awaits)
- a breaking point below 100 connections
- `leakSuspected`, or RSS rising steadily through a soak

Put the endpoint path and the word "slow", "latency" or "memory leak" in the title. For anything else, use judgment. Read the handler code first, then record (see the wreck-trace skill):

| Signal | Likely cause to check in code | Severity guide |
|---|---|---|
| p99 high even at 10 connections | N+1 queries (a query or fetch inside a loop over results), unbounded query (no `limit`), missing index on the filter/sort column, heavy serialization | high if > 1 s, medium if > 300 ms |
| Latency climbs linearly with connections, CPU-bound | synchronous work on the request path (sync crypto/fs, big JSON, regex, sorting large arrays) blocking the event loop | high |
| Error rate jumps at N connections | connection-pool exhaustion, no backpressure, rate limits | high if N < 100, medium otherwise |
| Spike doesn't recover | resource leak, stuck pool, crashed worker | high |
| `leakSuspected` / rising RSS in soak | module-level arrays/maps/caches that grow per request, listeners added per request | high |

Write the finding with:
- `steps`: `[{"action":"http","method":"GET","url":"/api/products"}]`
- `actual`: the numbers, e.g. "p99 1840 ms at 10 connections; 12% errors at 100"
- `expected`: a target, e.g. "p99 < 300 ms at 50 connections"
- `source`: from tracing

Set `reproduced: true` once a second run shows the same signal.

## Finish

`WRECK run stage load done`

Summarize the results as two short tables:
- pages: route, Lighthouse score, LCP / CLS / TBT, and whether it was a dev server
- endpoints: p50/p99 at 10 and 100 connections, breaking point, memory
