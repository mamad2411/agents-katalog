---
name: flink-cdc-connectors
description: >
  Operate and harden Apache Flink CDC connectors (MySQL/Postgres/Oracle/SQL Server, etc.):
  binlog/WAL privileges, snapshot vs streaming phases, schema change handling, exactly-once
  sinks, and secret management. Use when building owned change-data-capture pipelines into
  Flink, reviewing CDC source configs, or troubleshooting lag and consistency—not for
  unauthorized database access.
---

# Flink CDC Connectors

## Scope And Authorization

- **In scope:** databases and Flink clusters you own or are authorized to integrate.
- **Out of scope:** enabling CDC against third-party databases without permission.
- Prefer replicas/read accounts for snapshots where supported; limit prod impact.
- Redact JDBC URLs passwords and binlog positions containing sensitive ops data if needed.
- Pair job code with `code-quality-standards`.

## When To Use

- Ingesting **database change events** into Flink with Flink CDC (or Debezium-based CDC sources).
- Configuring hostname, credentials, table include/exclude lists, startup modes.
- Handling DDL schema evolution and downstream type mapping.
- Securing connector privileges (REPLICATION, SELECT) and network paths.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Flink checkpoint storage security | `flink-checkpoint-security` |
| Savepoint upgrade ops | `flink-savepoints-ops` |
| Generic protocol RE | `protocol-reverse-engineering` |
| Secrets rotation program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Phase | Behavior |
| --- | --- |
| Snapshot | Initial consistent table read (can be heavy) |
| Binlog/WAL streaming | Incremental changes after snapshot offset |
| Schema changes | DDL events; job must tolerate evolution |
| Sink | Kafka/Iceberg/JDBC/etc. with idempotence |

| Source (examples) | Privileges / notes |
| --- | --- |
| MySQL | SELECT, REPLICATION SLAVE/CLIENT; `binlog_format=ROW` |
| PostgreSQL | REPLICATION, SELECT; logical decoding slot |
| SQL Server | CDC enabled tables; appropriate roles |
| Oracle | LogMiner/XStream setup per connector docs |

## Workflow

### 1. Confirm scope and success criteria

1. Source DB engines/versions, tables, PII classes, lag SLO, destination systems.
2. Success: only listed tables captured; credentials least privilege; snapshot completes without locking out prod unacceptably; failover retains offsets.
3. Change window for enabling CDC features on DB if required.

### 2. Inventory connectors and jobs

```bash
# Flink UI / CLI — owned cluster
flink list
# Search job configs
rg -n "mysql-cdc|postgres-cdc|debezium|Flink CDC|source.*cdc" -g '*.{yml,yaml,properties,java,scala,sql}'
```

1. Record startup mode: `initial`, `latest-offset`, `timestamp`, `specific-offset`.
2. Map secrets injection (K8s secret, Flink config, env).

### 3. Baseline DB readiness

```sql
-- MySQL examples (owned)
SHOW VARIABLES LIKE 'binlog_format';
SHOW VARIABLES LIKE 'binlog_row_image';
-- Postgres
SHOW wal_level;  -- logical for logical decoding
```

1. Estimate snapshot size and peak IOPS.
2. Confirm monitoring for replication lag / slot lag.

### 4. Configure CDC securely

```sql
-- Flink SQL sketch (versions differ)
-- CREATE TABLE orders_cdc (
--   id BIGINT, status STRING, PRIMARY KEY (id) NOT ENFORCED
-- ) WITH (
--   'connector' = 'mysql-cdc',
--   'hostname' = 'db.internal',
--   'username' = 'flink_cdc',
--   'password' = '${secrets.db_password}',
--   'database-name' = 'shop',
--   'table-name' = 'orders',
--   'server-time-zone' = 'UTC'
-- );
```

1. **Least privilege user** dedicated to CDC; no SUPER unless unavoidable.
2. TLS to database when supported; private network only.
3. Explicit table allowlists—never entire server without need.
4. Align checkpointing so source offsets commit consistently with sinks (`flink-checkpoint-security` for storage).
5. Handle PII: prefer column projection / redaction before broad sinks.
6. Resource: tune chunk sizes for snapshot; avoid crushing primary.

### 5. Verify with evidence

| Test | Expect |
| --- | --- |
| Insert row on source | Appears downstream within SLO |
| Update/delete | Correct op semantics at sink |
| Unauthorized table name | Not captured |
| Bad password | Job fails closed; secrets not logged |

```bash
# Lag dashboards: CDC delay, checkpoint duration, restart count
```

### 6. Operate schema changes

1. Rehearse ADD COLUMN in staging with job running.
2. Document incompatible changes requiring savepoint/stop (`flink-savepoints-ops`).
3. Alert on connector schema-incompatible errors.

### 7. Hand off

1. Runbook: restart from savepoint, slot cleanup (Postgres), binlog retention sizing.
2. Owners for DB privileges and Flink job.
3. Apply `code-quality-standards` for UDFs/jobs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Privileges | CDC-only role | App admin user reused |
| Tables | Explicit include list | `.*` on shared cluster |
| Secrets | Secret store injection | Password in git SQL |
| Snapshot | Staged load test | Surprise full scan on Friday prod |
| Network | Private link | Public DB + CDC user |
| Offsets | Checkpoint aligned | At-most-once mystery loss |

## Output Checklist

- [ ] Source DBs, tables, and authorization recorded
- [ ] Connector type/version documented
- [ ] DB CDC prerequisites verified
- [ ] Least-privilege credentials and TLS/private net
- [ ] Startup mode and offset strategy chosen
- [ ] End-to-end change test evidenced
- [ ] Schema change runbook
- [ ] Monitoring for lag and job health
- [ ] `code-quality-standards` applied

## Rules

- Authorized databases only.
- CDC privileges are powerful—scope tightly and audit.
- Prefer documented Flink CDC options for your exact version.
- Coordinate checkpoints/savepoints with neighbor Flink skills.
