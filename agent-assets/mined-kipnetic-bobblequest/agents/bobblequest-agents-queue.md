# @t/queue — Agent Guide

## What this owns

Queue port and BullMQ/InMemory implementations for the persistence layer.
Responsible for: the `QueueClient` port interface, a BullMQ-backed
`BullMQQueueClientImpl` (Redis via ioredis under the hood), and an
`InMemoryQueueImpl` test double.

## Layout

```
packages/queue/
  src/
    entities/
      ports/          QueueClient (interface — enqueue/process surface)
    infrastructure/
      BullMQQueueClientImpl.ts  Real impl — BullMQ worker + queue, Redis-backed
      InMemoryQueueImpl.ts      Test double — in-process, no Redis required
    dependency-injection/
      registerQueueDI.ts   (see DI Registrar below)
  tests/
    infrastructure/
      BullMQQueueClientImpl.test.ts  (mocked Redis transport)
      InMemoryQueueImpl.test.ts
```

## DI Registrar

File: `packages/queue/src/dependency-injection/registerQueueDI.ts`

Signature: `registerQueueDI(container: Container, opts: RegisterQueueDIOptions): void`

Selection logic:
- `environment === 'testing'` — binds `InMemoryQueueImpl` (no Redis required).
- all other environments — requires `config.redis`; constructs `BullMQQueueClientImpl`
  with `config.redis` and a `createGlobalLogger({})` instance. Throws if `config.redis`
  is absent (config hard-fails on missing env).

Exported key: `QUEUE_DEPENDENCY_KEY`
(alias of `dependencyKeys.global.QUEUE` from `@t/dependency-injection`).

Lifetime: singleton — BullMQ workers own long-lived Redis connections;
transient/scoped lifetime would thrash connect/close per request.

## Consumers

Wired by `apps/api/src/composition.ts` — `buildContainer()` calls `registerQueueDI`
alongside `registerDbDI` and `registerCacheDI`. Both the `config` and `environment`
values come from the composition root; `@t/queue` itself performs no `process.env` reads.

## Conventions

- Port-first: consumers depend on `QueueClient`, never on `BullMQQueueClientImpl` directly.
- Both test suites must stay green: BullMQ tests (mocked Redis) AND InMemory tests.
- No raw BullMQ or ioredis leakage outside `@t/queue`; the impl owns connection lifecycle.
- `testTimeout: 10_000` in `vitest.config.ts` — async worker/queue setup in mocked tests.
- Coverage thresholds 100% (statements/branches/functions/lines);
  `src/**/index.ts` and `src/entities/QueueClient.ts` (pure interface) excluded.
- `@t/logging` is a runtime dependency — `BullMQQueueClientImpl` takes a logger at
  construction via the composition root, not via DI container resolution.

## Links

- Architecture doc: `docs/architecture/platform/queue.md`
