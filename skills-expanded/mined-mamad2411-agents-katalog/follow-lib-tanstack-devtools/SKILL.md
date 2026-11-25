---
name: follow-lib-tanstack-devtools
description: Set up TanStack Devtools — Query, Router devtools integration
argument-hint: "[framework]"
related:
  - follow-lib-tanstack-ecosystem
  - resolve-errors
  - follow-tool-vite-devtools
---

## Goal

Set up TanStack Devtools to inspect the Query cache, Router state, and other libraries in dev mode

## Scope

Use when configuring devtools for TanStack libraries — Query devtools, Router devtools, or the unified `@tanstack/devtools` panel — dev-only, no impact on the production bundle

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Read Current Config

> Goal: check the existing TanStack libraries and devtools

1. Check `package.json` for installed `@tanstack/*-query`, `@tanstack/*-router`, or other libraries
2. Check the entry point for an existing devtools component — if present → merge config, never overwrite
3. If no TanStack library is found at all → stop and do the `/follow-lib-tanstack-ecosystem` setup first

### 2. Install Devtools

> Goal: install devtools as a dev dependency

1. Query: `bun add -D @tanstack/react-query-devtools` (or `solid-query-devtools`, `vue-query-devtools` per framework)
2. Router: `bun add -D @tanstack/react-router-devtools` (or `@tanstack/solid-router-devtools`)
3. Unified panel: `@tanstack/devtools` + a plugin per library — see the official docs at `https://tanstack.com/devtools` for the latest package names
4. Always install into `devDependencies` — devtools is not a runtime dependency

### 3. Integrate Devtools Component

> Goal: render devtools in dev mode only

1. Query: render `<ReactQueryDevtools initialIsOpen={false} />` inside `QueryClientProvider`
2. Router: render `<TanStackRouterDevtools />` beside `RouterProvider`
3. Guard with a dev check such as `import.meta.env.DEV` or `process.env.NODE_ENV !== 'production'` if the bundler doesn't tree-shake devtools automatically
4. Use a lazy/dynamic import for devtools so it stays out of the production bundle:

   ```ts
   const Devtools = import.meta.env.DEV
     ? lazy(() => import('@tanstack/react-query-devtools').then(m => ({ default: m.ReactQueryDevtools })))
     : () => null
   ```

### 4. Verify

> Goal: confirm devtools works and doesn't leak into production

1. Run the dev server — the devtools panel must open and show the cache/route state
2. Run a production build and check the bundle — devtools code must not be in the output (do `/deep-review-codebase` if confirmation is needed)
3. On failure → revert the part just changed, then do `/resolve-errors`

## Rules

- Always install devtools into `devDependencies`
- Never render devtools in production — guard with an env check or a lazy import
- Never overwrite unrelated existing config — merge only
- The devtools must be positioned inside the provider it inspects (QueryClientProvider, RouterProvider)
- Use `/follow-lib-tanstack-ecosystem` for the overview

## Expected Outcome

- The devtools panel shows the Query cache and Router state in dev mode
- The production bundle contains no devtools code
- The existing config is not clobbered
