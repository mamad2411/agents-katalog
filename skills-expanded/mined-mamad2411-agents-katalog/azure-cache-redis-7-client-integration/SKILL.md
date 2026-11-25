---
name: azure-cache-redis-7-client-integration
description: Guides Azure Cache for Redis Enterprise and Enterprise Flash Redis 7 application integration, including connection resilience, key modeling, TTLs, eviction-aware design, batching, pipelining, timeouts, retries, and safe client behavior.
license: MIT
compatibility: Works across languages and frameworks; pair with language-specific plugins for implementation details.
---

# Azure Cache for Redis 7 Client Integration

This skill helps agents review and design application code that uses Azure Cache for Redis Redis 7.2.

## When to Use This Skill

Use it for:

- Redis client configuration.
- Timeouts, retries, reconnects, and circuit breakers.
- Cache-aside, sessions, rate limits, Pub/Sub, Streams, and distributed locks.
- Key naming, TTLs, eviction safety, and value sizing.
- Avoiding expensive commands and production anti-patterns.

## Workflows

- `workflows/client-resilience-review-workflow.md`: Use when reviewing connection handling, timeout, retry, and fallback behavior.
- `workflows/cache-key-modeling-workflow.md`: Use when designing or refactoring key structure, TTLs, value formats, and invalidation.

## Resources

- `resources/client-patterns-checklist.md`: Application integration checklist.

## Examples

- `examples/safe-key-patterns.md`: Key design examples and anti-patterns.

## Guidance

1. Prefer cache-aside for ordinary database acceleration unless the application has a clear reason for another pattern.
2. Every cacheable key should have an intentional TTL unless the data model explicitly requires a no-TTL exception.
3. Avoid large values and unbounded multi-key operations in hot paths.
4. Use `SCAN` for operational discovery, not `KEYS *`.
5. Configure client timeouts, reconnects, retry policy, and backpressure.
6. Treat Redis as a shared dependency that can be unavailable; design graceful degradation.
7. Never log full connection strings, access keys, tokens, or sensitive cached values.
