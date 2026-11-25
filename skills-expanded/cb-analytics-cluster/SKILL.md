---
name: cb-analytics-cluster
description: |
  Use this skill when the user wants to inspect or configure the Couchbase
  cluster itself — node membership, memory quotas, rebalance, auto-failover,
  system events, or just verifying that a cluster is reachable. Trigger when
  they mention "cluster info", "ping", "rebalance", "auto-failover",
  "system events", "nodes", "memory quota", or "who_am_i".
license: MIT
---

# Cluster operations

You have 9 cluster-level tools, mostly read-only.

## Reachability and identity

- `ping_cluster(cluster)` — fast yes/no liveness check. Use this first when
  troubleshooting any other tool failure.
- `get_cluster_info(cluster)` — UUID + implementation version. Cheap; safe
  to call often.
- `who_am_i(cluster)` — what the cluster sees the current MCP user as
  (roles, domain). Useful when an `AnalyticsAuthError` shows up.

## Capacity and health

- `get_cluster_details(cluster)` — nodes, memory quotas (`memoryQuota`,
  `cbasMemoryQuota`), `balanced`, `rebalanceStatus`. Read before any
  capacity decision.
- `get_cluster_tasks(cluster)` — every in-flight task (rebalance, compaction,
  XDCR). Empty list is the happy path.
- `get_rebalance_progress(cluster)` — focused view: rebalance only.
  Returns `{"status": "none"}` when nothing's running.

## Auto-failover

- `get_auto_failover_settings(cluster)` — read current settings.
- `configure_auto_failover(enabled, timeout, max_count, cluster)` —
  Couchbase recommends `enabled=True, timeout=120, max_count=1` for
  3-node clusters; larger clusters can use `max_count=2+`.

## System events

`get_system_events(since_time, cluster)` returns recent operational events
(`info` / `warning` / `error`). `since_time` is an ISO 8601 timestamp; omit
it for "everything the cluster will give us".

Use this for post-incident triage:

> User: "Why did the cluster fail over at 03:00?"
> 1. `get_system_events(since_time="2026-05-24T02:50:00Z")`
> 2. Look for `severity="warning"|"error"` entries around that timestamp.

## Confirmation patterns

- `configure_auto_failover` *changes durable cluster state*. Always confirm
  before calling. Restate the values you're about to set and which cluster.
- Never call any of these against the wrong cluster — `cluster` parameter
  is optional but if you have any doubt, pass it explicitly. Use
  `list_clusters` from the meta tools when in doubt.

## What to avoid

- Don't poll `get_cluster_tasks` faster than once a second during a long
  rebalance; the management endpoint is shared with the GUI.
- Don't disable auto-failover in production unless you have an immediate
  reason and a plan to re-enable. Note the original values in chat before
  you change them so they're easy to restore.

## Rate limits & safety

Cluster tools are almost all `read` (60/sec):
`ping_cluster`, `get_cluster_info`, `get_cluster_details`,
`get_cluster_tasks`, `get_rebalance_progress`,
`get_auto_failover_settings`, `get_system_events`, `who_am_i`.

The single `write` (1/sec) tool here is `configure_auto_failover` —
matches the safety advice above: never call this without explicit
confirmation, and the rate limit gives you exactly one shot per second
to fat-finger it.

When polling `get_rebalance_progress` during a long rebalance, the read
rate (60/sec) is plenty but the management endpoint is shared with the
GUI. Once every 2–5 seconds is the polite poll interval; faster won't
get you better data and stresses the management plane.

If `RateLimitExceeded` comes back, honour `retry_after_sec` — back off,
don't retry-storm.

## Related skills

- `cb-analytics-admin` — Analytics service-level health (ingestion status, active queries) rather than cluster-level
- `couchbase-mcp` — full cluster administration (rebalance, node management, XDCR, eventing) via MCP-Couchbase
