---
name: follow-lib-orpc-define-procedures
description: oRPC procedures + router impl — os/os.contract, context, middleware, lazy loading, implement()
argument-hint: "[scope]"
related:
  - follow-lib-orpc
  - run-test
  - resolve-errors
---

## Goal

Implement oRPC procedures + router — `implement(contract)`, procedure builder `os`, context injection, middleware chaining, lazy routers

## Scope

server-side implementation — procedures, context types, middleware, router assembly; contract design → `define-contracts`; serving → `serve-openapi`/adapters

## Execute

### 1. Implement Contract

```ts
import { implement } from '@orpc/server'

const pub = implement(contract).$context<Context>()   // typed context required

export const router = pub.router({
  getUser: pub.getUser.handler(async ({ input, context, errors }) => {
    const user = await context.db.users.find(input.id)
    if (!user) throw errors.NOT_FOUND({ data: { id: input.id } })
    return user
  }),
})
```

- `implement(contract)` — builder bound to contract (types enforce handler signature)
- `errors.NOT_FOUND({ data })` — typed error throw matching contract `.errors()` map
- `os` (non-contract) — procedure builder without a contract: `os.input().output().handler()`

### 2. Context And Middleware

```ts
const requireAuth = middleware(({ context, next, errors }) => {
  if (!context.user) throw errors.UNAUTHORIZED()
  return next({ context: { user: context.user } })  // extend context downstream
})

const authed = pub.use(requireAuth)
```

- `context` injected per-request — typed via `$context<Context>()`
- `.use(middleware)` — compose; middleware can extend context + short-circuit
- `onError`, `onSuccess`, `onFinish` interceptors in middleware options

### 3. Router Composition

- `pub.router({...})` — nested paths auto-prefix
- `implement(contract).lazy(() => import('./heavy-router'))` — lazy-load sub-routers (cold start)
- Merge routers: `os.router({ a: routerA, b: routerB })`

### 4. Handler Utilities

- `input`/`output` auto-validated per the contract schemas
- `event`/`signal` — request signal, headers access via context adapter
- Streaming: `eventIterator` types (`@orpc/server` event iterator responses)

## Rules

- Typed errors throw via `errors.KEY` — never raw `throw` for declared errors
- Middleware extends context through `next({ context })` — never mutate the context directly
- Contract impl must cover every proc — a missing handler = type error (good)
- `$context<Context>` is declared at implement time — the context shape must match the serving adapter

## Expected Outcome

- Handlers fully implement the contract, context/middleware typed
- Errors declared + typed — the client can consume them type-safely
