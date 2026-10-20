# Copilot instructions — Retro Board

Next.js **16.2.4** / React **19.2.4** / TypeScript (strict) / Tailwind **v4** app. A team
retrospective board (columns, cards, votes, discussion mode) persisted to **Azure Cosmos DB**,
authenticated with **Microsoft Entra ID** via NextAuth v5. Package manager is **bun**
(`bun.lock`); `npm` also works.

## ⚠️ This is NOT the Next.js you know

Next.js 16 has breaking changes vs. model training data (async `params`, server/client
boundaries, fetch caching, routing conventions). **Before writing any code that touches a
Next.js API, read the relevant guide in `node_modules/next/dist/docs/`.** Heed deprecation
notices. Note `params` is a `Promise` and must be awaited (see `app/boards/[id]/page.tsx`).

## Commands

- `bun run dev` — dev server (http://localhost:3000)
- `bun run build` — production build **and** the primary typecheck signal. Run this before
  considering any change done; there is no separate test suite.
- `bun run lint` — ESLint (`eslint-config-next` core-web-vitals + typescript)
- `bun run seed` — seed Cosmos with demo boards (`tsx --env-file=.env.local scripts/seed-cosmos.ts`)
- Deploy: `.\infra\deploy.ps1 -NameSuffix jryu -SkipInfra` (app-only). See the `deploy` skill
  in `.agents/skills/deploy/SKILL.md` — always `-WhatIf` first for infra changes.

There is no unit test runner. "Run a single test" does not apply; validate with `bun run build`
and manual golden-path testing in the dev server.

## Architecture — the big picture

**Client store is the source of truth for the UI; Cosmos is the system of record.**

- `app/_data/store.ts` — a module-level pub/sub store (not React state, not Redux/Zustand)
  consumed via `useSyncExternalStore`. Mutations go through `storeActions.*`, which update
  in-memory state optimistically, then **debounced-PUT** the whole board to
  `/api/boards/[id]`. Hooks `useStore`, `useBoard`, `useBoardPolling`, `useBoardsListPolling`
  are the read/subscribe surface. Do not add a state library without raising it first.
- **Concurrency = Cosmos ETags.** Every fetch/PUT captures the board `_etag`; writes send it
  as `If-Match`. A `412` triggers refetch-then-retry-once. Preserve this pattern — it is how
  concurrent editors don't clobber each other. `lib/cosmos.ts#stripSystemFields` surfaces
  `_etag` as `etag` and strips other Cosmos internals.
- **Realtime is polling, not sockets.** The active board polls ~1.5s (ETag `304` short-circuit);
  boards list ~5s. `usePresencePolling` + `lib/presence.ts` (in-memory, TTL-pruned Map) give a
  live presence stack. Presence is touched as a side effect of the board `GET` heartbeat.
- **Auth boundary:** `proxy.ts` (root) wraps every route except `/api/*` with the NextAuth
  `proxy` middleware. API route handlers do their own `await auth()` and return `401 JSON`
  themselves. User identity is the Entra `oid`, threaded onto `session.user.id` in `lib/auth.ts`.
- **Data model:** `app/_data/retro.ts` defines `Board`/`Column`/`Card`/`Voter`/`ActionItem`.
  Cosmos containers: `boards` (partitioned by `workspaceId`) and `userState`. Because board
  URLs carry only `id`, several handlers do a cross-partition `SELECT ... WHERE c.id` to resolve
  the partition key — keep that in mind before "optimising" to point-reads.

## Conventions specific to this repo

- **API route handlers** set `export const runtime = "nodejs"` and
  `export const dynamic = "force-dynamic"`, start with `await auth()` → `401`, validate body,
  and return `Response.json(...)`. Match this shape for new endpoints.
- **File layout:** `app/_components/` (UI), `app/_data/` (shapes + store), `app/_hooks/`,
  `app/_lib/` (pure utils). Server-only helpers live in top-level `lib/`. Import alias is
  `@/*` → repo root.
- **`"use client"` only where interactivity is needed.** Server components (e.g.
  `generateMetadata`, page shells) stay server-side. `RetroApp.tsx` is the main client tree.
- **Styling:** Tailwind v4 is installed but the app is styled with **CSS classes and design
  tokens in `app/globals.css`**. Add new styles there using existing tokens; don't sprinkle
  Tailwind utilities into files that use plain CSS classes.
- **TypeScript strict, no `any`** unless justified in a comment. Every prop typed.
- **Comments explain WHY, not WHAT.** The codebase leans on this heavily (see the block comments
  in `store.ts` / `cosmos.ts`); don't reference tickets or "added for X".
- **Persisted shape changes** bump `SCHEMA_VERSION` in `store.ts`.

## Product workflow (specs live in `.claude/specs/`)

Features are tracked as **F-XX** items. The pipeline is **product-owner → designer →
developer**: `backlog.md` defines scope, `design-F-XX.md` is the UI/interaction spec, then
implementation. `tech-debt.md` tracks known debt. Read the matching spec before touching a
feature area. Custom agents for these roles exist under `.claude/agents/`. The product is a
**retro board** — the kanban-like columns/cards/DnD are a *mechanic*, not a surface to build out.

> Note: `HANDOVER.md` and `.claude/agents/developer.md` predate the Cosmos/auth migration and
> describe an older in-memory/localStorage-only prototype. Trust the code in `lib/` and
> `app/_data/store.ts` over those docs for persistence behaviour.

## Deployment target

Azure App Service (Bicep in `infra/main.bicep`), Cosmos private-endpoint only, managed identity
in prod (`DefaultAzureCredential`), key auth only for the local emulator. `next.config.ts` uses
`output: "standalone"` — required for the deploy bundle. Env is read from `.env.local`
(see `.env.local.example`).
