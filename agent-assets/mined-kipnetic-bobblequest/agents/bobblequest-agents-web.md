# apps/web — Agent Scope File

Routed here by the Scope Routing Table when work touches `apps/web/**`. Read this before acting.
Do not repeat root AGENTS.md rules.

## What this is

Primary authenticated product UI. Next.js 15 + Turbopack, React 19, App Router in RSC-first mode.
Auth is owned entirely by Clerk (`@clerk/nextjs`): `clerkMiddleware()` runs on every request,
`<ClerkProvider>` wraps the root layout, and Clerk JWTs are forwarded to `apps/api` via tRPC
`httpBatchLink`. No backend of its own — all data flows through `AppRouter` from `@t/api`.

## Tech Stack

| Package | Version |
| --- | --- |
| `next` / `react` / `react-dom` | `^15.0.0` / `^19.0.0` / `^19.0.0` |
| `@clerk/nextjs` | `^7.2.3` |
| `@trpc/client` + `@trpc/react-query` | `^11.0.0` |
| `@tanstack/react-query` | `^5.59.0` |
| `tailwindcss` + `@tailwindcss/postcss` | `^4.0.0` (CSS-first, no `tailwind.config.*`) |
| `posthog-js` | `^1.372.3` |
| Linter / test runner | Biome + Vitest (unit) + Playwright (e2e) |

## Entry Points

```text
src/
  middleware.ts               clerkMiddleware() + createRouteMatcher (every request)
  app/
    layout.tsx                RSC root — <ClerkProvider> + <TrpcProvider>; analytics boot
    page.tsx                  RSC home, public
    globals.css               Tailwind v4 entry — @import "tailwindcss"
    dashboard/page.tsx        RSC — auth() + redirectToSignIn() guard
    sign-in/[[...sign-in]]/   Clerk <SignIn /> catch-all
    sign-up/[[...sign-up]]/   Clerk <SignUp /> catch-all
    providers/                client-boundary provider tree
  lib/
    trpc/client.ts            createTRPCReact<AppRouter>()
    trpc/provider.tsx         'use client' — QueryClient + httpBatchLink + Clerk Bearer
    composition.ts            'server-only' DI: config → logger → analytics
    utils.ts                  cn() (clsx + tailwind-merge)
```

## Run / Test / Build Commands

| Task | Command |
| --- | --- |
| Dev (port 3000) | `bun run --filter ./apps/web dev` |
| Build / Start | `bun run --filter ./apps/web build` / `start` |
| Unit tests | `bun run --filter ./apps/web test` (Vitest) |
| Unit coverage | `bun run --filter ./apps/web test:coverage` |
| E2E | `bun run --filter ./apps/web test:e2e` (Playwright, needs dev server) |
| Lint check | `bun run --filter ./apps/web check` (Biome) |
| Typecheck | `bun run --filter ./apps/web typecheck` |

Playwright `baseURL` and `webServer` both target `:3000`.

## App-Specific Conventions

- **RSC-first.** Default to Server Components. Add `'use client'` only at the narrowest boundary.
- **Clerk owns auth.** RSC: `auth()` / `currentUser()` from `@clerk/nextjs/server`. Client:
  `useAuth()` / `useUser()` from `@clerk/nextjs`. Never roll custom session handling.
- **Middleware guards routes.** Declare protected paths in `middleware.ts` via `createRouteMatcher`
  + `auth().protect()` — not inside the page.
- **tRPC for all API calls.** Wire through `src/lib/trpc/client.ts`; `TrpcProvider` injects
  `Authorization: Bearer <token>` via Clerk's `getToken()`. No `transformer` — `@t/api` has none.
- **Tailwind v4 CSS-first.** Tokens live in `globals.css` under `@theme { ... }`. No hardcoded
  values; use CSS variables.
- **shadcn/ui.** New primitives → `src/components/ui/`. Scaffold with
  `bunx --bun shadcn@latest add <component>` (never pnpm/npx).
- **Server-only DI.** `src/lib/composition.ts` is `server-only`. Never import from client components.
- **Env hard-fails.** `@t/config` throws at boot for missing required vars. Fix `.env.local`,
  never add `?? 'fallback'` patches.

## Required Env Vars

- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` / `CLERK_SECRET_KEY` — Clerk keys (browser / server)
- `NEXT_PUBLIC_CLERK_SIGN_IN_URL` / `NEXT_PUBLIC_CLERK_SIGN_UP_URL` — `/sign-in`, `/sign-up`
- `NEXT_PUBLIC_TRPC_URL` — `http://localhost:3000/trpc` in dev
- `NEXT_PUBLIC_POSTHOG_KEY` — `phc_*` key; schema hard-fails if missing
- `NEXT_PUBLIC_POSTHOG_HOST` — PostHog ingest URL
- `NEXT_PUBLIC_REVENUECAT_PUBLIC_API_KEY` — optional; empty = NoOp billing tracker

## Banned in This Scope

- `useEffect` + `fetch` / tRPC calls — use RSC fetch or `trpc.<proc>.useQuery()` / `useMutation()`.
- `localStorage` / `sessionStorage` for auth — Clerk owns it.
- `any`, `@ts-ignore`, `eslint-disable`.
- `axios` — use native `fetch`.
- Direct `@t/db` imports — all data goes through tRPC.
- `transformer` on tRPC links — `@t/api` server has none.
- `--no-verify` / `LEFTHOOK_EXCLUDE` — fix the hook failure.

## Links

- Architecture: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\apps\web.md
- Rules: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\.agents\rules\
- API scope: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\AGENTS.md
