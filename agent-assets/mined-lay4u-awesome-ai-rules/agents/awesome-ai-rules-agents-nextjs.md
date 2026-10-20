# Codex Next.js Rules

## Mission
- Deliver production-safe Next.js 15+ features using App Router conventions.
- Execute end-to-end autonomously: edit, verify, and report concrete outcomes.

## Execution Protocol
- Before edits: inspect route structure, runtime targets, and existing scripts.
- During edits: keep diffs minimal and preserve server-first architecture.
- After edits: run verification commands and report pass/fail per command.

## Required Verification Commands
- `pnpm -s exec prettier -c .` (or project formatter equivalent)
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm next build`
- If `pnpm` is unavailable, use the repo’s package manager (`npm`/`yarn`/`bun`).

## App Router Standards
- Use `app/` only; do not add new `pages/` routes.
- Model hierarchy with nested layouts and route groups.
- Implement APIs through Route Handlers (`app/**/route.ts`).
- Keep route files thin; move domain logic into `lib/` or `server/` modules.

## Server Components and Client Boundaries
- Default to Server Components for data-heavy rendering.
- Add `'use client'` only when interactivity or browser APIs require it.
- Keep client islands small to control bundle growth.
- Do not pass non-serializable values across the server/client boundary.

## Server Actions and Data Integrity
- Prefer Server Actions for mutations and forms.
- Validate inputs at server boundaries with shared schemas.
- Use React 19 mutation patterns (`useActionState`, `useOptimistic`) when helpful.
- Revalidate caches intentionally using `revalidatePath`/`revalidateTag`.

## Runtime, Security, and Performance
- Choose runtime (`edge` vs `nodejs`) explicitly when needed.
- Avoid Node-only APIs in edge-targeted handlers.
- Use `next/image`, `next/font`, and metadata APIs for production quality.
- Keep secrets server-side and never expose privileged values to client code.

## Completion Criteria
- All required commands pass for the touched scope.
- New behavior includes tests for success and failure states.
- Changes follow App Router, RSC, and Server Action conventions.
