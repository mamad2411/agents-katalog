---
name: debezium-cdc-postgres
description: >
  Configure Debezium CDC for owned PostgreSQL databases: wal_level logical,
  publications/slots, connector configs, snapshot vs streaming, heartbeats,
  schema evolution, and operational monitoring. Use when capturing row-level
  changes to Kafka or other sinks — not for unauthorized replication of data
  you do not own.
---

# Debezium CDC for PostgreSQL

## Scope And Authorization

- **In scope:** PostgreSQL instances and Kafka/Debezium deployments you operate.
- **Out of scope:** Enabling logical replication on third-party databases without permission; shipping PII to unapproved topics.
- Prefer non-prod first; production slots consume disk if consumers stall — monitor aggressively.
- Redact connection passwords; prefer least-privilege replication roles.
- Pair with Kafka ops, privacy review, and `code-quality-standards` for SMTs/transforms.

## When To Use

- Near-real-time sync from Postgres to Kafka, warehouses, or search.
- Replacing batch dumps with change streams.
- Multi-table capture with consistent snapshots.
- Troubleshooting slot lag, toasts, or replica identity issues.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| dbt modeling of landed data | dbt skills |
| Postgres failover | `db-failover-checklist` |
| Schema expand/contract for apps | `db-migration-expand-contract` |
| General Kafka security | Kafka security skills |
| Implementation quality baseline | `code-quality-standards` |

## Prerequisites (Postgres)

| Setting / object | Purpose |
| --- | --- |
| `wal_level = logical` | Required for logical decoding |
| Sufficient `max_replication_slots` / `max_wal_senders` | Slot + sender capacity |
| Replication user | `REPLICATION` attr + table privileges |
| `REPLICA IDENTITY` | Full/default for old values on updates/deletes as needed |
| Publication | Tables included in CDC |

```sql
-- Example role (owned DB)
CREATE ROLE debezium REPLICATION LOGIN PASSWORD '...';  -- use secret manager
GRANT SELECT ON ALL TABLES IN SCHEMA app TO debezium;
ALTER DEFAULT PRIVILEGES IN SCHEMA app GRANT SELECT ON TABLES TO debezium;

-- Replica identity if you need before-images for tables without PK carefully
-- ALTER TABLE app.orders REPLICA IDENTITY FULL;
```

## Workflow

### 1. Confirm scope and success criteria

1. Tables, PII classification, sink topics, throughput estimate.
2. Success: snapshot completes; streaming lag within SLO; deletes captured as required; slot stays healthy under load tests.

### 2. Prepare database

```sql
SHOW wal_level;  -- must be logical
SHOW max_replication_slots;
SHOW max_wal_senders;
```

Restart may be required for `wal_level` changes (plan maintenance).

### 3. Connector configuration (Kafka Connect example)

```json
{
  "name": "orders-postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "db.example.local",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${file:/secrets/db.pass}",
    "database.dbname": "app",
    "topic.prefix": "pg.app",
    "table.include.list": "app.orders,app.order_items",
    "plugin.name": "pgoutput",
    "publication.autocreate.mode": "filtered",
    "slot.name": "debezium_orders",
    "heartbeat.interval.ms": "10000",
    "snapshot.mode": "initial"
  }
}
```

Notes:

1. Prefer `pgoutput` on modern Postgres.
2. Unique **slot.name** per connector; never share slots carelessly.
3. `topic.prefix` stable — renames are painful.
4. Heartbeats help advance slots on low-traffic DBs (configure heartbeat table if needed).

### 4. Snapshot then stream

| Mode | Behavior |
| --- | --- |
| `initial` | Snapshot once then stream |
| `never` | Stream only (misses existing rows) |
| `always` / other modes | Version-specific — read current Debezium docs |

During snapshot: watch DB load, long transactions, and Connect task memory.

### 5. Schema changes

1. Compatible expands usually flow; test `ALTER` in staging with connector running.
2. Primary key changes and table renames need deliberate procedures.
3. SMTs (masking, routing) versioned as code.
4. Coordinate with app expand/contract so CDC consumers understand dual columns during migration.

### 6. Operate and monitor

| Signal | Risk if bad |
| --- | --- |
| Replication slot lag / retained WAL | Disk fill → primary outage |
| Connect task failed | Stale sinks |
| Transaction ID age / long txs | Snapshot or decoding issues |
| Tombstones / delete handling | Downstream soft-delete bugs |

```bash
# Postgres
SELECT slot_name, active, restart_lsn, confirmed_flush_lsn
FROM pg_replication_slots;

# Kafka Connect
curl -sS http://connect.example.local:8083/connectors/orders-postgres-connector/status
```

Alert on inactive slots with retained WAL growth. Drop abandoned slots promptly.

### 7. Verify

```bash
# Insert/update/delete in staging; observe Kafka topic messages
# Check envelope: op c/u/d/r, before/after per replica identity
```

Validate ordering expectations per key; consumers must be idempotent.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Privileges | Least-privilege SELECT + replication | Superuser connector |
| Slots | Monitored + named | Forgotten slots filling disk |
| Snapshot | Staged + load tested | First run on largest prod peak |
| PII | Topic ACLs + masking SMT | Unrestricted Kafka mirror |
| PK | Tables with stable PKs | CDC heap tables without identity plan |

## Output Checklist

- [ ] wal_level and limits confirmed
- [ ] Replication role least privilege
- [ ] Publication/tables listed
- [ ] Connector config in code/config repo
- [ ] Snapshot strategy chosen
- [ ] Heartbeat/lag monitoring on
- [ ] Slot lag alerts configured
- [ ] Schema change runbook linked
- [ ] Downstream idempotency confirmed
- [ ] PII/topic security reviewed

## Rules

- Stalled consumers + slots can take down Postgres — monitor WAL retention.
- Capture only approved tables; privacy review for topics.
- Authorized databases only.
- Focus on **Debezium CDC with PostgreSQL**.
