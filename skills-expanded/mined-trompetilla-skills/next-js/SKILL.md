---
name: Next.js
description: Avoid common Next.js mistakes — server/client boundaries, caching gotchas, and App Router pitfalls.
metadata: {"clawdbot":{"emoji":"▲","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## Server vs Client Components
- Default is Server Component in App Router — no useState, useEffect, browser APIs
- `'use client'` at top of file for client — marks component and descendants as client
- Can't import Server Component into Client — only pass as children or props
- Client components can't be async — only Server Components can await directly

## Caching Gotchas
- `fetch` cached by default in Server Components — add `cache: 'no-store'` for dynamic
- `revalidate` in seconds — `next: { revalidate: 60 }` for ISR
- Route Handlers not cached by default — except `GET` with no dynamic data
- `revalidatePath('/path')` or `revalidateTag('tag')` for on-demand — in Server Actions

## Data Fetching
- Fetch in Server Components, not useEffect — no waterfalls, better performance
- Parallel fetches with `Promise.all` — not sequential awaits
- `loading.tsx` for Suspense boundary — automatic streaming
- Error boundaries with `error.tsx` — catches errors in segment

## Environment Variables
- `NEXT_PUBLIC_` prefix for client-side — otherwise only available on server
- Server Components access all env vars — no prefix needed
- `.env.local` for secrets — `.env` checked into repo, `.env.local` gitignored
- Runtime env with `process.env` — build-time with `env` in next.config.js

## Route Handlers (API Routes)
- `route.ts` in App Router — `pages/api` is Pages Router
- Export named functions: `GET`, `POST`, etc. — not default export
- `NextRequest` and `NextResponse` — typed request/response
- Dynamic by default — `export const dynamic = 'force-static'` to cache

## Server Actions
- `'use server'` at top of function or file — marks as server action
- Can be called from Client Components — automatic RPC
- Form `action={serverAction}` — progressive enhancement, works without JS
- Revalidate cache after mutation — `revalidatePath` or `revalidateTag`

## Middleware
- Runs on Edge, not Node — limited APIs, no fs, limited npm packages
- `matcher` config to limit routes — don't run on static assets
- Can't throw errors — return redirect or next()
- Cookies and headers access — but can't call database directly

## Dynamic Routes
- `[slug]` folder name for params — `page.tsx` receives `params.slug`
- `[...slug]` for catch-all — array of segments
- `generateStaticParams` for SSG — return array of param objects
- `dynamicParams = false` to 404 unknown — otherwise renders on demand

## Common Mistakes
- Using `router.push` in Server Component — only works in Client, use `redirect()`
- `<Link>` prefetches in viewport — can cause excessive requests, `prefetch={false}` to disable
- `next/image` without width/height — required unless `fill` prop with positioned parent
- Metadata in Client Component — `generateMetadata` only in Server Components
- `cookies()` makes route dynamic — can't be statically generated
