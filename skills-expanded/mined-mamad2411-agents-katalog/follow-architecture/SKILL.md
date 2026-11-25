---
name: follow-architecture
description: Pick and apply the architecture pattern — Clean, Layered, monorepo layout, workspace file structures
argument-hint: "[clean | layered | monorepo | architecture | target]"
related:
  - refactor
  - deep-review-codebase
  - scan-codebase
  - follow-monorepo
  - follow-my-techstack
  - create-plan-in-dot-devin
  - update-references
  - run-check
  - follow-tool-madge
  - report-before-after
  - ask-me
  - improve
  - update-agents-md
  - update-astgrep-rules
  - use-lib-effective
---

## Goal

Pick the one architecture pattern that fits the target from evidence, then apply it — never restructure from a guess; microservices and distributed topology are out of scope

## Scope

> Invoked as `/follow-architecture` — the architecture SSOT dispatched by `/refactor` for architecture scopes (`/refactor ### 2` plan + `/refactor ### 3` architecture bullet); pattern selection + Clean/Layered guides + monorepo layout + file structure per workspace type, all inline in this single file (promoted back from the `refactor/workflows/architecture/` workflow; `event-driven.md` deleted — messaging work routes to `/improve {events,queues,realtime}`)

| Argument | Seen When | Run |
|----------|-----------|-----|
| (none), `target`, `architecture` | target needs an architecture — the argument `/refactor` passes on | `### 1` → `### 4` full path |
| `clean` | `packages/*`, `crates/*`, or several apps sharing a domain | pick Clean → `## Clean Pattern` |
| `layered` | a single app | pick Layered → `## Layered Pattern` |
| `monorepo` | repo root holds several workspaces | `## Monorepo Architecture` first, then per-workspace pattern |

Handed off elsewhere: microservices/distributed topology (see `## Goal`) · the target is a skill package → `/refactor-skills` · folder move only → `/relocation` · naming only → `/rename` · boundary checking without a restructure → `/deep-review-codebase` dimension `review-architecture`

## Execute

### 1. Detect Target

> Goal: know what the target is and how many apps it has

1. Run `/scan-codebase` at the root — identify `apps/*`, `packages/*`, `crates/*`, and the target the user specifies
2. Read what the project already decided: its `AGENTS.md` `Follow Architecture` section + `.devin/rules/` — a recorded pattern is repaired, not re-picked; write back at `### 4`
3. Count app entry points; check for shared domain/modules several apps must use together (unified support)
4. `/deep-review-codebase` dimension `review-architecture` on the target — coupling/boundary/dependency-direction evidence; explicit `clean`/`layered` argument → that pattern directly, skipping `### 2`

### 2. Select Pattern

> Goal: pick the single pattern that fits the target

| No. | Condition | Pattern |
|-----|-----------|---------|
| 1 | Several `apps/*` need unified support — share `modules/`/`core/`/`contracts/` across entry points | Clean |
| 2 | `packages/*`, `crates/*` (shared libs, domain packages) | Clean |
| 3 | A single app standing alone — a CLI that is one entry among `api`+`worker`+`cron` is not single → row 1 | Layered |
| 4 | Other targets — high testability/domain-heavy → Clean; UI-driven/CRUD → Layered | by code character |

1. Read the table top-down — first row that fits wins (rows 1–2 are mechanical, row 4 is judgement); still unclear → run `/ask-me` before choosing, never mix patterns in one target — handle one target at a time
2. Target matches a row of `## File Structure By Workspace Type` → the owner skill's template is canonical for that stack (pattern rules here still apply)
3. Bulk scope → `/create-plan-in-dot-devin` first; while planning run `/use-lib-effective` — reuse before writing anything new

### 3. Apply The Pattern

> Goal: restructure through the matching section, one batch at a time

1. Read `## Clean Pattern` or `## Layered Pattern` and follow its `### Restructure` steps
2. Mixed concerns found during a move → fix them with `/refactor` `### 3` (concerns split) first
3. After each move batch → `/update-references` + `/run-check` green before the next; red → rollback that batch

### 4. Verify Pattern Real

> Goal: the pattern stays real in code, not just folder names — and it is provable

1. Boundaries hold: `core/` + `modules/*/domain/` (Clean) or `types/` + `utils/` + `services/` (Layered) stay pure — no IO/framework imports, `services/` holds business rules only with IO reached through `infra/`; dependency direction never reversed; public API through barrels only, no deep imports from outside
2. `/follow-tool-madge` (no circular) + `/deep-review-codebase` dimension `review-architecture` vs baseline; tests pass as before, original public API still works
3. Persist the boundary so it stays enforced: import-direction rules → `/update-astgrep-rules` (`rules/architecture/` + `rules/dependencies/`), chosen pattern → the target's `AGENTS.md` `Follow Architecture` section via `/update-agents-md`
4. `/report-before-after` with the old → new layer map

## Monorepo Architecture

> Goal: repo-level layout before per-workspace pattern choice; conventions/tooling verified by `/follow-monorepo`

```text
repo/
├─ apps/<name>/       # Deployable entry points (web, api, worker, cli) — each picks its own pattern
├─ packages/<name>/   # Shared TS libs (domain, ui, config) — Clean-shaped, no app/ layer inside
├─ crates/<name>/     # Shared Rust libs — same role as packages/ (one Cargo workspace)
├─ tools/<name>/      # Internal dev scripts/CLIs — never shipped, never imported by packages/
├─ infra/             # Deploy/observability config — not a workspace
├─ docs/              # root docs only — test specs stay per workspace at apps/<name>/specs/ (/update-specs)
└─ package.json | Cargo.toml | moon.yml / turbo.json   # workspace manifests + task orchestrator
```

1. Workspace types: `app` (leaf — may import shared), `package`/`crate` (shared, Clean internals), `tool` (dev-only); dependencies flow apps → shared → nothing — shared packages are leaves (`/follow-tool-madge` proves no cycles)
2. Every workspace gets its own pattern from `### 2`: single-app workspace → Layered; workspace exposing a domain to several apps → Clean; a shared package with ports/adapters/IO → Clean subset (`core/` + `modules/` only)
3. Extract to `packages/`/`crates/` only with ≥2 real consumers — coincidental similarity stays duplicated (`/refactor` shared bullet)
4. Task graph, version/type catalogs, CI, workspace conventions → `/follow-monorepo`; new dep choice for a layer → `/follow-my-techstack`

## Clean Pattern

> When: several `apps/*` needing unified support, or `packages/*`/`crates/*` shared libraries. Dependency direction `core` ← `modules` ← `adapters` ← `infra` ← `app` — never reverse it; `contracts/` + `config/` are leaves any layer may import; inside a module the order is `domain` ← `features` ← `usecases` (see `### Layer Table`)

### Restructure

1. Prepare: `/scan-codebase` the target — domain logic, side effects, external deps; identify the current public API (barrel `index`) and consumers — they must be preserved
2. Create the structure below; move pure logic → `modules/*/domain/` + `core/`; application use cases called by `app/` → `modules/*/usecases/`; feature orchestration → `modules/*/features/`; interfaces → `ports/`; IO/framework → `infra/` + `adapters/`
3. Define the ports `features/` needs — `adapters`/`infra` implement them; wire everything at the `app/runtime.ts` composition root
4. Verify: no imports from `core/`/`domain`/`features` into `infra/`/`adapters/`; run `/run-check` + the tests

### File Structure

```text
src/
├─ app/                                  # Entry points + composition roots
│  ├─ api/                               # routes/, middleware/, server.ts
│  ├─ web/                               # routes/, components/, hooks/ (optional UI), middleware/, server.ts
│  ├─ cli/  worker/  cron/  plugin/      # commands/ or jobs/ + runner.ts; plugin adds loader/registry
│  ├─ runtime.ts                         # composition root — wire ports → adapters
│  └─ layers.ts                          # canonical layer names — single source for import-boundary checks
├─ modules/<name>/                       # Business capabilities (bounded contexts) — one per domain: auth, users, orders, payments
│  ├─ domain/                            # model.ts, errors.ts, schema.ts — pure types + rules, no IO/framework
│  ├─ usecases/                          # login.ts, checkout.ts — entries called by app/ (optional — when orchestration spans features or several entries)
│  ├─ features/                          # create.ts, session.ts — feature logic orchestrating domain + ports
│  ├─ ports/                             # interfaces the module needs — session-store, user-store, payment-gateway
│  ├─ adapters/                          # dto.ts, mappers/ — module-level boundary translation
│  └─ index.ts                           # module barrel — public API only
├─ core/                                 # Pure shared kernel: errors/, result.ts, option.ts, ids.ts, time.ts, events.ts (mechanism only — event payloads live in contracts/events/), pagination.ts + ports/ (clock, random, id-generator)
├─ adapters/                             # Cross-module boundary translation, no IO: http/ request-response shapes, persistence/ dto, messaging/ envelopes, payments/, auth/
├─ infra/                                # IO implementations of ports: database/, postgres/, queue/, cache/, storage/, email/, http/ transport client, clock/, observability/
├─ contracts/                            # Cross-boundary pure types: api/, events/, plugins/ — leaf, imports nothing
└─ config/                               # env.ts, app.ts, database.ts, services.ts — leaf
tests/                                   # unit/ (core, modules) · integration/ (infra, adapters) · e2e/ (app entry points)
scripts/  docs/  package.json  tsconfig.json  README.md  .env.example
```

### Layer Table

| No. | Layer | Contains | Tests | Deps | Risk |
|-----|-------|----------|-------|------|------|
| 1 | `core/` | pure primitives: `result.ts`, `option.ts`, `errors/`, `ids.ts`, `time.ts`, `events.ts` (mechanism — payloads → `contracts/events/`), `pagination.ts` + `ports/` | pure unit — no IO mocks | leaf — imports no other layer | high — shared kernel |
| 2 | `modules/*/domain/` | `model.ts`, `errors.ts`, `schema.ts` — pure types + business rules | pure unit | → `core/` only | high |
| 3 | `modules/*/usecases/` | application use cases called by `app/` (optional) | unit with mocked ports | → `features/`, `domain/`, `ports/`, `core/` | medium — application boundary |
| 4 | `modules/*/features/` | feature logic orchestrating domain + ports | unit with mocked ports | → `domain/` (same module), `ports/`, `core/` — never `usecases/` | medium |
| 5 | `modules/*/ports/` | `*Port` interfaces the module needs | — (types only) | → `domain/` types only | low |
| 6 | `modules/*/adapters/` | module-level boundary translation/mappers | integration | → `domain/`, `ports/` | medium |
| 7 | `contracts/` | api schemas, event schemas (payloads), plugin contracts — pure types | schema validation | leaf | low |
| 8 | `adapters/` | cross-module translation, no IO: `http/` shapes, `persistence/` dto, `messaging/` envelopes | integration | → module ports, `contracts/` | medium |
| 9 | `infra/` | `database/`, `postgres/`, `queue/`, `cache/`, `storage/`, `email/`, `http/` transport, `observability/` — IO implementations of ports | integration | → `core/`/module `ports/`, `adapters/` | medium — IO/framework |
| 10 | `app/` | entry points `api/`, `web/`, `cli/`, `worker/`, `cron/`, `plugin/` + `runtime.ts` | smoke + e2e | → `usecases/` (fallback `features/`), `contracts/`, `config/`; `runtime.ts` imports `infra/`/`adapters/` for wiring only | low |
| 11 | `config/` | `env.ts`, `app.ts`, `database.ts`, `services.ts` | config tests | leaf | low |

### Rules

- `domain/` + `core/` stay pure — no IO, framework imports, or side effects; no `fx/` layer — side effects live in `infra/`, orchestrated through `features/` + ports
- `adapters/` maps shapes, `infra/` owns transport: an HTTP/fetch client belongs to `infra/http/`, its request/response types to `adapters/http/` — never put IO in `adapters/`, never put DTO shapes in `infra/`
- `contracts/` and `config/` are leaves — every layer may use them, they never import back; modules reach each other only through `contracts/` events or ports — never import another module directly
- `usecases/` is optional per module — use when orchestration spans features or several entry points share one flow; `app/` calls `usecases/` first when present (fallback → `features/`); direction `usecases → features → domain` never reversed
- `app/runtime.ts` is the single composition root wiring ports → implementations; `app/web/components/` + `hooks/` are optional UI-only — call `usecases/`/`features/` + `contracts/`, never `infra/`/`domain/` directly
- Public API only through the module/layer `index.ts` barrel — no deep imports from outside

## Layered Pattern

> When: a single app — one `apps/*` or a single-app project; flat folders grouped by type, layers point one way down: `presentation` → `domain` → `data`, no bypass; if the app grows into several apps sharing a domain → upgrade to Clean

### Restructure

1. Prepare: `/scan-codebase` the target — routes/pages, business logic, data access; identify the public API and route entry points to preserve
2. Map folders: presentation → `app/`+`components/`+`hooks/`; domain → `usecases/`+`services/`+`features/`; data → `infra/`+`lib/`; shared leaves → `types/`+`constants/`+`utils/`+`config/`
3. Create the flat type-grouped folders below — never nest by capability; prefix file names with the domain (`user-service.ts`); move files one batch at a time
4. Enforce dependencies: presentation → domain → data only; `app/` calls `usecases/`/`features/` only; public API through the `index` barrel; align tests per layer
5. Verify: no layer bypass (e.g. `components/` calling `infra/` directly), no cross-layer deep imports; run `/run-check` + the tests

### File Structure

```text
src/
├─ app/                                  # Entry & routes — wire layers (presentation): routes/ or pages/, middleware/, server.ts, index.ts
├─ components/                           # UI components — PascalCase, presentational (presentation, optional if UI)
├─ hooks/                                # hooks / composables — UI state + view logic (presentation, optional)
├─ usecases/                             # application use cases — login.ts, create-order.ts (domain, required)
├─ services/                             # domain services — user-service.ts, order-service.ts — pure business rules (domain, required)
├─ features/                             # feature-level logic composing services — checkout.ts (domain, optional)
├─ infra/                                # repositories, database/ (client, schema, migrations), external APIs (data, required)
├─ lib/                                  # third-party wrappers / singleton clients — db.ts, stripe-client.ts (data, optional)
├─ types/  constants/  utils/  config/   # shared leaves — pure, no IO; every layer imports them, they never import back
└─ index.ts                              # barrel — public API
tests/                                   # unit/ (usecases, services, features, utils) · integration/ (infra, lib) · e2e/ (app routes + components)
scripts/  docs/  package.json  tsconfig.json  README.md  .env.example
```

### Layer Table

| No. | Layer | Folder | Contains | Required | Deps |
|-----|-------|--------|----------|----------|------|
| 1 | presentation | `app/` | routes/pages, middleware, `server.ts` | required | → `usecases/`, `features/` + shared leaves |
| 2 | presentation | `components/` | UI components — PascalCase, presentational | if UI | → `hooks/`, `usecases/` + shared leaves — never `infra/`/`lib/` |
| 3 | presentation | `hooks/` | hooks / composables — UI state + view logic | if UI framework | → `usecases/` + shared leaves |
| 4 | domain | `usecases/` | orchestration entries (`login.ts`, `create-order.ts`) | required | → `services/`, `features/`, `infra/` + shared leaves |
| 5 | domain | `services/` | `*-service.ts` — pure business rules | required | → `infra/`, `lib/` + shared leaves — never presentation |
| 6 | domain | `features/` | feature-level logic composing services | optional | → `services/` + shared leaves — never `usecases/` |
| 7 | data | `infra/` | repositories, `database/`, external APIs | required | shared leaves only — bottom layer |
| 8 | data | `lib/` | third-party wrappers / singleton clients | optional | shared leaves only |
| 9 | shared leaf | `types/` | shared types — pure types only | optional | leaf — never import back |
| 10 | shared leaf | `constants/` | constants | optional | leaf — usable by every layer |
| 11 | shared leaf | `utils/` | pure utilities — no IO | optional | leaf — usable by every layer |
| 12 | shared leaf | `config/` | `env.ts`, `app.ts`, `database.ts` | optional | leaf — usable by every layer |
| 13 | root | `index.ts` | barrel — public API | required | → every layer |

### Rules

- Flat folders only — never nest by capability/domain; group by type and prefix file names with the domain (`user-service.ts`, `order-service.ts`)
- Dependencies point one way down: presentation → domain → data — no bypassing and never pointing up; `app/` calls `usecases/`/`features/` only, never `services/`/`infra/` directly when a usecase wraps them
- `types/`, `constants/`, `utils/`, `config/` are leaves — every layer may import them, they never import back into layer folders; `utils/` + `types/` stay pure (no IO, framework imports, side effects)
- Public API through the `index.ts` barrel — no deep imports across layers; use the project's path aliases instead of cross-folder relative imports
- Preserve existing behavior — routes/pages work exactly as before the restructure

## File Structure By Workspace Type

> Owner skills hold the stack templates — never copy a structure here; the pattern rules above still apply inside each workspace

| Type | Owner | Variants (templates live in the owner skill) |
|------|-------|----------------------------------------------|
| Web | `/follow-create-web` (dispatcher) | nextjs, nuxt, svelte, vite-spa, solid SPA + TanStack Router, TanStack Start → CF Workers / Nitro (`/follow-solid-framework`), docs site, WebMCP, Rust WASM |
| Mobile / Desktop | `/follow-create-mobile` / `/follow-create-desktop-tauri` | Capacitor cross-platform, iOS+Android native (KMP), Tauri, Dioxus |
| CLI / TUI / Library | `/follow-create-cli` / `/follow-create-tui-ratatui` / `/follow-tool-tsdown` | Bun CLI, Rust CLI, Rust crate, Nushell module, PowerShell module, TS library |
| Plugin / Extension | `/follow-create-plugins` (dispatcher) | vite, rolldown, bun, nitro, elysia, biome, eslint, oxlint, vitest, storybook, tauri, vscode, browser (WXT), obsidian, nvim, zed, raycast, claude, codex, devin |
| Bot / Service / Product | `/follow-create-bot` / `/follow-create-sdk` / `/follow-create-product` | discord, github bot + GitHub App, line, slack, telegram, MCP server, Docker image, GitHub Action, SDK, Slidev deck, Devin project skills |

> This table lists owner skills only, never actions — the upgrade trigger (a Layered app growing into several `apps/*` sharing a domain) lives in `## Layered Pattern`, and multi-entry targets are already `### 2` row 1

## Rules

- Single Entry — every architecture restructure goes through this skill (`### 1`–`### 4`), dispatched from `/refactor` for architecture scopes; never duplicate pattern detail elsewhere
- One pattern per target, one move batch per `/update-references` + `/run-check` cycle; preserve behavior and the original public API (same Two Hats / Safety Net rules as `/refactor` `## Rules`)
- No churn without cause — a layout that already holds the direction and purity checks keeps its pattern: repair the violations in place, never big-bang a working pattern into the other one; re-pick only when `### 1` evidence genuinely changed
- Event-driven/messaging redesign is not a pattern restructure here: semantics → `/improve events`, queue ops → `/improve queues`, transport → `/improve realtime`
- Improvement loop over this skill's findings → `/improve architecture` (scope-map resolves to `/follow-architecture`)

## Expected Outcome

- The target is restructured with the fitting pattern — multi-app unified / `packages/` / `crates/` = Clean, single app = Layered (flat type-grouped); a monorepo is laid out by workspace type
- No circular dependencies; the original public API still works; passes `/run-check` and the tests; the boundary is persisted (`/update-astgrep-rules`) and the chosen pattern recorded in the target's `AGENTS.md`
- `/report-before-after` shows the old → new layer map
