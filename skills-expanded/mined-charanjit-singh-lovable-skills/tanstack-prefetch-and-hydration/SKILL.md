---
name: tanstack-prefetch-and-hydration
description: >-
  Use when prefetching TanStack Query data on hover/route-enter, hydrating
  server-rendered queries, or speeding up navigation. Not for CSR-only apps
  where prefetch isn't desired or for non-TanStack stacks.
---

# TanStack prefetch and hydration

Make routes feel instant. Prefetch on intent (hover, focus, route prepare); hydrate when SSR or prerendering is used.

Companion skills: [`tanstack-query-alternative`](../tanstack-query-alternative/), [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/), [`performance-budget`](../performance-budget/).

## Prefetch on hover / focus

```tsx
function ProjectLink({ project }: { project: Project }) {
  const qc = useQueryClient();
  return (
    <Link
      to={`/projects/${project.id}`}
      onMouseEnter={() =>
        qc.prefetchQuery({
          queryKey: projectKeys.detail(project.id),
          queryFn: () => fetchProject(project.id),
          staleTime: 30_000,
        })
      }
      onFocus={() =>
        qc.prefetchQuery({
          queryKey: projectKeys.detail(project.id),
          queryFn: () => fetchProject(project.id),
        })
      }
    >
      {project.name}
    </Link>
  );
}
```

`staleTime` on the prefetch matches the consumer — otherwise the consumer refetches immediately after navigation.

## Prefetch on route enter (React Router)

```ts
// router config
{
  path: "projects/:id",
  loader: async ({ params }) => {
    await queryClient.prefetchQuery({
      queryKey: projectKeys.detail(params.id!),
      queryFn: () => fetchProject(params.id!),
    });
    return null;
  },
  element: <ProjectPage />,
}
```

In the page, `useQuery` reads from cache without a flash:

```ts
const { data } = useQuery({ queryKey: projectKeys.detail(id), queryFn: () => fetchProject(id) });
```

## Hydration (SSR / prerender)

When the page is server-rendered or prerendered, ship a serialized cache so the client doesn't refetch immediately.

### Server (or build-time)

```ts
import { dehydrate, QueryClient } from "@tanstack/react-query";

const qc = new QueryClient();
await qc.prefetchQuery({ queryKey: pageKeys.detail(slug), queryFn: () => fetchPage(slug) });
const dehydratedState = dehydrate(qc);

// embed into HTML
res.send(`
  <html>
    <body>
      <div id="root">${html}</div>
      <script>window.__RQ_STATE__ = ${JSON.stringify(dehydratedState).replace(/</g, "\\u003c")};</script>
    </body>
  </html>
`);
```

### Client

```tsx
import { HydrationBoundary } from "@tanstack/react-query";

<QueryClientProvider client={queryClient}>
  <HydrationBoundary state={window.__RQ_STATE__}>
    <App />
  </HydrationBoundary>
</QueryClientProvider>
```

Hydrated entries are treated as fresh until `staleTime` elapses.

## When to prefetch (and when not)

| Prefetch | Don't prefetch |
|----------|----------------|
| Card → detail page links above the fold | Pages users rarely visit (settings deep links) |
| Wizard "next step" data | Expensive queries that may go unused |
| Predictable nav (breadcrumbs) | Authenticated data on public marketing pages |

Each prefetch is a real network request — over-prefetching wastes bandwidth and Supabase egress.

## Background revalidation strategy

- `staleTime: 0` → refetch on every mount (fresh, costly).
- `staleTime: 30_000` → trust cache for 30 s, then refetch in background.
- `staleTime: Infinity` with explicit invalidation → ideal for static config (feature flags, plans list) you mutate via specific actions.

## Avoid

- Prefetching everything on app start.
- `staleTime: 0` everywhere — defeats caching.
- Sending the dehydrated state without `JSON.stringify` escape; it's an XSS vector.
- Prefetching authenticated queries on hover in a logged-out shell.

## Checklist

- [ ] Hover/focus prefetch on primary navigation links.
- [ ] Route loader prefetches detail data before render where applicable.
- [ ] If SSR/prerender used, `HydrationBoundary` wraps the app.
- [ ] `staleTime` tuned per resource, not global zero.
