---
name: void-loading-error-boundaries
description: Place loading.tsx, error.tsx, not-found.tsx files at the right level — neither too high (poor UX) nor too low (unhandled errors). The skeleton matches the layout it replaces.
---

# loading-error-boundaries

Use when adding or restructuring routes in `app/`. Next.js boundary files (`loading.tsx`, `error.tsx`, `not-found.tsx`) define UX during Server Component rendering, server failures, and missing-resource cases. Placement matters: too high = whole page flashes on partial load; too low = errors leak past the intended catch.

## The 4 boundary files

| File | Wraps | Renders when |
|---|---|---|
| `loading.tsx` | Sibling `page.tsx` in a Suspense boundary | Async server work in progress |
| `error.tsx` | Sibling `page.tsx` + descendants in an Error Boundary | Server throws OR client error |
| `not-found.tsx` | Triggered by `notFound()` call | `notFound()` from a Server Component / handler |
| `global-error.tsx` | Wraps the root `app/layout.tsx` itself | Layout throws (rare) |

`error.tsx` and `global-error.tsx` MUST be Client Components (they catch React errors).

## Placement: as low as practical

Place boundary files **at the segment that owns the unique loading state**, not at the root.

```
app/
├── (app)/
│   ├── layout.tsx           # auth check, app shell
│   ├── dashboard/
│   │   ├── page.tsx
│   │   ├── loading.tsx      # skeleton of dashboard widgets
│   │   └── error.tsx        # error display in app shell context
│   └── settings/
│       ├── page.tsx
│       └── loading.tsx      # skeleton of settings form
└── (marketing)/
    ├── layout.tsx
    └── blog/
        ├── [slug]/
        │   ├── page.tsx
        │   ├── loading.tsx  # article skeleton
        │   └── error.tsx    # "couldn't load article" message
        └── page.tsx          # blog index (no skeleton — small enough)
```

Per-route boundaries mean a slow `/dashboard` doesn't blank out `/settings` when the user is on `/settings`. Each route streams in independently.

## Skeleton design: match the final layout

A skeleton's job is to **reserve the space** the real content will occupy. The user's eye should not jump when the content arrives.

```tsx
// app/(app)/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="grid grid-cols-3 gap-4 p-6">
      <Skeleton className="h-32" />           {/* matches card height */}
      <Skeleton className="h-32" />
      <Skeleton className="h-32" />
      <Skeleton className="col-span-3 h-64" />{/* matches chart */}
    </div>
  );
}
```

- ✗ Spinner in the middle of the page — gives no spatial cue, content appearance is jarring
- ✗ Skeleton that's the wrong height — layout shift on content arrival = bad CLS
- ✓ Skeleton bricks matching the final layout shape, neutral gray fill, optional shimmer

For text content: 3-5 lines of skeleton bars at varying widths look more realistic than perfect rectangles.

## `error.tsx`: handle, don't display the stack

Error boundary should:

- Hide the technical detail from end users
- Log to Sentry (composes with `void-observability`)
- Offer a recovery path (reset button, link back)

```tsx
'use client';

import { useEffect } from 'react';
import * as Sentry from '@sentry/nextjs';

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <div className="p-6">
      <h2>Quelque chose s'est mal passé.</h2>
      <p>L'équipe est notifiée. Vous pouvez réessayer.</p>
      <button onClick={() => reset()}>Réessayer</button>
    </div>
  );
}
```

The `digest` prop is the server-side error ID — useful to correlate Sentry with the user report (display it discreetly: `<small>ID: {error.digest}</small>`).

## `not-found.tsx` — the route's own 404

```tsx
// app/(marketing)/blog/[slug]/not-found.tsx
export default function NotFound() {
  return (
    <div className="p-6 text-center">
      <h1>Article introuvable</h1>
      <p>Cet article n'existe pas ou a été supprimé.</p>
      <Link href="/blog">← Retour aux articles</Link>
    </div>
  );
}
```

Triggered from a Server Component:

```tsx
import { notFound } from 'next/navigation';

export default async function Article({ params }) {
  const post = await db.query.posts.findFirst({ where: eq(posts.slug, params.slug) });
  if (!post) notFound();
  return <ArticleView post={post} />;
}
```

Without a `not-found.tsx` at the route, Next falls back to the nearest ancestor. Provide one at the level that knows the resource — a blog `not-found` is contextually richer than the root 404.

## `global-error.tsx` — last resort

Catches errors in `app/layout.tsx` itself (and its providers). Rare; usually empty until needed.

```tsx
// app/global-error.tsx
'use client';

export default function GlobalError({ error, reset }) {
  return (
    <html>
      <body>
        <h1>Application non disponible.</h1>
        <button onClick={() => reset()}>Recharger</button>
      </body>
    </html>
  );
}
```

Must render its own `<html>` and `<body>` because it replaces the root layout entirely.

## Anti-patterns

- ✗ **One `loading.tsx` at app root** — every route shows the same skeleton; no granularity
- ✗ **Spinner-only loading** — no spatial cue, content appearance is jarring
- ✗ **Error boundary displaying the raw stack** — leaks internal info, scares users
- ✗ **`not-found.tsx` only at the root** — every "not found" looks the same; misses context
- ✗ **No `useEffect` Sentry capture in error.tsx** — errors swallowed silently
- ✗ **Catching errors in components via try/catch instead of `error.tsx`** — bypasses React's error boundary mechanism

## Workflow

1. **At each route segment**, ask: does this content need its own loading state?
2. **If yes**, write a `loading.tsx` whose skeleton matches the final layout's shape.
3. **For routes that fetch data**, write an `error.tsx` with Sentry capture + recovery action.
4. **For routes with parameterized resources** ([slug], [id]), write a `not-found.tsx` and call `notFound()` when the resource is absent.
5. **`global-error.tsx` only when** root layout starts having logic that can fail.

## Composition

- `void-cache-component-pattern` — cached pages have predictable load times; loading.tsx is mostly for the cold cache case.
- `void-parallel-routes-slots` — each `@slot` can have its own `loading.tsx` / `error.tsx`.
- `void-observability` — `error.tsx` is the Sentry capture point for server errors.
- `void-accessibility-check` — skeletons should have `aria-busy` or `aria-live="polite"` regions.
