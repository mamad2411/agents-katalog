---
description: Admin SPA suboptimal operations - scale regimes, Big-O vs cache locality, V8 DoD parity with hot-path.mdc
globs:
  - web/**
  - scripts/ci/admin/web.sh
  - scripts/ci/check_ui*.sh
alwaysApply: false
---

# Frontend Hot Path - Suboptimal Operations

## Purpose

Formalize **suboptimal operation** for admin SPA (`web/`). Same engineering stance as tracker ingest (`hot-path.mdc`): classify surface tier, pick the dominant cost model at current scale, reject work that violates it.

Runtime patterns (fetch, canvas, windowing): `react.mdc`. Layout and server contracts: `ui.mdc`. Frontend patterns (races, cancellation, effects): `frontend-patterns.mdc`. Layer boundaries: `frontend-modular.mdc`.

## Definition

An operation is **suboptimal** when it pays a cost class that the current **scale regime** cannot absorb:

| Cost class | What it measures | Dominates when |
| :--- | :--- | :--- |
| **Asymptotic (Big-O)** | Extra passes over `n` elements | Large `n`: client-held hundreds+ rows/points, MB payloads, sustained stream append |
| **Constant / locality** | Alloc size, shape polymorphism, cache stride, layout read | Small `n` but high **frequency**: every render, scroll event, animation frame |
| **Architectural** | Wrong tier ownership (browser vs server) | Any `n` — not fixable by micro-optimization |

Tracker analogy (`hot-path.mdc`):

| Go ingest | Admin SPA |
| :--- | :--- |
| `RunAuction` scan cap p99 < 500 candidates | Client visible window + server `limit`/`offset` |
| `CRC32C` + slot table: ~5.6 ns, sequential 8-byte limbs | Typed column buffers: index walk, no per-cell object graph |
| `atomic.Pointer` catalog snapshot | Immutable fetch snapshot; replace reference, never patch `items[i]` |
| `newobject` / `panicIndex` in inner loop (objdump red flag) | Fresh `{...row}`, inline `style={{}}`, arrow in `map` on Hot surfaces |
| `interface{}` boxing on `/track` | Unstable prop shapes, polymorphic row component per index |
| `fmt.Sprintf` in filter loop | `formatMoney` / template concat inside cell render |

## Scale regimes

Pick regime **before** optimizing. Wrong regime = wasted complexity (SoA on a 50-row Cold page) or missed bug (O(n^2) on a telemetry grid).

| Regime | Typical `n` | Payload | Cadence | Optimize for | Defer / forbid |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S — Small** | <= 100 visible rows or points | <= 64 KiB JSON | Per navigation or low churn | Monomorphic shapes, stable keys, one sequential `map` | SoA, windowing, Profiler budgets |
| **L — Large** | Hundreds+ client-held without server page | > 256 KiB JSON | Scroll or stream | O(n) max one pass; windowing; worker parse; server pagination | Full-list client sort/filter |
| **F — Frequent** | Any `n` under sustained tick | Chart/stream | rAF, WebSocket, 1+ Hz | Alloc/op near zero; imperative canvas/buffer write | React tree rebuild per point |

**Default admin page = Cold + regime S** (`react.mdc`). Classify **Hot + F** only for live charts and streaming telemetry.

### Regime decision (operator / agent)

```
1. Server paginates at 25/50/100?  -> L work belongs in Go handler; browser is S
2. Client holds full array without pagination? -> L rules apply
3. Updates faster than human interaction? -> F rules apply (even if n is small)
4. Profiler: Scripting ~ linear in n on scroll/tick? -> escalate S -> L or F
```

## Suboptimal operation taxonomy

### Class A — Architectural (always suboptimal)

Scale-independent. Same severity as cold I/O on `/track`.

| Operation | Why |
| :--- | :--- |
| Client filter/sort/aggregate over full `items[]` | O(n) or O(n log n) in browser; belongs in handler (`ui.mdc`) |
| Fetch entire directory when API supports `limit`/`offset` | O(network) + O(parse) waste |
| Business rules in `useMemo` (money, status, report keys) | Duplicates Go; drifts from OpenAPI |
| Page-level Context broadcasting `now`, scroll, mouse | O(tree) invalidation each tick |
| `JSON.parse` / heavy transform in **render** | Blocks paint; no abort |

### Class L — Large-n asymptotic

Suboptimal when `n` is large or unbounded. **Big-O first.**

| Pattern | Complexity | Fix |
| :--- | :--- | :--- |
| `.sort` / `.filter` on full client array | O(n log n) / O(n) | Server query params + refetch |
| `.find` / `.includes` inside row/cell render | O(n^2) visible | `Map`/`Set` built once per snapshot outside render |
| `items.map` -> spread clone each tick | O(n) alloc | Imperative buffer update (Hot) or snapshot replace (Cold) |
| Deep `structuredClone` / `JSON.parse(JSON.stringify)` per update | O(n) | Patch field server-side; replace snapshot reference |
| Render all rows without window | O(n) DOM | Virtual window + overscan (`react.mdc`) |
| Main-thread `JSON.parse` > 256 KiB | O(n) string scan | Worker (`parse_json.worker.ts`) |

### Class S — Small-n locality

Suboptimal at **small `n`** when constant factors dominate (V8 hidden classes, IC, layout). Mirrors asm/cache-line focus for `StaticSlotSharder` and SoA bucket walks.

| Pattern | Locality / engine cost | Fix |
| :--- | :--- | :--- |
| In-place `items[i].field = x` | Breaks hidden class; defeats `memo` | Replace snapshot immutably |
| `delete row.optional` | Dictionary mode on object | Treat DTO read-only; omit field server-side |
| Mixed key order/types per row object | Polymorphic shape at same map site | Stable DTO from API; no ad-hoc row augmentation |
| `row => <DynamicIcon type={row.type} />` switching component type | Megamorphic callsite | Stable component per column; map type -> icon table |
| `cn({ [k]: cond })` object form in row loop | Fresh object per row | String-arg `cn('base', cond && 'modifier')` |
| Inline `style={{ width: n }}` per row | Fresh object + style recalc | CSS class or single CSS variable on container |
| Unstable `key={index}` on sorted list | Wrong reuse -> full subtree churn | `key={row.id}` |

At regime S with <= 50 rows, Class S issues rarely matter unless **Class F** cadence applies.

### Class F — High-frequency (alloc per frame)

Suboptimal when invoked every rAF, scroll event, or stream message. Analog: **0 allocs/op** on tracker filter loop.

| Pattern | Per-invocation cost | Fix |
| :--- | :--- | :--- |
| `points.map(p => ({ ...p, label: fmt(p) }))` each tick | O(n) alloc + GC pressure | SoA columns; write buffer; canvas `setData` |
| New arrow `onClick={() => ...}` per row each parent render | Closure alloc + child reconcile | Stable handler + `data-id` or row component boundary |
| React re-render page chrome on chart tick | O(tree) | Chart in `memo` leaf; imperative ref update |
| `getBoundingClientRect` per row in scroll handler | Layout thrash O(n) | Single sentinel measure; `IntersectionObserver` |
| `setState` spreading prior list each message | O(n) copy | Ring buffer or append index + window slice |

Forbidden on Hot/F surfaces — same spirit as `hot-path.mdc` **Forbidden on request path**:

| Category | Forbidden |
| :--- | :--- |
| Alloc per point/row/tick | Spread-map, inline objects, string concat in inner loop |
| O(n^2) | Nested linear search in render |
| Boxing / polymorphism | Unstable element type per index; object-form `cn()` |
| JSON in hot loop | `parse` / `stringify` in render or undebounced scroll |
| Broadcast | Context or parent state for high-frequency scalars |

## Data-oriented design (regime L and F)

Go RTB `CampaignAuctionRegistry` (`hot-path.mdc`, `catalog_shard.go`): parallel slices, bucket indices, atomic snapshot. **Hot admin only** — not Cold CRUD.

| Go hot pattern | Frontend Hot equivalent |
| :--- | :--- |
| SoA slices (`CampaignIDs`, `Bids`, ...) | `Float64Array` / aligned `number[]` per series |
| Bucket start indices | Window `start` + `windowSize` into column buffers |
| `atomic.Pointer` snapshot swap | `setState(nextSnapshot)` — new reference, no in-place patch |
| Early break on score floor | Render visible window only; overscan +3..5 |
| `cpu.CacheLinePad` on contended atomics | Isolate 1 Hz ticker as sibling `memo` leaf — not parent of table |

Cold directory (regime S): `items.map(row => <Row row={row} />)` is optimal. **Do not** build SoA.

## Allowed patterns (by regime)

| Regime | Allowed |
| :--- | :--- |
| S (Cold default) | Server pagination; `items.map`; `AbortController`; module-scope `const` options; `*_display` from API |
| L | Server `limit`/`offset`; one `Map` build per snapshot; DOM windowing; worker parse |
| F | `useRef` chart instance; rAF-coalesced resize; `Float64Array` buffers; `dispose()` on unmount |
| S + optional | `memo(Row)` when props stable; prefetch next page in `useRef` on idle |

## Verification

### Regime S (Cold — default)

```bash
cd web && npm run typecheck
bash scripts/ci/admin/ui_surface.sh
bash scripts/ci/admin/web.sh
```

No Profiler requirement. Suboptimal = Class A primarily.

### Regime L or F (Hot)

| Step | Proves |
| :--- | :--- |
| Node microbench | `bash scripts/ci/admin/web_bench.sh` or `cd web && npm run bench` — campaign list widths/VM, dashboard mock series, nav filter, JSON prefs parse |
| Holdout tests | `campaign_list_perf_holdout.test.ts`, `nav_config_perf_holdout.test.ts` in `npm test` |
| Go command palette | `go test ./internal/commandpalette/ -bench=BenchmarkPrefixRank -benchmem -count=1` |
| React Profiler (scroll/tick) | Page chrome not in every commit |
| Playwright perf (nightly) | `ADMIN_WEB_E2E_PERF=1 bash scripts/ci/admin/web_e2e_perf.sh` — chart/campaigns/palette wall-clock |
| Performance 6x slowdown | Scripting not O(n) per frame; GC bar not locked to frame |
| Memory: 10 route cycles | Detached nodes stable |
| Record `n` | Visible rows/points at test time |

Budgets: `web/src/lib/perf/budgets.ts` (Node, +15% tolerance). Browser marks: `?admin_perf=1` via `web/src/lib/perf/browser_marks.ts`.

Before claiming Hot perf: paste Profiler note + `n` + regime (L/F). Admin chart timing != tracker p99 (`anti-slop.mdc`).

### DevTools signals (manual)

| Signal | Likely class |
| :--- | :--- |
| Scripting grows linearly with row count on scroll | L or F |
| Minor GC sawtooth every frame on static chart | F |
| Layout / Recalculate Style per scroll event | S layout thrash -> F |
| 50-row page, navigation-only updates | Do not over-optimize; verify Class A absent |

## Agent checklist

| Step | Action |
| :--- | :--- |
| 1 | Classify tier: Cold (default) vs Hot (`react.mdc`) |
| 2 | Pick regime: S (default), L (large client set), F (frequent tick) |
| 3 | Class A absent: server owns filter/sort/page |
| 4 | Regime L: no O(n^2); pagination or windowing |
| 5 | Regime F: no alloc per tick; canvas/SoA/ref |
| 6 | Regime S: stable keys/shapes; no SoA/windowing ceremony |
| 7 | Paste verification tier: typecheck/gates (S) or Profiler + `n` (L/F) |

## Related rules

`react.mdc`, `hot-path.mdc`, `ui.mdc`, `frontend-modular.mdc`, `cold-path.mdc`, `anti-slop.mdc`, `boundaries.mdc`, `core.mdc`.
