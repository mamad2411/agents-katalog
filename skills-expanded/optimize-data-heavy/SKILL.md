---
name: optimize-data-heavy
description: "Methodology + deep rulebook for making a data-heavy / graph-heavy page fast, cheap, and reliable — the 'second optimization pass' after a feature works. Use when a user says a page/table/chart/dashboard is slow, laggy, janky, or expensive; when filters/sorting/pagination feel heavy; when a query is slow or the payload is huge; or when asked to optimize speed, reliability, or resource consumption on a site that shows lots of rows, aggregates, or charts. Covers Postgres/SQL query tuning, backend compute + caching, API payload + compression + HTTP caching, React re-render + virtualization, chart/dataviz downsampling, client-side fetch orchestration (request dedup, stale-while-revalidate, prefetch), and reliability (timeouts, cancellation, singleflight, error boundaries). Stack-general with concrete recipes for Bun/Hono/React/recharts/Drizzle/Postgres."
model: fable
effort: xhigh
---

# Optimize a Data-Heavy / Graph-Heavy Page

The reusable "second pass": a page works, but with 100k+ rows behind it, it's slow to load, laggy to interact with (sort, filter, switch tab, change scope), or expensive to serve. This skill is the disciplined way to make it fast **without guessing** — and without breaking correctness.

> **The one rule that matters most: measure before you touch code, and measure again after.** Nearly every expensive optimization mistake comes from optimizing the thing that *looked* slow instead of the thing that *was* slow. In one real case a "chart lag" turned out not to be the chart at all — it was a ~1,100-row table re-rendering on every interaction, plus a cache key that turned six sort buttons into six full recomputes. You only find that by measuring.

---

## Non-negotiable invariant: speed is never bought with functionality or UX

An optimization that changes what the user sees, can do, or how good it looks is **not an optimization — it's a regression with a faster clock.** Every change in this skill must be *behavior-preserving*. Hold these as hard constraints, not trade-offs:

- **Correctness is invariant.** The optimized path must return the **same data, same rows, same order, same totals** as before. Prefer changes that are byte-identical by construction (same computation, cached/shaped differently) over ones that require proving two different computations agree. When you *do* replace a computation (e.g. move JS scoring into SQL), pin it with a test that asserts the new output **equals** the old across several inputs — and pass the *same* reference values (timestamps, seeds) into both so they can't drift.
- **No feature loss.** Don't drop a filter value, a signal, a sort option, a column, a drill-down, or a tab to make the code simpler. If the full dataset was reachable before, it must stay reachable (cap the *default view*, keep "show all" / pagination / the underlying data).
- **No silent data hiding.** When you cap or paginate, the UI must say so ("showing top 25 of 1,100") and the total must stay accurate. A cap that reports the capped count as the total is a data bug, not an optimization.
- **Display quality is invariant.** Charts keep their visual fidelity — downsampling must preserve peaks, troughs, and shape (LTTB/min-max, never blind every-Nth that drops spikes); never reduce below what's visually meaningful. Keep axis labels, tooltips, legends, and interactivity.
- **UX polish stays unless it's the *proven* bottleneck.** Animations, transitions, hover states, loading skeletons, button feedback — don't strip them for cycles on a guess. Only touch them if the profiler shows they're the measured cost *and* removing/replacing them doesn't degrade the feel (e.g. disable a chart's enter-animation only on a large series where it visibly janks; keep it on small ones).
- **When in doubt, keep the behavior and find another rung.** There is almost always a higher rung on the strategy ladder that's both faster *and* behavior-preserving (cache the computation, precompute, index, memoize) before you'd ever need to cut a feature. If the only speedup you can find removes functionality, stop and raise it with the user — don't ship it silently.

The verify step (4) and guard step (5) exist to *enforce* this: re-measure proves it got faster; the equality/regression test proves it still does the same thing.

---

## The methodology (follow in order)

### 0. Reproduce & baseline — get ONE number
Don't read code to design a fix yet (reading just enough to find the route, params, and auth for the measurement is fine). Reproduce the exact slow interaction the user described and capture a concrete number for it. Pick the metric that *decides success* (e.g. "click a sort icon → chart updates" in ms; "open the analytics tab → data visible" in ms; "bytes over the wire"; "$/day of DB or ingest cost"). Write it down. This is the number you must move, and the number a regression test will later protect.

> **Measure the *current* state, not the assumed one — and cold AND warm.** A backlog note or memory that says "this endpoint is unoptimized" may be stale: it might already have a cache, an index, or a partial fix. Baseline what's *actually there right now*, or you'll "fix" a problem that's already solved and miss the one that isn't. Always take a **cold** number (right after a restart / cache-invalidation) and a **warm** number (second call) — a big cold/warm gap means caching/singleflight is the lever; a flat, slow warm number means the per-request work itself is the problem. (Real case: an endpoint flagged as "retains 139k rows, unoptimized" already had scan-caching — the *real* live finding was that it cached 76 MB to serve 17 KB, which only the current-state measurement revealed.)

### 1. Localize the bottleneck — bisect the layers
A slow page is one of these, and you must find **which** before you fix anything. Split total time into three buckets and attribute the cost:

| Bucket | How to measure | If this dominates → read |
|--------|----------------|--------------------------|
| **Server time** (TTFB) | `curl -s -w '%{time_starttransfer}'` vs `%{time_total}`; server-side timing logs / `Server-Timing` header | `references/01-database.md`, `references/02-backend-compute-caching.md` |
| **Transfer** (bytes on the wire) | `curl -s -o /dev/null -w '%{size_download}'` twice — with and without `-H 'Accept-Encoding: gzip'`; Network panel "Size" vs "Content" | `references/03-transport-payload-bundle.md` |
| **Client render** (paint/JS) | React DevTools Profiler; DevTools Performance flame chart; "Paint flashing" / "Rendering" panel | `references/04-frontend-react.md`, `references/05-charts-dataviz.md` |

Rule of thumb: if `curl` to the endpoint is fast but the browser feels slow, it's **render** (React/charts). If `curl` itself is slow, it's **server** (DB or compute). If both are fast but the page is heavy on first load, it's **transfer/bundle**. And if the *endpoint* is fast but the *page* still is chatty — the same URLs firing on every mount, tab-switch, or back-navigation — it's **client fetch orchestration** (`references/07-client-data-fetching.md`): the request the client never needed to send.

### 2. Rank fixes by impact × effort (Amdahl)
Fix the **dominant** cost first. Optimizing a 20ms step while a 400ms step sits next to it is wasted work. Note the bigger deferred wins explicitly so they're not lost — a triage backlog like "ranking endpoint retains 139k objects to serve 30", "no singleflight → 5 cold requests = 5 recomputes" comes from exactly this pass.

### 3. Fix at the right layer — climb the strategy ladder
Prefer the **highest** rung that solves it. Each rung is cheaper than the one below at runtime:

1. **Don't do the work** — eliminate it, precompute it (nightly rollup), or serve it from cache.
2. **Do it once and share** — memoize, coalesce (singleflight), cache the *computation* (the SCAN) so presentation variants share it — or the finished response, when it's a deterministic pure function of one key.
3. **Do less of it** — push aggregation into the DB, project only needed columns, cap/paginate rows, downsample chart points to visual resolution.
4. **Do it in the right place** — aggregate in SQL not JS; sort/limit server-side not client-side; render on the server where it helps.
5. **Do it faster** — the right index, a better algorithm, a Set instead of an array scan.
6. **Do it off the critical path** — background job, lazy-mount, defer, code-split.
7. **Send less / render less** — compress, 304, virtualize, `React.memo`.

Reach for a database index or a faster loop (rung 5) only after checking you can't just *not compute the thing* (rungs 1–3).

### 4. Verify with the SAME measurement
Re-run step 0's measurement. Confirm the number actually moved. Then check you didn't regress a sibling path (a cache key change can bleed across tenants; a memo can go stale; a downsample can drop a real spike).

### 5. Guard against regression
Add a test that **fails without the fix** — and prove it fails by removing the fix once. A mutation-guard test that passes whether or not the bug is present (e.g. asserting on a field that is identical in both seed rows) is worse than no test: it gives false confidence. This happened in a real pass — a shared-scan-reorder test first asserted on `date` where both seed rows shared a date, so it couldn't detect the reorder. It had to assert on `percentChange` to genuinely fail.

---

## Fast triage table (symptom → likely cause → first move)

| Symptom | Most likely cause | First thing to check | Reference |
|---------|-------------------|----------------------|-----------|
| Sort/filter/tab click lags, no network call | Uncapped list re-rendering; no `React.memo`; derived state stored in state | React DevTools Profiler — what re-rendered on click? | `04`, `05` |
| Sort/filter click is slow AND hits network | Presentation params (sort/order/limit) in the cache key → every variant recomputes | Is the cache keyed on data-inputs only? | `02` |
| Chart with many points is janky | Rendering thousands of SVG nodes; no downsampling; animations on | Point count vs pixel width; SVG vs canvas | `05` |
| Endpoint slow (curl slow), CPU spikes | Query fetches N rows to reduce to K in JS; missing index; Seq Scan | `EXPLAIN (ANALYZE, BUFFERS)` the hot query | `01` |
| Endpoint slow only when cold; fine when warm | No singleflight — concurrent cold requests each recompute | Is there in-flight coalescing? | `02` |
| First load downloads megabytes | Uncompressed / unminified bundle; no code-split; native route bypasses compress middleware | `curl -H 'Accept-Encoding: gzip'` size | `03` |
| Same data refetched constantly | No client cache/dedup; no HTTP caching / ETag | Duplicate requests in the Network panel? 304 on repeat? | `07`, `03` |
| Same URL fires N× on load, or refetches on tab-switch/back-nav | No client-side dedup / cache-across-navigation | Count identical requests per load; does back-navigation refire? | `07` |
| Deep pagination gets slower per page | `OFFSET N` scans and discards N rows | Keyset/cursor pagination | `01` |
| Aggregates recomputed every request | No precompute; real-time when it needn't be | Can it be a scheduled rollup? | `01`, `02` |
| Memory grows unbounded | Cache with no cap; retaining full result sets | LRU entry/byte cap; result caps | `02`, `06` |
| Page hangs / no cancel on fast re-clicks | No request cancellation; races | AbortController / `cancelled` guard | `04`, `06` |

---

## How to run it

**Small, obvious win (1 layer):** read the matching `references/*.md`, apply, measure, add a guard test. Done.

**A whole page is slow and you don't know why:** run the methodology top-to-bottom. For a big surface, fan out a **read-only** investigation across layers in parallel — one look at the DB/queries, one at backend/caching, one at the React render, one at the payload/bundle — each reporting the measured cost of its layer and the single highest-impact fix. Then synthesize, rank, and fix the dominant cost first. (Keep the investigators strictly read-only — they report findings and measurements; you make the changes.)

**Always finish with:** re-measure against step 0's number, a regression guard test, a before/after note wherever this project records changes (PR body, changelog, status doc), and — for multi-file changes — an independent review pass before committing (a code-review agent or audit skill if the project has one).

---

## References (deep rulebook, by layer)

- `references/00-measure-first.md` — profiling recipes: `curl` timing, `EXPLAIN`, `pg_stat_statements`, React Profiler, DevTools. **Read this first if you're about to guess.**
- `references/01-database.md` — Postgres + Drizzle: indexes (composite/partial/covering), `EXPLAIN` reading, aggregation pushdown, N+1 batching, keyset pagination, precomputed rollups, approximate counts, `ANALYZE`/bloat.
- `references/02-backend-compute-caching.md` — cache the SCAN not the response, cache-key completeness, singleflight, TTL + prefix invalidation, cache warming, LRU caps, precompute jobs, moving work off the request path.
- `references/03-transport-payload-bundle.md` — payload shape & over-fetch, gzip/brotli, ETag/304, HTTP caching, the "native route bypasses compress middleware" trap, code-splitting, bundle size, waterfalls.
- `references/04-frontend-react.md` — re-render elimination (`memo`/`useMemo`/stable refs), derived state, virtualization vs capping, debounce/`useDeferredValue`/`useTransition`, request cancellation, lazy-mount.
- `references/05-charts-dataviz.md` — downsampling (LTTB/min-max), SVG-vs-canvas point budgets, disabling animations/dots, aggregate-to-pixel-resolution, memoized chart data, lazy-mount hidden charts.
- `references/06-reliability.md` — timeouts, cancellation, singleflight, error boundaries, graceful degradation, backpressure, memory caps, observability & tripwires.
- `references/07-client-data-fetching.md` — client fetch orchestration: request dedup (in-flight map), cache-across-navigation/remount, stale-while-revalidate, prefetch-on-intent, the three composing cache layers (client → ETag → server), and the per-user/invalidation/bound correctness rules. The request the client never has to send.

Each layer reference (`01`–`07`) follows the same shape: **symptom → how to detect (concrete command) → the fix (with code) → how to verify**.

For calibration on what a full pass looks like end-to-end — five real before/after cases (1.1 s → 17 ms, 500 ms → 1 ms, 2.3 s → 1 ms, …), including the wrong turns and the "no fix warranted" verdicts — read `CASE_STUDIES.md`.
