---
name: follow-solid-framework
description: SolidJS app dispatcher — SPA (TanStack Router) / full-stack TanStack Start, deploy CF Workers or Nitro
argument-hint: "[spa|start|nitro-bun|nitro-cf]"
related:
  - follow-lib-solidjs
  - follow-lib-tanstack-ecosystem
  - follow-lib-unocss
  - follow-lib-nitro
  - follow-lib-drizzle
  - follow-lib-orpc
  - follow-lib-effect-ts
  - follow-service-cloudflare
  - follow-tool-vite
  - follow-lang-typescript
  - follow-single-responsibility
  - follow-web-standard
  - run-dev
---

## Goal

Build a SolidJS application — pick the variant by deploy target, then execute that variant's sections

## Scope

Covers every Solid app archetype:

| Variant | Stack | Deploy | When |
|---|---|---|---|
| `spa` | Solid + TanStack Router + UnoCSS | static bundle | client-only (dashboard, Tauri/Capacitor embed) |
| `start` | TanStack Start (SSR + server fns/routes) + Drizzle/D1 | Cloudflare Workers | full-stack on CF (canonical) |
| `nitro-bun` | TanStack Start + Nitro preset `bun` | `.output/server/index.mjs` self-host/Docker | own server, local `bun:sqlite` |
| `nitro-cf` | TanStack Start + Nitro preset `cloudflare-module` | wrangler deploy from `.output/` | nitro-native CF path (instead of `@cloudflare/vite-plugin`) |

Other frameworks → `/follow-create-web`; lib only → `/follow-lib-solidjs`

## Execute

### 0. Choose Variant

> Goal: pick the right Solid variant (SPA vs full-stack) before scaffolding

Choose from the Scope table — if unclear, default = `start` (full-stack) or ask the user

### 1. Setup Project (all variants)

> Goal: scaffold the project and get the dev server running

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions per `/update-devin-global-skills`, then `/deep-review-codebase` to summarize the stack
2. Scaffold: `bun create vite@latest my-app -- --template solid` (spa) or `npx @tanstack/cli@latest create --framework solid` / gitpick `TanStack/router` example `solid/start-basic` (start variants)
3. Modules: `src/modules/<feature>/` (components + hooks + schemas + types + `index.ts` barrel), shared UI `src/components/`, infra `src/lib/` — canonical file structure in `templates/`

### 2. Dependencies

> Goal: install exactly the deps the chosen variant needs

```bash
# spa (pure Router) — or use @tanstack/solid-start with spa.enabled mode (see §3)
bun i @tanstack/solid-router solid-js
bun i -D vite vite-plugin-solid typescript @tanstack/router-plugin unocss @iconify-json/mdi

# start variants (+ server)
bun i @tanstack/solid-start @tanstack/solid-router solid-js drizzle-orm
bun i -D vite vite-plugin-solid typescript nitro unocss @iconify-json/mdi drizzle-kit wrangler
bun i -D vite-tsconfig-paths         # ~/ alias from tsconfig paths
# CF deploy via the vite-plugin path → bun i -D @cloudflare/vite-plugin
```

Optional: `zod` (validator), `effect` (`/follow-lib-effect-ts`), `@orpc/*` (`/follow-lib-orpc`)

### 3. Vite Config — Per Variant

> Goal: configure Vite correctly for the chosen variant

**spa — 2 patterns** (pick one or the other):

```ts
// (a) pure Router — a true SPA, unrelated to Start
plugins: [
  tsConfigPaths(),
  tanstackRouter({ target: 'solid', autoCodeSplitting: true }),
  UnoCSS(),
  viteSolid(),
]

// (b) Start spa mode — same codebase as fullstack / prerender shell (Capacitor)
plugins: [
  tsConfigPaths(),
  tanstackStart({ spa: { enabled: true, prerender: { outputPath: '/index' } } }),
  UnoCSS(),
  viteSolid({ ssr: true }),   // required — prerender still builds an ssr bundle
]
```

**start — Cloudflare canonical (dept-saw path)** uses `@cloudflare/vite-plugin`, not nitro:
```ts
plugins: [
  tsConfigPaths(),
  cloudflare({ viteEnvironment: { name: 'ssr' } }),   // D1 binding via env
  tanstackStart(),
  UnoCSS(),
  viteSolid({ ssr: true }),
]
```

**nitro variants** — always `viteSolid({ ssr: true })` after `tanstackStart()`:
```ts
import { nitro } from 'nitro/vite'

// preset via option or env — env is safer (some nitro versions' types don't accept the option)
process.env.NITRO_PRESET ??= '<preset>'   // 'bun' | 'cloudflare-module'

plugins: [tsConfigPaths(), tanstackStart(), nitro(), UnoCSS(), viteSolid({ ssr: true })]
```

| Variant | engine | preset | main config |
|---|---|---|---|
| start | `@cloudflare/vite-plugin` | — | `vite.config.ts` |
| nitro-bun | `nitro()` | `bun` | `vite.config.bun.ts` |
| nitro-cf | `nitro()` | `cloudflare-module` | `vite.config.ts` |

Multiple targets in one repo → split `vite.config.*.ts` (pattern in dept-saw: `build` CF + `build:bun` nitro + `build:spa` capacitor)

### 4. TypeScript

> Goal: set strict TS config that matches the variant

`jsx: "preserve"` + `jsxImportSource: "solid-js"`, `moduleResolution: "Bundler"`, `target: "ES2022"`, `skipLibCheck: true`; `paths: {"~/*": ["./src/*"]}` + `vite-tsconfig-paths` for the `~/` alias; full-stack avoids `verbatimModuleSyntax` (server leaks into client); CF → `wrangler types` → `worker-configuration.d.ts`

### 4.5 Quality Scripts

Set up `check`/`verify`/`ci` + `scan` (ast-grep rules) per `/follow-tasks` Minimal — lint/format via biome (`biome.json` config overrides only, per `/follow-default-config`), test via `bun test` (bun-native) or `vitest`

### 5. Router (all variants)

> Goal: wire file-based routing with typed routes

1. `createFileRoute`/`createRootRoute` file-based — `routeTree.gen.ts` is generated, never edit
2. `defaultPreload: 'intent'` + `scrollRestoration: true` + `validateSearch`
3. `import 'virtual:uno.css'` in `__root.tsx`/entry — **never `@import` in css** (postcss resolves it as a file → ENOENT)

### 6. Full-Stack Only (start/nitro-*)

> Goal: add server functions and SSR wiring when the variant is full-stack

1. **Server fns**: `createServerFn({ method })` + `.validator()` + `.handler()` — internal RPC; the client calls it like a local fn then `router.invalidate()`
2. **Server routes**: `src/routes/api/*.ts` `server.handlers` — for webhooks/external only; wildcard `api.$.ts`
3. **Server-only**: `.server.ts` / `serverOnly()` guard — never import DB/secrets into the client bundle
4. **Drizzle**: `src/lib/schema.ts` = source of truth; `drizzle.config.ts` + `migrations/` per `/follow-lib-drizzle`
5. **DB adapter** per target:
   - CF → `drizzle(env.DB)` with `drizzle-orm/d1`; bindings in `wrangler.jsonc` → `d1_databases`
   - nitro-bun → `bun:sqlite` via `sqlite-proxy`; auto-migrate/seed at startup if the DB is empty
   - runtime-detect adapter → see `dept-saw/src/lib/db.server.ts`

### 7. Build And Deploy — Per Variant

> Goal: produce a passing production build and deploy to the variant's target

**spa**: `bun run build` → static `dist/` (embeddable in Tauri/Capacitor — `vite.config.spa.ts` + `spa.prerender` per dept-saw)

**start (CF canonical)**: `bun run build` → `wrangler deploy`; bindings declared in `wrangler.jsonc` only; secrets via `wrangler secret put`; rollback via `wrangler rollback`

**nitro-bun**: `bun run build` → `.output/`; run `bun .output/server/index.mjs` (port from `PORT`/`NITRO_PORT`); Docker `FROM oven/bun` + `COPY .output`; the sqlite file is a runtime artifact, don't commit it

**nitro-cf**: `bun run build` → `wrangler.jsonc` pointing `"main": ".output/server/index.mjs"` + `"assets": {"directory": ".output/public"}` + `compatibility_flags: ["nodejs_compat"]` → `wrangler deploy` — ref https://nitro.build/deploy/providers/cloudflare

## Rules

- **spa**: client-only — no `createServerFn`/`.server.ts`/server imports
- **start variants**: `.validator()` on every server fn that takes input; server routes for external HTTP only; never inline server code in components
- Nitro preset via the `NITRO_PRESET` env or `nitro({ preset })` — env is safer (some nitro versions' types don't accept the option); see all presets in `/follow-lib-nitro`
- CF bindings declared in `wrangler.jsonc` only — code reads them via typed `env.*`
- Never combine `@cloudflare/vite-plugin` with the nitro-cf path in one config — pick one route (`start` = vite-plugin, `nitro-cf` = nitro)
- Never edit `routeTree.gen.ts`; import `virtual:uno.css` from the JS entry only
- Shared leaves (`utils/`/`types/`) must be isomorphic-safe on start — no `node:*`/`bun:*` (move to `server/utils/`)
- Performance: `defaultPreload: 'intent'`, lazy routes + `Suspense`, `manualChunks` vendor split
- Use /deep-test component to verify component render/states
- UI markup: semantic HTML, native widgets (`<dialog>`, popover, native form validation), standard Web APIs over libraries — per `/follow-web-standard`

## Expected Outcome

- The chosen variant runs `bun run dev` and builds through its own target
- Type-safe routes + (full-stack) server fns/routes + Drizzle all working
- Deploy succeeds per target — static / Worker / portable bun server

## Templates

- `templates/file-structure-web-solid-spa.md` — SPA flat-layered structure
- `templates/file-structure-web-solid-start.md` — Start full-stack structure (isomorphic, `server/fns`, `infra/` server-only)
