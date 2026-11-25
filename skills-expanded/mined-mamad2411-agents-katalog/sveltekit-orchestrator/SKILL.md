---
name: sveltekit-orchestrator
description: Use when a SvelteKit request spans multiple capability domains and needs one deterministic intake, explicit phase ownership, and a unified execution contract.
---

# SvelteKit Orchestrator

## Specialization

Coordinate cross-domain SvelteKit requests from one intake when work spans routing, data loading, form actions, rendering options, hooks, adapters, advanced routing, or error handling.

This skill provides intake, phase ownership, and unified synthesis. It does not replace deep execution guidance for any single domain.

## Objective

Produce one deterministic SvelteKit execution contract from a single intake, with explicit phase ownership, evidence expectations, and completion checks.

## Trigger Conditions

- A SvelteKit request spans more than one capability domain.
- Teams need one intake instead of disconnected routing, loading, and deployment workflows.
- Cross-project reuse matters more than a one-off local optimisation.
- A feature requires explicit ownership across routing, data, actions, rendering, hooks, adapters, or error handling.

## Scope Boundaries

In scope:

- Deterministic SvelteKit intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed SvelteKit requests.
- Domain routing map to the eight specialist skill domains.

Out of scope:

- Deep implementation of any single specialist domain.
- Non-SvelteKit product areas unless they materially constrain the SvelteKit slice.
- Generic project governance unrelated to SvelteKit delivery.

## Domain Capability Catalog

Each domain maps to a dedicated specialist skill. Invoke the specialist directly when only one domain is involved.

| Domain | Specialist Skill | Scope Summary |
|---|---|---|
| Routing | `sveltekit-routing` | File-system routes, pages, layouts, navigation, `$page` store |
| Load Functions | `sveltekit-load` | Server load, universal load, streaming, invalidation, `fetch` |
| Form Actions | `sveltekit-actions` | `actions` export, `fail()`, `redirect()`, `use:enhance` |
| Page Options | `sveltekit-page-options` | `ssr`, `csr`, `prerender`, `trailingSlash`, `entries()` |
| Hooks | `sveltekit-hooks` | `handle`, `handleError`, `handleFetch`, `sequence`, `locals` |
| Adapters | `sveltekit-adapters` | `adapter-node`, `adapter-static`, `adapter-vercel`, `adapter-cloudflare` |
| Advanced Routing | `sveltekit-advanced-routing` | Route groups, optional params, rest params, matchers, layout reset |
| Errors | `sveltekit-errors` | `+error.svelte`, `error()`, `handleError`, `App.Error`, boundaries |
| Server Endpoints | `sveltekit-server-endpoints` | `+server.ts` HTTP verb exports, `json()`, `text()`, CORS, streaming |
| State Management | `sveltekit-state-management` | `$app/state` runes, `$app/stores` legacy, `App.PageState`, `navigating`, `updated` |
| Authentication | `sveltekit-auth` | Cookie sessions, OAuth, JWT, `locals.user`, Auth.js, Lucia |
| Environment Variables | `sveltekit-environment` | `$env/static/private`, `$env/dynamic/public`, server-only module boundaries |
| Observability | `sveltekit-observability` | `instrumentation.server.ts`, OpenTelemetry, `Server-Timing` headers |
| Testing | `sveltekit-testing` | Vitest, Playwright, `@sveltejs/kit/testing`, mock `RequestEvent` |
| Configuration | `sveltekit-configuration` | `svelte.config.js`: `paths.base`, aliases, CSP, CSRF, version management |
| Packaging | `sveltekit-packaging` | `@sveltejs/package`, `exports` map, `svelte` field, library publishing |

## Inputs

- User objective and target SvelteKit surface.
- Scope boundaries, environments, and risk level.
- Required outputs, known evidence, and delivery constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Intake contract | Objective, boundaries, and required outputs |
| Phase-output ownership matrix | One owning domain per required output |
| Unified SvelteKit execution recommendation | `narrow-execution`, `phased-execution`, or `stop-pending-blockers` |
| Rejected-candidate table | Domains excluded with reason codes |
| Closure check | Confirmation that all required outputs are owned |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one mixed SvelteKit request | One intake and one phase contract exist |
| L2 Delivery | Coordinate one cross-domain SvelteKit effort | Every required output has one owning domain |
| L3 Hardening | Support production-grade SvelteKit delivery | Risks, evidence expectations, and blockers are explicit |
| L4 Expert Standardisation | Establish reusable SvelteKit operating model | Reusable intake, ownership, and routing rubric documented |

## Phase Dependency Map

Apply before finalising phase ownership to catch mandatory sequencing requirements:

| Phase | Hard Dependency | Risk if Skipped |
|---|---|---|
| Load Functions | Routing must be resolved first | Load module files attach to route files; mismatched paths cause 404 |
| Form Actions | Routing must be resolved first | Actions live in `+page.server.ts`; routing gaps break action binding |
| Page Options | Load Functions decision must be known | `prerender: true` is incompatible with server-only data; `ssr: false` breaks server load |
| Hooks | Load and Actions phases must be defined | `locals` populated in hooks must match what load and actions consume |
| Adapters | Page Options must be finalised | Each adapter enforces its own SSR, edge, and static constraints |
| Error Handling | Hooks phase must be defined | `handleError` lives in hooks files; duplication or gaps cause silent error loss |

## Deterministic Workflow

1. Lock objective, risk boundary, target deployment platform, and required outputs.
2. Classify the request into one or more domains from the capability catalog.
3. Apply the phase dependency map to establish mandatory sequencing.
4. Assign exactly one owning domain per required output.
5. Reject any phase plan with unowned or multiply owned outputs.
6. Define evidence expectations and handoff criteria between phases.
7. Produce one unified execution recommendation.
8. Publish closure status with residual risks and unresolved blockers.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Domain | Evidence Expectation |
|---|---|---|
| Route structure and URL design | Routing | File tree, parameter types, layout inheritance |
| Data fetching and streaming | Load Functions | Module type decision, typed return, streaming plan |
| Form submission and mutation | Form Actions | Action file, `fail()` contract, `use:enhance` applied |
| Rendering mode per section | Page Options | Options exports, `entries()` for prerendered dynamic routes |
| Request interception and auth | Hooks | `handle` with `locals`, `handleError` safe message |
| Deployment and platform bindings | Adapters | Adapter config, env var strategy, platform binding types |
| Complex URL patterns | Advanced Routing | Group folders, matchers, layout resets |
| Error boundaries and logging | Errors | `+error.svelte` placement, `handleError` contract |

## Unified Decision Rules

- `narrow-execution`: one domain owns the meaningful work; adjacent domains are informational.
- `phased-execution`: two or more domains are required and ownership is unambiguous.
- `stop-pending-blockers`: required outputs are unowned, evidence is materially missing, or deployment risk cannot be bounded.

## Rejected Candidate Reasons

- `R1`: Outside the SvelteKit slice.
- `R2`: Adds overlap without adding required-output coverage.
- `R3`: Expands scope beyond the bounded objective.
- `R4`: Requires evidence or environment access not available.
- `R5`: Better handled by a single-domain workflow.

## Cross-Domain Risk Signals

Flag these patterns for explicit risk review during intake:

- `prerender: true` with dynamic route parameters and server load — static output may be incomplete or incorrect.
- `adapter-static` with server load functions — server load does not execute at runtime on static hosts.
- `locals` populated in hooks without typing `App.Locals` — type-unsafe and error-prone at scale.
- Sensitive data returned from universal load (`+page.ts`) — value reaches the client bundle.
- `adapter-auto` in production — determinism requires an explicit adapter selection.
- Nested `handle` functions without `sequence()` — order-dependent interception bugs are common.
- `handleError` defined in both `hooks.ts` and `hooks.server.ts` without coordination — duplicate or conflicting error shapes.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| One SvelteKit intake | Objective + Deterministic Workflow |
| Phase sequencing | Phase Dependency Map |
| Domain ownership clarity | Phase-Output Ownership Matrix Template |
| Deterministic orchestration | Unified Decision Rules |
| Rejected-scope record | Rejected Candidate Reasons |
| Cross-phase risk identification | Cross-Domain Risk Signals |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.


