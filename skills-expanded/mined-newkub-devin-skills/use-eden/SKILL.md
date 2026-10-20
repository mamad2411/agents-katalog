---
name: follow-lib-elysia-use-eden
description: Eden type-safe client — treaty, fetch, WS subscriptions, type exports for FE
argument-hint: "[mode]"
related:
  - follow-lib-elysia
  - run-typecheck
  - run-test
  - resolve-errors
---

## Goal

Use Eden — the end-to-end type-safe client for Elysia apps — `treaty`, `edenFetch`, WS subscriptions, `App` type export

## Scope

client-side type safety — `@elysiajs/eden` treaty (fetch-based typed client), `eden` helpers; server routes → `define-routes`/`validate-requests`

## Execute

### 1. Export App Type

```ts
// server — export the type, the client imports it (no need to import server code)
const app = new Elysia().get('/users/:id', h).listen(3000)
export type App = typeof app
```

### 2. Treaty Client

```ts
import { treaty } from '@elysiajs/eden'
import type { App } from './server'         // type-only import

const api = treaty<App>('localhost:3000')
const { data, error } = await api.users({ id: '1' }).get()
const { data: created } = await api.users.post({ name: 'x' })
```

- `treaty<App>(url)` — path-chained calls mirror routes; `data`/`error` discriminated result (doesn't throw)
- Params: `api.users({ id }).get()`; body: `.post(body)`; query: `.get({ query: {...} })`; headers: `.get({}, { headers })`
- `error.value` is typed from the `response` schemas — typed error handling on the client

### 3. Eden Fetch (low-level)

```ts
// treaty(...).fetch — fetch-compatible escape hatch for edge cases
const res = await api.users({ id: '1' }).get({ fetch: { credentials: 'include' } })
```

- fetch options (credentials, headers, signal) go through the `{ fetch: {...} }` param

### 4. WS Subscriptions

```ts
const chat = api.chat.subscribe()
chat.on('message', ({ data }) => { /* typed messages */ })
chat.send(msg)
chat.close()
```

- WS routes → typed subscriptions via treaty — `subscribe`, `on('message'|'open'|'close')`, `send`

### 5. Response Type Requirements

- Eden inference needs `response` schemas — add a `response:` key on every route the client consumes
- File uploads: `t.File` fields → treaty `.post({ file })` auto multipart

## Rules

- `treaty` preferred — full path/method inference; the fetch escape hatch when needed
- Import `type App` only — never let server code leak into the client bundle
- `data`/`error` destructured pattern — never try/catch (treaty doesn't throw by default)
- Response schemas complete = client types complete — missing `response` schemas leave the client types unknown

## Expected Outcome

- Client calls typed end-to-end (params/body/query/response/errors)
- WS subscriptions typed; no manual API types
