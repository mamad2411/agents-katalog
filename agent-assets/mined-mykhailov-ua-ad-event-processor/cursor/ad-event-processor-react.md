---
description: React admin runtime - Hot (charts/telemetry) vs Cold (CRUD), heap leaks, canvas
globs:
  - web/src/pages/**
  - web/src/domains/**
  - web/src/shell/**
  - web/src/api/**
  - web/src/workers/**
  - scripts/ci/admin/web.sh
  - scripts/ci/check_ui*.sh
alwaysApply: false
---

# React Runtime - Admin SPA

## Status

Applies when `web/src/pages` and `web/src/domains` exist (`ui.mdc`, `frontend-modular.mdc`, `frontend-patterns.mdc`). Layout and server contracts: `ui.mdc`. Layer boundaries: `frontend-modular.mdc`. Frontend patterns (effects, races, errors, async/cancel): `frontend-patterns.mdc`.

## Purpose

Admin UI is **mostly Cold** (standard React). **Hot** rules apply only to live charts and streaming telemetry — not to CRUD directories.

Tracker ingest (`hot-path.mdc`) optimizes 0 allocs/op on `/track`. Admin Cold surfaces optimize **correct fetch lifecycle** (abort, snapshot replace). Admin Hot surfaces optimize **allocation rate per frame** and **bounded reconciliation**.

Formal taxonomy (Big-O vs cache locality, scale regimes S/L/F, suboptimal operation classes A/L/S/F): `frontend-hot-path.mdc`.

## Scope: Hot vs Cold

| Tier | Surfaces | Required patterns |
| :--- | :--- | :--- |
| **Cold** (default) | CRUD directories, detail forms, login, settings, integrations, billing lists | Server pagination + sort; `AbortController`; `items.map()`; immutable snapshot replace |
| **Hot** (strict) | Live real-time charts, streaming telemetry, sub-second series updates | DoD/SoA buffers, canvas imperatives, DOM windowing when client holds large visible sets |

**Default assumption: Cold.** A server-paginated directory with 50 rows per page is Cold — do not apply SoA, row windowing, or Profiler budgets unless the page is explicitly Hot.

### Cold path (standard React)

| Rule | Detail |
| :--- | :--- |
| Pagination | `limit`, `offset`, `total` from API; refetch on page/sort change |
| Render | `data.items.map((row) => <Row key={row.id} row={row} />)` — 50 rows is sub-ms; **no SoA** |
| Fetch lifecycle | `AbortController` per request; abort on param change and unmount |
| Snapshot | Replace whole `data` on fetch complete; never mutate `items[i]` in place |
| Mutation errors | `apiFetch` throws `ApiError` on non-2xx; surface via `ErrorBlock` / `userErrorMessage` -- never silent catch (`frontend-slop.mdc` **Mutation validation**) |
| Labels | Prefer `*_display`, `*_label` from handler — no client money/status math |
| Filters | Draft local; Apply copies to URL params once; server refetch (`ui.mdc`) |
| User action coalescing | Manual refresh: 500 ms leading window + in-flight guard in owner hook; mutations: `disabled` + `loading` until settled (`frontend-slop.mdc` **User action coalescing**) |
| Errors | `ErrorBlock` on blocking error; stale-while-revalidate when `data` present (`ui.mdc`) |

**Render errors (Cold):** async fetch errors use `ErrorBlock`; **synchronous render throws** use `AppRouteErrorBoundary` around routed `<Outlet />` so sidebar navigation clears PAGE ERROR without Ctrl+R (`frontend-slop.mdc` **RB-E***). Do not wrap every leaf in a boundary — one route subtree owner in `app_shell.tsx`.

**Class-B overlay stability:** filter toolbars mount many `Select` / `DropdownMenu` / `Popover` instances. Unstable context identity + effects that depend on whole `ctx` cause React **#185** and can trip the route boundary — see **OV-*** in `frontend-slop.mdc` (`mergeOverlayPosition`, memoized provider value, no `[ctx,` deps).

Forbidden on Cold directory tables:

- Parallel string arrays / SoA `useMemo` builds for display columns
- Client windowing when server already pages at 25/50/100
- Client sort/filter over full datasets
- Profiler / SoA requirements in PR for standard list pages

Optional on Cold (not required):

- Prefetch next page into `useRef` on idle
- `memo` on row component when props are stable
- Worker `JSON.parse` for payloads > 256 KiB

### Hot path (strict DoD / canvas)

Apply **only** when the page has:

- Live chart series updating at animation-frame or streaming cadence
- Telemetry tables fed by WebSocket/SSE with sustained high-frequency appends
- Client-visible sets in the hundreds+ **without** server pagination, and Profiler shows Scripting scales with point/row count during scroll or tick

Hot techniques (not for Cold CRUD):

| Technique | When |
| :--- | :--- |
| SoA column buffers | Homogeneous numeric/time series in canvas or virtualized grid |
| DOM windowing | Client-held list with hundreds+ visible rows and measured scroll jank |
| rAF coalescing | Scroll/resize handlers on high-frequency surfaces |
| Imperative chart API | `setData` / `setOption` in place — React owns container ref only |

Go RTB SoA (`hot-path.mdc`, `catalog_shard.go`) is the mental model for **Hot admin only** — not for `customers_page.tsx`.

## Shared rules (Cold and Hot)

### Fetch and abort

```ts
useEffect(() => {
  const ctrl = new AbortController();
  void listCustomers(params, ctrl.signal)
    .then(setData)
    .catch((err) => {
      if (err.name === 'AbortError') return;
      setError(err);
    });
  return () => ctrl.abort();
}, [params]);
```

| Rule | Detail |
| :--- | :--- |
| Stale response | Generation id or abort before `setState` after param change |
| Unmount | Always abort in effect cleanup |
| Timeout | `RESOURCE_FETCH_TIMEOUT_MS` (15 s) — clear `fetching` in `finally` (`ui.mdc`) |
| Manual refresh | Coalesce in owner before dep bump or fetch; `useResource` abort alone is not enough (`frontend-slop.mdc` **User action coalescing**) |
| One intent, N requests | Count network lanes per Apply/Refresh/open; trim with scoped tokens, parent snapshots, session cache (`frontend-slop.mdc` **RF-***) |

### Request fan-out (one trigger)

Before adding a shared `refreshToken` dep to another `useResource`, ask whether that hook **must** rerun on this operator action.

| Prefer | When |
| :--- | :--- |
| Scoped token per surface | Facets, overview, and list refresh on different schedules (**RF-1**) |
| Parent snapshot -> child overlay | Row metrics, breadcrumb labels (**RF-3**, **RF-5**) |
| `*_cache.ts` with inflight dedupe | Same GET reused across pages in one session (**RF-4**) |
| Tab-gated / `skipFetch` hook | Detail page with many tabs (contrast: `customer_detail_page.tsx`) |

`Promise.all` of **distinct** endpoints for one hub screen is not fan-out slop when the UI renders all results. Catalog: `frontend-slop.mdc` **Request fan-out (RF-*)**.

### Freshness ticker (isolated leaf)

1 Hz (or slower) freshness chips must **not** re-render the page tree.

| Rule | Detail |
| :--- | :--- |
| Placement | Ticker as **sibling** to table/content — not parent of list |
| Component | Dedicated `memo` leaf with local `useState` / `useEffect` interval |
| Context | Do not put `now` or lag seconds in page-level Context |
| Cleanup | `return () => clearInterval(t)` in effect |

### Closures and retention (heap leaks)

| Leak | Fix |
| :--- | :--- |
| `setInterval` without cleanup | `return () => clearInterval(t)` |
| `document.addEventListener` | Remove in effect cleanup |
| Fetch after unmount | `AbortController` + generation check |
| Closure over `items` in timer | `itemsRef.current = items` |
| Portal menu left mounted | Unmount on close (Radix handles most cases) |
| Unbounded module `Map` cache | Cap or `WeakMap` |

`WeakRef` / `FinalizationRegistry`: optional caches only.

### Charts and canvas (Hot)

| Rule | Detail |
| :--- | :--- |
| Ownership | React: container `div` + resize observer only |
| Update | `setOption` / `setData` / buffer write in place — no React series rebuild per tick |
| Ref | Chart instance lives in `useRef`; created once on mount |
| Unmount | `dispose()` / `destroy()` in effect cleanup |
| Resize | rAF-debounced `ResizeObserver`; one layout read per frame |

### Effects and subscriptions

| Rule | Detail |
| :--- | :--- |
| One concern per effect | fetch / subscribe / URL sync |
| Minimal deps | Refs for values that must not retrigger |
| Strict Mode | Cleanup idempotent |
| Fetch | `useResource` or effect + abort — never in render |
| Poll | Single effect; push snapshot, not per-tick spread of list |

## Hot-only: data-oriented design (DoD)

When a surface is classified **Hot** (see scope table above).

### Snapshot reader

```
Fetch or stream event
  -> setState(nextSnapshot)     // replace reference
  -> useMemo: SoA columns or window slice (Hot only)
  -> render: windowed map or canvas draw
```

| Rule | Detail |
| :--- | :--- |
| One writer | Only fetch/stream handler replaces snapshot |
| No in-place patch | `items[i].status = x` breaks `memo` and hidden classes |
| Generation id | Ignore stale responses before `setState` |

### SoA (Hot only)

Structure-of-arrays for **homogeneous columns** when hundreds+ values update per frame (chart buffers, virtualized telemetry grid).

| Cold (default) | Hot (when Profiler proves need) |
| :--- | :--- |
| `items.map(row => <Row row={row} />)` | Parallel `Float64Array` / `string[]` aligned by index |
| Server `*_display` on each DTO | Pre-built column buffers for canvas `setData` |
| 50 rows from API page | Windowed DOM slice + spacer rows |

Do **not** build SoA for a standard 50-row directory page.

### Windowing (Hot only)

When client holds a large visible set without server pagination:

| Rule | Detail |
| :--- | :--- |
| Visible window | Render `start..start+windowSize` only; spacer rows for scroll height |
| Stable `key` | `row.id` — never index-only on sorted lists |
| Overscan | +3–5 rows above/below viewport |

### Hot render path (forbidden)

Inside high-frequency `map`, scroll handlers, or chart ticks on **Hot** surfaces — **Class F** in `frontend-hot-path.mdc`:

| Category | Forbidden |
| :--- | :--- |
| Alloc per point/row | `map(r => ({ ...r, label: format(r) }))` each tick |
| O(n²) | `.find` / `.filter` inside cell render on full dataset |
| Fresh objects | Inline `style={{}}`; object-form `cn()` every row |
| JSON | `JSON.parse` / `stringify` in render |
| Context broadcast | Scroll offset, mouse position at page root |
| Layout thrash | `getBoundingClientRect` per row in scroll handler |

## Worker offload (optional)

| Workload | Thread |
| :--- | :--- |
| `JSON.parse` on payloads > 256 KiB | `parse_json.worker.ts` |
| CSV / aggregate report post-process | `report_aggregate.worker.ts` |
| Typical list page (< 64 KiB) | Main thread `api()` is fine |

- Transferable buffers when possible (`postMessage(buf, [buf])`).
- One long-lived worker per page session; `terminate()` on unmount.

## State shape (Cold)

```
Server snapshot (useState / useResource)
  -> render: items.map(Row)
```

| Rule | Detail |
| :--- | :--- |
| One source of truth | API DTO in `data`; UI toggles separate primitives |
| Draft vs applied | Filter draft local; Apply copies to URL params once |
| URL sync | On Apply / page change — not every keystroke |

Forbidden: giant spread state; duplicated row arrays; client sort over full `items[]`.

## Memoization and callbacks (Cold)

Default: **plain functions and inline derivations**. `useCallback` / `useMemo` are opt-in tools, not hygiene.

### When `useCallback` is required

| Trigger | Example |
| :--- | :--- |
| Prop to `React.memo` child that shallow-compares the callback | Stable `onSelect` on memoized table row |
| Callback stored in Context consumed by memoized descendants | Rare in admin Cold surfaces |
| Library requires referential stability | Some Radix/subscription APIs (document in PR) |

### When `useCallback` is slop (**RP-1**)

| Pattern | Why |
| :--- | :--- |
| Every handler wrapped "for performance" | No memo child -> zero reconcile savings; deps array alloc on every render |
| `useCallback` only to satisfy `useEffect` deps | Prefer `useEffect` + ref to latest handler, or extract fetch to `useResource` |
| Identical deps churn (`[customerId, navigate, setOpen]`) | Same cost as recreating the function |

`setQuery` / `setOpen` from `useState` are already stable -- do not re-wrap them.

### When `useMemo` is required

| Trigger | Example |
| :--- | :--- |
| Expensive derivation measured or obviously O(n) on large n | Row VM build over visible page (`buildCampaignRowVm`) |
| Referential equality required by child/library | Stable options array passed to memoized select |

### When `useMemo` is slop (**RP-2**)

| Pattern | Why |
| :--- | :--- |
| `useMemo(() => arr.filter(...), [arr])` on < 200 rows | Cheaper to compute inline than maintain deps |
| `filter` inside `some` for id dedup | Use `Set` once: `const ids = new Set(recents.map(r => r.id))` |
| Memo wrapping trivial string/boolean | `trimmedQuery = query.trim()` needs no memo |

Cold list pages: **no default Profiler/memo policy**. Add `memo` on rows only when a parent effect proves full-table reconcile on header interaction.

## Async UI lanes (Cold)

Correlated fetch UI (`loading`, `error`, `items`, `degraded`) must not sprawl as unrelated `useState` hooks that share fields across lanes (**RP-3**, **RP-4**).

| Lane | Canonical owner |
| :--- | :--- |
| Single list / detail snapshot | `useResource` (`use_resource.ts`) |
| Open dialog + catalog load | One `useResource` keyed on `open` |
| Debounced typeahead search | Separate status object **or** second `useResource` keyed on debounced query |
| Prerequisite missing | `fetcher` returns `Promise.resolve(undefined)`; `hasSnapshot={data != null}` |

**Banned:** catalog load and debounced search both calling `setLoading` / `setError` on the same primitives -- search keystrokes can clear catalog errors or fight the catalog spinner.

**Banned:** introducing TanStack Query / SWR for admin CRUD when `useResource` exists (**RP-6**). Extend `useResource`, `use_coalesced_callback`, or a domain hook (`use_command_palette.ts`).

### Debounced search (allowed shape)

Trailing debounce on **input** only (`frontend-slop.mdc` coalescing table: command palette **300 ms**). Pattern:

1. Local `query` state (keystrokes).
2. `useEffect` with `setTimeout` + `AbortController` on debounced value -- same as `react.mdc` **Fetch and abort**.
3. Separate `searchError` / `searchFetching` from catalog `useResource` when both can be active.

Do not cite "race-prone hand-rolled debounce" as slop without naming **RP-4** shared-state collision.

## Row and list item reuse (**RP-5**)

When the same row chrome appears **twice in one component** (palette item, directory row, menu entry):

| Rule | Detail |
| :--- | :--- |
| Extract | `function CommandPaletteRow({ item, onSelect }: …)` or shared shell export |
| Props | `item` DTO + callbacks only -- no fetch state inside row |
| Styling | One Tailwind block; change once applies everywhere |

Copy-pasted `map` bodies differing only by `key` source are **RP-5** slop on touch.

### Best-effort side effects (**EH-SI6**)

`record*` / analytics POSTs that must not block navigation:

| Allowed | Banned |
| :--- | :--- |
| `void recordFoo(...)` without await when failure is non-blocking | Same pattern on `list*` / `search*` that owns visible data |
| Shared `fireAndForgetSideEffect(fn)` helper documenting intent | Raw `.catch(() => undefined)` scattered in components |

Operator-visible fetch errors still require `ErrorBlock` / `setActionError` (**EH-SI1**).

## V8-friendly habits (Hot surfaces)

| Habit | Detail |
| :--- | :--- |
| Module-scope options | `const STATUS_OPTIONS = [...] as const` |
| `cn()` in row loop | String args only (`lib/utils.ts`) |
| Avoid `delete` on DTOs | Treat API objects as read-only |

## Verification

### Cold pages (default)

```bash
cd web && npm run typecheck
bash scripts/ci/admin/ui_surface.sh
bash scripts/ci/admin/web.sh
```

No Profiler requirement for standard directory pages.

### Hot pages (charts / streaming)

| Step | Command / tool |
| :--- | :--- |
| React Profiler | Scroll/tick — page chrome not in every commit |
| Performance (6x slowdown) | Scripting + GC during tick — GC bar should not track frame-by-frame |
| Memory | 10 navigate cycles — detached nodes stable |
| Honesty | Admin chart microbench ≠ tracker p99 (`anti-slop.mdc`) |

Before claiming Hot surface perf: paste Profiler note + visible point/row count.

## Agent checklist

| Step | Action |
| :--- | :--- |
| 1 | Classify page: Cold (default) or Hot (charts/streaming) |
| 2 | Cold: server pagination + AbortController + `items.map()` — no SoA |
| 3 | Hot: SoA/windowing/canvas refs only when scope table applies |
| 4 | Ticker: isolated `memo` leaf; `clearInterval` on cleanup |
| 5 | Charts: imperative update via ref; `dispose()` on unmount |
| 6 | Paste `typecheck` + gates for Cold; Profiler note for Hot |
| 7 | Memo: **RP-1** / **RP-2** -- no blanket `useCallback`; `useMemo` only when justified |
| 8 | Async: **RP-3** / **RP-4** -- `useResource` per lane; no shared loading/error across search + catalog |
| 9 | DRY: **RP-5** -- extract repeated list-row JSX before third copy |
| 10 | Fan-out: map operator action -> Network request count; cite **RF-*** if N > necessary |

## Related rules

`frontend-patterns.mdc`, `frontend-hot-path.mdc`, `frontend-modular.mdc`, `ui.mdc`, `anti-slop.mdc`, `quality.mdc`, `hot-path.mdc`, `cold-path.mdc`, `boundaries.mdc`.
