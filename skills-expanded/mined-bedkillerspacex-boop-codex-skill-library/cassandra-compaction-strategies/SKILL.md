---
name: cassandra-compaction-strategies
description: >
  Cassandra compaction strategy choice and ops for owned clusters: STCS, LCS, TWCS,
  UCS notes, when to switch, tombstone handling, compaction throughput, and monitoring.
  Use when Cassandra compaction pending, TWCS time-series, LCS read amp, or disk blow-ups
  during compaction — pair reads/consistency with `cassandra-consistency-tuning`.
---

# Cassandra Compaction Strategies

## Scope And Authorization

- **In scope:** Cassandra/Scylla clusters you operate (note Scylla differences).
- **Out of scope:** Compaction changes on clusters without ownership; destructive ops without change windows.
- Compaction strategy changes can be expensive — validate in staging with prod-like data volume.
- Pair with `cassandra-consistency-tuning` and ops runbooks.

## When To Use

- Choosing or changing table compaction strategy.
- High read latency from too many SSTables; write amplification issues.
- Time-series data candidates for TWCS.
- Disk usage spikes, pending compactions, tombstone warnings.
- Planning major version upgrades affecting compaction (UCS on newer Cassandra).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Consistency levels / repair | `cassandra-consistency-tuning` |
| Generic capacity planning only | SRE capacity skills |
| App data modeling CQL design deep | data modeling skills |
| Implementation quality for app code | `code-quality-standards` |

## Domain Focus

| Strategy | Best for | Watch outs |
| --- | --- | --- |
| STCS (Size-Tiered) | Write-heavy, unknown patterns (default classic) | Many SSTables → read amp; space overhead |
| LCS (Leveled) | Read-heavy, update-heavy rows | Write amp; disk IO; more compaction CPU |
| TWCS (Time-Window) | Time-series, TTL expiry windows | Out-of-order / late writes; window sizing |
| UCS (Unified, newer) | Modern multi-workload (version-dependent) | Learn params; validate on your version |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster version, table workloads (read/write ratio, TTL, time-series?), SLOs.
2. Success: strategy matches workload; pending compactions stable; p99 reads improved or space recovered; no prolonged overload.
3. Change window + snapshot/backup verified.

### 2. Inventory current state

```bash
nodetool status
nodetool compactionstats
nodetool tablestats keyspace.table
nodetool tpstats
# CQL
# DESCRIBE TABLE keyspace.table;
```

1. Note `compaction = { 'class': '...' , ...}` per table.
2. Metrics: pending tasks, blocked flush, disk free, read latency, SSTables per read.
3. Tombstone histograms / warnings in logs.

### 3. Match strategy to workload

| Workload signal | Lean toward |
| --- | --- |
| Heavy sequential time data + TTL | TWCS |
| Point reads, frequent updates | LCS |
| Bulk writes, analytics style | STCS (or UCS carefully) |
| Mixed uncertain | Benchmark STCS vs LCS on staging; consider UCS on supported versions |

**TWCS sizing:** window size ≈ bucket of time you write then rarely update; align with TTL.

### 4. Apply changes carefully

```cql
-- Example: switch to TWCS (syntax varies slightly by version)
ALTER TABLE keyspace.events WITH compaction = {
  'class': 'TimeWindowCompactionStrategy',
  'compaction_window_unit': 'HOURS',
  'compaction_window_size': '24'
};

-- LCS example
ALTER TABLE keyspace.users WITH compaction = {
  'class': 'LeveledCompactionStrategy'
};
```

1. Changing strategy may rewrite large data — monitor disk (**need free space**).
2. Throttle if needed: `nodetool setcompactionthroughput` (MB/s) during business hours.
3. Avoid major concurrent repairs + heavy compaction storms without capacity.

### 5. Operate compaction health

```bash
nodetool compactionstats
nodetool garbagecollect keyspace table   # careful; version/support dependent
# Inspect SSTable counts via tablestats
```

| Issue | Direction |
| --- | --- |
| Pending compactions grow | Throughput/IO capacity; reduce load; check for overload |
| Tombstones hurt reads | TTL/repair; avoid wide partitions; read repair settings |
| TWCS late data | Adjust windows; reduce out-of-order writes |
| LCS high write amp | Hardware IO; consider if STCS/UCS better |
| Disk full risk | Pause noncritical; expand; emergency compaction control |

### 6. Verify

1. Compare `tablestats` SSTables-per-read and latency before/after steady state.
2. Disk curve stabilizes; no continuous full compact storms.
3. Application SLOs held during/after switch.
4. Snapshot of `DESCRIBE TABLE` stored in change ticket.

### 7. Hand off

1. Document strategy rationale per table in runbook.
2. Alerts: pending compactions, disk < threshold, compaction executor blocked.
3. Coordinate with repair schedule (`cassandra-consistency-tuning`).
4. IaC/CQL migrations reviewed with `code-quality-standards` if automated.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Choice | Workload-driven + staging proof | LCS on everything “for speed” |
| TWCS | Window fits TTL write pattern | TWCS on heavily updated non-TS data |
| Change | Throttled + monitored | Alter all prod tables Friday 5pm blind |
| Space | Free space planned | Start major compact at 95% disk |
| Tombstones | Model + repair hygiene | Ignore warnings until read timeout |
| Docs | Per-table rationale | Tribal knowledge only |

## Output Checklist

- [ ] Version and workload profile recorded
- [ ] Baseline compactionstats/tablestats saved
- [ ] Strategy selected with rationale
- [ ] Staging validation done for large tables
- [ ] Prod change window + free disk confirmed
- [ ] Throughput throttling plan
- [ ] Post-change metrics improved/stable
- [ ] Alerts and runbook updated
- [ ] Consistency/repair interactions considered

## Rules

- Strategy changes are operationally heavy — never casual on huge tables.
- Always keep disk headroom for compaction.
- Align TWCS with true time-series write patterns.
- Authorized clusters only.
- Consistency/repair details → `cassandra-consistency-tuning`.
