---
name: follow-lib-tanstack-query
description: Use TanStack Query end to end — setup, queries/mutations, caching, infinite queries, prefetch, optimistic updates, persistence
argument-hint: "[framework] [feature]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Query (v5) from setup to production patterns — provider, queries, mutations, caching strategy, dependent/infinite queries, prefetching, optimistic updates

## Scope

Works with React, Solid, Vue, Svelte, Angular — covers install, `QueryClient` config, `useQuery`/`useMutation`/`useInfiniteQuery`, cache management, devtools, and testing patterns

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install Package

> Goal: install the package matching the framework in use

1. Detect the framework from `package.json`, then install per the naming convention `@tanstack/{framework}-query`:
   - `bun add @tanstack/react-query` / `solid-query` / `vue-query` / `svelte-query` / `angular-query-experimental`
2. If already present → skip install and verify the version (idempotent); if unsure of latest → `npm view @tanstack/react-query version`

### 2. Setup QueryClientProvider

> Goal: one `QueryClient` wrapping the app

```ts
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,      // data stays "fresh" for 60s — no refetch within this window
      gcTime: 300_000,        // keep cache 5 minutes after it becomes unused
      retry: 1,
      refetchOnWindowFocus: false,  // disable if the app doesn't need it
    },
    mutations: { retry: 0 },  // mutations should not retry automatically (non-idempotent)
  },
})
```

- React: `<QueryClientProvider client={queryClient}>`; Vue: `app.use(VueQueryPlugin)`; SSR (Next/Start) → one client per request per the docs
- SSR + dehydration → `HydrationBoundary` + `dehydrate`/`hydrate` to pass the cache from the server

### 3. Query Patterns

> Goal: use queries in every shape

1. **Basic**: `useQuery({ queryKey: ['todos', filters], queryFn })` — queryKey is an array, include every variable queryFn uses
2. **Dependent**: `useQuery({ ..., enabled: !!userId })` — the query waits on a dependency
3. **Select**: `select: (data) => data.map(...)` — transform + subscribe only to the derived value (fewer re-renders)
4. **Infinite**: `useInfiniteQuery({ queryKey, queryFn: ({pageParam}) => fetch(pageParam), initialPageParam: 0, getNextPageParam })` + `fetchNextPage`/`hasNextPage`
5. **Shared options**: `queryOptions({ queryKey, queryFn })` — reuse across `useQuery`, `ensureQueryData`, and prefetch
6. **Suspense**: `useSuspenseQuery` when using `<Suspense>` boundaries (v5 splits the hook)

### 4. Mutation And Cache Patterns

> Goal: correct writes + invalidation

1. `useMutation({ mutationFn, onSuccess })` + `queryClient.invalidateQueries({ queryKey: ['todos'] })` — invalidate only the affected subtree
2. **Optimistic update**: `onMutate` → `cancelQueries` + `getQueryData` snapshot + `setQueryData` optimistic → `onError` rollback → `onSettled` invalidate:

   ```ts
   useMutation({
     mutationFn: updateTodo,
     onMutate: async (newTodo) => {
       await queryClient.cancelQueries({ queryKey: ['todos'] })
       const prev = queryClient.getQueryData(['todos'])
       queryClient.setQueryData(['todos'], (old) => [...old, newTodo])
       return { prev }
     },
     onError: (_e, _v, ctx) => queryClient.setQueryData(['todos'], ctx.prev),
     onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
   })
   ```

3. **Prefetch**: `queryClient.prefetchQuery` on hover/route load — fewer loading spinners
4. **Polling**: `refetchInterval: 5000` or a function-based interval
5. **Persist cache**: `persistQueryClient` + an async storage persister for offline/resume

### 5. Devtools And Testing

> Goal: debuggable and testable query code

1. `bun add -D @tanstack/react-query-devtools` → `<ReactQueryDevtools />` (or the unified panel — see `config-devtools`)
2. Test query-using components: wrap with a `QueryClientProvider` configured with `retry: false` + a mocked `queryFn`
3. Run `/run-typecheck` and `/run-test`
4. If it fails → `/resolve-errors` max 3 rounds

## Rules

- One `QueryClient` instance per app — never create it inside a component render
- queryKey is an array containing every dependency — an incomplete key = stale cache bugs
- Set `staleTime` to the data's real freshness needs — `staleTime: 0` (default) = refetch on every mount
- Mutations: always invalidate or `setQueryData` after success — never leave stale UI
- `isLoading` = first load only; `isFetching` = every fetch — pick the right one for the UX
- Server state lives only in Query — never copy it into a Store/useState (`follow-store`)
- Use `/follow-lib-tanstack-ecosystem` for the overview and library selection

## Expected Outcome

- Queries work fully: fetch, cache, invalidate, optimistic, infinite, prefetch
- Cache config matches the data freshness requirements
- Devtools + tests are ready for debugging
