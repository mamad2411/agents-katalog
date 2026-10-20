# @t/cache — Agent Guide

## What this owns

Cache port and Redis/InMemory implementations for the persistence layer.
Responsible for: the `CacheClient` port interface, a Redis-backed `RedisCacheImpl`
(ioredis), an `InMemoryCacheImpl` test double, and `withCacheLock` helper for
distributed locking semantics.

## Layout

```
packages/cache/
  src/
    entities/
      ports/          CacheClient (interface — get/set/del/lock surface)
    helpers/          withCacheLock (distributed-lock utility)
    infrastructure/
      RedisCacheImpl.ts    Real impl — ioredis client, connect/quit lifecycle
      InMemoryCacheImpl.ts Test double — Map-backed, no network
    dependency-injection/
      registerCacheDI.ts   (see DI Registrar below)
  tests/
    infrastructure/   InMemoryCacheImpl.test.ts, RedisCacheImpl.test.ts (mocked)
    registerCacheDI.test.ts
    withCacheLock.test.ts
```

## DI Registrar

File: `packages/cache/src/dependency-injection/registerCacheDI.ts`

Signature: `registerCacheDI(container: Container, opts: RegisterCacheDIOptions): void`

Selection logic:
- `environment === 'testing'` — binds `InMemoryCacheImpl` (no Redis required).
- all other environments — requires `config.redis`; binds `RedisCacheImpl` singleton.
  Throws at construction time if `config.redis` is absent (config hard-fails on missing env).

Exported key: `CACHE_DEPENDENCY_KEY`
(alias of `dependencyKeys.global.CACHE` from `@t/dependency-injection`).

Lifetime: singleton — `RedisCacheImpl` owns a long-lived ioredis connection;
transient/scoped lifetime would thrash connect/quit per request.

## Consumers

Wired by `apps/api/src/composition.ts` — `buildContainer()` calls `registerCacheDI`
alongside `registerDbDI` and `registerQueueDI`. Both the `config` and `environment`
values come from the composition root; `@t/cache` itself performs no `process.env` reads.

## Conventions

- Port-first: consumers depend on `CacheClient`, never on `RedisCacheImpl` directly.
- Both test suites must stay green: Redis tests (mocked transport) AND InMemory tests.
- No raw ioredis client leakage outside `@t/cache`; `RedisCacheImpl` owns the connection.
- `testTimeout: 10_000` in `vitest.config.ts` — covers async Redis mock latency.
- Coverage thresholds 100% (statements/branches/functions/lines);
  `src/**/index.ts` excluded.
- `vitest.integration.config.ts` covers live Redis scenarios (Docker-gated).

## Links

- Architecture doc: `docs/architecture/platform/cache.md`
