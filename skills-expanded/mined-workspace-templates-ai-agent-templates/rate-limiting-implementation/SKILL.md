---
name: rate-limiting-implementation
description: Adds token bucket rate limits per API key or user, with a shared store, correct 429 responses and RateLimit headers, and tests for the edge cases.
---

# Rate limiting implementation

Decide who is limited, by how much, and where the counter lives.

## Steps

1. Choose the key per route: API key or user id for authenticated routes, IP plus account name for login, IP only for anonymous public routes. Check how the real client IP arrives behind your proxy (`X-Forwarded-For` is spoofable unless the proxy overwrites it).
2. Choose budgets from data. Read access logs for the 99th percentile of requests per client per minute and set the limit above it. Give expensive routes (search, export, login) their own lower limits.
3. Implement a token bucket: capacity is the burst, refill rate is the sustained rate. Store tokens and the last refill time under the key in Redis and update them in one Lua script or atomic command; read-then-write races let bursts through.
4. Set a TTL on the keys equal to the time to refill from empty, so memory does not grow.
5. On rejection return 429 with `Retry-After` in seconds and the problem body your API already uses. On success send `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset`.
6. Decide the failure mode when the store is unreachable. Fail open for general API traffic; fail closed for login.
7. Test: burst up to capacity passes, the next request gets 429, waiting one refill interval restores one token, and two keys do not affect each other.

## Rules

- Never trust a client-supplied header as the identity.
- Never use a fixed window counter for strict limits; it allows double the rate at the window boundary.
- Never log full API keys.

## Report

Keys and budgets per route, store and script, failure mode chosen, and tests added.
