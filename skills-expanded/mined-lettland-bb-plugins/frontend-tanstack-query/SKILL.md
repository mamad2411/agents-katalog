---
name: frontend-tanstack-query
description: Use when fetching server state with TanStack Query (React Query) — queries, mutations, query keys, invalidation, suspense, infinite, optimistic updates.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [react, typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [react, typescript, ts-zod, frontend-react-hook-form, frontend-react-router]
---

# TanStack Query

**Iron Law: server state is not client state. Never store fetched data in `useState` or Zustand. The cache key IS the contract — co-locate it with the fetcher in a query-key factory. `useEffect(() => fetch())` is a bug.**

**Versions:** Current `5.x` · No LTS series — _v5 introduced the single-object signature (`useQuery({ queryKey, queryFn })`), renamed `cacheTime` → `gcTime`, removed callbacks (`onSuccess`/`onError` on queries — use `useEffect` on `data` or the mutation form). v6 is unreleased; expect React 19 transitions + first-class server-actions interop._

## When it fits

| Fits                                             | Doesn't                                                                         |
| ------------------------------------------------ | ------------------------------------------------------------------------------- |
| Any network-derived data (lists, detail, search) | Truly local state (form inputs, modal open) — keep in `useState`                |
| Caching, dedup, background refetch               | One-off imperative call (POST and forget) — `mutation` once or raw fetch        |
| Optimistic UI, infinite scroll, suspense         | WebSocket streams — use `useSyncExternalStore` or a socket hook, dispatch to QC |

## Query-key factory pattern (non-negotiable)

```ts
// queries/projects.ts
export const projectKeys = {
  all: ["projects"] as const,
  lists: () => [...projectKeys.all, "list"] as const,
  list: (filters: ProjectFilters) => [...projectKeys.lists(), filters] as const,
  details: () => [...projectKeys.all, "detail"] as const,
  detail: (id: string) => [...projectKeys.details(), id] as const,
};
```

Then:

```ts
useQuery({ queryKey: projectKeys.list(filters), queryFn: () => api.listProjects(filters) });
qc.invalidateQueries({ queryKey: projectKeys.lists() }); // invalidates ALL list variants
qc.invalidateQueries({ queryKey: projectKeys.detail(id) }); // just one detail
```

Without a factory, invalidation becomes string-matching guesswork across the codebase. The factory is the contract.

## Query options object (v5)

```ts
export const projectQuery = (id: string) => ({
  queryKey: projectKeys.detail(id),
  queryFn: () => api.getProject(id),
  staleTime: 60_000,
});

useQuery(projectQuery(id)); // hook usage
qc.ensureQueryData(projectQuery(id)); // loader prefetch (React Router)
qc.prefetchQuery(projectQuery(id)); // fire-and-forget warming
```

One object, used everywhere. Survives refactors that hooks alone don't.

## staleTime vs gcTime

| Knob                       | What it controls                                                | Default            | Tune when                                               |
| -------------------------- | --------------------------------------------------------------- | ------------------ | ------------------------------------------------------- |
| `staleTime`                | how long data is considered fresh — no auto-refetch while fresh | `0` (always stale) | data changes rarely → `5 * 60_000`; near-realtime → `0` |
| `gcTime` (was `cacheTime`) | how long unused cache entries linger before garbage collection  | `5 * 60_000`       | offline-first → much longer; memory-tight → shorter     |

**Set `staleTime` at `QueryClient` defaults, not per-hook.** Per-hook overrides for exceptions only.

```ts
const qc = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000, retry: 1, refetchOnWindowFocus: false } },
});
```

## Mutations + invalidation

```ts
const updateProject = useMutation({
  mutationFn: (input: UpdateInput) => api.updateProject(input),
  onSuccess: (updated) => {
    qc.setQueryData(projectKeys.detail(updated.id), updated); // write-through
    qc.invalidateQueries({ queryKey: projectKeys.lists() }); // lists need refresh
  },
});
```

Two-step pattern: **set** the known result into cache (instant UI), **invalidate** anything you can't compute. Don't `refetch()` — let staleness do its job.

## Optimistic updates (with rollback)

```ts
const toggleFavorite = useMutation({
  mutationFn: (id: string) => api.toggleFavorite(id),
  onMutate: async (id) => {
    await qc.cancelQueries({ queryKey: projectKeys.detail(id) });
    const prev = qc.getQueryData<Project>(projectKeys.detail(id));
    qc.setQueryData<Project>(projectKeys.detail(id), (p) => p && { ...p, favorite: !p.favorite });
    return { prev }; // rollback context
  },
  onError: (_err, id, ctx) => ctx?.prev && qc.setQueryData(projectKeys.detail(id), ctx.prev),
  onSettled: (_d, _e, id) => qc.invalidateQueries({ queryKey: projectKeys.detail(id) }),
});
```

Always `cancelQueries` first — otherwise an in-flight refetch will clobber your optimistic write.

## Suspense queries

```ts
const { data } = useSuspenseQuery(projectQuery(id)); // never undefined; throws to nearest <Suspense>
```

Combine with `<ErrorBoundary>` for error UI and `<Suspense>` for loading. Removes the `if (isLoading) ... if (isError) ...` ladder. Plays well with React Router loaders and React 19 `<Suspense>` transitions.

## Infinite queries

```ts
const q = useInfiniteQuery({
  queryKey: projectKeys.list(filters),
  queryFn: ({ pageParam }) => api.listProjects({ ...filters, cursor: pageParam }),
  initialPageParam: null as string | null,
  getNextPageParam: (last) => last.nextCursor ?? undefined, // undefined ends pagination
});
// q.data.pages: Array<PageShape>; flatten with .flatMap((p) => p.items)
```

## Retries + backoff

```ts
useQuery({
  retry: (n, err) => n < 3 && !is4xx(err),
  retryDelay: (n) => Math.min(1000 * 2 ** n, 30_000),
});
```

Don't retry 4xx. Don't retry mutations by default — they're not idempotent unless you made them so.

## Persistence (offline / refresh-survive)

```ts
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";

persistQueryClient({
  queryClient: qc,
  persister: createSyncStoragePersister({ storage: window.localStorage }),
  maxAge: 24 * 60 * 60 * 1000,
  buster: APP_BUILD_HASH, // bump → invalidate persisted cache
});
```

Use IndexedDB persister for >5MB caches. Set `buster` to your build hash so deploys don't serve stale schemas.

## SSR / hydration

```ts
// server
const qc = new QueryClient();
await qc.prefetchQuery(projectQuery(id));
return { dehydratedState: dehydrate(qc) };

// client
<HydrationBoundary state={dehydratedState}><App/></HydrationBoundary>
```

## Anti-patterns

- `useEffect(() => fetch(...))` then `setState` — you've reimplemented Query badly. Use `useQuery`.
- Storing query results in Zustand "to share across components" — components share via the queryKey
- Stringly-typed query keys scattered across files — extract a factory
- `refetch()` after every mutation — invalidate instead
- Mutations without `onError` rollback when you used `onMutate` — broken UI on failure
- `enabled: !!id` checks duplicated — wrap into the query options factory
- Manual `setInterval` for polling — use `refetchInterval`
- Calling `useQuery` inside a loop or condition — violates React rules-of-hooks
- Disabling `refetchOnWindowFocus` globally because "it's annoying" — for dashboards, fresh data is the point. Tune per-query.

## Red flags

| Thought                                    | Reality                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| "I'll cache it in Zustand"                 | TanStack Query already caches it. You're duplicating + de-syncing.                      |
| "Just refetch after the mutation"          | `invalidateQueries` does it lazily AND for every observer. `refetch` only hits one.     |
| "I need a useEffect to load the page data" | Use a route loader with `qc.ensureQueryData(opts)`. See `Skill(frontend-react-router)`. |
| "Polling every second"                     | Reconsider WebSockets/SSE. If polling, set `refetchInterval` and a sane `staleTime`.    |

## Hand-off

For the route loader pattern that prefetches queries: `Skill(frontend-react-router)`. For schema-validating API responses with zod: `Skill(ts-zod)`. For forms that POST via mutations: `Skill(frontend-react-hook-form)`. For testing queries with MSW: `Skill(react)`.
