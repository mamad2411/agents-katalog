---
name: cassandra-consistency-tuning
description: >
  Cassandra read/write consistency tuning for owned clusters: CL choices (ONE, QUORUM,
  LOCAL_QUORUM, ALL), replication factor, lightweight transactions, repair (anti-entropy),
  read repair, and latency tradeoffs. Use when Cassandra consistency level, quorum math,
  hinted handoff, or repair strategy — pair storage layout with `cassandra-compaction-strategies`.
---

# Cassandra Consistency Tuning

## Scope And Authorization

- **In scope:** Cassandra/compatible clusters and apps you operate.
- **Out of scope:** Attacking or overwhelming clusters you do not own.
- Changing default CL affects durability and latency — use change control.
- Pair with `cassandra-compaction-strategies`, app retry skills, `code-quality-standards`.

## When To Use

- Choosing write/read consistency levels per query type.
- Investigating stale reads, missing data after node failure, or RF misconfig.
- Setting up repair (opscenter/reaper/nodetool) schedules.
- Multi-DC `LOCAL_*` vs cross-DC consistency.
- LWT (`IF` conditions) for compare-and-set needs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Compaction strategy | `cassandra-compaction-strategies` |
| App retry/backoff | `retry-backoff-patterns` |
| Generic distributed systems theory only | architecture skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Term | Meaning |
| --- | --- |
| RF | Replication factor per keyspace/DC |
| CL | Consistency level for a request |
| Quorum | `RF/2+1` for simple RF |
| LOCAL_QUORUM | Quorum in local DC (NetworkTopologyStrategy) |
| Hinted handoff | Temporary write buffering for down nodes |
| Repair | Merkle-tree anti-entropy sync |
| LWT | Paxos-based conditional updates (higher cost) |

**Strong enough rule of thumb:** for RF=3, `LOCAL_QUORUM` write + `LOCAL_QUORUM` read ⇒ strong consistency for that DC (while RF maintained).

## Workflow

### 1. Confirm scope and success criteria

1. Keyspaces, RF map, DC topology, RPO/RTO, latency SLOs.
2. Success: documented CL matrix per operation class; repair healthy; no silent RF=1 production data.
3. Identify multi-DC failover expectations.

### 2. Inventory topology and keyspaces

```bash
nodetool status
# CQL
# DESCRIBE KEYSPACES;
# SELECT * FROM system_schema.keyspaces;
```

```cql
CREATE KEYSPACE IF NOT EXISTS app
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc1': '3',
  'dc2': '3'
};
```

1. Avoid `SimpleStrategy` in multi-node prod.
2. Note tables using LWT / materialized views / secondary indexes (extra care).

### 3. Define CL matrix by operation

| Operation class | Write CL | Read CL | Notes |
| --- | --- | --- | --- |
| User profile critical | LOCAL_QUORUM | LOCAL_QUORUM | RF≥3 |
| Metrics/telemetry | LOCAL_ONE | LOCAL_ONE | Accept loss window |
| Cross-DC strong | EACH_QUORUM / QUORUM | QUORUM | Latency cost |
| Absolute rare | ALL | ALL | Availability fragile |
| Idempotent cache fill | ONE | ONE | App-level OK |

1. **Never** assume `ONE` write + `ONE` read is safe for money/authz data.
2. Match client drivers default CL; do not rely on server default alone.
3. Document downgrade behavior on failures (driver speculative/retry).

### 4. Application driver settings

```python
# Conceptual Cassandra driver
from cassandra.query import ConsistencyLevel
session.execute(insert_stmt, values, consistency_level=ConsistencyLevel.LOCAL_QUORUM)
```

1. Timeouts separate from CL — tune both.
2. Idempotent retries for safe statements only.
3. Token awareness + DC awareness enabled.
4. Avoid unbounded retry storms (`retry-backoff-patterns`).

### 5. Repair and anti-entropy

```bash
# Prefer incremental/full repair strategy per org; example
nodetool repair -pr keyspace  # careful primary-range; scheduling via Reaper recommended
```

| Control | Guidance |
| --- | --- |
| Repair schedule | Regular per keyspace before gc_grace elapses |
| gc_grace_seconds | Coordinate with repair frequency for deletes |
| Hinted handoff | Monitor; do not replace repair |
| Read repair | Chance settings; understand extra load |
| Node down long | Bootstrap/replace procedures |

1. Deletes need timely repair to avoid zombie data after gc_grace.
2. Alert on failed repairs and growing unrepaired ranges (if metrics available).

### 6. LWT and contention

```cql
UPDATE accounts SET balance = 10 WHERE id = ? IF balance = 10;
```

1. Use LWT only when CAS required — higher latency/contention.
2. Hot partitions with LWT → severe bottlenecks; redesign keys if needed.
3. Prefer application idempotency keys when possible over heavy LWT.

### 7. Verify and hand off

```bash
# Chaos lab: stop one node RF=3 LOCAL_QUORUM should still work
# Stop two nodes → LOCAL_QUORUM fails — expected
```

1. Consistency tests in staging with intentional node downtime.
2. Measure p99 for LOCAL_QUORUM vs ONE on hot paths.
3. Runbook: RF change steps (never reduce RF carelessly), CL incident rollback.
4. Apply `code-quality-standards` on client code CL changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| RF | NTS RF=3 per DC | RF=1 prod “for speed” |
| Money path | LOCAL_QUORUM R+W | ONE everywhere |
| Multi-DC | LOCAL_* + clear failover | QUORUM cross-DC accidental latency |
| Deletes | Repair before gc_grace | Never repair; zombies |
| LWT | Rare CAS | LWT on hottest partition for everything |
| Drivers | Explicit CL per query class | Random defaults differ per service |

## Output Checklist

- [ ] Topology RF/DC documented
- [ ] CL matrix by operation class
- [ ] Drivers set explicit CL
- [ ] Repair schedule + gc_grace aligned
- [ ] Failure tests (node down) executed in lab/staging
- [ ] Latency impact measured
- [ ] LWT usage reviewed
- [ ] Alerts on repair/failure modes
- [ ] App retry policy compatible
- [ ] Compaction interactions considered

## Rules

- Consistency is a client choice — document it per query path.
- RF and CL math must match durability promises.
- Repair is mandatory operational hygiene, not optional.
- Authorized clusters only.
- Compaction performance → `cassandra-compaction-strategies`.
