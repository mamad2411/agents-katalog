---
name: redis-7-rate-limit-review
description: Reviews Redis 7-backed API rate limiting, quota enforcement, throttling, abuse protection, atomicity, TTLs, failure behavior, and correctness boundaries. Use when designing or auditing Redis rate limits.
license: MIT
compatibility: Requires Redis Open Source 7.x context. Does not assume a specific application framework or Redis client library.
---

# Redis 7 Rate Limit Review

Use this skill when Redis is used for rate limiting, throttling, quotas, abuse protection, request deduplication, or admission control.

## Workflow

- `workflows/rate-limit-review-workflow.md`: Use for a structured review of Redis-backed rate limits.

## Resource

- `resources/rate-limit-design-checklist.md`: Use to evaluate rate-limit design.

## Example

- `examples/rate-limit-patterns.md`: Language-neutral pattern guidance.

## Review Priorities

- Rate limit role and failure behavior.
- Correctness boundary: rate limit is not the only protection for critical writes.
- Atomicity of counter/token updates.
- TTL and memory bounds.
- Identity key privacy.
- Fairness and algorithm tradeoffs.
- Observability and safe logs.
- Tests for concurrency, timeouts, and retry storms.

## Agent Safety

- Do not encode raw credentials or sensitive identifiers in rate-limit keys.
- Do not rely on rate limiting as an authorization or idempotency substitute.
- Do not add unlimited retries when Redis is slow or unavailable.
- Do not introduce language-specific client APIs unless the repository already uses that client.
