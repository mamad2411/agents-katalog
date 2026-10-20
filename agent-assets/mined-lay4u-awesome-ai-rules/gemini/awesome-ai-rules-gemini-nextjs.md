# Gemini CLI Next.js Rules

## CLI-First Workflow
- Work from terminal commands with reproducible, reviewable output.
- Keep loops tight: edit -> typecheck -> test -> build.
- Prefer small commits of behavior over large refactors.

## Standard Command Set
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm next build`
- `pnpm -s exec prettier -w .` when formatting is required.
- Fall back to `npm`/`yarn`/`bun` only if the repo uses them.

## App Router Conventions
- Use App Router (`app/`) for all new routing work.
- Avoid adding new Pages Router endpoints under `pages/`.
- Use `layout.tsx`, `loading.tsx`, `error.tsx`, and `not-found.tsx` intentionally.
- Keep route handlers in `app/**/route.ts` and domain logic outside handlers.

## Server Components and Client Boundaries
- Default to Server Components for data fetching and rendering.
- Add `'use client'` only when browser APIs or interactivity require it.
- Keep client components leaf-oriented to minimize JS payload.
- Avoid non-serializable server-to-client props.

## Server Actions and React 19
- Prefer Server Actions for writes and form handling.
- Validate action inputs at the server boundary.
- Use React 19 mutation patterns (`useActionState`, `useOptimistic`) for UX.
- Revalidate cache explicitly after successful mutation paths.

## Caching, Performance, and SEO
- Choose cache strategy intentionally (`no-store`, `force-cache`, `revalidate`).
- Use `next/image` and `next/font` for production defaults.
- Add route metadata via `metadata` or `generateMetadata`.
- Use dynamic imports for heavy client-only features.

## Delivery Expectations
- Keep TypeScript strict and avoid `any` in route params/payloads.
- Add tests for route handlers, server actions, and key route states.
- Ensure commands complete cleanly before handoff.
