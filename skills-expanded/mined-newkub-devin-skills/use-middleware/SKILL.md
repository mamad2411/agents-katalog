---
name: follow-lib-orpc-use-middleware
description: oRPC middleware + auth — use(), context extension, interceptors, error handling, auth patterns
argument-hint: "[scope]"
related:
  - follow-lib-orpc
  - run-test
  - resolve-errors
---

## Goal

Use oRPC middleware — context extension, auth guards, interceptors (onError/onSuccess), shared bases

## Scope

cross-cutting server concerns — `@orpc/server` `middleware()`, `.use()` composition, context typing, auth/ratelimit/logging patterns

## Execute

### 1. Middleware Basics

```ts
import { os, middleware } from '@orpc/server'

const logMiddleware = middleware(async ({ path, next, context }, input) => {
  const start = Date.now()
  const result = await next()
  console.log(`${path.join('.')} ${Date.now() - start}ms`)
  return result
})

const authed = base.use(logMiddleware)
```

- `middleware(fn)` — `{ context, path, input, next, errors, signal, ... }` params
- `next()` returns `{ output }` — wrap around result; `next({ context: {...} })` extends downstream context

### 2. Auth Pattern

```ts
const requireAuth = middleware(({ context, next, errors }) => {
  const user = context.session?.user
  if (!user) throw errors.UNAUTHORIZED()
  return next({ context: { user } })          // narrowed context to the handler
})

const authedBase = implement(contract).$context<Context>().use(requireAuth)
// authedBase.proc uses context.user without re-checking
```

- Context extension = type-level — downstream handler sees extended context
- Short-circuit: throw typed error / return `next()` response early

### 3. Interceptors

```ts
middleware(({ next, onError, onSuccess, onFinish }) => {
  onError(e => report(e))
  onSuccess(() => metrics.ok())
  onFinish(() => cleanup())
  return next()
})
```

- `onError`/`onSuccess`/`onFinish` — observe the lifecycle without breaking the flow

### 4. Shared Bases

- `base = implement(contract).use(mw1).use(mw2)` — proc builders with middleware baked in
- Per-domain bases: `adminBase = base.use(requireAdmin)` — route prefix + guard paired

## Rules

- Middleware composition through `.use()` — order = declaration order
- Extend context via the `next({ context })` return — never mutate the `context` object
- Typed `errors` from the contract are available in middleware too — auth failures = typed errors
- Interceptors are for observability — not control flow

## Expected Outcome

- Middleware chain composable, context typed downstream
- Auth/logging/metrics not duplicated in handlers
