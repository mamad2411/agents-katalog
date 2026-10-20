---
name: follow-lib-elysia-define-routes
description: Elysia routing — methods, params/wildcards, path types, groups/prefix, macro, mount, WebSocket routes
argument-hint: "[scope]"
related:
  - follow-lib-elysia
  - run-dev
  - run-test
  - resolve-errors
---

## Goal

Design Elysia routes completely — HTTP methods, path params/wildcards, route groups, `.mount` sub-apps, macros, WebSocket routes

## Scope

routing surface — `app.get/post/put/delete/...`, path typing, `.group` prefix, `.guard`, `.macro`, `.mount`, `.ws`; request validation → `validate-requests`; lifecycle hooks → `use-lifecycle`

## Execute

### 1. Route Basics

```ts
import { Elysia } from 'elysia'

new Elysia()
  .get('/', () => 'hello')
  .post('/users', ({ body }) => body)
  .get('/users/:id', ({ params }) => params.id)         // typed params
  .get('/files/*', ({ params }) => params['*'])          // wildcard
  .get('/opt/:id?', ({ params }) => params.id)           // optional param
  .listen(3000)
```

- Methods: `get`/`post`/`put`/`patch`/`delete`/`options`/`head`/`all`/`ws`
- Handler signature: `({ params, body, query, headers, cookie, set, request }) => value`
- Return types auto: object→JSON, `Response`→raw, `file()`/`stream` support

### 2. Path Params And Types

- `:param` typed as string by default — validate/transform via the `params` schema (TypeBox/Standard Schema)
- `* wildcard`, `:param?` optional, custom path types — params inferred into the handler
- `set.status`/`set.headers` — response control inside the handler

### 3. Groups, Guards, Mount

```ts
new Elysia()
  .group('/api', app => app
    .get('/a', () => 'a')            // /api/a
    .guard({ isAuth: true }, g => g  // scoped guard
      .get('/b', () => 'b')))
  .mount('/sub', subApp.fetch)       // or .use(subApp) an Elysia sub-app
```

- `.group(prefix, app => ...)` — path prefix + scoped hooks/schemas
- `.guard(schemas|options)` — apply validation/hooks inside the block only
- `.use(plugin)`/`mount` — compose sub-apps; instance isolation via `.use()` semantics (prefix per instance)

### 4. WebSocket Routes

```ts
.ws('/chat', {
  message(ws, msg) { ws.send(msg) },
  open(ws) {}, close(ws) {},
})
```

- `ws` route — `message`/`open`/`close`/`drain` handlers; Bun-native WS
- Body validation works for ws messages too

## Rules

- Handler return = response body — use `set.status`/`set.headers` for status/headers
- Path params typed+validated via schema — don't trust the raw string
- `.group` for prefixes; `.guard` for scoped constraints — never duplicate prefix strings
- WS uses `.ws()` — not a manual upgrade

## Expected Outcome

- Routes cover methods/params/wildcards/groups in the right pattern
- Sub-app composition + WS routes work
