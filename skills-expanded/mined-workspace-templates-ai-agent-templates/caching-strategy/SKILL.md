---
name: caching-strategy
description: Decides what is worth caching, designs keys, TTLs and invalidation, and proves the change with hit rate and latency numbers before and after.
---

# Caching strategy

A cache must earn its place with numbers.

## Steps

1. Measure the target: latency percentiles, requests per minute and how many distinct inputs there are. If the call is already under 20 ms or every request is unique, do not cache; fix the query or index instead.
2. Ask what staleness is acceptable, in seconds, from the product owner or the code's behavior. That number becomes the TTL ceiling.
3. Design the key: `service:entity:version:id:variant`, with every input that changes the result (locale, user role, query params, feature flags). A missing input causes one user to see another's data.
4. Choose the pattern. Cache-aside for most reads. Write-through only when reads must see writes immediately. Add a version number in the key so a deploy can invalidate everything by bumping it.
5. Invalidate on write: delete the key in the same code path that updates the data, after the database commit, not before.
6. Prevent stampedes: for hot keys, take a short Redis lock (`SET key:lock 1 NX PX 5000`) so one worker recomputes, or serve stale while refreshing. Add random jitter of 10 percent to TTLs.
7. Cache absence too, with a short TTL, if missing ids are queried often.
8. Instrument hits, misses and recompute time. Run a realistic load and report the hit rate and p95 before and after.

## Rules

- Never cache anything user-specific under a shared key.
- Never cache errors for longer than a few seconds.
- Never set a TTL of "forever" without an invalidation path.

## Report

What was cached or rejected and why, key format, TTL, invalidation point, and measured hit rate and latency.
