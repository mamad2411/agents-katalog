---
name: clickhouse-replicated-merge-tree
description: >
  Operate ClickHouse ReplicatedMergeTree: ZooKeeper/ClickHouse Keeper paths, replica
  identity, queue/log repair, deduplication, PART/FETCH issues, and add/remove replica.
  Use on owned CH clusters for replication health and RMT table design — not for RBAC,
  dictionaries, or generic MV design (sibling ClickHouse skills).
---

# ClickHouse ReplicatedMergeTree Ops

## Scope And Authorization

- **In scope:** owned ClickHouse clusters using Keeper/ZooKeeper and Replicated*MergeTree engines.
- **Out of scope:** deleting Keeper paths or FORCE drops without backup and authorization.
- Prefer staging cluster for DDL experiments; replication mistakes can desync prod.
- Redact Keeper credentials and internal hostnames as required.
- Pair with `clickhouse-access-control` for who may SYSTEM RESTART REPLICA etc.

## When To Use

- Creating or diagnosing **ReplicatedMergeTree** (and Summing/Aggregating/Replacing variants).
- Fixing `system.replicas` unhealthy, lost replica, stuck merges, or `part` fetch errors.
- Adding a replica, renames, or recovering after node loss.
- Tokens: ReplicatedMergeTree, Keeper, ZooKeeper path, replica name, queue, log_pointer, dedup.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Users/roles | `clickhouse-access-control` |
| Materialized views | `clickhouse-materialized-views-ops` |
| Dictionaries | `clickhouse-dictionaries` |
| Generic disk full Linux | OS/ops skill |
| Backup/restore product strategy | backup skill / vendor runbook |

## Core Concepts

| Concept | Meaning |
| --- | --- |
| ZooKeeper/Keeper path | Shared metadata root for a logical table |
| Replica | `{shard}` / `{replica}` identity macros |
| Replication log | Ordered mutations/parts coordination |
| Deduplication | Insert block IDs prevent double insert on retry |
| Quorum insert | Optional stronger insert ack (latency cost) |

**Create pattern:**

```sql
CREATE TABLE analytics.events ON CLUSTER '{cluster}'
(
    ts DateTime,
    tenant_id UInt32,
    payload String
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/analytics/events', '{replica}')
PARTITION BY toYYYYMM(ts)
ORDER BY (tenant_id, ts)
TTL ts + INTERVAL 90 DAY;
```

Macros in `config.xml` must make `{shard}`/`{replica}` unique and stable.

## Workflow

### 1. Confirm scope and success criteria

1. Cluster map: shards, replicas, Keeper endpoints, CH version.
2. Success: `system.replicas` is_readonly=0, queue small, inserts replicate, no long-lived exceptions.
3. Break-glass: known good backup + procedure for lost replica rebuild.

### 2. Inventory replication health

```sql
SELECT
  database, table, replica_name, is_leader, is_readonly,
  absolute_delay, queue_size, inserts_in_queue, merges_in_queue,
  last_queue_update, total_replicas, active_replicas
FROM system.replicas
ORDER BY absolute_delay DESC;

SELECT * FROM system.replication_queue LIMIT 50;
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/tables' LIMIT 20;  -- if permitted
```

```bash
clickhouse-client -q "SELECT version()"
# Keeper connectivity from node logs / monitoring
```

### 3. Baseline before change

1. Snapshot `system.replicas` and disk free per node.
2. Export `SHOW CREATE TABLE` for affected tables.
3. Note ongoing mutations: `system.mutations WHERE is_done = 0`.

### 4. Operate safely

**Add replica (high level):**

1. Provision node with correct macros (`shard` same, `replica` unique).
2. Create same RMT table (same ZK path) or restore metadata via your provisioning tool.
3. Allow fetch of parts; watch `system.replicas` until `active_replicas` expected.

**Common SYSTEM ops (authorized, understand blast radius):**

```sql
SYSTEM RESTART REPLICA analytics.events;
SYSTEM SYNC REPLICA analytics.events;
SYSTEM RESTORE REPLICA analytics.events;   -- dangerous; only per docs when metadata broken
SYSTEM DROP REPLICA 'replica-name' FROM ZKPATH '/clickhouse/tables/...';  -- careful
```

**Inserts:**

1. Prefer idempotent clients; rely on insert dedup for retries.
2. Use quorum inserts only when product requires and latency allows.
3. Avoid writing different schemas to same logical path.

**DDL:**

1. Prefer `ON CLUSTER` consistent DDL; verify each replica `SHOW CREATE`.
2. Do not manually invent conflicting ZK paths for “the same” table.

### 5. Diagnose common failures

| Symptom | Likely cause | Direction |
| --- | --- | --- |
| `is_readonly = 1` | Keeper session lost / config | Fix Keeper; check network; restart carefully |
| Growing `queue_size` | Fetch/merge stuck, disk, corrupt part | `replication_queue` errors; disk; part checks |
| `absolute_delay` high | Node behind | Network, I/O, too many merges |
| Duplicate data | Non-replicated path / dual non-RMT | Engine audit |
| Part `lost` / `no active replicas` | Replica death | Rebuild replica from healthy peer + backup |

```sql
SELECT * FROM system.replication_queue
WHERE last_exception != ''
ORDER BY create_time DESC
LIMIT 20;
```

### 6. Verify with evidence

1. Insert on replica A with identifiable marker; `SELECT` on replica B within SLO.
2. `active_replicas` equals expected count; delay under threshold.
3. After node restart, replica resyncs without permanent readonly.
4. Mutations complete: `system.mutations` is_done=1.

### 7. Hand off

1. Document macros, ZK path convention, shard map, owners.
2. Alerts: readonly, delay, queue size, Keeper latency, disk.
3. Runbooks: add replica, drop dead replica, restore from backup.
4. Link MV ops if replicated targets feed aggregates.

## Design Checklist (new RMT tables)

| Item | Guidance |
| --- | --- |
| ORDER BY | Query filters + uniqueness needs |
| PARTITION | Manageable size; avoid too many parts |
| TTL | Align with compliance and disk |
| Path | Unique per logical table; include shard |
| Index granularity | Default often fine; measure |
| Compression / codec | Large columns |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Paths | Stable macros, one path per table | Copy-paste path across unrelated tables |
| Recovery | Documented rebuild + backup | Random DROP REPLICA in panic |
| DDL | ON CLUSTER + verify all nodes | Manual drift per replica |
| Monitoring | replicas + queue + Keeper | Only CPU graphs |
| Inserts | Idempotent + dedup awareness | Firehose without disk headroom |

## Output Checklist

- [ ] Cluster/shard/replica/Keeper map recorded
- [ ] `system.replicas` baseline healthy or issues listed
- [ ] Changes applied with path/macros correctness
- [ ] Cross-replica insert visibility verified
- [ ] Queue/exceptions cleared or ticketed
- [ ] Alerts and runbooks updated
- [ ] Backup/restore path confirmed for table
- [ ] Residual risks (single Keeper, disk) noted
- [ ] Access to SYSTEM commands restricted

## Rules

- Authorized clusters only; treat Keeper metadata as critical state.
- Prefer reversible, documented recovery over ad-hoc ZK surgery.
- Evidence from `system.replicas` / queue over “it should sync”.
- Focus on **ReplicatedMergeTree ops**; RBAC/MV/dict are separate skills.
- Never paste live secrets or full ZK ACLs into public notes.
