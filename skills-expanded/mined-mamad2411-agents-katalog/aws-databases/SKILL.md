---
name: aws-databases
description: Choose and operate AWS databases (DynamoDB, Aurora, Aurora DSQL, RDS, ElastiCache) with schema design and migration patterns. Use when the user is picking a datastore, modeling tables, or planning a migration on AWS.
---

# AWS Databases

## Selection, fast

| Need | Pick |
|---|---|
| Key-value / document, single-digit ms, any scale | DynamoDB |
| Relational, MySQL/Postgres compat, spiky or idle-heavy load | Aurora serverless |
| Relational Postgres-compatible, multi-region active-active, zero infra | Aurora DSQL |
| Relational, steady load or non-Aurora engine (SQL Server, Oracle, MariaDB) | RDS |
| Sub-ms cache, pub/sub, sessions | ElastiCache (Valkey/Redis OSS) |

Rules of thumb: access patterns known up front and scale matters, DynamoDB.
Ad hoc queries, joins, constraints, Aurora/RDS. Multi-region writes with
strong consistency: Aurora DSQL or DynamoDB global tables with MRSC.

## DynamoDB

- Model access patterns first. Single-table design with generic `PK`/`SK`,
  GSIs for alternate access paths; avoid hot partition keys.
- On-demand capacity by default; switch to provisioned + auto scaling only
  with sustained, predictable traffic.
- Global tables: multi-Region strong consistency (MRSC) needs exactly 3
  regions (or 2 + witness), RPO zero. Since 2026, replication can span AWS
  accounts.
- TTL for expiry, Streams or Kinesis for CDC, DAX only for read-heavy
  hot-key workloads.
- `aws dynamodb query` beats `scan` always; paginate with
  `--max-items/--starting-token` in scripts.

## Aurora and RDS

- Aurora serverless (the renamed Serverless v2): scales 0 to 256 ACUs in
  0.5 ACU steps, scales to zero when idle, about $0.12/ACU-hour. Great for
  dev, agents, and bursty prod. Watch: resume from zero adds seconds of
  first-connection latency.
- Provisioned Aurora with readers for steady high throughput; Global
  Database for cross-region DR (single writer region).
- RDS Proxy in front of Lambda or any high-churn connection source;
  Postgres connections are expensive.
- Blue/green deployments for engine upgrades and risky schema changes.
- Backups: PITR on, verify restore actually works; snapshots before
  migrations.

## Aurora DSQL

Serverless distributed Postgres-compatible engine, active-active
multi-region, IAM-based auth (no passwords), scales to zero.

- Auth via IAM tokens; official connectors for Go (pgx), Python (asyncpg),
  Node.js, .NET (Npgsql), Rust (SQLx) handle token refresh.
- 2026 additions: JSON and JSONB types with compression, identity columns
  and sequences, CDC to Kinesis (GA July 2026), Flyway and Prisma support.
- Not full Postgres: no extensions and a list of unsupported features
  (foreign key constraints among them); check the compatibility page
  before porting an existing schema.
- Optimistic concurrency: transactions can fail at commit under
  contention; the app must retry.

## ElastiCache

- Valkey is the default engine going forward (cheaper than Redis OSS
  flavors); Memcached only for dead-simple memory cache.
- Serverless mode for variable load; node-based for steady throughput at
  scale.
- Set TTLs on everything; cache-aside pattern; never treat it as the
  system of record.

## Migrations

- Relational schema changes: Flyway or Liquibase, versioned SQL in the
  repo, applied by CI, never by hand. Expand-and-contract (add column,
  backfill, switch reads, drop) for zero-downtime.
- Heterogeneous or live migrations between engines: AWS DMS with CDC for
  the cutover window; Schema Conversion Tool for engine translation.
- DynamoDB imports/exports go through S3 (`aws dynamodb import-table` /
  `export-table-to-point-in-time`), which is also the cheap analytics path
  (query the export with Athena instead of scanning the table).

Verify pricing and regional availability live via the `aws-knowledge` MCP
server; database pricing shifts often.
