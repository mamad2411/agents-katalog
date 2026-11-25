---
name: nextjs-route-scaffold
description: Scaffolds necessary Next.js App Router file conventions and route-level SEO metadata (page.tsx, layout.tsx, error.tsx, not-found.tsx, loading.tsx, default.tsx, global-error.tsx, metadata, generateMetadata, canonical, robots, openGraph, twitter) for a given route path. Checks existing files, reads them for context, and generates only missing files. Use when user provides a route path and wants to add missing special files or SEO metadata, or asks to "scaffold", "create files for", or "set up route files" for a Next.js App Router route.
---

# Next.js Route Scaffold

## Step 1 — Analyze the route and project

**1a. Resolve the path**
- Check if the given path exists in the project
- If not found, ask the user to confirm the correct path
- Handle both `app/` and `src/app/` structures automatically

**1b. Scan existing files at the path**
- List all files already present in the directory
- Read existing files (especially `page.tsx`) to understand:
  - Component structure and naming
  - Import patterns and UI library in use
  - Whether components are Server or Client Components (`'use client'` directive)
  - Styling approach (Tailwind, CSS modules, etc.)

**1c. Search for shared Skeleton/Loading components**
- Before creating `loading.tsx`, search the project for existing Skeleton or Loading components (common locations: `components/ui/`, `components/common/`, `components/shared/`)
- If found, use them in `loading.tsx`
- If not found, create a reusable Skeleton component and use it

**1d. Check Next.js version**
- Read `package.json` and extract the `next` version (e.g. `"next": "^16.2.0"`)
- Strip semver prefix (`^`, `~`) and compare major.minor: **≥ 16.2 → use `unstable_retry`; < 16.2 → use `reset`**
- Store this as `USE_UNSTABLE_RETRY` for use in Step 5

**1e. Parse route characteristics**
- **Is root layout?** (`app/layout.tsx` or `src/app/layout.tsx`) — needs `<html>` and `<body>` tags + `global-error.tsx`
- **Has dynamic segments?** (`[slug]`, `[...slug]`, `[[...slug]]`) — affects `params` type, prompt for `generateStaticParams`
- **Is parallel route slot?** (segment starts with `@`) — may need `default.tsx`
- **Is route group?** (`(group)`) — ignore for naming; URL-invisible

## Step 2 — Decide which files to create

Skip files that already exist. Create only what is missing.

| File | Create when |
|------|-------------|
| `page.tsx` | Always — makes route publicly accessible |
| `layout.tsx` | Route needs shared UI wrapping children; always for root `app/` |
| `loading.tsx` | Always — use shared Skeleton or create one |
| `error.tsx` | Always |
| `not-found.tsx` | Route has dynamic segments (`[id]`, `[slug]`, etc.) |
| `global-error.tsx` | Root `app/` only |
| `default.tsx` | Parallel route slots (`@slotName`) only — explain and confirm first |
| `template.tsx` | Only when user explicitly requests — explain and confirm first |

## Step 3 — Metadata and SEO rules

Always include metadata. Determine placement:

1. `page.tsx` does not exist → add to new `page.tsx`
2. `page.tsx` exists and is a **Server Component** → add to `page.tsx`
3. `page.tsx` exists and is a **Client Component** → add to `layout.tsx`
4. Both `page.tsx` and `layout.tsx` are Client Components → **stop and ask the user**

For public indexable pages, include the minimum SEO set that fits the route:

- `title`
- `description`
- `alternates.canonical`
- `openGraph`
- `twitter`
- `robots`

Use `metadataBase` in the root layout when the project needs absolute URLs. For routes that should not be indexed, set `robots.index = false` and `robots.follow = false`.

Keep this skill focused on route-local SEO metadata. If the user wants site-wide SEO assets such as `sitemap.ts`, `robots.ts`, or structured data conventions, use [references/seo.md](references/seo.md) for the detailed patterns.

Dynamic routes use `generateMetadata`; static routes use `metadata` constant:

```tsx
// Static route
export const metadata: Metadata = {
  title: 'Page Title',
}

// Dynamic route
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  return { title: slug }
}
```

## Step 4 — Dynamic routes: ask about generateStaticParams

For routes with dynamic segments (`[id]`, `[slug]`, etc.), ask:
> "Do you want this route statically generated (SSG)? I can add `generateStaticParams` if so."

If yes, add to `page.tsx`:

```tsx
export async function generateStaticParams() {
  return [{ slug: 'example' }]
}
```

## Step 5 — Generate each file

Use content from existing files to keep new files consistent in structure and style.

### `page.tsx`

```tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <div>{slug}</div>
}
```

- Server Component by default
- `params` and `searchParams` are `Promise<...>` — always `await`
- Omit `params` if no dynamic segments; omit `searchParams` if not needed

### `layout.tsx`

Non-root:
```tsx
export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ slug: string }>
}) {
  return <section>{children}</section>
}
```

Root (`app/layout.tsx`):
```tsx
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

- Cannot read `searchParams`
- Does NOT re-render on navigation (use `template.tsx` if re-render per navigation is needed)

### `loading.tsx`

```tsx
// Use shared Skeleton component if available; otherwise create one
export default function Loading() {
  return <SkeletonComponent />
}
```

- Server Component, no props
- Automatically wraps `page.tsx` in a `<Suspense>` boundary

### `error.tsx`

**Next.js ≥ 16.2** (use `unstable_retry` — re-fetches + re-renders):

```tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string }
  unstable_retry: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={unstable_retry}>Try again</button>
    </div>
  )
}
```

**Next.js < 16.2** (use `reset` — clears error state only, no re-fetch):

```tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

- **Must be `'use client'`**
- `error.tsx` renders **inside** the parent `layout.tsx` — surrounding layout stays intact. Keep error UI self-contained (no full-page styles).
- Does NOT catch errors thrown by `layout.tsx` in the same segment
- For root layout errors, use `global-error.tsx` instead

### `global-error.tsx` (root only)

Same version rule applies (`USE_UNSTABLE_RETRY` from Step 1d).

**Next.js ≥ 16.2:**

```tsx
'use client'

export default function GlobalError({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string }
  unstable_retry: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong</h2>
        <button onClick={unstable_retry}>Try again</button>
      </body>
    </html>
  )
}
```

**Next.js < 16.2:**

```tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong</h2>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  )
}
```

- Must include `<html>` and `<body>` — replaces the root layout when active

### `not-found.tsx`

```tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find the requested resource.</p>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

- Triggered by calling `notFound()` from `next/navigation`
- Server Component

### `default.tsx` (parallel routes only)

Explain before creating:
> "`default.tsx` is used in Parallel Routes (`@slotName`) as a fallback when Next.js cannot recover the slot's active state after a full-page load. Do you need this?"

```tsx
export default function Default() {
  return null
}
```

### `template.tsx` (on request only)

Explain before creating:
> "`template.tsx` works like `layout.tsx` but re-mounts on every navigation. Useful for per-visit animations, `useEffect` page-view tracking, or resetting state on tab switches. Do you need this?"

## Step 6 — Component hierarchy reference

```
layout.tsx
  └── error.tsx          ← error boundary
        └── loading.tsx  ← Suspense boundary
              └── not-found.tsx
                    └── page.tsx
```

`error.tsx` does NOT wrap `layout.tsx` of the same segment.

## Dynamic segment type reference

| Pattern | `params` type |
|---------|--------------|
| `[slug]` | `{ slug: string }` |
| `[id]` | `{ id: string }` |
