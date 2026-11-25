---
name: managing-materialize
description: |
  Use when working with Materialize — materialize streaming database management
  — monitor clusters, sources, sinks, materialized views, indexes, and dataflow
  health. Use when debugging ingestion lag, inspecting view dependencies,
  auditing cluster utilization, or reviewing error logs.
connection_type: materialize
preload: false
---

# Managing Materialize

Manage and monitor Materialize streaming database — clusters, sources, sinks, materialized views, and dataflow health.

## Discovery Phase

```bash
#!/bin/bash

mz_cmd() {
    psql "$MATERIALIZE_URL" --no-psqlrc -t -A -F $'\t' -c "$1" 2>/dev/null
}

echo "=== Clusters ==="
mz_cmd "SELECT id, name, managed, size, replication_factor
        FROM mz_clusters
        ORDER BY name
        LIMIT 10;" | column -t

echo ""
echo "=== Sources ==="
mz_cmd "SELECT id, name, type, size, cluster_id
        FROM mz_sources
        WHERE id LIKE 'u%'
        ORDER BY name
        LIMIT 15;" | column -t

echo ""
echo "=== Materialized Views ==="
mz_cmd "SELECT id, name, cluster_id
        FROM mz_materialized_views
        WHERE id LIKE 'u%'
        ORDER BY name
        LIMIT 15;" | column -t

echo ""
echo "=== Sinks ==="
mz_cmd "SELECT id, name, type, cluster_id
        FROM mz_sinks
        WHERE id LIKE 'u%'
        ORDER BY name
        LIMIT 10;" | column -t

echo ""
echo "=== Schemas ==="
mz_cmd "SELECT s.name AS schema, d.name AS database
        FROM mz_schemas s JOIN mz_databases d ON s.database_id = d.id
        ORDER BY d.name, s.name
        LIMIT 15;" | column -t
```

## Analysis Phase

```bash
#!/bin/bash

mz_cmd() {
    psql "$MATERIALIZE_URL" --no-psqlrc -t -A -F $'\t' -c "$1" 2>/dev/null
}

echo "=== Source Ingestion Status ==="
mz_cmd "SELECT s.name, ss.status, ss.error, ss.updated_at
        FROM mz_source_statuses ss
        JOIN mz_sources s ON ss.id = s.id
        ORDER BY ss.updated_at DESC
        LIMIT 10;" | column -t

echo ""
echo "=== Sink Status ==="
mz_cmd "SELECT s.name, ss.status, ss.error, ss.updated_at
        FROM mz_sink_statuses ss
        JOIN mz_sinks s ON ss.id = s.id
        ORDER BY ss.updated_at DESC
        LIMIT 10;" | column -t

echo ""
echo "=== Cluster Replica Status ==="
mz_cmd "SELECT c.name AS cluster, cr.name AS replica, crs.status, crs.updated_at
        FROM mz_cluster_replica_statuses crs
        JOIN mz_cluster_replicas cr ON crs.replica_id = cr.id
        JOIN mz_clusters c ON cr.cluster_id = c.id
        LIMIT 10;" | column -t

echo ""
echo "=== Materialized View Freshness ==="
mz_cmd "SELECT mv.name,
               EXTRACT(EPOCH FROM mz_now() - write_frontier)::int AS lag_seconds
        FROM mz_materialized_views mv
        JOIN mz_frontiers f ON mv.id = f.object_id
        WHERE mv.id LIKE 'u%'
        ORDER BY lag_seconds DESC
        LIMIT 10;" | column -t

echo ""
echo "=== Recent Errors ==="
mz_cmd "SELECT source_name, error, count, last_occurred
        FROM mz_source_status_history
        WHERE error IS NOT NULL
        ORDER BY last_occurred DESC
        LIMIT 10;" | column -t
```

## Output Format

```
CLUSTERS
ID       Name           Managed  Size     Replication
<id>     <cluster>      true     <size>   <n>

SOURCES
ID       Name           Type     Size     Cluster
<id>     <source>       <type>   <size>   <cluster-id>

SOURCE STATUS
Name           Status     Error    Updated
<source>       running    <null>   <timestamp>

MV FRESHNESS
Name             Lag (seconds)
<mv-name>        <n>

CLUSTER REPLICAS
Cluster      Replica    Status     Updated
<cluster>    <replica>  ready      <timestamp>
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

