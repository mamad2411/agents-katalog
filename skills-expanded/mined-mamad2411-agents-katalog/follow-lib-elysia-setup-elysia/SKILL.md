---
name: follow-lib-elysia-setup-elysia
description: Install Elysia — bun add, app.listen, routes, basic plugins
argument-hint: "[scope]"
related:
  - follow-lib-elysia
  - use-bun-native-api
  - run-install
  - run-dev
  - resolve-errors
---

## Goal

Install and configure Elysia on Bun — `new Elysia()`, `.listen()`, routes and basic plugins

## Scope

Use when setting up an Elysia API for the first time — covers install, app instance, routes, schema validation and basic plugin registration (Bun runtime only)

## Execute

### 1. Install Elysia

> Goal: install Elysia on the Bun runtime

1. Install with `bun add elysia` or create a new project with `bun create elysia app`
2. Install `bun add @elysia/eden` if you want end-to-end type safety
3. If already present → only verify the version in `package.json` (idempotent)
4. Use Bun as the runtime only — do `/use-bun-native-api`
5. Use `bun --hot` for hot reload in dev

### 2. Create App Instance

> Goal: create `new Elysia()` and `.listen()`

```ts
import { Elysia } from 'elysia'

const app = new Elysia()
  .get('/', () => 'Hello Elysia')
  .listen(3000)
```

1. Create one instance per app — methods can be chained
2. `.listen(port)` starts the server — use `Bun.serve` only through `.listen()`
3. Export `type App = typeof app` if using the Eden client

### 3. Define Routes And Validation

> Goal: basic routes with schema validation

1. HTTP verbs: `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`; params via `/users/:id`; wildcards `/*`
2. `.group('/api', app => app...)` for prefix grouping
3. Validation with `Elysia.t` (TypeBox) in route options: `body`, `query`, `params`, `response`
4. Standard Schema (Zod/Valibot/ArkType) works if the project already uses it — do `/follow-lib-zod` if using Zod
5. `context.status(code, value)` for type-safe status codes (v1.4)

### 4. Register Plugins

> Goal: use `.use()` and basic plugin patterns

1. `.use(plugin)` registers a plugin — declare dependencies clearly (main must `.use()` first)
2. `.decorate()` injects properties into the context; `.state()` injects mutable state
3. `.guard()` for scoped validation; `.scope()` controls merge behavior
4. Split logic into small reusable plugins

### 5. Verify

> Goal: smoke test the API endpoints

1. Run `bun --hot src/index.ts` or `bun run dev` — the server starts on the specified port
2. `curl` or open the endpoint to test the response and validation (an invalid body must return 422)
3. If broken → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Bun runtime only — Elysia doesn't support Node.js as a primary target
- Create a single instance — chain `.use()`/routes on the same instance
- Use `Elysia.t` as the default validator — Standard Schema only when the project already uses it
- Route order: static paths before dynamic paths
- Use `/follow-lib-elysia` for the full reference, lifecycle hooks and version notes
- Use `/run-install` when other dependencies must be installed alongside
- Use `/run-dev` when running the project's dev server that already has scripts set up

## Expected Outcome

- Elysia server runs on Bun with routes and validation
- Plugins registered correctly with `.use()`
- Smoke test endpoints pass
