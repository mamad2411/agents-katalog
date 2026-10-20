---
name: gcp-spanner-stale-reads
description: >
  Cloud Spanner stale (bounded-staleness / exact-staleness) reads: when to use
  strong vs stale timestamps, max staleness, read-only transactions, performance
  tradeoffs, and correctness pitfalls. Use for owned Spanner databases optimizing
  read latency/throughput without sacrificing documented consistency requirements.
---

# GCP Spanner Stale Reads

## Scope And Authorization

- **In scope:** Owned Spanner instances/databases; authorized performance work.
- **Out of scope:** Unauthorized access to customer Spanner data; destructive load tests
  on production without change control.
- Stale reads can return **older** data — never use for balances, locks, or “read your
  writes” paths without an explicit product decision.
- Redact query results containing PII from notes.
- Pair application code with `code-quality-standards`.

## When To Use

- Read-heavy paths that tolerate seconds (or sub-second) of staleness.
- Reducing leader-driven strong-read load / commit-wait for analytical-ish queries.
- Tuning dashboards, search indexes, caches populated from Spanner.
- Educating engineers on `exact_staleness` vs `max_staleness` vs strong reads.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Spanner schema / interleaving design | schema design skills |
| General DB migration safety | `database-migration-safety` |
| Caching in front of Spanner | `caching-strategies` |
| Observability of latency | `observability-metrics-tracing` |
| Pub/Sub driven eventual consistency | `gcp-pubsub-exactly-once` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Mode | Behavior |
| --- | --- |
| Strong read | Sees all committed data before the read starts; may require replica coordination |
| Exact staleness | Read at a timestamp chosen as `now - interval` (bounded past) |
| Max staleness | Spanner may pick any timestamp within the staleness window (often fresher when possible) |
| Read-only transaction | Multiple reads at one consistent timestamp; can use staleness options |
| Read-write transaction | Strong; use for mutations and read-your-writes |
| Bounded staleness benefit | Often served from closest replica without negotiation to latest |

### Correctness rules of thumb

| Workload | Prefer |
| --- | --- |
| Account balance, inventory decrement check | Strong / R-W txn |
| User profile display, product catalog | Max staleness 5–15s (example) |
| Multi-row report snapshot | Read-only txn + exact or strong |
| Immediately after own write in same client | Strong or use write timestamp |

## Workflow

### 1. Confirm consistency requirements

1. Record instance, database, critical queries, SLO latency, authorization.
2. For each query class, document **maximum acceptable staleness** with product owner.
3. Success: p99 read latency improved; no correctness incidents; metrics show stale read use.

### 2. Inventory current read patterns

```bash
gcloud spanner instances list --project=PROJECT_ID
gcloud spanner databases list --instance=INSTANCE --project=PROJECT_ID

# Schema overview
gcloud spanner databases ddl describe DATABASE \
  --instance=INSTANCE --project=PROJECT_ID
```

In code/APIs, search for:

- Default single-use strong reads
- Read-only transactions without staleness
- Hot keys causing contention on strong reads

Capture baseline: CPU, request latencies, lock wait (if any), QPS by query shape.

### 3. Choose staleness parameters

| Option | Typical use |
| --- | --- |
| `max_staleness = 15s` | UI reads; prefer freshest available within 15s |
| `exact_staleness = 10s` | Repeatable “10 seconds ago” snapshot semantics |
| Strong | AuthZ decisions, financial, post-write read |

Start conservative (small window); widen only with evidence.

### 4. Apply in clients

**SQL (example pattern):**

```sql
-- Exact staleness via timestamp bound (client API usually preferred)
-- Use official client: SingleUse / ReadOnly with TimestampBound
```

**Go client sketch:**

```go
// Read-only transaction with max staleness
ro := client.ReadOnlyTransaction().WithTimestampBound(
    spanner.MaxStaleness(15 * time.Second),
)
defer ro.Close()
// ro.Query(ctx, stmt)
```

**Python sketch:**

```python
# snapshot = database.snapshot(max_staleness=datetime.timedelta(seconds=15))
# results = snapshot.execute_sql("SELECT ...")
```

Guidelines:

1. Do not mix stale snapshot assumptions with subsequent writes without re-read strong.
2. For multi-query consistency, use **one** read-only transaction, not independent
   single-use reads with different timestamps.
3. Document staleness in API docs for downstream consumers.

### 5. Verify correctness and performance

| Test | Expect |
| --- | --- |
| Write then immediate stale read | May miss write within window |
| Write then strong read | Sees write |
| Load test stale vs strong | Latency / CPU improvement on stale path |
| Failover / multi-region | Stale reads still within bound |

```bash
# Monitoring: use Cloud Monitoring Spanner metrics
# api/request_latencies, cpu utilization, transaction metrics
# Tag application metrics: read_mode=strong|stale
```

### 6. Roll out

1. Feature-flag stale path for non-critical endpoints first.
2. Compare error rates and business metrics (stale content complaints).
3. Expand to more queries; keep financial paths strong.
4. Add integration tests that assert “eventual visibility within bound.”

### 7. Hand off

- Runbook: which queries use which bound; how to disable flag.
- Dashboards for read latency by mode.
- Review quarterly whether bounds still match product requirements.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Money paths | Strong reads | Stale “to go faster” |
| Snapshots | One RO txn for multi-query | Multiple independent max-stale reads as one report |
| Tuning | Measure p99 before/after | Guess 1 hour staleness |
| Docs | Bound in code comments + API | Hidden default staleness |
| After write | Strong or session guarantee | Assume stale sees own write |

## Output Checklist

- [ ] Instance/DB and authorization recorded
- [ ] Query classes classified by max acceptable staleness
- [ ] Baseline latency/CPU captured
- [ ] Client code uses explicit TimestampBound / snapshot options
- [ ] Correctness tests for write visibility
- [ ] Performance evidence for stale path
- [ ] Feature flags / rollback documented
- [ ] Metrics labeled by read mode
- [ ] `code-quality-standards` applied

## Rules

- Owned databases only; production load tests under change control.
- Never trade undocumented consistency for latency.
- Prefer max staleness when fresher-is-better; exact when fixed lag required.
- Redact PII in query samples.
- Focus on Spanner stale reads; schema and caching are separate skills.
