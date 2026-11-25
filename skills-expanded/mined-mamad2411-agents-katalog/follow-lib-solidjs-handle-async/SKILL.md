---
name: follow-lib-solidjs-handle-async
description: SolidJS async — createResource, Suspense, lazy loading, streaming SSR, error handling
argument-hint: "[scope]"
related:
  - follow-lib-solidjs
  - run-test
  - resolve-errors
---

## Goal

Handle async data in SolidJS — `createResource` fetch/track/mutate, `Suspense` boundaries, `lazy` code-split, SSR streaming

## Scope

async lifecycle — `createResource`, `Suspense`, `ErrorBoundary` integration, `lazy()`, transition (`useTransition`), SSR `Suspense` streaming

## Execute

### 1. createResource

```ts
const [data, { refetch, mutate }] = createResource(userId, fetchUser)
// userId() changes → auto refetch (source signal)
data()           // value | undefined
data.loading     // boolean
data.error       // thrown error
data.latest      // last resolved (not reset on refetch)
mutate(newData)  // manual update cache
refetch()        // re-fetch
```

- The source signal = a reactive dependency — it changes → an automatic re-fetch
- Options: `{ initialValue }`, `{ storage: createSignal }`, `{ deferStream }`

### 2. Suspense And Boundaries

```tsx
<Suspense fallback={<Spinner />}>
  <Profile />         {/* uses data() — suspends until resolved */}
</Suspense>
<ErrorBoundary fallback={err => <Error err={err} />}>...</ErrorBoundary>
```

- `Suspense` catches pending resources — nested boundaries for granular fallbacks
- `<SuspenseList>` for SSR ordered reveal (revealOrder/collapsible/tail)

### 3. Transitions And Deferred

```ts
const [pending, start] = useTransition()
start(() => setTab('heavy'))    // keeps the old UI until the new branch resolves
```

- `useTransition` — non-blocking updates (stale-while-loading UI)
- `createDeferred` — defer an expensive computed (debounce-like)

### 4. Code Split And SSR

- `const Heavy = lazy(() => import('./Heavy'))` — component code split + Suspense-ready
- SSR: `Suspense` streaming — the page renders first, pending chunks stream in after (SolidStart)
- `isServer`/`onMount` — client-only code paths (`onMount` does not run on the server)

## Rules

- `createResource` = the canonical async — don't do manual `useEffect`-style fetching in `createEffect` (race conditions)
- Wrap `Suspense` around suspended branches — without it = crash on SSR paths
- `mutate`/`refetch` for cache updates — not re-creating the resource
- Use `SuspenseList` for SSR streaming when ordering is needed — see the SolidStart docs for SSR deploys

## Expected Outcome

- Async data tracked + refetched correctly via `createResource`
- Suspense/ErrorBoundary complete on every pending branch
