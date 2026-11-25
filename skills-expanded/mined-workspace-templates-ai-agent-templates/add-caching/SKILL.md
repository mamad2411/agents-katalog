---
name: add-caching
description: Adds caching to a hot read path with clear keys, an expiry and invalidation on writes, after proving the path is hot.
disable-model-invocation: true
---

Add caching to: $ARGUMENTS

1. Read the code and its callers. Confirm it is worth caching: estimate how often it is read versus written, and how costly each call is. If it is cheap or write-heavy, say so and stop.
2. Use the cache already in the project. Do not add Redis or a new package without asking.
3. Build the key from every input that changes the result (ids, locale, filters, tenant, user role). Prefix it with a version string so a format change can invalidate everything.
4. Pick a TTL from how stale the data may be, and add jitter so many keys do not expire at once. Protect against a stampede with a lock or request coalescing when the miss is expensive.
5. Invalidate on every write path that changes the source data. List those paths explicitly.
6. Never cache errors or empty results from failures.
7. Add tests for hit, miss, expiry and invalidation, then run them.

Report the key format, TTL, invalidation points and the risk of stale reads.
