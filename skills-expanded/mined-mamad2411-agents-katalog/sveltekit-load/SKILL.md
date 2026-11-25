---
name: sveltekit-load
description: Use when implementing or reviewing SvelteKit load functions including server load, universal load, streaming, data invalidation, and fetch behaviour.
---

# SvelteKit Load

## Specialization

Expert guidance for SvelteKit load functions. Covers universal load (`+page.ts` / `+layout.ts`), server load (`+page.server.ts` / `+layout.server.ts`), streaming with `Promise` returns, `depends()` dependency declaration, `invalidate()` and `invalidateAll()`, and safe `fetch` usage inside load.

## Trigger Conditions

- Implementing data fetching for a SvelteKit page or layout.
- Deciding between server load and universal load.
- Streaming slow data to the page using deferred `Promise` values.
- Triggering data reload after a user action without a full navigation.
- Diagnosing stale data, cache mismatches, or over-fetching.

## Scope Boundaries

In scope:

- `+page.ts`, `+layout.ts` (universal load): runs on server and client.
- `+page.server.ts`, `+layout.server.ts` (server load): runs only on the server.
- Load function signature: `({ params, url, data, fetch, setHeaders, depends, parent })`.
- `depends(key)` for custom invalidation targets.
- `invalidate(key)` and `invalidateAll()` from `$app/navigation`.
- Streaming: returning unresolved `Promise` values for deferred rendering.
- `setHeaders()` for cache-control and other response headers.
- `parent()` to access parent layout data.
- Typed `PageData` / `LayoutData` via generated types.

Out of scope:

- Form actions (covered by `sveltekit-actions`).
- Page rendering options: `ssr`, `csr`, `prerender` (covered by `sveltekit-page-options`).
- Route parameter definition (covered by `sveltekit-routing`).
- Error throwing in load (covered by `sveltekit-errors`).

## Inputs

- Data requirements for each page or layout.
- Whether data must be available server-side only (secrets, DB access).
- Streaming requirements for slow dependencies.
- Cache and revalidation policy.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Load function implementation | Correct module file (`+page.ts` or `+page.server.ts`) with typed return |
| Server vs. universal decision | Documented rationale for chosen load module type |
| Streaming plan | `Promise` fields identified and deferred appropriately |
| Invalidation strategy | `depends()` keys declared; `invalidate()` call sites identified |
| Load quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Fetch data for a single page | `PageData` flows from load to `+page.svelte` |
| L2 Practical Delivery | Implement a feature with server load, streaming, and invalidation | All data paths work; streaming tested in browser; invalidation triggers re-run |
| L3 Specialist Hardening | Optimise load performance with caching and parallel fetches | `setHeaders` cache policy set; parallel fetches confirmed; streaming latency measured |
| L4 Expert Standardisation | Establish load patterns and conventions for a project | Load decision guide, typing policy, and invalidation key registry documented |

## Workflow

1. Identify what data each page and layout needs and its source (DB, API, file system).
2. Decide server vs. universal load: use server load when data requires secrets, DB access, or must never reach the client bundle; use universal load for data safe to expose to the browser.
3. Implement load function with destructured event parameters; return a plain object.
4. Declare `depends(key)` for any data that must be independently invalidatable.
5. For slow dependencies, return them as unresolved `Promise` values to enable streaming.
6. Use the SvelteKit-provided `fetch` (not global `fetch`) inside load functions to ensure SSR and credentials work correctly.
7. Set `setHeaders({ 'cache-control': '...' })` when CDN or browser caching is required.
8. Call `parent()` only when layout data is genuinely needed; avoid tight coupling between layout and page loads.
9. Type return values using generated `PageServerLoad` / `PageLoad` types.
10. Run the load quality checklist.

## Load Quality Checklist

- [ ] Server load used when data requires environment secrets or direct DB access.
- [ ] Universal load used only for data that is safe to expose to the browser.
- [ ] SvelteKit `fetch` used inside load; global `fetch` is never called directly.
- [ ] `depends()` declared for every key targeted by `invalidate()` calls.
- [ ] Slow dependencies returned as `Promise` values when streaming is beneficial.
- [ ] `setHeaders()` used to control caching; headers are not mutated after return.
- [ ] Load functions do not perform side effects beyond data retrieval.
- [ ] `parent()` used sparingly and only when layout data is genuinely required.
- [ ] Return types use the generated `PageLoad` or `PageServerLoad` type, not `any`.

## Security Notes

- Never return secrets, tokens, or sensitive internal data from a universal load function; these values reach the client.
- Validate and sanitise `params` and `url.searchParams` before using them in queries or API calls.
- Use parameterised queries or typed API clients; do not concatenate user-controlled values into URLs or SQL.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Server vs. universal decision | Workflow step 2 + Required Outputs |
| Load function implementation | Workflow steps 3–4 |
| Streaming | Workflow step 5 |
| Fetch safety | Workflow step 6 |
| Cache control | Workflow step 7 |
| Invalidation | Workflow step 4 + checklist |
| Type safety | Workflow step 9 |
| Quality validation | Load Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
