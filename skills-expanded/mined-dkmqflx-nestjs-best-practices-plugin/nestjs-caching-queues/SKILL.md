---
name: nestjs-caching-queues
description: NestJS caching and background-job queue best practices. Use when adding caching or async job processing to NestJS — CacheModule, cache-manager, Redis, or BullMQ/Bull queues. Triggers on CacheModule, @InjectQueue, @Processor, cache TTL, or background jobs.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Caching & Queues

Best practices for two related NestJS performance techniques: **caching** (`@nestjs/cache-manager`, backed by Keyv/Redis) and **background-job queues** (`@nestjs/bullmq`, backed by Redis). Caching avoids recomputing or re-fetching hot data; queues move slow or unreliable work off the request path so HTTP responses stay fast. Both are Redis-backed in production and share the same core concern: predictable behavior under load and failure.

Verified against the NestJS v10/v11 docs (`techniques/caching`, `techniques/queues`). Note the units gotcha: **cache TTLs are in milliseconds** since `@nestjs/cache-manager` v2 / `cache-manager` v5+.

## When to Apply

Reference these rules when:

- Registering `CacheModule` or injecting `CACHE_MANAGER` / using `CacheInterceptor`
- Choosing a cache store (in-memory dev vs. Redis prod via `@keyv/redis`)
- Setting or debugging cache TTLs and cache invalidation
- Deciding whether work belongs inline or in a queue (email, image/video processing, external API calls)
- Wiring `BullModule`, `@InjectQueue`, or a `@Processor` consumer
- Configuring retries/backoff, or scaling workers as a separate deployment

## Rules

| Rule | Impact | Topic |
|------|--------|-------|
| `cache-module-setup` | HIGH | Register `CacheModule` globally; in-memory for dev, Redis for prod |
| `set-sensible-ttl` | HIGH | Always set a TTL (in ms); never leave caches unbounded |
| `cache-keys-explicit` | HIGH | Deterministic, namespaced keys; invalidate on writes |
| `offload-heavy-work-to-queues` | CRITICAL | Move slow/external work off the request path into a queue |
| `idempotent-processors` | CRITICAL | Processors must tolerate retries and duplicate deliveries |
| `retries-and-backoff` | HIGH | Configure `attempts` + exponential `backoff` for transient failures |
| `separate-worker-process` | MEDIUM | Run consumers as a separate process/deployment for scaling & isolation |

## How to Use

1. **Caching first.** Start with `cache-module-setup`, then apply `set-sensible-ttl` and `cache-keys-explicit` to every cached value — a cache without a TTL or an invalidation story is a correctness bug, not just a performance one.
2. **Queues for anything slow or flaky.** Apply `offload-heavy-work-to-queues` to decide what to enqueue, then `idempotent-processors` and `retries-and-backoff` to make the consumer safe to re-run. These two are CRITICAL: BullMQ retries and at-least-once delivery mean a non-idempotent processor will double-charge, double-send, or corrupt data.
3. **Scale out.** Apply `separate-worker-process` when CPU-bound jobs threaten the event loop or you need to scale producers and consumers independently.

Each rule file shows an **Incorrect** and **Correct** example. Prefer BullMQ (`@nestjs/bullmq`) for new projects; Bull (`@nestjs/bull`) is in maintenance mode.
