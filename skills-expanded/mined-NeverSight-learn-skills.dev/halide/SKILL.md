---
name: halide
description: Build Hono-based API and proxy servers with Halide — routing, auth, SPA serving, middleware, OpenAPI, and observability
---

## Overview

Halide is a Hono-based server wrapper that makes it easy to serve a SPA with API routes and proxy support. It handles auth (bearer/JWKS), CORS, CSP, rate limiting, request IDs, and OpenAPI documentation automatically.

## Quick Start

Edit `server.ts` to configure your server:

```typescript
import { createServer, apiRoute, proxyRoute } from 'halide';

const server = await createServer({
  apiRoutes: [
    apiRoute({
      access: 'public',
      handler: async () => ({ status: 'ok' }),
      method: 'get',
      path: '/health',
    }),
  ],
  proxyRoutes: [
    proxyRoute({
      methods: ['get'],
      path: '/api/external',
      target: 'https://api.example.com',
    }),
  ],
  spa: {
    name: 'my-app',
    root: 'dist',
  },
});

await server.start();
```

## Route Configuration

### API Routes

Use `apiRoute()` to create API endpoints:

- `access`: `'public'` or `'private'` (private requires auth config)
- `handler`: async function `(ctx, claims, logger) => response`
  - `ctx` is `RequestContext & { body: TBody }` (plain object, not Hono Context)
  - `claims` is `TClaims | undefined` (populated when access is `'private'`)
  - `logger` is `Logger`
- `method`: `'get'`, `'post'`, `'put'`, `'delete'`, etc.
- `path`: URL path

### Proxy Routes

Use `proxyRoute()` to proxy requests to external APIs:

- `methods`: array of HTTP methods (required)
- `path`: URL path to match
- `target`: base URL to proxy to
- `access`: `'public'` or `'private'`

## Auth

Configure auth in `security.auth`:

```typescript
security: {
  auth: {
    strategy: 'bearer',  // or 'jwks'
  }
}
```

- **bearer**: Uses `hono/jwt` — set `secret` to a string or function returning a string
- **jwks**: Uses `hono/jwk` — set `jwksUrl` to the JWKS endpoint URL

Private routes require `security.auth` to be configured — validation will throw otherwise.

## CSP

Content Security Policy directives use **camelCase** (`defaultSrc`), not kebab-case (`default-src`). The config validator throws on kebab-case.

```typescript
security: {
  csp: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      connectSrc: ["'self'"],
    },
  },
}
```

## SPA

The `spa` config serves static files from a directory. `apiPrefix` defaults to `'/api'` — paths starting with that prefix get 404 instead of the SPA fallback. Set `apiPrefix: ''` to disable.

```typescript
spa: {
  name: 'my-app',
  root: 'dist',
  fallback: 'index.html',
  apiPrefix: '/api',
}
```

## CORS

```typescript
security: {
  cors: {
    origin: ['http://localhost:4200'],
    credentials: true,
    methods: ['get', 'post'],
  },
}
```

CORS wildcard origin (`*`) cannot be combined with `credentials: true` — config validator will throw.

## OpenAPI

Enable OpenAPI documentation with Scalar UI:

```typescript
openapi: {
  enabled: true,
  path: '/swagger',
}
```

## Gotchas

- **Framework**: Hono (not Express). All HTTP types come from `hono`
- **Config**: `ServerConfig` uses separate arrays: `apiRoutes` + `proxyRoutes`, not a single `routes` array
- **CSP**: camelCase directives only (`defaultSrc`), not kebab-case
- **Node.js**: >=24.0.0 required
- **Graceful shutdown**: SIGINT/SIGTERM are handled automatically — `server.stop()` is called before exit
