---
name: nextjs-app-router
description: "Build, debug, and deploy Next.js 14+ App Router applications. Covers SSG pitfalls, Link+event handler patterns, static generation timeouts, and production-readiness gaps."
version: 1.1.0
---

# Next.js App Router — Development Patterns

Use this skill when building, debugging, or deploying a Next.js 14+ App Router application. Covers the common footguns that break builds and how to fix them.

## Trigger Conditions

- User is working on a Next.js 14+ project with App Router
- Build is failing during static generation (SSG)
- User asks about error boundaries, loading states, 404 pages, or API error handling in Next.js
- Pre-deploy production-readiness audit

---

## P0 Pitfall: `<Link>` + Event Handlers Break Static Generation

**Symptom:** `next build` fails with:
```
Error: Event handlers cannot be passed to Client Component props.
  {href: "/some-path", ..., onMouseEnter: function onMouseEnter, onMouseLeave: ..., children: ...}
```

**Root cause:** Next.js 14 tries to serialize event handlers during static page generation (SSG). `<Link>` from `next/link` is a special component — it bridges server and client, and event handlers on it CANNOT be serialized for static generation.

**This fails even if the parent component has `'use client'`** — Next.js still pre-renders the static HTML shell and chokes on the event handlers.

### Fix Pattern

Convert `onMouseEnter`/`onMouseLeave` on `<Link>` to Tailwind `hover:` CSS utility classes. The pattern is always the same:

**Before (broken):**
```tsx
<Link
  href="/target"
  className="px-4 py-2 rounded-xl transition-all"
  style={{ backgroundColor: '#001B3D', color: 'white' }}
  onMouseEnter={e => {
    e.currentTarget.style.backgroundColor = '#002856'
    e.currentTarget.style.transform = 'translateY(-2px)'
  }}
  onMouseLeave={e => {
    e.currentTarget.style.backgroundColor = '#001B3D'
    e.currentTarget.style.transform = 'translateY(0)'
  }}
>
  Click Me
</Link>
```

**After (fixed):**
```tsx
<Link
  href="/target"
  className="px-4 py-2 rounded-xl transition-all bg-[#001B3D] text-white hover:bg-[#002856] hover:-translate-y-0.5"
>
  Click Me
</Link>
```

Key conversions:
- `style={{ backgroundColor: 'X' }}` → `bg-[X]` Tailwind class
- `style={{ color: 'X' }}` → `text-[X]` Tailwind class
- `onMouseEnter` backgroundColor change → `hover:bg-[color]`
- `onMouseEnter` transform → `hover:-translate-y-0.5` or `hover:-translate-y-px`
- `onMouseEnter` boxShadow → `hover:shadow-lg` or `hover:shadow-md`
- `style={{ border: '...' }}` → `border border-slate-200` Tailwind classes
- `onMouseEnter` borderColor → `hover:border-[color]`

### Detection

The `search_files` tool from `hermes_tools` may silently miss these patterns. Use `grep` directly if `search_files` returns zero results but the build still fails:

```bash
grep -rn 'onMouseEnter\|onMouseLeave' src/ --include='*.tsx'
```

To verify only `<Link>` instances (not `<button>`, `<a>`, `<div>`):

```bash
for f in $(grep -rl 'onMouseEnter\|onMouseLeave' src/ --include='*.tsx'); do
  grep -n 'onMouseEnter\|onMouseLeave' "$f" | while read line; do
    linenum=$(echo "$line" | cut -d: -f1)
    prev=$((linenum - 5)); [ $prev -lt 1 ] && prev=1
    sed -n "${prev},${linenum}p" "$f" | grep -q '<Link' && echo "$f:$line"
  done
done
```

**Event handlers on `<button>`, `<a>`, and `<div>` are FINE** — they do NOT cause the build error. Only fix `<Link>` from `next/link`.

### Scale Note

In a real codebase, this can be 40-50+ instances across 15+ files. Fix the shared components first (`Navigation`, `Footer`, `Hero`) since those appear on every page, then work through page-specific files. Always rebuild after fixing shared components to confirm the count is going down.

---

## P1: `useSearchParams()` Must Be Wrapped in Suspense

**Symptom:** `next build` fails with:
```
⨯ useSearchParams() should be wrapped in a suspense boundary at page "/signup".
```

**Root cause:** Next.js 15 tries to statically pre-render pages at build time. `useSearchParams()` reads from the URL at runtime — it has no value during SSG. Next.js requires any component using it to be wrapped in `<Suspense>`.

**Fix pattern — extract the form into a child component and wrap it in Suspense:**

```tsx
// BEFORE (broken):
"use client";
import { useSearchParams } from "next/navigation";

export default function SignupPage() {
  const params = useSearchParams();  // 💥 breaks SSG
  return <form>...</form>;
}

// AFTER (fixed):
"use client";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";

function SignupForm() {
  const params = useSearchParams();  // safe — inside Suspense
  return <form>...</form>;
}

export default function SignupPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SignupForm />
    </Suspense>
  );
}
```

**Detection:**
```bash
grep -r "useSearchParams" src/app/ --include="*.tsx"
# Check each file for a wrapping <Suspense>
```

This also affects any page with `searchParams` in a server component that passes them to a client component — the client component must be Suspense-wrapped.

---

## P2: Static Generation Timeout

**Symptom:** `Static page generation for /some-page is still timing out after 3 attempts`

**Causes:**
- Too many static pages (e.g., 304 pages with city data)
- Slow data fetching during `generateStaticParams`
- Cold starts on large pre-rendered pages

**Fixes (in order of preference):**

1. **Increase timeout** in `next.config.js`:
```js
staticPageGenerationTimeout: 300,
```

2. **Reduce pre-rendered pages** in `generateStaticParams`:
```ts
// Before: all cities
return cities.map(c => ({ id: state.id, cityId: c.id }))

// After: top 30 per state
return cities.slice(0, 30).map(c => ({ id: state.id, cityId: c.id }))
```

3. **Force dynamic for slow pages** (if SSG isn't critical):
```ts
export const dynamic = 'force-dynamic'
```

---

## P3: PostCSS Config Must Use CommonJS `module.exports`

**Symptom:** `next build` fails with:
```
Error: Your custom PostCSS configuration must export a `plugins` key.
```

**Root cause:** Next.js 15.5+ requires the PostCSS config to use CommonJS format (`module.exports`) with an explicit `plugins` key. ESM `export default` format is not supported for PostCSS config at build time.

**Fix — use CommonJS format only:**
```js
// postcss.config.js — CORRECT (CommonJS)
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

// postcss.config.js — WRONG (ESM, will fail)
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**Also:** Delete any `postcss.config.mjs` if it exists — it can shadow the `.js` config and reintroduce the ESM error.

---

## P4: Async Params in Next.js 15.5+

**Symptom:** `next build` fails with:
```
Type error: Type '{ params: { id: string; } }' does not satisfy the constraint 'PageProps'.
  Types of property 'params' are incompatible.
    Type '{ id: string; }' is missing the following properties from type 'Promise<any>': then, catch, finally, [Symbol.toStringTag]
```

**Root cause:** In Next.js 15.5+, the `params` prop passed to page components is a `Promise` that must be awaited. This affects all dynamic route pages (`[id]`, `[slug]`, etc.) including nested catch-all routes.

**Fix — make the page `async` and `await` the params:**

```tsx
// BEFORE (broken in Next.js 15.5+):
export default function Page({ params }: { params: { id: string } }) {
  const item = findItem(params.id)  // 💥 params is a Promise, not an object
  return <div>{item.name}</div>
}

// AFTER (fixed):
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params  // ✅ await the Promise
  const item = findItem(id)
  return <div>{item.name}</div>
}
```

**For nested routes** (`[id]/cities/[cityId]`):
```tsx
export default async function CityPage({ params }: { params: Promise<{ id: string; cityId: string }> }) {
  const { id, cityId } = await params
  // ...
}
```

**Detection:** Every dynamic route file (`[*.tsx`) needs the `async` + `await params` pattern. The TypeScript compiler catches all instances, so one build cycle reveals every affected file.

---

## P5: tailwind.config.ts → tailwind.config.js

**Symptom:** Intermittent or hard-to-diagnose issues during build — sometimes PostCSS-related, sometimes font-loader-related.

**Fix:** Prefer `tailwind.config.js` (CommonJS) over `tailwind.config.ts` (TypeScript). The TypeScript config can cause edge cases with Next.js's build pipeline, especially when combined with `next/font`.

```bash
mv tailwind.config.ts tailwind.config.js
```

The content is identical — just the extension changes.

---

## P6: Importing Pipeline-Generated JSON into Pages

When a data pipeline outputs JSON to `src/data/`, Next.js supports importing it directly in server components. No API routes or `fetch()` needed.

```tsx
// src/app/(app)/elections/page.tsx
import fecData from '@/data/elections/fec_candidates.json'
import cityGovData from '@/data/generated/city_government_structures.json'

// Use directly — TypeScript infers types from the JSON shape
const candidates = fecData.candidates || []
const senateCands = candidates.filter((c: any) => c.office === 'Senate')

// For filtering by dynamic params:
const stateFed = (fecData as any).by_state?.[stateAbbreviation] || { senate: [], house: [] }
```

**Key rules:**
- JSON files must be inside `src/` (bundled by webpack) or `public/` (served as static)
- TypeScript `resolveJsonModule` must be enabled in `tsconfig.json` (it is by default in Next.js)
- Large JSON files (50KB+) are fine — they get tree-shaken at build time
- This only works for server components; client components need `fetch()` or props

## Production Readiness Checklist

When hardening a Next.js app for launch, verify these BEFORE trying to build:

| # | Item | Status |
|---|---|---|
| 1 | Error boundaries on all route pages | `error.tsx` + `ErrorBoundary` component |
| 2 | Loading skeletons for API-dependent pages | `loading.tsx` per route |
| 3 | Custom 404 page | `not-found.tsx` |
| 4 | API route try/catch error handling | Every route returns proper error responses |
| 5 | Environment variable validation | Check at startup, warn on missing keys |
| 6 | No `<Link>` + event handlers | All converted to Tailwind `hover:` classes |

### Boilerplate Files

**`src/app/error.tsx`** (Next.js global error boundary):
```tsx
'use client'
export default function GlobalError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <html><body>
      <main className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1>Something went wrong</h1>
          <p>{error.message}</p>
          <button onClick={reset}>Try Again</button>
        </div>
      </main>
    </body></html>
  )
}
```

**`src/app/not-found.tsx`** — Should include Navigation, Footer, branded design, search CTA, and link back to home.

**`src/app/[route]/loading.tsx`** — Use `animate-pulse` with placeholder divs matching the page layout shape.

**`src/lib/env.ts`** — Validate required env vars, log warnings in development, expose `getEnvWarningMessage()` for user-facing errors.

---

## References

- `references/link-event-handler-pitfall.md` — Full reproduction recipe and fix walkthrough from the Civic Pie build session
