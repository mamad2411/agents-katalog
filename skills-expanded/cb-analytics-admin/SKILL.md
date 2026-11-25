---
name: cb-analytics-admin
description: |
  Use this skill when the user wants to inspect or manage the Analytics
  service's runtime — checking ingestion health, killing runaway queries,
  restarting nodes, or diagnosing performance. Trigger when they mention
  "ingestion status", "active queries", "completed requests", "restart
  service", "cancel request", "service status", or "Analytics health".
license: MIT
---

# Analytics service admin

You have 7 tools for runtime management.

## Status snapshot (read-only, safe)

- `get_service_status(cluster)` — overall service state, replica lag,
  authorised node list
- `get_ingestion_status(cluster)` — per-link ingestion state, pending ops
- `get_active_requests(cluster)` — what's running right now
- `get_completed_requests(client_context_id=None, cluster)` — recent
  history; pass `client_context_id` to filter to one request

## Diagnostic workflow

When a user says "queries are slow" or "ingestion looks stuck":

1. `get_service_status` — is the service even healthy? Watch `ccRevLag`
   (replication lag).
2. `get_ingestion_status` — for each link, look at `pendingOperations`. A
   non-zero pending count after a quiet period usually means a stuck link.
3. `get_active_requests` — long-running queries appear here with
   `elapsedTime`. Anything over a few seconds is suspect.
4. `get_completed_requests` — look for a pattern of errors or unusually
   long durations.

## Destructive operations (use with care)

- `cancel_request(client_context_id, cluster)` — abort one in-flight query.
  Get the id from `get_active_requests`.
- `restart_node(cluster)` — restart only the Analytics process on the
  local node. May briefly disrupt queries routed to that node.
- `restart_service(cluster)` — **cluster-wide** Analytics restart. All
  active queries fail. Don't suggest this lightly; warn the user.

## Confirmation patterns

When the user asks to cancel or restart anything, **always confirm** by
naming what you're about to do, with the specific request id or cluster
name. Example:

> Cancel request `cb-12345` on cluster `prod`? This will return an error
> to whichever client issued it.

After they confirm, run the tool and report success or failure based on
the returned `ok` field.

## What to avoid

- Don't restart the service to "fix" a slow query — try cancelling it first.
- Don't call `cancel_request` on a `client_context_id` that's already
  completed; it's a no-op but generates a confusing error.
- Don't poll `get_active_requests` aggressively (e.g. every second). Once
  per few seconds is fine.

## Rate limits & safety

Admin tools split across two rate-limit categories:

- **`read`** (60/sec): `get_service_status`, `get_ingestion_status`,
  `get_active_requests`, `get_completed_requests`.
- **`write`** (1/sec, intentionally conservative): `cancel_request`,
  `restart_service`, `restart_node`.

The write bucket is small on purpose. Cancelling one runaway query per
second is plenty; restarting a service every second would be madness.
If a `RateLimitExceeded` response comes back, the response includes
`retry_after_sec` — honour it. Don't retry-storm; that just keeps the
bucket empty.

Status calls share the read bucket with every other read-only tool across
the server (list_users, list_clusters, ping_cluster, etc.). If you're
polling status in a loop, keep the interval ≥ 2 seconds so the bucket
stays healthy for other concurrent work.

## Related skills

- `cb-analytics-query` — the query tools that generate the requests you'll be monitoring and cancelling
- `cb-analytics-cluster` — cluster-level health (nodes, rebalance, auto-failover) that underpins Analytics service health
