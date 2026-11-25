---
name: caching-patterns
description: Redis caching strategies, cache invalidation, write-through/write-behind, TTL management, and cache stampede protection. Grok-native with hooks and compound.
when-to-use: When adding or reviewing caching layers (Redis or in-memory) for performance or cost.
---

# Caching Patterns Skill

The patterns that actually work in production for making things faster without making them wrong or expensive to operate.

## Core Patterns

### Cache-Aside (Lazy)
- Read: check cache → miss → load from source → populate cache + return.
- Write: update source → invalidate cache (or update cache).
- TTL always. Invalidation preferred over long TTL when possible.

### Write-Through
- Write: update cache + source in same operation (atomic where possible).
- Good for read-heavy after write.

### Write-Behind (Write-Back)
- Write: update cache immediately, queue the source update.
- Riskier (durability) but great for high write throughput.

### Stampede Protection
- Single-flight / lock on hot key miss.
- Probabilistic early expiration.
- Background refresh for predictable hot keys.

### Invalidation Strategies
- Event-driven (pub/sub on write).
- Versioned keys (append version to key).
- Tag-based invalidation for groups of related data.

## Grok Integration
- Pair with redis-expert agent.
- Record friction when cache caused correctness bugs or stampede.
- on_run_completion can capture hit rate / latency wins or losses.
- Pre-flight: "Have we defined invalidation + TTL + stampede protection for every cache key?"

## Production Contract
- Pre-Flight: know the access patterns and consistency tolerance.
- Ledger for complex multi-layer caching work.
- Friction for every "cache was the source of the bug".
- Compound promotes winning patterns into reusable skills.

These patterns exist because "just add Redis" has bitten every team at least once. Use the contract.