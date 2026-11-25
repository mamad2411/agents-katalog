---
name: redis-7-keyspace-review
description: Reviews Redis 7 key naming, TTL usage, keyspace hygiene, memory growth, static Redis writes, and suspicious use as durable state. Use when inspecting Redis keys, code that writes Redis data, or memory-risk changes.
license: MIT
compatibility: Requires Redis Open Source 7.x context. Static hook script requires Python 3.
---

# Redis 7 Keyspace Review

Use this skill when reviewing Redis key names, TTLs, keyspace memory risk, and Redis write patterns.

## Workflows

- `workflows/keyspace-review-workflow.md`: Use when reviewing Redis key design, TTL policy, memory risk, or code that writes Redis keys.

## Resources

- `resources/keyspace-risk-matrix.md`: Use to classify Redis keyspace risk.

## Examples

- `examples/keyspace-review-findings.md`: Example review output.

## Scripts

- `scripts/redis-7-code-guard.py`: Hook helper for static code scans. Run with `--help` before manual use.

## Review Focus

- Consistent namespaced key names.
- TTL on ephemeral data.
- Bounded collections.
- Avoidance of sensitive identifiers in keys and values.
- Avoidance of Redis as accidental source of truth.
- Memory and eviction impact.
- Safe scan and invalidation patterns.

## Static Hook Guidance

The static hook script uses conservative heuristics. Treat findings as review prompts, not proof. Prefer improving code clarity and Redis helper APIs over bypassing the hook.
