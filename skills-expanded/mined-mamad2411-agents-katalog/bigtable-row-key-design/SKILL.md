---
name: bigtable-row-key-design
description: >
  Google Cloud Bigtable row key design for owned tables: hotspot avoidance, key
  salting/hashing, reverse timestamps, tall vs wide rows, and query-pattern-first
  modeling. Use when designing or fixing Bigtable schemas for throughput and
  latency — not for unauthorized access to others’ instances.
---

# Bigtable Row Key Design

## Scope And Authorization

- **In scope:** Bigtable instances/tables you own or are authorized to design/load.
- **Out of scope:** Scanning or bulk-reading production tables without need; load tests without approval.
- Bad keys cause hotspots and outages — validate with realistic traffic.
- Pair Beam pipelines with `beam-runner-choice`; use `code-quality-standards` for client code.

## When To Use

- Greenfield table design for time series, IoT, user events, ad graphs.
- Fixing hotspotting on sequential keys (user ids, timestamps as prefix).
- Choosing between tall rows (many related keys) vs wide rows (many columns).
- Planning range scans vs point lookups.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cosmos DB partition keys | `azure-cosmos-autoscale` (different product) |
| Beam runner selection | `beam-runner-choice` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Row key | Sorted string; lexicographic order drives tablet splits |
| Hotspot | Many writes to contiguous key range → one node overloaded |
| Salt/hash prefix | Spread load; may sacrifice simple range scans |
| Reverse timestamp | `max-ts` ordering for recent-first reads |
| GC rules | Column family TTL / max versions |
| Tooling | `cbt`, Bigtable Key Visualizer, client metrics |

## Workflow

### 1. Confirm scope and success criteria

1. Access patterns (read/write QPS, key distribution), latency SLO, authorization.
2. Success: no hotspot under load test; p99 within SLO; scans return needed windows efficiently.
3. Document all query patterns first — design keys for queries, not entities alone.

### 2. Inventory queries and data

```bash
# Example admin
cbt -instance "$INSTANCE" ls
cbt -instance "$INSTANCE" ls "$TABLE"
# App: list all read/write paths and filters
```

1. Rank top queries by QPS and latency sensitivity.
2. Estimate key cardinality and burst patterns (e.g. popular tenants).
3. Note multi-tenancy isolation needs.

### 3. Baseline anti-patterns

| Anti-pattern | Problem |
| --- | --- |
| `timestamp#user` ascending | All writes hit latest tablet |
| Monotonic ID prefix | Hotspot on insert |
| Huge rows (>100 MB) | Latency, memory pressure |
| Unbounded column growth | Wide row pain |
| Leading tenant with few tenants | Hot partitions |

### 4. Design keys

**Patterns:**

```text
# Point lookup user profile
userId

# Time series recent-first for a device
deviceId#revts   where revts = (MAX_TS - event_ts_ms)

# Spread writes with field promoted for scan
shard = hash(userId) % N
shard#userId#revts

# Avoid
event_ts#userId   # sequential hotspot
```

1. Keep keys short but unique; prefer human-debugable only if no hotspot.
2. Choose delimiter carefully (`#`) and escape user content if needed.
3. Tall vs wide: prefer many rows with same prefix for huge histories; bound columns per row.
4. Column families: group by access frequency/TTL; don’t put unrelated data together.
5. Plan migrations: new key scheme often means dual-write + backfill.

### 5. Verify with evidence

```bash
# Load test authorized nonprod; watch CPU per node / Key Visualizer heatmap
cbt -instance "$INSTANCE" read "$TABLE" count=10
```

1. Key Visualizer shows even heat, not a vertical hot line.
2. Point reads and planned range scans meet latency.
3. GC rules reclaim old versions as expected.

### 6. Observe and harden

1. Metrics: server CPU, node storage, error rates, row size distribution.
2. Alerts on hotspot indicators and oversized rows.
3. Review new query patterns before they force full table scans.

### 7. Hand off

1. Key format specification with examples and forbidden patterns.
2. Client library helpers for encoding keys.
3. Backfill/migration runbook.

## Query → Key Cheat Sheet

| Query | Key sketch |
| --- | --- |
| Get profile by id | `userId` |
| Latest N events for device | `deviceId#revts` |
| All events for user on day | `userId#yyyyMMdd#revts` or salt carefully |
| Global recent feed | Hard — need fan-out or different store |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Writes | High-cardinality leading key | Timestamp-leading keys |
| Reads | Matches prefix ranges | Full table scan per request |
| Rows | Bounded size | Multi-GB rows |
| Schema | Query-first design | Entity dump without queries |
| Change | Dual-write migration | In-place rewrite hope |

## Output Checklist

- [ ] Query patterns ranked and documented
- [ ] Row key format specified with examples
- [ ] Hotspot analysis completed
- [ ] Tall/wide and CF/GC decisions made
- [ ] Load test / Key Visualizer evidence
- [ ] Client encoding helpers provided
- [ ] Monitoring for row size and hotspots
- [ ] Migration plan if replacing old keys
- [ ] `code-quality-standards` applied

## Rules

- Authorized instances only.
- Design for queries and even write distribution.
- Avoid sequential leading keys for high QPS writes.
- Bound row sizes.
- Measure with Key Visualizer/metrics, not intuition alone.
