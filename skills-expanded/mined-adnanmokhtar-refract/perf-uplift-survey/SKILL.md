---
name: perf-uplift-survey
description: Survey a feature being ported from V1 to V2 for migration-time performance wins — N+1 queries, missing indexes, unbounded SELECT *, sequential awaits over independent I/O, missing caching, in-app filtering, oversized payloads. Outputs a structured candidate list with cost / saving / parity-preservation argument so each can be decided (applied / deferred / rejected) before V2 ships.
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# perf-uplift-survey

The port is the cheapest moment to apply performance improvements: V2's code is being written anyway; V2's data access is being re-shaped anyway; V1 + V2 cohabitation lets you A/B perf measurements directly. This skill systematises the survey so wins are caught and decided, not improvised.

## Premise

Find real wins, no hand-waves. Every candidate cites V1's offending site (`<v1-path:line>`) and V2's transformation site (`<v2-path:line>`), with a measurement: query count, p95 latency, bytes-on-wire, plan output from `migration-rehearsal`. "This will be faster" without before/after measurement is a hypothesis, not a candidate. Parity preservation is argued per row against the contract's Caller assumptions and Outputs sections — not asserted. New infrastructure (cache layer, parallelism primitive, client wrapper) goes through the V2 anchors check before being added; do not invent a parallel primitive when V2 declares one.

## Halt conditions

- Halt on candidates without V1 + V2 path citations and a measured (or rehearsed) before/after.
- Halt on "applied" rows whose parity tests didn't run pre- and post-change.
- Halt on perf changes that introduce a primitive (per-feature HTTP client instance, per-feature connection pool, hand-rolled cache) when `_v2-anchors.md` declares one for the same concern.
- Halt on contract-breaking perf changes (ordering, nullability, sync→async side effect) without an ADR + caller migration plan.

This skill is the procedural arm of `migration-discipline.md` § "Should — Migration-time perf uplift" + `feature-port.md` Phase 5.

## When to use

- Phase 5 of a per-feature port (after V2 is written + parity tests green; before cutover).
- Re-running on a feature whose V2 shipped but where prod telemetry shows missed perf opportunities.
- Auditing a queue of pending features to estimate aggregate migration-time perf gain (e.g., "if we apply all parity-preserving uplifts, what's the projected p95 reduction?").

## When NOT to use (refuse + explain)

- Before V2 is written — the uplift survey reads V2's plan/code, not just V1's; running it without a V2 design produces speculative recommendations.
- On a feature whose parity tests are not green — the survey assumes parity is a fixed point; uplift on a broken parity baseline produces faster-but-still-broken code.
- As a substitute for the `performance` pack's profile-based audit — this skill catches *migration-time* wins (the ones that are cheap because we're rewriting anyway). Steady-state perf optimisation belongs in the `performance` pack.

## Prerequisites

- Feature has a contract (`ai/migration/contracts/<feature>.md`) — the **Performance characteristics** + **Side effects** sections are read directly.
- V2 implementation exists (or, at minimum, V2's plan with concrete data-access decisions).
- `_extracted-codebase.md § Performance hot paths` + `§ Concurrency primitives` populated.
- Access to: V1 query logs (or `EXPLAIN` against prod-sized data), V1's cache config (Redis / in-process), V1's pool sizes, V1's API client configs.

## Procedure

For each candidate below, examine V1 + V2's plan, classify, and emit a candidate row in `ai/migration/perf-decisions/<feature>.md`.

### 1. N+1 queries

```text
V1 trigger:                                 V2 transformation (parity-preserving):
  for o in orders:                            customer_ids = unique(o.customer_id for o in orders)
    c = getCustomer(o.customer_id)            cust_by_id = getCustomersByIds(customer_ids)  # 1 query, IN clause
    o.customer = c                            for o in orders:
                                                o.customer = cust_by_id[o.customer_id]
```

- Detect: V1's call graph shows a function called inside a loop with each iteration's input being independent.
- Estimate: V1 cost = N round-trips × per-query latency + DB connection holding time. V2 cost = 1 round-trip with `IN` of size N (capped — split into chunks of e.g., 500 if N > 1000 to stay within DB stmt limits).
- Parity: same returned data, just fewer round-trips. Order may differ — assert tolerance is `order_insensitive` or use a dict-lookup pattern.

### 2. Missing or wrong indexes (for V2's query shape)

V2's query shape often differs from V1's because V2 reorganises queries (joins moved, predicates added, sorts added). The pre-existing index on V1 may not cover V2.

- Detect: run `EXPLAIN ANALYZE` on V2's queries against prod-sized data (use `database/skills/migration-rehearsal/SKILL.md`). Look for `Seq Scan` on tables > 10K rows where a `WHERE` clause exists.
- Estimate: V1 with index = O(log N) lookup; V2 sequential scan = O(N). At 10M-row tables this is the difference between 1ms and 1500ms.
- Apply: write a reversible migration (`CREATE INDEX CONCURRENTLY ...` on Postgres; equivalent on other engines). Composite index ordering matters — leftmost columns are the most-selective predicates.
- Parity: same rows returned, faster. Always parity-preserving (no observable change).
- Caveat: index on a write-heavy table costs write latency. Measure both directions before committing.

### 3. Column projection (`SELECT *` → minimal columns)

V1 frequently uses `SELECT *` or full ORM model hydration even when the consumer reads 3 fields. V2 can project minimally.

- Detect: V1's query returns full row → consumer reads `<small subset>`. ORM models with 30+ columns are common in legacy code.
- Estimate: bytes-on-wire reduction (often 70–90%) + ORM hydration CPU + GC pressure (object construction is the hidden cost).
- Apply: V2 returns a DTO with only the consumed columns. Update parity tolerance to `superset` (V1 returned more fields; V2 returns the documented consumed subset; parity test asserts exact match on the documented columns).
- Parity: ONLY parity-preserving if the consumers truly don't read the dropped columns. The contract's **Caller assumptions** section is the authoritative answer — re-check before applying. If any consumer reads a dropped column, this is a contract break (ADR + caller migration plan).

### 4. Caching (the user's specific concern)

Three caching tiers, decide per call site:

| Tier | Use when | Examples |
|---|---|---|
| **Per-request memoisation** | Same lookup happens multiple times within one request | `getUser(id)` called by 5 different handlers in one request — memoise on a request-scoped map |
| **Cross-request in-process cache** | High-frequency, low-staleness-tolerance lookups; data fits in process memory | Feature flag config, currency rates updated hourly |
| **Cross-request distributed cache (Redis / Memcached)** | High-frequency, can tolerate stale-by-TTL, must be shared across replicas | Computed aggregates, expensive joins, session data |

For each call site, capture:
- **Call rate**: requests/sec hitting the underlying source. From V1 telemetry or estimate from feature traffic.
- **Payload size**: average + p95 bytes per cached item. (Affects cache memory budget.)
- **Staleness tolerance**: how stale can the data be? (Sets TTL.) Some data is "tolerable for minutes" (lookup tables); some is "must be live" (account balance) — the latter doesn't cache without an event-driven invalidation rule.
- **Invalidation rule**: TTL-only? Event-driven (on row update)? Both? Document explicitly. Cache without invalidation rule is a bug waiting to happen.
- **Hit-rate projection**: from call-rate + key-cardinality + TTL.

Apply: V2 wraps the underlying source with the cache. Parity tests still hit the underlying source (not the cache) by default — separate cache-enabled tests verify the cache layer is correct.

Reject if: the cached value depends on user-specific authz (cache key must include user/tenant), or the TTL window allows a stale value to violate a business rule (e.g., a price cache with 1h TTL on a feature where prices can change immediately).

### 5. Sequential awaits over independent I/O

(Cross-references `backend/skills/parallelize-independent-ops/SKILL.md`.)

- Detect: V1's call graph shows `for x in xs: await f(x)` where `f`'s arguments don't depend on prior iterations.
- Estimate: wall-clock = N × per-call latency. Parallel wall-clock = max-call latency + bounded overhead. For N=10, p95=100ms each, sequential = 1000ms, parallel = ~120ms.
- Apply: V2 uses bounded parallelism via the project's primitive. Cap = ≤ 8 for HTTP, ≤ pool-size for DB.
- Parity: parity-preserving IF iterations are truly independent (the rule's "data dependency" check). Order of completion may differ — tolerance must be `order_insensitive` if the contract pins order, otherwise tighter.

### 6. In-app filtering / sorting → DB filtering / sorting

```text
V1:                                          V2:
  rows = db.findAll(Orders)                    rows = db.findWhere(Orders, status='ACTIVE')
  active = [r for r in rows if r.active]       # done — DB returned only active rows
```

- Detect: V1 fetches a wide set then filters in app code; or fetches then sorts in app code.
- Estimate: row reduction (often 90%+) + bytes-on-wire + ORM hydration.
- Parity: same rows after filter; faster.
- Apply: push the filter / sort to the DB. Add the index for the filter column if missing.

### 7. Batched inserts / updates

```text
V1: for row in rows: db.insert(row)          V2: db.bulkInsert(rows, chunk_size=500)
```

- Detect: loop with single inserts/updates.
- Estimate: round-trip reduction (commonly 50–100×). Be careful with constraint validation — bulk inserts skip per-row triggers in some ORMs.
- Parity: same data persisted; check trigger / ON CONFLICT semantics carefully.

### 8. Avoid hydrating into ORM models when raw values suffice

```text
V1: users = ORM.find()  # hydrates 30 fields × Python class instance overhead
V2: rows = sql_select_dict('SELECT id, name FROM users WHERE ...')
```

- Detect: V1 hits an ORM.find then immediately maps to a DTO using a few fields.
- Estimate: ORM hydration CPU + memory; can be 5–10× faster on hot paths.
- Parity: ORM-side validation is bypassed — only safe when the contract doesn't depend on it (read paths typically don't; write paths usually do).

### 9. Move synchronous external HTTP off the hot path

```text
V1 hot path: POST /orders → store order → call externalEmail(api) → return 200
V2 hot path: POST /orders → store order → enqueue(emailJob) → return 200
                                                                ↓
V2 background:                                                  → emailJob → call externalEmail(api)
```

- Detect: a hot-path handler does external HTTP synchronously, with a retry/timeout that costs the user request budget.
- Estimate: p95 reduction equal to externalEmail's p95.
- Parity: usually a contract break (the email is now eventually sent rather than guaranteed-before-response). Requires ADR + caller migration if any caller depends on synchronous side-effect ordering.
- Reject if: the side effect MUST land before response (e.g., audit log for compliance). In those cases, accept the latency or use a same-transaction outbox pattern (own ADR).

### 10. Compression / payload shape (API responses)

- Detect: V1 returns a 50KB JSON for a list endpoint; V2's column projection brings it to 5KB. With gzip/br compression, on-the-wire savings are smaller — but the JSON-construction CPU is significant.
- Apply: V2 returns minimal DTOs; enable compression at the framework level.
- Parity: caller assumes `superset` shape; enforce via the contract.

## Output format

`ai/migration/perf-decisions/<feature>.md`:

```markdown
# Perf decisions: <feature>

> Phase: 5 (perf uplift) | Status: in progress / final
> Contract: ai/migration/contracts/<feature>.md
> Run by: <name> | Reviewed by: <name>

## Candidates

### 1. N+1 in customer lookup — APPLIED
- **V1 path**: `Reports/views.py:472-498` — `for o in orders: c = Customer.objects.get(id=o.customer_id)`.
- **V2 transformation**: bulk `Customer.objects.filter(id__in=customer_ids)` then dict-by-id lookup.
- **Cost (V1)**: ~15 queries per request (N=15 typical, max=50). p95 latency contribution: 75ms.
- **Saving (V2 measured)**: 1 query per request. p95 contribution: 8ms. Net savings: 67ms p95.
- **Parity**: order_insensitive on response.customers list (already declared in tolerance.yaml).
- **Decision**: applied in V2 (`<v2-path:line>`).
- **Verification**: parity tests green; before/after p95 measured.

### 2. Missing index on (status, created_at) — APPLIED
- **V1 query**: `WHERE status = ? AND created_at > ?` covered by single-column `(status)` index — leftmost match only.
- **V2 query**: same, but called 5× more frequently due to V2's pagination.
- **Plan rehearsal** (`migration-rehearsal`): without composite index, seq scan on 12M rows, 1800ms; with composite (status, created_at), index scan, 12ms.
- **Migration**: `db/migrations/2026_04_27_orders_status_created_idx.sql` — `CREATE INDEX CONCURRENTLY ...`.
- **Decision**: applied. Reversible via `DROP INDEX CONCURRENTLY` if reverted.

### 3. SELECT * → 4 columns — APPLIED
- **V1**: `SELECT * FROM users` — returns 47 columns; consumer reads 4 (id, name, email, status).
- **V2**: explicit projection.
- **Saving**: ~85% bytes on wire; ~70% ORM hydration CPU.
- **Parity**: response.user is now a 4-field object. Tolerance updated to assert exact match on the 4 documented fields; ignores absence of the other 43 (consumers verified to not read them — see contract's Caller assumptions).
- **Decision**: applied.

### 4. Per-request cache for getUser — APPLIED
- **Detect**: getUser called 7× per request on average across handlers.
- **Cache**: request-scoped Map keyed on userId.
- **Invalidation**: per-request automatic (Map dies with request).
- **Saving**: ~6 queries per request avoided.
- **Decision**: applied.

### 5. Cross-request distributed cache for tax rate — DEFERRED
- **Detect**: getTaxRate(jurisdiction) called per order; rates change infrequently.
- **Plan**: distributed cache (the project's shared-cache primitive), TTL 6h, invalidate on tax-config-update event.
- **Blocker**: shared-cache infra not in V2's stack yet; ETA 2026-05-15.
- **Decision**: deferred until infra lands. Captured here so it isn't forgotten; ledger row notes `deferred-perf` flag.

### 6. Move email send off hot path — REJECTED
- **Detect**: POST /orders synchronously calls the email vendor; p95 contribution 250ms.
- **Plan**: enqueue email job; respond immediately; worker sends.
- **Reject reason**: contract break — current callers expect "if 200 OK, email is sent". Compliance team requires synchronous send for tax-receipt orders. ADR-014 explored async; rejected. Defer indefinitely.

## Summary

- **Applied**: 4 (rows 1, 2, 3, 4)
- **Deferred**: 1 (row 5)
- **Rejected**: 1 (row 6)
- **Aggregate measured saving (applied)**: -73% p95 latency (820ms → 220ms), -82% queries/call (24 → 4), -84% bytes/response.
- **Indexes added**: 1 (composite on orders(status, created_at)).
- **Cache layers added**: 1 (per-request).
- **Parity tests**: green pre-uplift, green post-uplift, green at each candidate's commit.
```

## Anti-pattern: structural perf

The port is not a license to introduce V1-shaped code in V2 under a "perf" label. The most common manifestation is ironic — a "perf cache" is added and lands as a parallel HTTP client instance with its own interceptors (frontend), or a per-feature connection pool that bypasses the canonical client (backend). The cache may be faster; the structure violates V2's layering and is a copy-paste of V1's worst habit.

The validator's `check_v2_structure` catches V1 copy-paste fingerprints — recognisable shapes from V1 root that should not appear under V2 root (e.g., the per-stack fingerprint catalogue lives in `frontend/rules/migration-frontend.md` / `backend/rules/migration-backend.md`). `check_composable_reuse` flags open-coded reusables where the project's shared inventory has one; `check_service_shape` flags direct HTTP-client calls where a service should mediate; `check_lifecycle_keepalive` flags wrong-hook-on-cached-route per the project's anchors.

Before applying any perf candidate that adds new infrastructure (cache layer, parallelism primitive, client wrapper, query helper), check:

1. Does V2's layering already declare a primitive for this concern? (`ai/migration/_v2-anchors.md` lists them.) If yes, extend that primitive — do NOT create a parallel one.
2. Does the perf change land in the same layer the contract assigns the side effect to? A cache moved from "service layer" to "component body" is a layering break dressed as perf.
3. Is the primitive shared across features? A per-feature HTTP client instance for one cached endpoint becomes 30 such instances by the end of the migration; each one is its own refresh-token bug, its own interceptor drift, its own audit failure.

If a perf gain genuinely needs new infrastructure, it's a separate ADR + separate PR, not a smuggled bullet under "perf uplift". Cross-references: see `migration-discipline.md` § "The Buried Perf Improvement" anti-pattern.

## Failure modes

- **Speculative perf claims**: "this is faster" without measurement = noise. Every applied row needs a measured before/after OR a `migration-rehearsal` plan output.
- **Smuggled contract breaks**: a "perf change" that quietly changes ordering / nullability / ID semantics. The parity test should catch it; if the test passes, the test is incomplete — re-extract the contract.
- **Cache-without-invalidation**: TTL-only caching of data that needs immediate invalidation (e.g., user permissions, prices). Flag and reject.
- **Parallelism without bounds**: applying recipe 5 with unbounded `Promise.all` over user-controlled arrays. Always bound per `concurrency-discipline.md`.
- **Index-everything**: indexes are not free — write latency cost. Measure before committing.
- **Optimising the wrong thing**: a 10ms saving in a request whose p95 is 800ms because of one external call. Profile first; optimise where the wall-clock is.
- **Skipping the deferred / rejected list**: discoveries that don't apply are still valuable — they prevent re-rediscovery + inform future work. Always populate the list.

## Related

- `migration-discipline.md` — the rule mandating this survey.
- `feature-port.md` — Phase 5 of the per-feature lifecycle.
- `extract-v1-contract.md` — produces the V1 baseline data this skill consumes.
- `parity-test-generate.md` — the parity tests this skill MUST keep green.
- `backend/skills/parallelize-independent-ops/SKILL.md` — the parallel-I/O recipe (this skill's row 5).
- `backend/rules/concurrency-discipline.md` — the bound + safety rules for parallel I/O.
- `database/skills/migration-rehearsal/SKILL.md` — measures V2 query plans on prod-sized data; output feeds rows 2 + 6.
- `database/agents/query-optimizer.md` — pair-program with this skill on rows 1, 2, 6, 7.
- `performance/_examples/perf-audit.md` — for steady-state perf work after migration; complements but doesn't replace this skill.
