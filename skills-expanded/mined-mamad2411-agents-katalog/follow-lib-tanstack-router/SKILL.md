---
name: follow-lib-tanstack-router
description: Use TanStack Router end to end — file routes, loaders, search param validation, type-safe navigation, layouts, SSR data
argument-hint: "[react|solid]"
related:
  - follow-lib-tanstack-ecosystem
  - run-dev
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Router (v1) fully — createRouter, file-based routes, type-safe params/search, loaders, navigation, layouts, error boundaries

## Scope

Works with React/Solid apps — covers route tree, params/search validation, data loading (`loader`), navigation APIs, nested layouts, pending/error states; full-stack SSR → `follow-start`

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install And Router Setup

> Goal: router ready with type registration

```bash
bun add @tanstack/react-router
bun add -D @tanstack/router-plugin   # file-based routes + code splitting
```

1. Vite plugin: `tanstackRouter({ target: 'react', autoCodeSplitting: true })` in `vite.config.ts` **before** the react plugin — auto-generates `routeTree.gen.ts`
2. `src/main.tsx`:

   ```tsx
   const router = createRouter({ routeTree })
   declare module '@tanstack/react-router' {
     interface Register { router: typeof router }  // makes the whole app type-safe
   }
   <RouterProvider router={router} />
   ```

### 2. File-Based Routes

> Goal: route tree from `src/routes/`

- `src/routes/__root.tsx` → `createRootRoute` + `<Outlet/>`
- `routes/about.tsx` → `createFileRoute('/about')`
- `routes/posts/$postId.tsx` → param route, read with `Route.useParams()`
- `routes/posts/route.tsx` → pathless layout route (wraps children `<Outlet/>`)
- `routes/_auth/` → pathless group (organizes without changing the URL)
- Code-based alternative: `createRoute({ getParentRoute, path, component })` — pick one only, never mix

### 3. Params, Search, Loaders

> Goal: type-safe URL state + data loading

1. **Params**: `$postId` → `useParams({ from: '/posts/$postId' })` typed for both name and value
2. **Search**: `validateSearch: (s) => ({ page: Number(s.page ?? 1) })` or a zod/standard schema — `useSearch` typed
3. **Loader**: `loader: ({ params }) => fetchPost(params.postId)` + `Route.useLoaderData()` — cache/staleTime via router options (`defaultPreload: 'intent'` = preload on hover)
4. Route context: `beforeLoad` for auth guards/redirects (`throw redirect({ to: '/login' })`)

### 4. Navigation And States

> Goal: navigate + full pending/error UX

1. `<Link to="/posts/$postId" params={{ postId }} search={{ page: 2 }}>` — type-checked for both params+search
2. `useNavigate()` / `router.navigate({ to, params, search })`
3. Per-route `pendingComponent`, `errorComponent`, `notFoundComponent` — router-level error boundaries
4. `router.invalidate()` re-runs loaders after a mutation (or pair with Query in the `loader`)

### 5. Verify

> Goal: routes + types work

1. `/run-dev` — actually navigate every route, `routeTree.gen.ts` regenerates correctly
2. `/run-typecheck` — Link params/search errors must be caught by typecheck
3. Test back/forward, deep-link, 404
4. If it fails → `/resolve-errors` max 3 rounds

## Rules

- File-based or code-based — pick one only; never hand-edit `routeTree.gen.ts`
- Every dynamic segment must be passed via the `params` prop when navigating — the compiler enforces it, don't cast to dodge it
- Search params are the source of truth for UI state that can be shared in the URL (filters, tabs, page)
- Loader data ≠ Query cache — data needing refetch/realtime should use `follow-query` in the component, not the loader
- The `Register` interface is required — without it, type safety is lost across the whole app

## Expected Outcome

- Route tree generates correctly, navigation is type-safe across params+search
- Loaders + pending/error boundaries work
- Deep-link/back-forward don't break
