---
name: follow-lib-tanstack-start
description: Use TanStack Start end to end — SSR/streaming, server functions, API routes, middleware, deployment
argument-hint: "[react|solid] [deploy-target]"
related:
  - follow-lib-tanstack-ecosystem
  - run-dev
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Start fully from scaffold to deploy — SSR/streaming, `createServerFn` RPC-style functions, API routes, middleware, deployment adapters

## Scope

Works with React/Solid full-stack apps — SSR routes, server functions, REST endpoints, middleware; supports only React/Solid — Vue/Svelte → Nuxt/SvelteKit; routing details → `follow-router`

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Scaffold Or Install

> Goal: a runnable Start app

1. New → `bunx @tanstack/cli create my-app` (see `use-cli`) or the official starter
2. Existing Vite app → `bun add @tanstack/react-start @tanstack/react-router` + devDeps per the docs
3. `vite.config.ts` uses the Start plugin:

   ```ts
   import { tanstackStart } from '@tanstack/react-start/plugin/vite'
   import viteReact from '@vitejs/plugin-react'

   export default defineConfig({ plugins: [tanstackStart(), viteReact()] })
   ```

### 2. App Shell And Routes

> Goal: hydration shell + file routes

1. `src/router.tsx` → `createRouter({ routeTree })` + `Register` module declaration
2. `src/routes/__root.tsx` — root document: `<html><head><Meta/><Scripts/></head>` + hydration shell + `<Outlet/>`
3. File routes in `src/routes/` per the `follow-router` conventions (`$param`, `_pathless`, `route.tsx` layouts)
4. A route `loader` runs on the server during SSR and on the client during navigate — write it isomorphic-safe

### 3. Server Functions

> Goal: server code callable from the client, type-safe

```ts
import { createServerFn } from '@tanstack/react-start'

export const getTodos = createServerFn({ method: 'GET' })
  .handler(async () => db.todos.findMany())

export const addTodo = createServerFn({ method: 'POST' })
  .inputValidator((data: { title: string }) => data)
  .handler(async ({ data }) => db.todos.create({ data }))
```

1. `.inputValidator()` validates the payload (can use zod/standard schema) — types flow all the way to the client call site
2. The client calls it like a normal function: `await addTodo({ data: { title } })` — Start handles serialization/HTTP
3. Server-only context: `getWebRequest()`, headers, cookies via `@tanstack/react-start/server` helpers (`setResponseHeader`, `getCookie`)

### 4. API Routes And Middleware

> Goal: REST endpoints + request pipeline

1. API routes: `src/routes/api/todos.ts` → `createFileRoute('/api/todos')({ server: { handlers: { GET, POST } } })` for external/webhook consumers
2. Middleware: `createMiddleware()` — a request/response pipeline for auth, logging, rate-limit; can be chained onto server functions
3. Choose correctly: **server functions** = app-internal RPC, **API routes** = external HTTP contract

### 5. SSR, Streaming, Deploy

> Goal: production-ready SSR

1. SSR streaming by default — slow data → deferred/`Await` patterns instead of blocking the whole page
2. Deploy per the adapter in the docs: Node (`bun run build` → `output/`), Cloudflare Workers, Vercel, Netlify — pick the preset/adapter by target
3. Static prerendering: static routes → prerender config in the `tanstackStart()` options

### 6. Verify

> Goal: prove SSR, server functions, and the production build pass before finishing

1. `/run-dev` — view-source shows SSR HTML, hydration doesn't mismatch
2. Actually test the server fn + API route (`curl` the API route, click the UI for the server fn)
3. `/run-typecheck` + production build + run the real output
4. If it fails → `/resolve-errors` max 3 rounds

## Rules

- Never import server-only modules (db clients, secrets) into shared/client code — the bundle will leak; use server functions as the boundary
- Always use `inputValidator` on server functions that take input — it's a trust boundary, like a real API
- Loaders must be isomorphic (run on both server+client) — put server-only code inside a server fn / `serverOnly()`
- Never hand-edit the generated route tree
- Use `/follow-lib-tanstack-ecosystem` for the overview

## Expected Outcome

- The SSR streaming app passes dev/build/deploy
- Server functions + API routes are type-safe, middleware works
- Hydration doesn't mismatch, server secrets don't leak
