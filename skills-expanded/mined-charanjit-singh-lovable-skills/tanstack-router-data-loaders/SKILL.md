---
name: tanstack-router-data-loaders
description: >-
  Use when adding TanStack Router loaders, pending/error components, search-param
  schemas, or integrating loaders with TanStack Query. Not for plain React Router
  apps without TanStack Router.
---

# TanStack Router data loaders

[TanStack Router](https://tanstack.com/router) provides typed routes with **loaders** that run before a route renders. Pair them with TanStack Query so data is prefetched, cached, and reused — no "flash of loading skeleton" on intra-app navigation.

Companion skills: [`tanstack-query-alternative`](../tanstack-query-alternative/), [`tanstack-prefetch-and-hydration`](../tanstack-prefetch-and-hydration/), [`tanstack-start-server-routes`](../tanstack-start-server-routes/), [`error-states-and-empty-ui`](../error-states-and-empty-ui/).

## File-based route with a loader

```ts
// app/routes/projects.$id.tsx
import { createFileRoute } from "@tanstack/react-router";
import { projectQueryOptions } from "~/api/projects";

export const Route = createFileRoute("/projects/$id")({
  loader: ({ context: { queryClient }, params }) =>
    queryClient.ensureQueryData(projectQueryOptions(params.id)),
  pendingComponent: ProjectSkeleton,
  errorComponent: ({ error, reset }) => <ProjectError error={error} reset={reset} />,
  component: ProjectPage,
});

function ProjectPage() {
  const { id } = Route.useParams();
  const { data: project } = useSuspenseQuery(projectQueryOptions(id));
  return <ProjectDetail project={project} />;
}
```

`ensureQueryData` is the loader-friendly version of `prefetchQuery`: returns the cached value or fetches once. The `useSuspenseQuery` in the component then reads from cache **synchronously** — no loading state needed.

## `queryOptions` factory (single source of truth)

```ts
// src/api/projects.ts
import { queryOptions } from "@tanstack/react-query";

export const projectQueryOptions = (id: string) =>
  queryOptions({
    queryKey: ["projects", "detail", id],
    queryFn: () => fetchProject(id),
    staleTime: 30_000,
  });
```

Use this in **both** the loader and the component so they share one cache key. Centralize per-resource options here.

## Provide the QueryClient via router context

```ts
// app/router.tsx
import { createRouter } from "@tanstack/react-router";
import { queryClient } from "~/lib/query-client";
import { routeTree } from "./routeTree.gen";

export const router = createRouter({
  routeTree,
  context: { queryClient },
  defaultPreload: "intent",  // prefetch on hover/focus
  defaultPendingMinMs: 300,  // avoid skeleton flash for fast loads
});
```

`defaultPreload: "intent"` makes every `<Link>` hover prefetch — pairs well with [`tanstack-prefetch-and-hydration`](../tanstack-prefetch-and-hydration/).

## Search-param schemas (typed querystrings)

```ts
import { z } from "zod";

const searchSchema = z.object({
  status: z.enum(["active", "archived"]).default("active"),
  page: z.number().int().min(1).default(1),
});

export const Route = createFileRoute("/projects")({
  validateSearch: searchSchema,
  loaderDeps: ({ search }) => ({ status: search.status, page: search.page }),
  loader: ({ context: { queryClient }, deps }) =>
    queryClient.ensureQueryData(projectListQueryOptions(deps)),
  component: ProjectList,
});
```

In the component:

```ts
const { status, page } = Route.useSearch();
const navigate = Route.useNavigate();
<Button onClick={() => navigate({ search: (p) => ({ ...p, page: p.page + 1 }) })}>Next</Button>
```

Search params become **typed**, validated, and shareable URLs — back-button works for free.

## Pending and error components

- `pendingComponent`: render only when the loader takes longer than `defaultPendingMinMs`. Use skeletons matching the page layout.
- `errorComponent`: receives `error` and `reset` — call `reset()` from a retry button.
- For 404s on detail pages, throw `notFound()` inside the loader and define a route-level `notFoundComponent`.

```ts
loader: async ({ context, params }) => {
  const project = await context.queryClient.ensureQueryData(projectQueryOptions(params.id));
  if (!project) throw notFound();
  return project;
},
```

## Parallel loaders for sibling data

```ts
loader: ({ context: { queryClient }, params }) =>
  Promise.all([
    queryClient.ensureQueryData(projectQueryOptions(params.id)),
    queryClient.ensureQueryData(membersQueryOptions(params.id)),
    queryClient.ensureQueryData(activityQueryOptions(params.id)),
  ]),
```

All three start in parallel; the route renders when all resolve.

## Auth-gated routes

Use route `beforeLoad` to short-circuit unauthenticated users:

```ts
export const Route = createFileRoute("/app")({
  beforeLoad: ({ context, location }) => {
    if (!context.auth.user) {
      throw redirect({ to: "/login", search: { redirect: location.href } });
    }
  },
});
```

Provide `auth` in the router `context` alongside `queryClient`.

## SSR / hydration

If the app uses [TanStack Start](https://tanstack.com/start) or any SSR, loaders run on the server first. Dehydrate the QueryClient and hydrate on the client so loaders don't refetch — see [`tanstack-prefetch-and-hydration`](../tanstack-prefetch-and-hydration/).

## Mutations and invalidation from loaders

Don't invalidate inside a loader — loaders are for reads. Invalidate in mutation `onSuccess` ([`tanstack-mutations-and-invalidation`](../tanstack-mutations-and-invalidation/)); the next navigation's `ensureQueryData` picks up the fresh value.

## Avoid

- Two `queryKey`s for the same resource (loader vs component) — always use the `queryOptions` factory.
- Fetching inside `useEffect` on the page when a loader already loaded the data.
- Long synchronous work in a loader (it blocks navigation).
- Skipping `pendingComponent` for slow loaders — users see a blank screen.
- Overusing `useSuspenseQuery` outside of routes that already ran the loader (you'll suspend the whole tree).

## Checklist

- [ ] Every detail route has a loader + `queryOptions` factory.
- [ ] `defaultPreload: "intent"` enabled in the router.
- [ ] Search params validated with a Zod schema.
- [ ] Pending and error components defined per route (or sensible global defaults).
- [ ] Auth routes use `beforeLoad` + `redirect`.
