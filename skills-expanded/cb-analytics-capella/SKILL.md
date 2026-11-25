---
name: cb-analytics-capella
description: |
  Use this skill when the user wants to manage Couchbase Capella resources
  through the Cloud Management API — listing organisations and clusters,
  provisioning or deleting clusters, triggering and restoring backups, or
  auditing API keys. Trigger when they mention "Capella", "cloud cluster",
  "capella_*", "organization", "project", "backup", "restore", or the
  Capella v4 API.
license: MIT
---

# Capella Management via cb-analytics-mcp

The 9 `capella_*` tools wrap Couchbase Capella's v4 Management API. They are
only available when `CB_CAPELLA_API_KEY_SECRET` is set; otherwise the tools
raise a clear `RuntimeError: Capella client is not configured`.

## The hierarchy

```
Organization (you may belong to several)
└── Project        (group of clusters; usually one per environment)
    └── Cluster    (the actual Capella deployment)
        └── Backup
```

Every cluster-scoped tool takes `(org_id, project_id, cluster_id)` in that
order. Use `capella_list_organizations()` and your own org's project IDs to
discover them — the tools don't accept names.

## Read-only first

- `capella_list_organizations()` — first call to discover IDs.
- `capella_list_clusters(org_id, project_id)` — see what exists.
- `capella_get_cluster(org_id, project_id, cluster_id)` — full details for one.
- `capella_list_backups(org_id, project_id, cluster_id)` — list available
  backups.
- `capella_list_api_keys(org_id)` — audit API key usage.

## Write operations (require confirmation)

- `capella_create_cluster(org_id, project_id, cluster_spec)` — `cluster_spec`
  is a free-form dict matching the v4 API schema; **don't guess it**, ask
  the user to paste the exact body, or refer them to Capella's UI's "View
  as JSON" feature.
- `capella_delete_cluster(org_id, project_id, cluster_id)` — **destructive**.
  Always restate the cluster name and project before calling.
- `capella_create_backup(org_id, project_id, cluster_id)` — triggers an
  immediate backup. Cheap; safe to retry on failure.
- `capella_restore_backup(org_id, project_id, cluster_id, backup_id, target_cluster_id=None)` —
  restore in place (omit `target_cluster_id`) or into a different cluster
  (set `target_cluster_id`). Always confirm the source backup id and
  destination cluster.

## What the tools won't do

- They don't create projects or organizations (rarely needed; do that in
  the Capella UI).
- They don't manage cluster networking, allowed CIDRs, or VPC peering — use
  the Capella UI or the broader v4 API directly.
- They don't subscribe / unsubscribe billing.

## Common failure modes

- **`AnalyticsAuthError`**: the API key is missing the required role for the
  org. The fix is in the Capella UI, not here.
- **`AnalyticsNotFoundError`**: a stale org/project/cluster id. Re-list
  parents to refresh.
- **`AnalyticsRequestError` with status 400**: the `cluster_spec` doesn't
  match what Capella expects. Surface the message body to the user
  verbatim; it usually names the offending field.

## What to avoid

- Don't `capella_delete_cluster` without an explicit, named confirmation in
  the conversation.
- Don't poll cluster status faster than every 30 seconds for long-running
  provisions; Capella throttles.
- Don't store the Capella API key in plain config files. Use the env var.

## Rate limits & safety

Capella tools split across rate-limit categories:

- **`read`** (60/sec): `capella_list_organizations`, `capella_list_clusters`,
  `capella_get_cluster`, `capella_list_backups`, `capella_list_api_keys`.
- **`write`** (1/sec): `capella_create_cluster`, `capella_delete_cluster`,
  `capella_create_backup`, `capella_restore_backup`.

Capella's own API throttles separately and more aggressively than our
local rate limit — long-running provisions reject status polling faster
than every ~30 seconds. So both buckets exist: ours (per-API-key,
in-process) plus Capella's (their service).

If a `RateLimitExceeded` comes back from our server, honour
`retry_after_sec`. If a 429/throttle comes from Capella itself, surface
the message verbatim — it usually names the offending limit.

Don't try to work around the write-rate limit on `capella_delete_cluster`
or `capella_restore_backup` by raising `RATE_LIMIT_WRITE_PER_SEC`. The
limit is there precisely because these operations are destructive at
cloud scale.

## Related skills

- `cb-analytics-cluster` — once connected to a Capella cluster, cluster-level ops use these tools
- `couchbase-mcp` — the MCP-Couchbase server has 16 read-only `capella_*` tools for org/project/cluster inspection (separate server, separate credentials)
