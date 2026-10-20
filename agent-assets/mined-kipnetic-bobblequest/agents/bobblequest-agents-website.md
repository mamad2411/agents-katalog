# apps/website — Agent Scope

Unauthenticated Next.js 15 marketing site and MDX blog. Runs on port 3002 as its own Railway
service. No auth, no tRPC, no database. All rendering is RSC or SSG; the only runtime branch is
`SITE_URL` flowing into sitemap/robots/OG metadata. A lightweight PostHog analytics layer and
server-side DI composition root (logger + config + analytics) are wired, but no app-shell auth
flows exist here — those live in `apps/web`.

## Tech Stack

| Piece | Version |
| --- | --- |
| Next.js | ^15.0.0 (App Router, RSC, Turbopack dev) |
| React | ^19.0.0 |
| Tailwind CSS | ^4.0.0 (`@tailwindcss/postcss`) |
| TypeScript | ^5.5.0 (strict) |
| Vitest | ^2.1.0 |
| Playwright | ^1.59.1 |
| Biome | ^2.4.13 |
| @next/mdx | ^15.0.0 |
| gray-matter | ^4.0.3 |
| rehype-pretty-code | ^0.14.3 |
| shiki | ^4.0.2 |
| posthog-js | ^1.372.3 |
| shadcn/ui | components.json present; primitives in `src/components/ui/` |

## Entry Points

```
src/
  app/
    layout.tsx          # RootLayout — generateMetadata (getWebsiteConfig), AppAnalyticsProvider
    page.tsx            # "/" landing (static RSC)
    globals.css         # Tailwind v4 import + CSS variable token surface
    api/health/route.ts # GET → { status:"ok" } — Railway healthcheck
    blog/page.tsx       # SSG post index
    blog/[slug]/page.tsx# SSG per-post (MDX import + gray-matter meta)
    sitemap.ts          # MetadataRoute.Sitemap — SITE_URL driven
    robots.ts           # MetadataRoute.Robots
  lib/
    composition.ts      # server-only DI root — buildContainer() / getContainer()
    config.ts           # getWebsiteConfig() — thin wrapper over @t/config
```

`composition.ts` wires `@t/config`, `@t/logging`, `@t/analytics` via `@t/dependency-injection`
`createContainer`. Use `getContainer()` for DI; use `getWebsiteConfig()` for config-only reads.

## Run / Test / Build

```bash
# from monorepo root
bun run dev                                    # full stack (Docker + all apps)
bun run --filter @t/website dev               # isolated, Turbopack, port 3002
bun run --filter @t/website build
bun run --filter @t/website typecheck
bun run --filter @t/website check             # Biome lint
bun run --filter @t/website test              # Vitest unit
bun run --filter @t/website test:e2e          # Playwright
```

## Conventions

- Server components by default — `"use client"` only for interactive islands (e.g., PostHog provider).
- All DI: go through `getContainer()` in `src/lib/composition.ts`; never instantiate infra classes directly.
- Config reads: use `getWebsiteConfig()` (`resolveWebsiteConfig(process.env)`); hard-throws if
  `SITE_URL` is missing — no silent fallbacks.
- Design tokens: Tailwind v4 CSS variables in `globals.css`; shadcn CSS variable contract; use `cn()`
  from `src/lib/utils.ts` for class merging.
- Shadcn components: installed to `src/components/ui/` via `npx shadcn@latest add <component>`.
- MDX blog: filesystem-driven collection from `src/content/blog/*.mdx`; frontmatter parsed with
  `gray-matter`; sorted by date descending; no manual slug map needed.
- Analytics: PostHog via `AppAnalyticsProvider` + `PostHogPageView` in `layout.tsx`; extend via
  `@t/analytics-browser`, not by importing `posthog-js` directly in new code.
- SSG-friendly: no `cookies()`, `headers()`, or `searchParams` in the default page tree outside of
  `layout.tsx` (which gates metadata on `connection()`).

## Banned in This Scope

- Clerk middleware (`middleware.ts`, `clerkMiddleware`, `@clerk/nextjs`) — auth is `apps/web` only.
- `auth()` / `currentUser()` from `@clerk/nextjs` — no protected routes on the marketing site.
- tRPC client or `@t/api` imports — no backend RPC calls from this app.
- `@t/db` or any Drizzle import — no direct DB access.
- `process.env.*` reads outside `src/lib/config.ts` and `src/lib/composition.ts` — all env access
  must go through `getWebsiteConfig()` or the DI container.
- `axios`, `lodash`, `moment`/`dayjs`, ESLint/Prettier — see root AGENTS.md Banned list.
- `any`, `@ts-ignore`, `eslint-disable` — strictly enforced by Biome/TypeScript.

## Links

- Architecture: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\apps\website.md
- Root AGENTS.md: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md
