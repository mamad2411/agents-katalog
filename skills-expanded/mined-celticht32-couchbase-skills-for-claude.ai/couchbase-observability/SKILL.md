---
name: couchbase-observability
description: "Monitor, alert on, and observe Couchbase clusters in production. Use whenever the user asks about Couchbase metrics, Prometheus, Grafana, alerting, alert thresholds, memory high watermark, disk usage, replication lag, query latency, index build progress, DCP lag, ops/sec, cache miss ratio, Couchbase Exporter, admin_stats_* tools, log aggregation, SIEM shipping, health checks, or 'how do I know if my Couchbase cluster is healthy.' Distinct from couchbase-mcp (calling the tools) and couchbase-security-hardening (audit log shipping). Use proactively for new production deployments needing an observability stack, incident response setup, and SLO definition."
license: MIT
---

# Couchbase Observability

A skill for *monitoring and alerting on* Couchbase clusters in production — metrics, thresholds, Prometheus integration, Grafana dashboards, log aggregation, and health check patterns.

Distinct from:
- `couchbase-mcp` — calling `admin_stats_*` tools to read current state
- `couchbase-security-hardening` — audit log configuration and shipping

## When this skill applies

- "How do I monitor Couchbase?"
- "What metrics should I alert on?"
- "How do I integrate Couchbase with Prometheus / Grafana?"
- "What's a good alert threshold for memory / disk / replication lag?"
- "How do I know if a node is healthy?"
- "How do I aggregate Couchbase logs?"
- "How do I set up dashboards for Couchbase?"
- "What does the cache miss ratio tell me?"
- "How do I detect query performance degradation?"

## Pick the right reference

| Question | Read |
|---|---|
| "What metrics matter and what do they mean?" | `references/key-metrics.md` |
| "Prometheus / Grafana setup — scraping, dashboards, recording rules" | `references/prometheus-grafana.md` |
| "Alert thresholds — what values should trigger pages vs warnings?" | `references/alert-thresholds.md` |
| "Log aggregation — shipping cluster logs to ELK / Splunk / Datadog" | `references/log-aggregation.md` |

## Three core principles

**Principle 1 — Alert on symptoms, not causes.**
"Disk usage > 80%" is a symptom. "Compaction not keeping up" is a cause. Alert on the symptom (disk), investigate causes during the incident. Symptom-based alerts have fewer false positives and fewer missed incidents.

**Principle 2 — Baseline before you threshold.**
Couchbase metrics vary enormously by workload. A cache miss ratio of 20% is catastrophic for a key-value workload and perfectly acceptable for an analytics workload. Baseline your metrics for one week before setting alert thresholds.

**Principle 3 — Every node matters.**
Couchbase is a distributed system. A single node with high memory pressure, disk usage, or replication lag can degrade the whole cluster. Aggregate cluster-level metrics for dashboards, but alert per-node on resource pressure.

## Quick tool map

| Task | Tool |
|---|---|
| Cluster-level stats (ops/sec, memory, disk) | `admin_stats_cluster` |
| Per-node stats | `admin_stats_nodes` |
| Bucket-level stats | `admin_stats_bucket` |
| Index stats (GSI) | `admin_stats_indexes` |
| XDCR replication stats | `admin_stats_xdcr` |
| Query service stats | `admin_stats_query` |
| FTS / Search stats | `admin_stats_fts` |
| Eventing stats | `admin_stats_eventing` |
| Analytics stats | `admin_stats_analytics` |
| System events (cluster history) | `admin_cluster_get_system_events` |
| Prometheus scrape targets | `admin_stats_prometheus_targets` |
| Cluster logs | `admin_cluster_get_logs` |

## Related skills

- `couchbase-mcp` — the `admin_stats_*` tools that expose the raw metric data
- `couchbase-security-hardening` — audit log shipping (separate from operational log shipping)
- `couchbase-xdcr` — XDCR-specific metric interpretation (`changes_left`, `docs_failed_cr_source`)
- `couchbase-eventing` — Eventing-specific stats (`dcp_backlog`, `failed_count`, `timeout_count`)
