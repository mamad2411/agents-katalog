# AGENTS.md -- Template Repository

<!-- OPENWIKI START -->
When the `openwiki/` directory exists, read it first for repository structure,
domain context, and implementation notes before making code or documentation
changes.
<!-- OPENWIKI END -->

## Issue tracker and triage labels

Issues and PRDs for this repo live in GitHub Issues for `Kipnetic/bobblequest`. Use the `gh` CLI for issue operations.

Use the current four-label mapping: `needs-triage`, `needs-info`, `human-required`, and `wontfix`.

When creating GitHub issues, ask or infer whether the user wants the issue held for human handling. Add `human-required` when a human must handle, approve, or decide the work. Omit `human-required` when Hermes/Kanban may intake and dispatch the issue automatically.

Do not create, apply, or require any legacy agent-ready or ready-for-agent opt-in label; that path is retired.


Production-ready monorepo template. See README.md for the quick-start guide.

## Scope Routing — READ THIS FIRST

Every agent spawns at the repo root, so this file is the only AGENTS.md guaranteed to load on every
turn. Per-scope `AGENTS.md` files MUST be read BEFORE the first edit into their subtree — they carry
the rules that actually govern that package or app. Path-scoped rules in `.agents/rules/` load
lazily by glob when matching files are touched. `docs/architecture/**` is reference depth — follow
links from per-scope `AGENTS.md` rather than reading it preemptively.

| If your task touches…                           | Read BEFORE first edit                  |
| ----------------------------------------------- | --------------------------------------- |
| apps/api/**                                     | apps/api/AGENTS.md                      |
| apps/web/**                                     | apps/web/AGENTS.md                      |
| apps/website/**                                 | apps/website/AGENTS.md                  |
| apps/mobile/**                                  | apps/mobile/AGENTS.md                   |
| apps/desktop/**                                 | apps/desktop/AGENTS.md                  |
| packages/analytics/**                           | packages/analytics/AGENTS.md            |
| packages/analytics-browser/**                   | packages/analytics-browser/AGENTS.md    |
| packages/analytics-rn/**                        | packages/analytics-rn/AGENTS.md         |
| packages/analytics-types/**                     | packages/analytics-types/AGENTS.md      |
| packages/billing/**                             | packages/billing/AGENTS.md              |
| packages/billing-browser/**                     | packages/billing-browser/AGENTS.md      |
| packages/logging/**                             | packages/logging/AGENTS.md              |
| packages/logging-browser/**                     | packages/logging-browser/AGENTS.md      |
| packages/logging-rn/**                          | packages/logging-rn/AGENTS.md           |
| packages/db/**                                  | packages/db/AGENTS.md                   |
| packages/cache/**                               | packages/cache/AGENTS.md                |
| packages/queue/**                               | packages/queue/AGENTS.md                |
| packages/auth/**                                | packages/auth/AGENTS.md                 |
| packages/config/**                              | packages/config/AGENTS.md               |
| packages/errors/**                              | packages/errors/AGENTS.md               |
| packages/dependency-injection/**                | packages/dependency-injection/AGENTS.md |
| scripts/**                                      | scripts/AGENTS.md                       |
| Cross-cutting / unsure / first-time orientation | docs/agents/landing.md                  |

## Stack

- **Runtime**: Bun (package manager, bundler, test runner)
- **Language**: TypeScript everywhere (strict mode)
- **API**: tRPC (internal, e2e type-safe) + Hono (HTTP server)
- **Database**: Postgres via Drizzle ORM (type-safe queries + migrations)
- **Auth**: Clerk (JWTs, session cookies) — `@clerk/nextjs` for web, `@clerk/clerk-expo` +
  SecureStore for mobile, Clerk JWT + electron-store for desktop
- **Web**: Next.js 15 (App Router, RSC) — port 3001
- **Website**: Next.js 15 (App Router, marketing, blog/MDX) — port 3002
- **Mobile**: React Native + Expo SDK 54 + NativeWind v4 + Tailwind v3 (inline)
- **Desktop**: Electron 32 + electron-vite + typed IPC via contextBridge
- **Styling**: Tailwind CSS v4 (web/website/desktop) + NativeWind v4 + Tailwind v3 (mobile, inline)
- **State**: Zustand (client) + TanStack Query (server, via tRPC)
- **Validation**: Zod (everywhere, pairs with tRPC)
- **Linting**: Biome (replaces ESLint + Prettier)
- **Testing**: Bun test (unit) + Playwright (E2E)
- **Hosting**: Railway

## Conventions

- Import shared packages from `@t/*` (config, db, api)
- Every tRPC procedure gets a Zod input schema
- All mutations use protected procedures (auth required)
- DB access only through `@t/db` Drizzle client — never raw SQL in app code (use Drizzle's `sql` tag
  if you truly need it)
- Server components by default in Next.js — `'use client'` only when needed
- Use Expo modules in mobile, not bare React Native APIs
- Mobile uses inline Tailwind v3 config (NativeWind v4) — do NOT extend
  `packages/config/tailwind.config.ts`
- tRPC v11: server has NO transformer; clients must NOT set `transformer` either
- Auth headers injected manually in mobile/desktop via Clerk session tokens (`getToken()`); web uses
  Clerk middleware + `auth()` on the server
- Platform SDK modules (AI, billing, notifications) live in `@nutraforgetechnologies/platform` — see
  README for TODO markers at integration sites

## Banned

- `axios` — use native `fetch`
- `lodash` — use native JS methods
- `moment` / `dayjs` — use `Intl` or `date-fns` if needed
- `express` — use Hono
- Prisma / TypeORM / Supabase JS client — use Drizzle ORM
- ESLint / Prettier — use Biome
- `any` type, `@ts-ignore`, `eslint-disable`
- NativeWind v5 (pre-release as of 2026-04; use v4)

## Commands

| Command | Description |
| --- | --- |
| `bun install` | Install all workspace dependencies |
| `bun run dev` | One-command full stack (Docker + migrations + all apps + auto-open) — see README "Quick start" for flags |
| `bun run dev:packages` | Turbo-only dev (no Docker, no auto-open) — package iteration |
| `bun run build` | Build all apps |
| `bun run check` | Biome lint check (turbo run check) |
| `bun run format` | Biome auto-format |
| `bun run typecheck` | TypeScript strict check (turbo run typecheck) |

## Structure

```text
apps/
├── api/          # tRPC + Hono API server — exposes AppRouter type via @t/api
├── web/          # Next.js 15 web app — Clerk auth (@clerk/nextjs), tRPC client
├── website/      # Next.js 15 marketing site — landing, blog/MDX, no auth
├── mobile/       # Expo SDK 54 + NativeWind — Clerk (@clerk/clerk-expo) + SecureStore, tRPC client
└── desktop/      # Electron + electron-vite — Clerk JWT + electron-store, tRPC client

packages/
├── config/       # Shared tsconfig base, Biome, Tailwind v3 (mobile use-case only)
└── db/           # Drizzle ORM client, schema, migrations, Zod schemas

Platform SDK (external): @nutraforgetechnologies/ai | billing | notifications
→ each app has TODO markers at AI/billing/notifications integration points
```

## Core Directives

1. **Interrogate intent before building.** Confirm purpose, audience, what it must NOT contain.
2. **Ask via structured options only.** 2–4 concrete options, recommendation first, rationale. Zero
   inline questions.
3. **Skills before action.** Load matching skills before the first substantive tool call.
4. **Subagents do the work.** Main context plans and synthesizes. 3+ files, heavy skill use, or
   self-contained tasks → subagent with structured returns.
5. **Todos for 2+ steps.** Create at task start; update in-flight.
6. **Research before action.** Versions, flags, schemas first. On errors: stop → diagnose → research
   → fix once. No trial-and-error.
7. **No speculative work.** Don't pre-launch agents for unconfirmed directions.

## Filesystem precedence

Global `~/.claude/CLAUDE.md` Section 0 defines the canonical precedence: `graphify` first, `rtk`
fallback, Read/Grep/Glob/Bash only as last resort. Always defer to that section; it is the single
source of truth for filesystem access ordering across all sessions.

## Definition of Done

A task is complete when ALL pass:

1. `bun run check` exits 0
2. `bun run typecheck` exits 0
3. `bun test` exits 0 with no failures
4. Changed files committed with conventional format (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`,
   `chore:`)

## Quality Gates

- No `any`, `@ts-ignore`, `eslint-disable`, or type casts to silence errors (strictly enforced by
  Biome/TypeScript).
- Every function handles its errors. No empty catches, no swallowed errors.
- Never expose secrets, credentials, API keys, or tokens in code, commits, or logs.

## TDD (Test-Driven Development)

Preferred for new features, bug fixes, and refactors.

- **Red** — Write failing tests that define success criteria as executable assertions.
- **Green** — Minimum implementation to pass.
- **Refactor** — Clean up with green tests as safety net.

*Test-after is acceptable for wiring, config, and integration code where TDD adds friction.*

## Communication Preferences

- **Completion reports:** what was done, what was tested, what to verify.
- **Structured options with recommendation:** never open-ended questions.
- **ASCII art for status/architecture:** use box-drawing chars, arrows, progress bars when
  communicating project state, multi-phase plans, or architecture diagrams.
- **Progress updates at natural breakpoints:** every 3–5 tasks or milestone.
- **Recover without drama:** no apologies, fix and move on.
- **Out-of-scope issues → findings:** not acted on without approval.

## Project Status

Before planning bootstrap work, read [docs/prd-status/overview.md](./docs/prd-status/overview.md) —
the live status diagram is the single source of truth.
