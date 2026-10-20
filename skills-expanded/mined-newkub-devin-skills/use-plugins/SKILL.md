---
name: follow-lib-elysia-use-plugins
description: Elysia plugins — @elysiajs/* (openapi, cors, jwt, static, cookie, html, cron), custom plugin authoring
argument-hint: "[plugin]"
related:
  - follow-lib-elysia
  - run-dev
  - resolve-errors
---

## Goal

Use the Elysia plugin ecosystem — `@elysiajs/*` official plugins (openapi/cors/jwt/static/cookie/html/cron/server-timing) + custom plugin authoring

## Scope

plugin usage + authoring — `.use()` composition, plugin prefix/scoping, common integrations; lifecycle internals → `use-lifecycle`

## Execute

### 1. Core Plugins

```ts
import { openapi } from '@elysiajs/openapi'
import { cors } from '@elysiajs/cors'
import { jwt } from '@elysiajs/jwt'
import { staticPlugin } from '@elysiajs/static'
import { html } from '@elysiajs/html'
import { cron } from '@elysiajs/cron'
import { serverTiming } from '@elysiajs/server-timing'

app
  .use(openapi({ documentation: { info: { title, version } } }))   // /openapi + Scalar UI
  .use(cors({ origin: ['https://app.example.com'] }))
  .use(jwt({ name: 'jwt', secret: process.env.JWT_SECRET! }))
  .use(staticPlugin({ assets: 'public', prefix: '/static' }))
  .use(html())
  .use(serverTiming())
```

- `@elysiajs/openapi` — spec + docs UI from schemas + route metadata (`detail: { tags, summary }`)
- `@elysiajs/jwt` — `jwt.sign`/`jwt.verify` in handlers/derive
- `@elysiajs/cron` — scheduled jobs; `@elysiajs/static` — assets; `@elysiajs/html` — JSX/HTML responses

### 2. Auth Pattern (jwt + derive)

```ts
app.use(jwt({ name: 'jwt', secret }))
   .derive(async ({ jwt, cookie: { auth } }) => ({ user: await jwt.verify(auth?.value) }))
   .onBeforeHandle(({ user, set }) => { if (!user) { set.status = 401; return 'unauthorized' } })
```

- Or `macro`/`guard` for per-route auth — see `define-routes` guard

### 3. Custom Plugin Authoring

```ts
const plugin = new Elysia({ name: 'my-plugin', seed: config })
  .decorate('service', svc)
  .derive(() => ({ helper: () => {} }))

app.use(plugin)
```

- Plugin = Elysia instance — `name` required for dedup; `seed` config dedup key
- Scope propagation: hooks/decorators local unless `.as('global'|'scoped')`

### 4. Community Integrations

- `elysia-rate-limit`, `@elysiajs/graphql-yoga`, `elysia-helmet` (security headers)
- DB: `.decorate('db', drizzle(client))` — drizzle → `/follow-lib-drizzle`
- Observability: `@elysiajs/opentelemetry`

## Rules

- `.use()` order matters — cors/openapi before route registration when they must be global
- `name` + `seed` on custom plugins — dedup + instance control
- Secrets via env → plugin options — never hardcode
- Check plugin compat version against the elysia major in use

## Expected Outcome

- Plugins covering the use case (openapi/cors/jwt/static/cron) wired correctly
- Custom plugins named/scoped correctly
