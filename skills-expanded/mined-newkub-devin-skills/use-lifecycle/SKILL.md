---
name: follow-lib-elysia-use-lifecycle
description: Elysia lifecycle hooks — onRequest→derive→beforeHandle→afterHandle→onError→onResponse, derive/decorate, guard scope
argument-hint: "[hook]"
related:
  - follow-lib-elysia
  - run-test
  - resolve-errors
---

## Goal

Use Elysia lifecycle hooks fully — request pipeline order, `derive`/`decorate`/`resolve`, error handling, scoped/global hooks

## Scope

lifecycle — `onRequest`, `parse`, `transform`, `beforeHandle`, `afterHandle`, `mapResponse`, `onError`, `onResponse`, `onStart`/`onStop`; `derive` (per-request), `decorate` (app state), `resolve` (derived+validated), `as` scope control

## Execute

### 1. Lifecycle Order

```
onStart → (server up)
per-request: onRequest → parse → transform → beforeHandle → [handler] → afterHandle → mapResponse → onResponse
errors: onError (validation/handler errors) ; onStop (shutdown)
```

### 2. Hook APIs

```ts
app
  .onRequest(({ request }) => { /* earliest — before parse */ })
  .onParse(({ request, contentType }) => customParser)
  .onTransform(({ body, params, query, headers }) => { /* mutate pre-validation */ })
  .onBeforeHandle(({ set }) => { set.status = 401; return 'nope' })   // short-circuit
  .onAfterHandle(({ response }) => { /* post-process response */ })
  .mapResponse(({ response }) => new Response(modified))
  .onResponse(() => log())
  .onError(({ code, error, set }) => code === 'VALIDATION' ? { detail: error } : error)
  .onStop(() => cleanup())
```

- Return value from `beforeHandle`/`onError` = short-circuit response
- `code` in onError: `VALIDATION`, `NOT_FOUND`, `PARSE`, `INTERNAL_SERVER_ERROR`, `UNKNOWN`, custom named errors

### 3. derive, decorate, resolve

```ts
app
  .decorate('db', dbClient)                       // app-level singleton
  .derive(({ headers }) => ({ user: auth(headers.authorization) }))  // per-request derived
  .resolve(({ cookie }) => ({ session: loadSession(cookie) }))       // derived + can validate
```

- `decorate` — shared services (db, logger); `derive` — per-request computed context (cheap, no validation)
- `resolve` — like derive but after validation, can short-circuit (return value → response, e.g. 401)

### 4. Scoped Hooks And Guards

- Hooks default = **local** (the instance that defines them) — `.as('global')` / `.as('scoped')` propagate to `.use()` consumers
- `guard({ beforeHandle: fn, schema keys })` — apply inside the block only
- Plugin pattern: `new Elysia({ prefix }).derive().onError()` self-contained → `.use(plugin)`

## Rules

- Order fixed — derive/transform before validation, beforeHandle after validation
- `resolve` for auth-style short-circuit; `derive` for pure computed context
- Hooks local by default — use `.as('global')` carefully (leak semantics)
- `onError` central error format — never try/catch per handler everywhere

## Expected Outcome

- Pipeline hooks in the right order — auth/derive/short-circuit work
- `decorate`/`derive`/`resolve` used with the right scope
