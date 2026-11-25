---
name: frontend-data
description: "Loading and changing server data from the client: a query library with caching, parallel requests instead of waterfalls, loading and error states per request, mutations with optimistic updates and rollback, pagination and infinite lists, real-time updates, cancellation and typed clients. Read before loading or saving data in a frontend."
---

# Server data on the client

The generated version fetches in `useEffect`, keeps the result in
`useState` and sets `loading` by hand. It shows the answer to an old
search when responses arrive out of order, fetches twice in development,
refetches on every mount, never retries, starts the second request only
after the first has rendered, and has no error branch. This is how to load
and change server data so screens are fast, correct and honest about
failure. The API client and key factories are in `frontend-architecture`.

## 1. A query library, not fetch in effects

A hand-written effect gets these wrong: races (the response for "ab"
lands after the one for "abc"), no cache (every return flashes a
skeleton), no deduplication, double requests (Strict Mode runs effects
twice in development), no retry, cancellation or refetch on focus. Use the
project's library: TanStack Query (React, Vue, Svelte, Solid, Angular),
SWR, RTK Query, Apollo or urql for GraphQL, or the framework's loaders
(section 3). Raw `fetch` belongs in the API client and query functions.

## 2. TanStack Query essentials

```ts
// src/lib/query-client.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000, retry: (failures, error) => failures < 3 && isRetryable(error) },
  },
});

/** Worth another try: the network, a timeout, 408, 429 and 5xx. Other 4xx will fail again. */
export const isRetryable = (error: unknown) =>
  error instanceof TypeError ||
  (error instanceof DOMException && error.name === "TimeoutError") ||
  (error instanceof ApiError && (error.status >= 500 || error.status === 408 || error.status === 429));
```

Defaults to know: `staleTime` 0 (every mount refetches in the background),
`gcTime` 5 minutes, refetch on mount, window focus and reconnect, queries
retried 3 times with backoff (1s, 2s, 4s, capped at 30s), mutations never.

| Data | `staleTime` |
|---|---|
| Reference data: countries, plans, feature flags | an hour to `Infinity`, invalidated when it changes |
| Records people edit: lists and details | 30s to 2 min |
| The signed-in user and their permissions | 5 min, invalidated on sign-in and role change |
| Live numbers: queues, stock, prices | 0 with `refetchInterval` of 5 to 30s, or pushed (section 9) |

- **Keys** are arrays from general to specific holding every input
  (`["orders", "list", { status, page }]`), from the feature's key factory.
  Pass the query function's `signal` on, so unneeded requests are cancelled.
- **After a write**, invalidate what it changed
  (`invalidateQueries({ queryKey: orderKeys.lists() })`): what is on
  screen refetches, the rest is marked stale.
- **Prefetch before the click**: on a link's hover or focus
  (`prefetchQuery(orderQuery(id))`) or in the route loader
  (`ensureQueryData`); TanStack Router's `defaultPreload: "intent"` does it.
- **`placeholderData: keepPreviousData`** for pages and filters: the old
  page stays while the next loads, `isPlaceholderData` dims it. `isPending`
  means no data yet; `isFetching`, any request in flight.
- **`select`** shapes what a component needs while the cache keeps the raw
  response; **`enabled: Boolean(id)`** waits for another query's result (a
  waterfall by design: could one endpoint return both?).
- **SWR** (`mutate`, `keepPreviousData: true`, deduplication within 2s)
  and **RTK Query** (`providesTags`, `invalidatesTags`, `updateQueryData`)
  have the same ideas.

## 3. Framework loaders

When the framework loads data per route, use it; add a query library only
where the client refetches and mutates a lot.

- **Next.js App Router**: `await` data in server components. `fetch` is
  uncached by default since Next 15; caching is opted into (`revalidate`,
  or `"use cache"` with Next 16's Cache Components), and server actions
  call `revalidatePath` or `revalidateTag` after a write.
- **React Router 7**: `loader` and `clientLoader`, `useLoaderData`; actions
  revalidate the page's loaders after a `<Form>` or `fetcher.submit`.
- **SvelteKit**: `load` in `+page.ts` or `+page.server.ts`, run in
  parallel; `depends("app:orders")`, then `invalidate("app:orders")`.
- **Nuxt**: `useFetch` or `useAsyncData` with a key, then `refresh()`.

## 4. No waterfalls

A waterfall is a request waiting on another for no reason: three 200ms
requests become 600ms.

- Start independent requests together, from the route loader rather than
  the component tree (children that fetch after their parent rendered are
  a cascade): `useQueries`, or `Promise.all` over `ensureQueryData` calls.
- Server-rendered pages fetch on the server, near the data, and stream the
  slow parts behind `Suspense`.
- A list that fetches each row's details (N+1 over HTTP) needs an endpoint
  that returns what the screen shows (`backend-api`).
- DevTools, Network, the waterfall column: bars that start where another
  ends are the ones to fix.

## 5. States

- A skeleton only while there is no data, after about 200ms so fast loads
  do not flash, shaped like the content (`ui-part-loading`). A refetch
  keeps the data on screen with a small indicator; it never returns to a
  skeleton.
- Errors per region with a retry, so one failed panel leaves the rest
  working (`frontend-errors`). Empty is its own state, saying why and
  offering the action that fills it, or to clear the filters.
- With Suspense (`useSuspenseQuery`, Next `loading.tsx`, streamed server
  components), loading is a `Suspense` fallback and failure an error
  boundary with a reset (`QueryErrorResetBoundary`), one pair per region.
- Check data before error: a background refetch that fails keeps the old
  data, still worth showing.

```tsx
const { data, error, isFetching, refetch } = useOrders(filters);
if (data) {
  if (data.items.length === 0) return <OrdersEmpty filters={filters} />;
  return <OrdersTable orders={data.items} refreshing={isFetching} stale={Boolean(error)} />;
}
if (error) return <RegionError error={error} onRetry={() => refetch()} />;
return <OrdersSkeleton />;
```

## 6. Retries and writes

- Reads: up to 3 retries with backoff for the network, timeouts, 408, 429
  and 5xx (`isRetryable`); on 429, wait for `Retry-After`.
- Writes: never retried automatically, since a retried POST can charge
  twice. The user retries with a button, and payments, orders and
  messages send an `Idempotency-Key` header, created once per attempt with
  `crypto.randomUUID()` and reused on each retry of it (`backend-api`).
- One submit per action: the button shows it is pending and ignores
  presses until it settles (`frontend-forms`). Offline, TanStack Query
  pauses mutations and runs them on reconnect: that is a queue, so decide
  whether you want one (`frontend-errors`).

## 7. Optimistic updates

For changes the server almost always accepts (rename, toggle, reorder,
like): snapshot, apply, roll back on error, then refetch.

```ts
const queryClient = useQueryClient();
const rename = useMutation({
  mutationFn: ({ id, name }: { id: string; name: string }) =>
    call(api.PATCH("/projects/{id}", { params: { path: { id } }, body: { name } })),
  onMutate: async ({ id, name }) => {
    await queryClient.cancelQueries({ queryKey: projectKeys.detail(id) }); // no older response on top
    const previous = queryClient.getQueryData<Project>(projectKeys.detail(id));
    queryClient.setQueryData<Project>(projectKeys.detail(id), (p) => (p ? { ...p, name } : p));
    return { previous };
  },
  onError: (_error, { id }, context) => queryClient.setQueryData(projectKeys.detail(id), context?.previous),
  onSettled: (_data, _error, { id }) => queryClient.invalidateQueries({ queryKey: projectKeys.detail(id) }),
});
```

- When one place shows the change, render it from the mutation's
  `variables` while `isPending` instead of editing the cache (React 19's
  `useOptimistic` does this for actions). A rollback is announced: the old
  value returns with a message saying the change failed and why.
- Not for payments, anything the server often refuses, or results the
  server computes (an id, a total): show pending and wait, then write the
  returned record with `setQueryData` and invalidate the lists.

## 8. Pagination and infinite lists

- Cursors when rows are added while people read (offsets skip or repeat
  rows as the list shifts); page numbers with a total when people jump to
  a page of a stable list (`backend-api`). The page lives in the URL
  (`frontend-state`); the look is `ui-part-pagination`.
- `useInfiniteQuery` with `initialPageParam` and
  `getNextPageParam: (last) => last.nextCursor ?? undefined`. An
  `IntersectionObserver` sentinel with a `rootMargin` of about 400px loads
  the next page early; a visible "Load more" button does it for keyboards,
  screen readers and when the observer never fires. Announce "20 more
  orders loaded" in a `role="status"` region. A footer under an infinite
  list is unreachable: move its links, or use "Load more" alone.
- Back keeps the place: the cache holds the pages (`gcTime` longer than
  people stay away), the router restores scroll (React Router's
  `<ScrollRestoration />`, TanStack Router's `scrollRestoration`, Next by
  default), a virtualised list keeps its offset in history state.

## 9. Real-time updates

- Polling (`refetchInterval`) for data that may be a minute old; Server-Sent
  Events (`EventSource`) for server-to-client updates, which reconnect and
  resume with `Last-Event-ID` by themselves; WebSockets when the client
  also sends often, reconnecting with backoff and jitter (1s doubling to
  30s).
- Merge events into the cache (`setQueryData` for a whole record,
  `invalidateQueries` for what it affects, debounced in bursts), and after
  a reconnect refetch what is on screen: events sent meanwhile are lost.

```ts
useEffect(() => {
  const source = new EventSource("/api/events", { withCredentials: true });
  let dropped = false;
  source.onerror = () => { dropped = true; }; // EventSource reconnects by itself
  source.onopen = () => { if (dropped) queryClient.invalidateQueries({ queryKey: orderKeys.all }); };
  source.addEventListener("order.updated", (event) => {
    const order = OrderSchema.parse(JSON.parse(event.data));
    queryClient.setQueryData(orderKeys.detail(order.id), order);
    queryClient.invalidateQueries({ queryKey: orderKeys.lists() });
  });
  return () => source.close();
}, [queryClient]);
```

## 10. Cancellation, time limits, search

- Pass the query's `signal` on; without a query library, one
  `AbortController` per request, aborted in the effect's cleanup and when
  a newer request starts. Every request has a time limit:
  `AbortSignal.any([signal, AbortSignal.timeout(15_000)])`.
- Search as you type: debounce 200 to 300ms, at least 2 characters, old
  results kept while new ones load:

```ts
const term = useDebouncedValue(input.trim(), 250); // a small hook, or the project's
const results = useQuery({
  queryKey: ["search", term],
  queryFn: ({ signal }) => call(api.GET("/search", { params: { query: { q: term } }, signal })),
  enabled: term.length >= 2,
  placeholderData: keepPreviousData,
});
```

## 11. Types, trust and auth

- Your API's types come from its contract (`frontend-architecture`). Parse
  with zod what you do not control (third-party APIs, `postMessage`,
  storage, an API with no contract): a failed parse is an error state with
  a report, not an `undefined` that crashes three components later.
- Dates arrive as ISO strings and money as integers in the smallest unit;
  format both with `Intl` (`i18n`), and never compute money with floats.
- The session is an `httpOnly` cookie; a cross-origin API needs
  `credentials: "include"` and CORS allowing your origin
  (`frontend-security`). Signing out, or in as someone else, clears the
  cache (`queryClient.clear()`): nobody sees the last person's data.
- A `401` is handled once, in the API client: refresh once (one refresh
  shared by every request that failed together), replay once, then
  sign-in with a return path. Never a loop.

```ts
let refreshing: Promise<boolean> | null = null;
export function refreshSession(): Promise<boolean> {
  refreshing ??= fetch("/api/auth/refresh", { method: "POST", credentials: "include" })
    .then((response) => response.ok, () => false)
    .finally(() => { refreshing = null; });
  return refreshing;
}
```

## Check it

- DevTools Network: Slow 4G, offline and back, one endpoint blocked; no
  request in the waterfall waits on another without cause.
- MSW handlers (`frontend-testing`) that delay 3s, return 500, 401, 429
  with `Retry-After`, and an empty list: each state shows in its region.
- Type fast in search, switch filters quickly, double-click a submit: no
  stale results, one request per action.
- Leave a screen and return: data at once, refreshed quietly. Sign out and
  in as another user: nothing of the first account shows. `preview` (with
  `login`): no console errors on any screen.

## Avoid

`fetch` in `useEffect` with hand-set loading flags; server data copied
into state or a store; a key missing the filters it depends on; a skeleton
on every refetch; a whole-page spinner for one slow panel; an error state
that hides data still worth showing; automatic retries of writes or of
4xx; optimistic payments; requests chained that could run together; no
time limit; a `401` handled in every component; a cache that survives a
sign-out.
