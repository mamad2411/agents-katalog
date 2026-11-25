---
name: postgres-infraforge-postgresql
description: Routes PostgreSQL administration and management tasks to the PostgreSQL specialist for InfraForge AI.
company: infraforge-ai
---

# PostgreSQL Administration Specialist

## Overview
This skill routes PostgreSQL-specific database administration tasks to the dedicated PostgreSQL specialist for InfraForge AI.

## Routing Criteria

Route to this skill when:
- PostgreSQL installation, configuration, and tuning
- Database clustering and replication setup
- PostgreSQL-specific performance optimization
- Connection pooling and pgBouncer configuration
- Backup strategies using pg_dump and WAL archiving
- Security configuration (pg_hba.conf, SSL, roles)
- PostgreSQL version upgrades and migrations
- Extensions management (PostGIS, pgvector, etc.)
- Troubleshooting PostgreSQL-specific issues

## Capabilities

### Installation & Configuration
- PostgreSQL installation on various platforms
- postgresql.conf tuning (memory, connections, parallelism)
- pg_hba.conf security configuration
- SSL/TLS setup for connections

### High Availability & Replication
- Streaming replication setup
- PostgreSQL Cluster management (Patroni, Stolon)
- Automatic failover configuration
- Read replicas and load balancing

### Backup & Recovery
- pg_dump and pg_dumpall usage
- Point-in-time recovery (PITR)
- WAL archiving and continuous archiving
- pgBackRest configuration
- Disaster recovery planning

### Performance Tuning
- Query planning and execution analysis
- Index strategies (B-tree, GiST, GIN, BRIN)
- Autovacuum tuning and maintenance
- Connection pooling with PgBouncer
- Workload-specific tuning

### Extensions & Advanced Features
- PostGIS geospatial operations
- Full-text search with pg_trgm
- JSON/JSONB operations
- Window functions and CTEs
- Partitioned tables
- Row-level security (RLS)

### Monitoring & Troubleshooting
- pg_stat_statements analysis
- Log analysis and slow query logging
- Lock monitoring and deadlock detection
- Connection and session management

## Related Skills

- `database-infraforge-database-infrastructure` - Core database infrastructure
- `postgres-devforge-advanced-queries` - Advanced PostgreSQL queries

## Examples

### Connection Pooling
```sql
-- Check connection usage
SELECT datname, numbackends, xact_commit, xact_rollback
FROM pg_stat_database;

-- pgBouncer statistics
SHOW POOLS;
SHOW STATS;
```

### Performance Analysis
```sql
-- Top slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Index usage analysis
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

*This skill routes to the PostgreSQL specialist agent for database administration tasks.*