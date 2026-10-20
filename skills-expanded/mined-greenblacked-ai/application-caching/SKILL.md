---
name: application-caching
description: "Design or review runtime application-data caching where correctness, isolation, or origin protection matters. Use when adding cache-aside or read-through caching, choosing cache keys and freshness rules, fixing stale reads or a late stale-fill race, preventing tenant or authorization leaks, handling negative entries, coalescing misses, planning cache-outage behavior, or making a cache rollout and rollback safe. Produces an explicit source-of-truth and staleness contract, key schema, read/write ordering, race defense, failure policy, and measurements. Do not use for CI dependency or build caches (ci-pipeline-design), LLM prompt-cache economics (llm-cost), general traffic and resource sizing (capacity-planning), or API response semantics (api-design)."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Application Caching

A cache is a copy with a failure policy. Its hit rate matters only after the copy cannot cross a tenant boundary, revive an old value, or turn a cache outage into an origin outage.

## Scope

Use this skill for runtime copies of application data: in-process caches, shared key-value stores, memoized reads, computed results, and negative entries. Review both a proposed design and an existing implementation.

Keep adjacent work with its owner: CI and build caches belong to `ci-pipeline-design`; LLM prompt caching belongs to `llm-cost`; fleet sizing belongs to `capacity-planning`; HTTP cache contracts belong to `api-design`; personal-data inventory and deletion obligations belong to `data-privacy`.

## Hard gates

Do not approve the cache until all four statements are concrete:

1. **Authority:** name the source of truth and whether reads may bypass it.
2. **Freshness:** state the maximum acceptable age per operation and what happens when it cannot be met.
3. **Isolation:** show that the key and lookup path preserve tenant and authorization boundaries.
4. **Publication:** show why an older in-flight load cannot overwrite a newer value.

A TTL answers when an entry may expire. It does not prove any of these statements.

## Workflow

### 1. Write the correctness contract

For every cached operation, record:

| Decision | Required answer |
| --- | --- |
| Source of truth | The database, service, or immutable object that owns the value |
| Allowed staleness | A duration or “none,” tied to a user or business consequence |
| Read guarantee | Strong, bounded-stale, read-your-writes, or best effort |
| Failure behavior | Bypass, serve stale, fail closed, or reject with backpressure |
| Invalidators | Every write, policy change, deletion, and upstream event that changes the answer |

Separate operations that look similar but carry different risk. A product description may tolerate minutes; account suspension, entitlement removal, and balance checks often cannot. If the team cannot state an acceptable stale result, do not cache that result yet.

Treat TTL as cleanup and a bound only when the contract explicitly permits that bound. Clock skew, delayed invalidation, eviction, and a stale refill can all make observed behavior differ from the intended TTL story.

### 2. Design the key as a security boundary

Write the key schema before code. Include every dimension that can change the returned bytes:

- tenant or organization;
- resource identity and source version;
- authenticated subject, role, scope, or policy version when authorization changes the result;
- locale, currency, feature cohort, fields, format, and schema version;
- canonicalized query inputs whose meaning affects the representation.

Prefer caching an authorization-independent object and checking access on every request. If the cached value is already filtered, its key must include the full authorization context or a stable policy generation. “User id is present” is insufficient when roles, grants, or organization membership can change.

Do not concatenate ambiguous user input. Use a canonical encoding, length-prefixing, or a structured hash so two input tuples cannot collide. Keep secrets and raw personal data out of observable key names; hash identifiers when operational visibility does not require them.

Review bulk invalidation and deletion by tenant as well as point lookup. A key nobody can enumerate may make a privacy deletion or incident containment plan impossible.

### 3. Trace hit, miss, and write ordering

Draw the actual sequence for a hit, a miss, a source error, and a mutation. For cache-aside reads:

1. Read the cache.
2. On a miss, read the source of truth.
3. Publish only if the loaded version is still current.
4. Return according to the freshness contract.

For a mutation, commit the source of truth before publishing or invalidating the cache. Invalidating first creates a window where a miss reloads the old committed value. Treat a cache update failure after the source commit as an explicit partial failure: retry from an outbox or change log, invalidate conservatively, or let a permitted short TTL bound it.

Never make source commit depend on a best-effort cache write unless the cache is intentionally part of the authoritative transaction and has matching durability semantics.

### 4. Defeat the late stale-fill race

Deletion alone is not enough. This interleaving is wrong even when every call succeeds:

1. Reader A misses and loads version 7 from the source.
2. Writer commits version 8 and deletes the cache entry.
3. Reader A finishes late and blindly stores version 7.

Use a mechanism that consults a shared generation advanced by every authoritative mutation. Tie advancing that generation reliably to the source commit, make readers discover the current generation, and retain it independently of evictable cached values. Then, at publication time:

- put the source version or a monotonic generation in the key, and move readers to the new generation after commit;
- compare-and-set only if the cached or authoritative generation still matches what the load observed;
- combine lease fencing with the source generation, rejecting a publication whose loaded source generation is not current;
- consume ordered change events and make application of older versions conditional.

The check and publication must be atomic with respect to the persistent shared generation being checked. Deleting or evicting a value must not delete the generation, and restore or reset behavior must preserve monotonic ordering. A process-local check followed by an unconditional shared-cache `SET` preserves the race.

A mutex or distributed lock can reduce duplicate loads, but it does not by itself prove freshness. Lease fencing orders holders, not source mutations: a loader can acquire a newer token while holding an old snapshot. A lease can also expire while a slow loader continues. Require both an authoritative source-generation check and ownership fencing when late publication is harmful. Do not add distributed locking when an idempotent versioned publish, a database check, or harmless duplicate work is simpler.

Read [race controls](references/race-controls.md) when choosing CAS, generations, leases, or fencing for a concrete cache.

### 5. Define negative caching separately

Cache “not found” only when absence has its own acceptable staleness. Use a distinct typed value so absence cannot be confused with a cache miss or transport error.

Use a shorter TTL than for stable positive values unless the creation model proves otherwise. Invalidate the negative entry when an object is created, restored, imported, or becomes visible through a policy change. Do not negative-cache authorization failures across subjects, and do not turn source timeouts or malformed responses into “not found.”

Add admission limits for attacker-controlled identifiers. Negative caching can protect the source from repeated misses, but an unbounded stream of unique keys consumes the cache and can evict useful entries.

### 6. Choose stampede control from the load shape

Estimate concurrent misses for one key and the source cost of each load. Then choose the smallest control that meets the failure policy:

- process-local singleflight for duplicate work inside one instance;
- a short shared lease when duplication across instances would overload the source;
- refresh-ahead for hot predictable keys;
- stale-while-revalidate only when the freshness contract permits serving stale data;
- request admission or bounded queues when the origin cannot absorb miss traffic.

For any lease, specify duration, owner identity, renewal, release, waiter timeout, and behavior when the holder dies. Add jitter to expirations so unrelated keys do not become misses together. Cap waiters and retries; coalescing that creates an unbounded queue only moves the outage.

Not every workload needs coalescing or a distributed lock. Low concurrency, cheap origins, naturally versioned immutable objects, and keys with little reuse may be safer without either.

### 7. Design cache-outage behavior

Test complete outage, high latency, partial timeouts, and mass eviction. A cache is often installed to protect an origin, so unconditional bypass during an outage can remove that protection precisely when all callers miss.

Set short cache timeouts relative to the request budget and bound cache retries. Limit concurrent fallbacks to the source, apply per-tenant admission, and shed optional work before the origin saturates. Serve stale only for entries and operations whose contract allows it; fail closed for authorization or safety decisions when stale data could grant access or cause harm.

Use circuit breaking as a load-control decision, not as proof that data is fresh. Record separately whether the response was a hit, source fill, stale fallback, rejection, or error.

Read [failure and rollout](references/failure-and-rollout.md) before choosing outage fallback, capacity headroom, or rollback steps.

### 8. Measure usefulness and correctness

Segment metrics by operation and key class. At minimum collect:

- request, hit, miss, negative-hit, stale-serve, fill, rejected-fill, and eviction counts;
- cache and source latency distributions, including timeout counts;
- entry age at serve and version lag from the source;
- fill concurrency, coalesced waiters, lease expiry, and origin fallback concurrency;
- cache memory, item size, admission, eviction reason, and hot-key concentration;
- source load and error rate during normal operation, cold start, and cache impairment.

An aggregate hit ratio can hide a useless large-object cache, a tenant with zero hits, or a hot key masking broad churn. Measure saved source work and latency by class, then compare it with cache cost and correctness incidents.

Set memory and item-size budgets from the working set. Confirm the eviction policy matches the access pattern, and exercise eviction under load; a nominal TTL does not guarantee an item remains resident until expiry.

### 9. Roll out and roll back without a miss storm

Start with shadow reads or a small cohort, comparing cached answers with the source where it can safely tolerate the comparison, and track mismatches by reason and version rather than as a count. Ramp by tenant or stable cohort while watching source headroom, and pre-warm only the bounded hot set you can identify from evidence — not the whole source as a rollout ritual.

Treat rollback as a traffic plan, not a cache flush: stop suspect fills first, keep known-good entries and reader compatibility across the window, and open bypass only at the source's measured miss capacity. Rehearse cold-cache recovery and know how long the origin can sustain it.

## Output format

Return a review or design with these sections:

1. **Correctness contract** — authority, freshness, read guarantee, and failure behavior per operation.
2. **Key schema** — dimensions, encoding, sensitivity, and invalidation reach.
3. **Sequences** — hit, miss, mutation, source error, and late-fill interleavings.
4. **Race control** — shared version, CAS, generation, or fencing rule and its atomic boundary.
5. **Failure controls** — negative caching, stampede policy, outage fallback, and backpressure.
6. **Evidence** — metrics, fault tests, mismatch checks, and source capacity assumptions.
7. **Rollout** — cohort ramp, compatibility window, rollback order, and cold-cache limit.
8. **Findings** — severity, affected operation, concrete failure, evidence, and required change.

## Review failures to call out

**TTL presented as consistency.** Expiration limits residence under some conditions; it neither orders a write against an in-flight fill nor proves an authorization change is visible.

**Tenant omitted from a key.** Identical resource ids across organizations can return another tenant's representation. Treat this as a security defect, not a tuning issue.

**Delete after write with blind refill.** The common mutation ordering still permits a reader that loaded before deletion to restore the old value afterwards.

**Cache outage means unlimited bypass.** Every request reaches an origin sized for cache-hit traffic, so a cache incident becomes a database incident.

**One hit-rate target.** It rewards caching cheap hot values and says nothing about source work saved, tail latency, stale serves, or tenant fairness.
