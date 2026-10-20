---
name: sveltekit-routing
description: Use when implementing or reviewing SvelteKit file-system routing including pages, layouts, navigation, and route parameter handling.
---

# SvelteKit Routing

## Specialization

Expert guidance for SvelteKit file-system routing. Covers the full routing surface: `+page.svelte`, `+layout.svelte`, `+page.ts`, `+page.server.ts`, named and positional route parameters, navigation helpers, and link preloading.

## Trigger Conditions

- Implementing or reviewing a SvelteKit page, layout, or nested route structure.
- Diagnosing routing mismatches, layout inheritance issues, or navigation behaviour.
- Choosing between client-side and server-side file module pairs.
- Implementing route parameters, slug pages, or catch-all routes.
- Preloading and prefetching links for performance.

## Scope Boundaries

In scope:

- File-system route conventions: `+page.svelte`, `+layout.svelte`, `+server.ts`, `+page.ts`, `+page.server.ts`.
- Route parameters (`[param]`) and their typed access via `$page.params`.
- Layout nesting, layout reset (`+layout@.svelte`), and named layout slots.
- Navigation helpers: `goto()`, `invalidate()`, `invalidateAll()`, `preloadData()`, `preloadCode()`.
- `<a>` link behaviour, `data-sveltekit-preload-data`, and `data-sveltekit-reload`.
- `$page` store: `url`, `params`, `route`, `status`, `error`, `data`, `form`.

Out of scope:

- Load function implementation detail (covered by `sveltekit-load`).
- Form actions (covered by `sveltekit-actions`).
- Advanced routing features: groups, optional params, rest params, matchers (covered by `sveltekit-advanced-routing`).
- Error page setup (covered by `sveltekit-errors`).

## Inputs

- Target route structure or file tree.
- Route parameter requirements and type constraints.
- Layout nesting intentions.
- Navigation requirements (programmatic or link-based).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Route file tree | Correct `src/routes/` directory structure with all required `+` files |
| Parameter access pattern | Typed `params` access via `PageData` or `$page.params` |
| Layout inheritance map | Which layouts nest where; reset points documented |
| Navigation implementation | `goto()`, link attributes, or preload calls as appropriate |
| Routing correctness checklist | Pass/fail against the routing rules below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Understand SvelteKit routing conventions | Single route with a page and layout renders correctly |
| L2 Practical Delivery | Implement a multi-route feature with shared layout | All routes, parameters, and layouts render with correct data flow |
| L3 Specialist Hardening | Optimise navigation and preloading for production | Preload strategy documented; LCP and navigation timing measured |
| L4 Expert Standardisation | Define reusable routing conventions for a project | Route structure guide, parameter typing policy, and layout reset rules documented |

## Workflow

1. Map the desired URL structure to a `src/routes/` directory tree.
2. Identify required `+page.svelte`, `+layout.svelte`, and server/universal module pairs per route segment.
3. Define route parameters using `[param]` folders; apply type constraints via matchers when needed.
4. Establish layout nesting: identify shared layouts and any reset boundaries (`+layout@.svelte`).
5. Implement `$page` store access for reactive URL, params, and route metadata.
6. Choose navigation strategy: declarative `<a>` links with preload attributes or programmatic `goto()`.
7. Apply `data-sveltekit-preload-data` to links that benefit from early load execution.
8. Validate each route resolves to the correct component and layout tree in development.
9. Run the routing correctness checklist.

## Routing Correctness Checklist

- [ ] Every URL segment maps to exactly one `+page.svelte` or `+server.ts` entry point.
- [ ] `[param]` folders are used for dynamic segments; no hand-rolled path parsing.
- [ ] `$page.params` access is typed through the generated `PageData` or `RouteParams` types.
- [ ] Layout nesting is intentional; layout reset (`@`) is used only when inheritance must break.
- [ ] `goto()` calls include `{ replaceState: true }` where back-button semantics require it.
- [ ] Preload attributes are applied to links with heavy server load functions.
- [ ] No route module exports non-SvelteKit symbols that conflict with the `+` file contract.

## Security Notes

- Treat route parameters as untrusted input; validate before use in load functions or actions.
- Do not embed secrets in route segments or expose internal identifiers through URL patterns.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Route file structure | Workflow steps 1–2 |
| Parameter definition and typing | Workflow step 3 + Routing Correctness Checklist |
| Layout nesting and reset | Workflow step 4 |
| Navigation implementation | Workflow steps 6–7 |
| Preloading strategy | Workflow step 7 |
| Correctness validation | Routing Correctness Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
