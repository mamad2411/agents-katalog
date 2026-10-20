---
name: manage-client-server-state
description: Sets up server-state with TanStack Query (caching, mutations, optimistic updates, hydration) and picks the right client-state tool; used when wiring data fetching or untangling state.
when_to_use: When the user wires data fetching/caching, mentions TanStack Query / React Query, useEffect fetch waterfalls, optimistic UI, SSR hydration, or choosing a state manager (Zustand/Context/Redux).
---

## When to Use

Reach for this skill when the task involves any of:
- Wiring data fetching/caching, or the prompt mentions **TanStack Query / React Query** (`useQuery`, `useMutation`, `QueryClient`).
- A component fetches in `useEffect` and stuffs results into `useState` (manual loading/error flags, refetch-on-prop-change, fetch waterfalls).
- **Optimistic UI** — update the screen before the server confirms, then roll back on failure.
- **SSR / RSC hydration** in Next.js (App Router) — prefetch on the server, hand off to the client without a refetch flash.
- Choosing a **client-state** tool: Context vs Zustand vs Redux, or fixing prop drilling / over-rendering.

Skip / hand off if the task is purely **form validation** (use `build-form-validation`) or **component scaffolding/markup** (component skill). This skill is about *where state lives and how it syncs*, not UI structure.

First principle, state the line out loud before coding: **Server state ≠ client state.** Server state is async, owned by the backend, shared, and can go stale (lists, user profile, search results) → TanStack Query. Client state is synchronous, owned by the UI, local (modal open, active tab, form draft, theme) → `useState` / Zustand / Context. Most "state is a mess" bugs are these two being managed by the same tool.

## Steps

1. **Classify every piece of state first.** Grep the file/feature for `useState`, `useEffect`, `useContext`, `dispatch`. For each, ask: does the value originate from an API/DB? → server state, migrate to TanStack Query. Is it ephemeral UI? → leave as client state. Do NOT migrate UI toggles into Query, and do NOT keep fetched data in `useState`.

2. **Provider + client setup (once per app).** Create one `QueryClient` and wrap the tree in `<QueryClientProvider>`. In Next.js App Router, the client MUST be created inside a `"use client"` component via `useState(() => new QueryClient())` (not a module-level singleton) so each request/user gets its own cache. Set sane defaults: `staleTime` 30–60s for most reads (0 means "always refetch on mount/focus" — usually not what you want), keep `gcTime` (v5; was `cacheTime`) default 5min unless memory-bound.

3. **Replace `useEffect`+`fetch` with `useQuery`.** Pattern:
   ```ts
   const { data, isPending, isError, error } = useQuery({
     queryKey: ['todos', { status, page }], // serializable, hierarchical
     queryFn: ({ signal }) => fetchTodos({ status, page, signal }),
     staleTime: 30_000,
   })
   ```
   Delete the manual `loading`/`error`/`data` `useState` and the `useEffect`. Pass `signal` into fetch for auto-cancel. **queryKey strategy:** array form, broad→narrow (`['todos']` → `['todos', id]` → `['todos', { filters }]`). Every variable the `queryFn` reads MUST appear in the key — missing deps = stale data served for the wrong params. Centralize keys in a `queryKeys` factory object to avoid typos and make invalidation greppable.

4. **Mutations + invalidation.** Use `useMutation` for writes. After success, invalidate the affected reads so they refetch:
   ```ts
   const qc = useQueryClient()
   useMutation({
     mutationFn: updateTodo,
     onSuccess: () => qc.invalidateQueries({ queryKey: ['todos'] }),
   })
   ```
   `invalidateQueries({ queryKey: ['todos'] })` matches all keys *prefixed* by `['todos']` — that's the lever the hierarchical key design buys you. Prefer invalidation over manually hand-editing the cache unless you're doing optimistic updates.

5. **Optimistic updates (only where latency is felt — toggles, likes, reorder).** The four-callback contract:
   ```ts
   useMutation({
     mutationFn: toggleTodo,
     onMutate: async (next) => {
       await qc.cancelQueries({ queryKey: ['todos'] })      // stop in-flight refetch clobbering us
       const prev = qc.getQueryData(['todos'])               // snapshot for rollback
       qc.setQueryData(['todos'], (old) => applyOptimistic(old, next))
       return { prev }                                       // context passed to onError
     },
     onError: (_e, _next, ctx) => qc.setQueryData(['todos'], ctx?.prev), // rollback
     onSettled: () => qc.invalidateQueries({ queryKey: ['todos'] }),     // reconcile w/ server
   })
   ```
   All three of `cancelQueries` / snapshot+rollback / `onSettled` invalidate are required — drop any one and you get flicker, lost rollback, or permanent drift from the server.

6. **SSR / RSC hydration (Next.js App Router).** In the **server component**: create a request-scoped `QueryClient`, `await queryClient.prefetchQuery({ queryKey, queryFn })`, then render `<HydrationBoundary state={dehydrate(queryClient)}>` wrapping the client component. The client component calls `useQuery` with the **identical queryKey** — it reads the dehydrated cache, no refetch, no loading flash. Mismatched keys between prefetch and `useQuery` = silent double-fetch on the client; this is the #1 hydration bug, verify keys are byte-identical.

7. **Pick the client-state tool (the non-server state from step 1):**
   | Need | Use |
   |---|---|
   | Low-frequency, rarely-changing (theme, locale, auth user object) | **Context** |
   | Cross-cutting, frequently-updated, shared across distant components (cart, wizard, filters) | **Zustand** |
   | Local to one subtree | keep `useState` / `useReducer`, lift only as far as needed |
   | Complex shared logic + time-travel/devtools/middleware genuinely needed | **Redux Toolkit** (default to NOT this) |
   Do **not** reach for Redux by reflex, and do **not** put server data in any of these — that's step 3's job.

8. **Kill prop drilling + unnecessary re-renders.** If a prop is threaded through 3+ layers only to reach a leaf, move it to Context or Zustand. For Zustand, **always select narrowly** — `useStore((s) => s.cart.count)`, never `useStore((s) => s.cart)` or the whole store, or every store change re-renders the component. For Context, split into multiple providers (e.g. separate `ThemeContext` and `AuthContext`) so a change to one doesn't re-render consumers of the other; memoize the provider `value`.

## Common Errors

- **`queryKey` missing a `queryFn` dependency** → wrong/stale data shown when params change. Every variable used in `queryFn` must be in the key.
- **Module-level `new QueryClient()` in Next.js** → cache leaks across requests/users on the server (one user sees another's data). Create it inside `useState`/per-request.
- **`v5` rename trap:** `cacheTime` → `gcTime`, `isLoading` → `isPending` (for "no data yet"), `useQuery` no longer takes positional args (options object only), callbacks `onSuccess/onError` removed from `useQuery` (still on `useMutation`). If you see those on a query, it's v4 code.
- **`staleTime: 0` (default) + refetchOnWindowFocus** → app hammers the API on every tab switch. Set a real `staleTime` for reads that don't need to be live.
- **Optimistic update without `cancelQueries`** → an in-flight background refetch resolves *after* your optimistic `setQueryData` and overwrites it → UI flickers back. Always `cancelQueries` in `onMutate`.
- **Hydration key mismatch** → server prefetches `['todos']`, client `useQuery(['todos', filters])` → no cache hit, refetch + flash. Keys must match exactly.
- **Subscribing to the whole Zustand store** → re-renders on unrelated state changes. Use a selector.
- **`invalidateQueries` with an over-narrow key** → sibling queries stay stale. Invalidate at the right prefix level.
- **Putting server data in Zustand/Context "to share it"** → you reimplement caching/invalidation/refetch badly. Let TanStack Query own server state; share the *query*, not a copy.

## Verify

- Search the touched files: no `fetch(`/axios call inside `useEffect` writing to `useState` remains for server data; those are now `useQuery`/`useMutation`.
- TypeScript/build passes; no v4-only API names (`cacheTime`, `useQuery({ onSuccess })`) left.
- Open React Query Devtools: each screen's queries appear with sensible keys, correct `fresh`/`stale` status, and no duplicate keys fetching the same data.
- Mutate something: the relevant query auto-refetches (invalidation works). For optimistic paths, throttle the network and confirm UI updates instantly then either persists or **rolls back** on a forced 500.
- SSR pages: disable JS or check the Network tab — initial data is in the server HTML and the client does **not** refetch on mount (no loading flash, no duplicate request).
- Profile a noisy interaction (React DevTools Profiler): components not consuming the changed slice do **not** re-render after the Context/Zustand split + selectors.
