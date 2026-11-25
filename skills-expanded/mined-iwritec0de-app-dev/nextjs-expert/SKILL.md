---
name: nextjs-expert
description: >-
  This skill should be used when the user asks to "build a Next.js app", "configure
  App Router routing", "implement data fetching", "create a server action",
  "optimize Next.js performance", or mentions "next.js", "app router", "server
  component", "client component", "next config", "middleware", "route handler",
  "server action", "ISR", "SSR", "SSG". Provides Next.js framework expertise for
  App Router, Server Components, data fetching, routing, middleware, and
  optimization.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Next.js Expert Skill

You are a Next.js expert specializing in the App Router architecture introduced in Next.js 13 and matured in 14+.

## Critical Rules

- **Always use App Router** — never suggest or scaffold Pages Router patterns in new code; App Router is the current model
- **Server Components by default** — components are Server Components unless they explicitly need client-side state, effects, or browser APIs
- **Add `'use client'` only when required** — event handlers, `useState`, `useEffect`, `useRef`, browser-only APIs, or third-party client libraries
- **Fetch data in Server Components** — avoid `useEffect` + `fetch` for initial data; let async Server Components do it
- **Use `next/image` for all images** — never use bare `<img>` tags; `next/image` handles lazy loading, sizing, and format optimization
- **Use `next/font` for typography** — load fonts via `next/font/google` or `next/font/local` to eliminate layout shift and self-host automatically
- **Follow file-based routing conventions** — use the correct special filenames (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`)
- **Never expose server secrets to the client** — `NEXT_PUBLIC_` prefix makes an env var available in the browser bundle; everything else is server-only

## App Router File Conventions

Each route segment is a directory. Special files control rendering and behavior:

| File | Purpose |
|------|---------|
| `page.tsx` | Renders the route UI; makes a segment publicly accessible |
| `layout.tsx` | Wraps children; persists across navigations within the segment |
| `loading.tsx` | Instant loading UI shown while the segment streams in (wraps in `<Suspense>`) |
| `error.tsx` | Error boundary for the segment; must be a Client Component |
| `not-found.tsx` | UI for `notFound()` calls or unmatched routes within the segment |
| `route.ts` | Route Handler (REST API endpoint); exports HTTP method functions |
| `middleware.ts` | Runs before requests match a route; lives at the project root |
| `template.tsx` | Like layout but re-mounts on every navigation (rare use case) |

Colocation tip: non-route files (components, utils) can live inside the `app/` directory; they
are not exposed as routes unless they are named `page.tsx` or `route.ts`.

## Data Fetching Patterns

### Server Components (preferred for initial data)

```tsx
// app/users/page.tsx — async Server Component
export default async function UsersPage() {
  // fetch() is extended by Next.js with caching options
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 60 }, // ISR: revalidate every 60s
  });
  const users = await res.json();

  return <UserList users={users} />;
}
```

No loading state management needed — use `loading.tsx` for Suspense boundaries.

### Route Handlers for API endpoints

```ts
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

### Server Actions for mutations

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  await db.user.create({ data: { name } });
  revalidatePath('/users'); // invalidate cached page
}

// In a Server Component form
<form action={createUser}>
  <input name="name" />
  <button type="submit">Create</button>
</form>
```

Server Actions run exclusively on the server. They can be called from both Server and Client Components.

## Rendering Strategies

| Strategy | How | When to use |
|----------|-----|-------------|
| **SSR** | `fetch(url)` with no cache options, or `{ cache: 'no-store' }` | User-specific data, real-time content |
| **SSG** | `generateStaticParams()` + `fetch` with default caching | Marketing pages, docs, blog posts |
| **ISR** | `fetch(url, { next: { revalidate: N } })` | Frequently updated but not real-time |
| **Client** | `'use client'` + SWR/React Query | Highly interactive, user-triggered fetches |

Default caching behavior: Next.js 14 caches `fetch()` results by default (like SSG). Opt out
per-request with `{ cache: 'no-store' }` or per-segment by exporting `export const dynamic = 'force-dynamic'`.

## Performance Optimization

- **Images:** always use `next/image` with explicit `width` and `height` (or `fill` + a sized container); set `priority` on above-the-fold images
- **Fonts:** use `next/font` — it self-hosts and injects `font-display: swap`; never load fonts via `<link>` in the `<head>`
- **Dynamic imports:** use `next/dynamic` with `{ ssr: false }` for heavy client-only components (maps, rich editors, charts)
- **Bundle analysis:** run `ANALYZE=true next build` with `@next/bundle-analyzer` to inspect bundle composition
- **Streaming:** wrap slow data-fetching components in `<Suspense>` to unblock the initial response and stream content progressively
- **Parallel data fetching:** `Promise.all()` multiple fetches in a Server Component rather than awaiting sequentially

## Security

- **Server-only modules:** use the `server-only` package to hard-fail if a server module is accidentally imported client-side
- **Environment variables:** `NEXT_PUBLIC_` prefix exposes the value in the browser bundle — use it only for non-sensitive config (API base URLs, feature flags); keep secrets unprefixed
- **Route Handler auth:** validate sessions/tokens at the top of every Route Handler; do not rely solely on middleware
- **Server Actions:** treat them like API endpoints — validate inputs, authenticate the caller; they are exposed as HTTP endpoints
- **Content Security Policy:** configure via `next.config.js` headers or middleware for XSS protection

## Anti-Patterns

- **Don't use Pages Router in new code** — `pages/` directory, `getServerSideProps`, `getStaticProps`, `getStaticPaths` are legacy; use App Router equivalents
- **Don't fetch in `useEffect` for initial page data** — this causes request waterfalls and layout shift; fetch in Server Components or loaders
- **Don't put secrets in `NEXT_PUBLIC_` variables** — they are inlined into the JS bundle at build time and visible to anyone
- **Don't make every component a Client Component** — interactivity should be pushed to the leaves of the component tree; keep parents as Server Components
- **Don't use `<img>` directly** — use `next/image` for performance and CLS prevention
- **Don't block streaming with top-level awaits when a Suspense boundary would work** — prefer `<Suspense>` + async child over awaiting at the layout level

## Related

- `reference/routing-patterns.md` — File-based routing, dynamic routes, route groups, parallel routes, intercepting routes, catch-all segments
- `reference/data-fetching.md` — Caching strategies, revalidation, Server Actions, Route Handlers, streaming with Suspense
- `reference/performance.md` — Bundle optimization, image/font, lazy loading, ISR, edge runtime, middleware patterns