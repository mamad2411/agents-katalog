---
name: "tdsk-proxy"
description: "Knowledge base for the Auth Gateway proxy repo"
tags: ["express", "jwt", "jwks", "proxy", "auth", "gateway", "typescript", "jose", "session", "sandbox"]
---
# Proxy Repo Skill

## Overview

- Auth Gateway and single entry point for all external traffic (`@tdsk/proxy`)
- Triple-auth: JWT (Neon Auth JWKS), API Key (`tdsk_*` Bearer), Session Token (ephemeral, for `/ai/ws`)
- Dual-proxy forwarding: sandbox subdomain proxy (preserves Host) + backend proxy (`/_/*`, `/ai/*`, `/proxy/*`)
- WebSocket upgrade dispatch via manual `onUpgrade` handler (both proxies use `ws: false`)
- Certificate pre-warming for Caddy on_demand_tls, echo endpoint for dev/test

## Directory Structure

```
repos/proxy/
├── configs/              # proxy.config.ts, vitest.config.ts
├── src/
│   ├── constants/values.ts   # PublicRoutes, SessionRoutes, DeferredAuthRoutes, ProxyForwardRoutes, SandboxHostRx
│   ├── endpoints/            # health, echo, auth/me, auth/logout, domains/validate
│   ├── middleware/            # setupServer, setupAuth, setupApiKeyAuth, setupSessionAuth, setupProxy, setupLogger, setupDatabase, setupEndpoints, setupErrorHandler, setupPrewarm, rateLimit.ts, setupRateLimit
│   ├── server/               # app.ts, router.ts (async), server.ts (HTTP/HTTPS + onUpgrade)
│   ├── services/auth.ts      # Auth class — JWKS client, token extraction, JWT verify, route classification
│   ├── types/                # proxy, auth, config, envs, express types
│   ├── utils/                # logger, signals, errors (errorHandler, exception)
│   ├── proxy.ts              # Main orchestrator
│   └── start.ts              # Entry point
└── package.json
```

## Route Constants (`src/constants/values.ts`)

- `PublicRoutes`: `/health`, `/domains/validate`, `/echo`
- `SessionRoutes` / `QueryTokenRoutes`: `/ai/ws`
- `DeferredAuthRoutes`: `/proxy` (auth attempted but not enforced; backend decides per-endpoint)
- `ProxyForwardRoutes`: `/ai`, `/proxy`
- `SandboxHostRx`: `/^\d+--sb-/` (detects sandbox subdomain patterns)

## Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | Public | Service health check |
| GET | `/auth/me` | JWT/API key | Returns decoded JWT user |
| POST | `/auth/logout` | JWT/API key | Logout acknowledgment |
| GET | `/domains/validate` | Public | Caddy domain validation |
| ALL | `/echo` | Public | Echoes request details (dev/test) |
| `/_/*` | (proxied) | JWT/API key | Admin routes → backend |
| `/ai/*` | (proxied) | Session (`/ai/ws`) or JWT/API key | AI routes → backend |
| `/proxy/*` | (proxied) | Deferred | Proxy engine → backend |
| `*` (sandbox subdomain) | (proxied) | Inherits | Sandbox → backend (Host preserved) |

## Middleware Chain Order

Defined in `src/proxy.ts`, wired in this order (11 middleware):
1. **setupLogger** — Request/response logging (skips OPTIONS)
2. **setupServer** — CORS, urlencoded, router mount
3. **setupRateLimit** — Rate limiting: `/auth` routes 20 req/min, `/_` routes 1000 req/min, uses `express-rate-limit` with draft-7 standard headers
4. **setupDatabase** — DB singleton on `app.locals.db`
5. **setupAuth** — JWT via JWKS (skips public + session routes; deferred routes set user but don't reject)
6. **setupApiKeyAuth** — `tdsk_*` validation (skips public + session; attaches `orgId`/`projectId` from key; fire-and-forget `touchLastUsed()`)
7. **setupSessionAuth** — Session token (ONLY `/ai/ws`; accepts Bearer header or `?token=` query param)
8. **setupPrewarm** — Caddy cert pre-warming interceptor
9. **setupEndpoints** — Route registration
10. **setupProxy** — Dual-proxy + WebSocket upgrade dispatch
11. **setupErrorHandler** — Global error handler

After setup, `initServer()` creates HTTP/HTTPS server and registers `onUpgrade`.

## Auth Flow

1. **Public routes** (`/health`, `/domains/validate`, `/echo`) — skip all auth
2. **Session routes** (`/ai/ws`) — skip JWT + API key; require session token (Bearer or `?token=`)
3. **Deferred routes** (`/proxy/*`) — JWT/API key attempted but not enforced; backend checks endpoint `public` flag
4. **All other routes** — JWT or API key required

Each route gets exactly ONE auth mechanism. API key auth sets `req.user` with `userId`, `role` (admin/member/viewer from scope), optional `orgId`/`projectId`, and `apiKeyId`.

## Auth Service (`src/services/auth.ts`)

The `Auth` class manages JWKS-based JWT verification and route classification. Key methods: `isPublic(path)`, `isDeferredAuth(path)`, `isSession(path)`, `usesQueryToken(path)`, `extract(req)` (Bearer header or `?token=` query param), `verify(token)` (maps jose errors to structured `TJWTValidationResult`).

## Dual-Proxy Architecture (`src/middleware/setupProxy.ts`)

**Sandbox forwarder** (`createSandboxForwarder`): Intercepts requests matching `SandboxHostRx`. Uses `changeOrigin: false` to preserve Host header for backend's sandboxProxy middleware. Mounted first so it intercepts before path-based routing.

**Backend proxy** (`createBackendProxy`): Handles `/_/*`, `/ai/*`, `/proxy/*`. Uses `changeOrigin: true`, sets custom `headerKey`/`headerValue` (shared secret), injects `X-User-Id`/`X-User-Role`/`X-User-Email` via `setAuthHeaders()`, enables `xfwd: true`. Returns 502 on proxy errors.

**WebSocket dispatch**: Single `onUpgrade` handler checks hostname — sandbox hosts go to sandbox proxy, all others to backend proxy. Both proxies use `ws: false` to avoid conflicting global upgrade listeners.

## Integration Points

- **Backend**: Dual-proxy forwards requests; `setAuthHeaders()` injects `X-User-*`; `headerKey`/`headerValue` for proxy identity; session tokens forwarded for backend validation
- **Domain**: `setAuthHeaders`, `adminPath`, `hashKey`, `ApiKeyPrefix`, `TApp`, `loadEnvs`, `inKube`
- **Database**: `database()` singleton for API key lookup and domain validation
- **Admin**: Validates JWTs from Neon Auth, CORS allows admin origin

## Config (`configs/proxy.config.ts`)

Five config sections: `server` (port, SSL, origins, certs), `backend` (url, adminPath, headerKey/Value), `logger` (label, level, pretty, silent), `jwks` (jwksUrl), `domains` (prewarmHeader). Backend URL resolved via `backendUrl()` helper supporting K8s service discovery (`inKube()` + `TDSK_BE_DEPLOYMENT`), direct URL, or host+port.

## Commands

```bash
pnpm start    # Dev with watch
pnpm build    # Production build
pnpm test     # Vitest tests (13 test files)
```
