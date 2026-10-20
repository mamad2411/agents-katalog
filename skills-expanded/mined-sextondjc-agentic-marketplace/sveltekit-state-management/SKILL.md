---
name: sveltekit-state-management
description: Use when implementing or reviewing reactive state in SvelteKit using $app/state runes, $app/stores legacy API, App.PageState typing, shallow routing state, or navigating/updated lifecycle signals.
---

# SvelteKit State Management

## Specialization

Expert guidance for SvelteKit reactive state. Covers the `$app/state` runes-based API (`page`, `navigating`, `updated`), the Svelte 4 `$app/stores` legacy API (`$page`, `$navigating`, `$updated`), `App.PageState` typing for shallow-routing state, safe migration patterns between the two APIs, and patterns for sharing state across layouts without prop drilling.

## Trigger Conditions

- Accessing the current URL, route ID, params, or form data reactively in a component.
- Reading or typing `page.state` for shallow-routing history state.
- Implementing a navigation progress indicator using `navigating`.
- Determining whether the app has been updated and prompting the user to reload.
- Migrating a Svelte 4 project from `$app/stores` to `$app/state`.
- Diagnosing stale state after navigation or SSR hydration mismatches.

## Scope Boundaries

In scope:

- `$app/state`: `page`, `navigating`, `updated` rune-based reactive objects (Svelte 5 / SvelteKit 2.12+).
- `$app/stores`: `$page`, `$navigating`, `$updated` legacy store API (Svelte 4 / pre-2.12 compatibility).
- `page` object fields: `url`, `params`, `route`, `status`, `error`, `data`, `form`, `state`.
- `App.PageState` interface declaration for type-safe shallow-routing state.
- `navigating` object fields: `from`, `to`, `type`, `delta`.
- `updated.check()` for polling the deployment version.
- `afterNavigate` and `beforeNavigate` lifecycle hooks for side-effect timing.
- Sharing state between layouts and pages using Svelte 5 runes context or module-level stores.
- SSR-safe state access: guards for server-side execution where browser APIs are absent.

Out of scope:

- Shallow routing implementation (`pushState`, `replaceState`) — covered by this skill's `App.PageState` section but the navigation API itself is documented in `sveltekit-advanced-routing`.
- Load function data flow — covered by `sveltekit-load`.
- Form action result state (`$page.form`) — covered by `sveltekit-actions`.
- Global application state unrelated to SvelteKit routing (Svelte stores, signals, Zustand-style patterns).

## Inputs

- Svelte version (4 or 5) and SvelteKit version (determines which API is available).
- State access pattern needed (URL, params, route, shallow state, navigation progress).
- Whether the code runs on server and/or client (SSR safety requirement).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| State access implementation | Correct import and usage of `$app/state` or `$app/stores` based on version |
| `App.PageState` declaration | Interface added to `src/app.d.ts` when `page.state` is used |
| Migration path | Step-by-step store → rune conversion for Svelte 4 → 5 projects |
| SSR safety guards | Any server-unsafe access wrapped or deferred appropriately |
| State quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Read current URL and route params in a component | `page.url` and `page.params` accessed correctly |
| L2 Practical Delivery | Navigation progress indicator and version update banner | `navigating` and `updated` both drive reactive UI |
| L3 Specialist Hardening | Type-safe shallow routing state and SSR-safe patterns | `App.PageState` declared; no browser-only code runs on server |
| L4 Expert Standardisation | Full migration from `$app/stores` to `$app/state` with shared layout state | All components migrated; no mixed API usage; SSR verified |

## Workflow

1. Determine the SvelteKit version: use `$app/state` for SvelteKit ≥ 2.12 with Svelte 5; use `$app/stores` for earlier versions or Svelte 4 components.
2. Import only the state objects needed: `import { page } from '$app/state'` (not the entire module).
3. Access `page.url`, `page.params`, `page.route.id`, `page.data`, `page.form`, or `page.state` as reactive properties in a `$derived` expression or directly in template expressions.
4. For navigation progress, import `navigating` from `$app/state`; render a progress bar when `navigating !== null`.
5. For deployment version checks, import `updated` and call `updated.check()` inside a lifecycle effect; show a refresh prompt when it returns `true`.
6. When using shallow routing state, declare `interface PageState { ... }` in `src/app.d.ts` to make `page.state` type-safe.
7. For Svelte 4 / `$app/stores`: import `page` from `$app/stores` and prefix with `$` in templates (`$page.url`, `$page.params`).
8. For SSR-safe code, guard browser-only side effects with `if (browser)` from `$app/environment` before accessing `window`, `document`, or `history`.
9. To share state across layouts, use Svelte 5 context (`setContext`/`getContext`) in layout files, or a module-level reactive state file with `$state` runes.
10. Run the state quality checklist.

## State Quality Checklist

- [ ] `$app/state` is used for all new Svelte 5 components; `$app/stores` is not mixed in the same component.
- [ ] `page.state` usage is accompanied by a typed `App.PageState` declaration in `src/app.d.ts`.
- [ ] Browser-only APIs (`window`, `history`, `document`) are guarded with `if (browser)`.
- [ ] `navigating` is accessed reactively, not cached in a local variable.
- [ ] `updated.check()` is called on a timer or user trigger, not unconditionally on render.
- [ ] No `$page` store subscriptions remain in Svelte 5 components after migration.
- [ ] SSR rendering produces no `undefined` errors from state access on the server.
- [ ] Shared layout state uses context or explicit state files, not module-level singletons that survive across SSR requests.

## Security Notes

- Do not store sensitive user data (tokens, PII) in `page.state` — it persists in `sessionStorage` via the shallow routing mechanism and is readable by any script on the page.
- `page.data` reflects what your load function returned; ensure server load functions do not inadvertently include server-only secrets in the return value.
- `App.PageState` is a client-side type only; never rely on it for server-side authorization.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Current URL/params access | Workflow steps 2–3 |
| Navigation progress indicator | Workflow step 4 |
| Deployment version check | Workflow step 5 |
| Type-safe shallow routing state | Workflow step 6 |
| Svelte 4 `$app/stores` usage | Workflow step 7 |
| SSR safety | Workflow step 8 |
| Shared layout state | Workflow step 9 |
| Migration path | Workflow steps 1 + 7 |
| Quality validation | State Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
