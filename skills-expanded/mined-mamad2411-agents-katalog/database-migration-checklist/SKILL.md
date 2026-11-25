---
name: database-migration-checklist
description: >-
  Database migration checklist for Azure. Covers SQL Server, PostgreSQL,
  MySQL, and Cosmos DB migrations with DMS workflows, offline vs online
  decisions, method comparison, and post-migration validation.
when-to-use: >-
  Invoke when planning a database migration to Azure, selecting migration
  tooling, choosing between offline and online approaches, or validating
  a completed migration.
categories:
  - database
  - migration
  - azure
---

# Database Migration Checklist

Migrate to dev first. Test everything. Then do it again in staging. Then production.

## Migration Decision Tree

```
What database engine?
├─ SQL Server → Azure SQL Database, Managed Instance, or SQL on VM
├─ PostgreSQL → Azure Database for PostgreSQL Flexible Server
├─ MySQL → Azure Database for MySQL Flexible Server
├─ MongoDB → Azure Cosmos DB (MongoDB API)
└─ Other → Evaluate compatibility and migration path
```

---

## Offline vs Online

| Factor | Offline | Online |
|---|---|---|
| Downtime | Full during migration | Minimal at cutover only |
| Complexity | Simple, fewer failure modes | More complex, replication involved |
| Best for | Planned maintenance windows, small DBs | Large databases, business continuity critical |

**Notable gap:** Online migration to Azure SQL Database is NOT supported — only offline. Online is supported for Managed Instance and SQL on VM targets.

---

## SQL Server → Azure SQL

### Workflow

1. **Assess** — Azure Migrate or Data Migration Assistant. Check compatibility, feature parity.
2. **SKU recommendation** — Right-size target based on current workload metrics.
3. **Schema migration** — DMA or SSDT for schema comparison and migration.
4. **Data migration** — DMS (online or offline), BACPAC, or transactional replication.
5. **Cutover** — Switch connection strings, verify data integrity, decommission source.
6. **Post-migration** — Enable HA, monitoring, backup policies. Validate performance.

### Method Comparison

| Method | Downtime | Best For |
|---|---|---|
| DMS offline | Full | Simple migrations, small databases |
| DMS online (MI/VM only) | Minimal | Large databases needing minimal downtime |
| BACPAC export/import | Full | Small databases, schema + data together |
| Transactional replication | Minimal | Complex scenarios, selective table migration |

---

## PostgreSQL → Flexible Server

### Workflow

1. Enable supported extensions on target (allowlist + `CREATE EXTENSION`)
2. Match server parameters between source and target
3. Migrate users and roles manually via `pg_dumpall --globals-only`
4. Remove superuser privileges (not supported in Flexible Server)
5. Disable HA and read replicas on target before migration
6. Run migration (online or offline)
7. Validate, then enable HA and replicas post-migration

### Key Constraints

- Online mode requires **primary keys on all tables** for replication tracking
- Superuser roles must be removed or adjusted before migration
- Extensions must be allowlisted and created on target before migration starts

### Sources Supported

On-prem PostgreSQL, Amazon RDS, Google Cloud SQL, Azure Single Server (upgrade path)

---

## MySQL → Flexible Server

- DMS supports: MySQL, Amazon RDS MySQL, Aurora MySQL, Cloud SQL MySQL, Percona
- Both online and offline modes — all GA
- Data-in replication available for hybrid scenarios

---

## MongoDB → Cosmos DB

- DMS for MongoDB to Cosmos DB (MongoDB API) — online and offline, both GA
- Data migration tool for JSON to Cosmos DB NoSQL
- Spark connector for bulk migration from any Spark-compatible source
- **Design partition key strategy BEFORE migrating** — cannot change after container creation

---

## Pre-Migration Checklist

- [ ] Run compatibility assessment (DMA, Azure Migrate)
- [ ] Document all blocking compatibility issues and remediation
- [ ] Right-size target SKU from workload metrics (CPU, memory, IOPS, storage)
- [ ] Plan network connectivity — private endpoint, VNet integration
- [ ] Test migration in dev environment first — full end-to-end
- [ ] Estimate migration duration and plan maintenance window
- [ ] Communicate downtime window to stakeholders
- [ ] Back up source database before starting

---

## Post-Migration Checklist

- [ ] Validate data integrity — row counts, checksums, spot-check critical tables
- [ ] Run application test suite against new target
- [ ] Run performance tests — compare query times vs source baseline
- [ ] Enable HA (geo-replication, failover groups, read replicas)
- [ ] Configure monitoring and alerting
- [ ] Set backup policies (PITR, LTR, geo-restore)
- [ ] Update connection strings in all consumers
- [ ] Monitor for 2-4 weeks post-migration before decommissioning source

---

## DMS Supported Scenarios (GA)

### Offline

| Source | Target |
|---|---|
| SQL Server | Azure SQL DB / MI / VM |
| Amazon RDS SQL Server | Azure SQL DB / MI / VM |
| MySQL / RDS MySQL / Aurora / Cloud SQL | MySQL Flexible Server |
| MongoDB | Cosmos DB |
| PostgreSQL / RDS PostgreSQL | PostgreSQL Flexible Server |

### Online (Minimal Downtime)

| Source | Target |
|---|---|
| SQL Server | Azure SQL MI / VM (**not** SQL Database) |
| Amazon RDS SQL Server | Azure SQL MI / VM |
| MySQL / RDS MySQL / Aurora / Cloud SQL | MySQL Flexible Server |
| MongoDB | Cosmos DB |
| PostgreSQL / RDS PostgreSQL | PostgreSQL Flexible Server |

## Related Skills

- `cost-optimization-checklist` — Right-sizing target database SKUs
- `disaster-recovery-planning` — Post-migration HA and replication setup
