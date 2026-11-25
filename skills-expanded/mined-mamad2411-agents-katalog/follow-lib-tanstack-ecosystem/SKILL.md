---
name: follow-lib-tanstack-ecosystem
description: Choose and use TanStack libraries in a project per use case and maturity
argument-hint: "[scope]"
related:
  - deep-analyze
  - ask-me
  - run-install
  - run-test
  - run-typecheck
---

## Goal

Choose and integrate TanStack libraries correctly per use case and each library's maturity

## Scope

For projects wanting the current TanStack ecosystem (see the latest list at `https://tanstack.com/libraries`):

- Framework: `Start` (full-stack SSR/streaming on Router + Vite, v1 stable), `Router` (type-safe routing for React/Solid, v1)
- Data & State: `Query` (server state, v5), `DB` (reactive client store, 0.x), `Store` (client state, 0.x), `AI` (framework-agnostic AI SDK, 0.x)
- UI & UX: `Table` (headless datagrid, v9), `Form` (form state, v1; v2 alpha), `Charts`, `Hotkeys`, `Markdown`, `Highlight`
- Performance: `Virtual` (virtualized lists, v3), `Pacer` (debounce/throttle/batch, 0.x)
- Tooling: `Devtools` (unified devtools panel), `Config`, `CLI`, `Intent`

- Latest: query `5.104.1` / router `1.170.41` / start `1.168.60` / table `9.2.4` / form `1.33.5` / virtual `3.14.13` / store `0.11.2` / db `0.11.1` / ai `0.63.0` / pacer `0.23.0` (react-pacer `0.24.0`) / charts `0.18.0` / hotkeys `0.12.1` / markdown `1.0.0` / highlight `1.0.0` / intent `0.5.0` / config `0.22.2` / cli `0.71.1` (verified 2026-10-02)

## Execute

### 1. Identify Needs

> Goal: determine which TanStack library is needed

1. Do `/deep-analyze` to understand state, data flow, routing, and form needs
2. Check what the project wants:
   - async server state / data fetching → `Query`
   - client state → `Store`
   - type-safe routing → `Router`
   - full-stack framework (SSR, server functions) → `Start`
   - form state + validation → `Form`
   - headless data tables → `Table`
   - virtualized long lists → `Virtual`
   - local-first reactive data / sync → `DB`
   - AI providers, chat, MCP integration → `AI`
   - debounce/throttle/rate-limit → `Pacer`
3. Check maturity before use: `0.x` or alpha/RC ones (e.g. `DB`, `AI`, `Pacer`, `Store`) may change their API — use only when the risk is acceptable
4. If unclear → stop and `/ask-me`

### 2. Install And Configure

> Goal: install the chosen library

1. Use the project's package manager (`npm`, `pnpm`, `bun`, `yarn`) via `/run-install`
2. Install packages per the `@tanstack/{framework}-{lib}` naming convention, e.g. `@tanstack/react-query`, `@tanstack/vue-query`, `@tanstack/solid-router`, `@tanstack/svelte-query` (some Angular ones still use `*-experimental`, e.g. `@tanstack/angular-query-experimental`)
3. Configure the provider/client in the entry point, e.g. `QueryClientProvider` for Query
4. Install `Devtools` as a dev dependency to inspect state while developing
5. Verify version compatibility with the framework version in `package.json`

### 3. Implement Feature

> Goal: use the library in a real feature

1. `Query`: create query keys and query functions, set `staleTime`/`gcTime`, use `select`, mutations + invalidation
2. `Form`: create the schema (supports Standard Schema such as Zod/Valibot/ArkType), fields, validation, submission
3. `Router`: build the route tree (file-based or code-based), loaders, search param validation, navigation
4. `Start`: create server functions, SSR routes, middleware
5. `Store`: create a store for client state that isn't server state
6. `Table`: configure columns, sorting, filtering, pagination (headless — render the UI yourself)
7. `Virtual`: attach the virtualizer to long lists/tables
8. `DB`/`AI`: configure collections/sync engine or AI provider adapters per the latest docs
9. `Charts`: declarative charts from data + axes + series (grammar-of-graphics)
10. `Markdown`/`Highlight`: doc model rendering or syntax highlighting (streaming-friendly)
11. `Hotkeys`: keyboard shortcuts + sequences + scopes
12. `Pacer`: debounce/throttle/rate-limit/queue/batch hooks

### 4. Test And Optimize

> Goal: confirm the integration works well

1. Run `/run-test` and `/run-typecheck`
2. Inspect `Query`/`DB` caching behavior via Devtools
3. Measure component re-renders
4. Check error boundaries, pending, and loading states

### Workflows

| Library | Skill |
|---------|----------|
| Start — full-stack framework (SSR, server fns) | `/follow-lib-tanstack-start` |
| Router — type-safe routing | `/follow-lib-tanstack-router` |
| Query — server state | `/follow-lib-tanstack-query` |
| DB — reactive client store, live queries, sync | `/follow-lib-tanstack-db` |
| Store — client state | `/follow-lib-tanstack-store` |
| AI — provider-agnostic AI SDK | `/follow-lib-tanstack-ai` |
| Table — headless datagrid | `/follow-lib-tanstack-table` |
| Form — headless forms + Standard Schema | `/follow-lib-tanstack-form` |
| Charts — grammar-of-graphics charts | `/follow-lib-tanstack-charts` |
| Markdown — serializable doc model / AI streams | `/follow-lib-tanstack-markdown` |
| Highlight — themeable syntax highlighting | `/follow-lib-tanstack-highlight` |
| Virtual — virtualized lists | `/follow-lib-tanstack-virtual` |
| Pacer — debounce/throttle/rate-limit/queue/batch | `/follow-lib-tanstack-pacer` |
| Hotkeys — type-safe shortcuts/sequences/scopes | `/follow-lib-tanstack-hotkeys` |
| Devtools — unified devtools panel | `/follow-lib-tanstack-devtools` |
| CLI — project scaffolding + add-ons | `/follow-lib-tanstack-cli` |
| Intent — ship agent skills in npm packages | `/follow-lib-tanstack-intent` |
| Config — publish/maintain packages | `/follow-lib-tanstack-config` |

## Rules

### 1. Library Selection

- Pick the library by real use case — don't install all of them
- `Query` and `Store` don't replace each other — use `Query` for server state, `Store` for client state
- `Router`/`Start` support React and Solid only — if using Vue/Svelte, use that framework's router
- Always cite the official docs `https://tanstack.com` as the primary source
- Per-library detail lives in the specialized `/follow-lib-tanstack-*` skills (all 18 libs — see the Workflows table; each skill's `references/apis.md` has package versions + API tables)

### 2. Type Safety

- Use the TypeScript types the library provides
- Make query keys, route params, and form schemas type-safe
- Avoid `any` in callbacks

### 3. Performance

- Use `select` and `staleTime` in `Query` to reduce refetching
- Use `Virtual` only for large lists
- Use `Pacer` for debounce/throttle instead of hand-rolling it
- Separate reactivity scopes properly in `Store`/`DB`

- See each `/follow-lib-tanstack-*` skill's `best-practices/` for recommended patterns and pitfalls

## Expected Outcome

- The chosen TanStack library fits the use case and maturity
- The integration works and passes typecheck/tests
- Appropriate performance, no over-fetching or over-rendering
- Readable, maintainable code
