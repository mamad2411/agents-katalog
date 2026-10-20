# AGENTS.md — `@t/dependency-injection`

## What this owns

DI token registry and Awilix re-exports for the monorepo. Provides the canonical
string keys every `register*DI` function binds to, the Awilix container primitives,
`lifetimeConfig` constants, and the `Container` type alias.

This package does NOT contain registrars or a pre-built composition root — those
live per-package and per-app respectively.

## Layout

```
packages/dependency-injection/src/
  entities/
    dependencyKeys.ts    — canonical token registry (global.* + request.*)
  infrastructure/
    container.ts         — Awilix re-exports + lifetimeConfig + Container type
  index.ts               — public re-export surface
```

## DI registrar / composition root

Each package ships its own `register<Pkg>DI(container, opts)` function. The
composition root in each app calls them in dependency order.

Reference composition root (website):
C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\website\src\lib\composition.ts

Reference composition root (api — full 8-registrar graph):
C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\composition.ts

**Wiring order rule:** `registerConfigRepo` is always first. Every other registrar
receives `config` as an explicit option — never reads `process.env` itself.

**Adding a new token:**
1. Add the string key to `dependencyKeys.global` or `dependencyKeys.request` in
   `dependencyKeys.ts`.
2. Update the token-shape tests in `tests/dependencyKeys.test.ts` (they lock exact
   values and count — they will fail intentionally).
3. Implement `register<Pkg>DI(container, opts)` in the owning package.

## Consumers

Every package and app that registers or resolves services:
`@t/auth`, `@t/config`, `@t/logging`, `@t/analytics`, `@t/db`, `@t/cache`,
`@t/billing`, `apps/api`, `apps/website`.

## Conventions

- **One token per service, owned by one package.** Token strings are stable — renaming
  is a breaking change requiring test + call-site updates.
- **`asValue` for pre-constructed instances** (e.g., config); **`asClass().singleton()`**
  for class-based singletons (e.g., auth, logger).
- **Lifetime default is `SINGLETON`** for global tokens. Use `SCOPED` only for
  request-scoped tokens (currently only `requestAnalytics`).
- **`Container` (not `AwilixContainer<any>`)** is the type used in all registrar
  signatures across the monorepo.
- No `any` on `container.resolve()` — narrow via the token's known type at the
  call site or use a typed helper.

## Token reference (global singletons)

| Token | String key | Owning package |
|-------|-----------|----------------|
| `CONFIG` | `"config"` | `@t/config` |
| `LOGGER_FACTORY` | `"loggerFactory"` | `@t/logging` |
| `LOGGER` | `"logger"` | `@t/logging` |
| `CACHE` | `"cache"` | `@t/cache` |
| `DB` | `"db"` | `@t/db` |
| `USER_REPOSITORY` | `"userRepository"` | `@t/db` |
| `EMBEDDING_STORE` | `"embeddingStore"` | `@t/db` |
| `AUTH` | `"auth"` | `@t/auth` |
| `ANALYTICS` | `"analytics"` | `@t/analytics` |
| `BILLING_REPOSITORY` | `"billingRepository"` | `@t/billing` |

Request-scoped: `REQUEST_ANALYTICS` (`"requestAnalytics"`) — `@t/analytics`.

## Links

- DI architecture: docs/architecture/platform/dependency-injection.md
- Root conventions: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md
- Token source: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\dependency-injection\src\entities\dependencyKeys.ts
