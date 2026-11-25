---
name: couchbase-upgrade
description: "Plan and execute Couchbase Server version upgrades, including rolling upgrades and the specific considerations for upgrading to 8.0. Use whenever the user asks about upgrading Couchbase, rolling upgrade, upgrade path, upgrade from 7.x to 8.0, upgrade checklist, cluster compatibility version, Magma storage engine default change in 8.0, 128 vBucket change in 8.0, EE features required for 8.0 defaults, pre-upgrade backup, post-upgrade verification, or 'how do I upgrade Couchbase without downtime.' Distinct from couchbase-mcp (which has an operational-runbooks reference covering rolling upgrade mechanics via MCP tools). This skill covers the planning, compatibility, and 8.0-specific breaking changes that require attention before and after the MCP-level upgrade steps."
license: MIT
---

# Couchbase Upgrade

Planning and executing Couchbase Server version upgrades — upgrade paths, breaking changes, pre/post-upgrade steps, and 8.0-specific considerations.

Distinct from the rolling upgrade section in `couchbase-mcp` (which covers the MCP tool sequence for executing the upgrade). This skill covers the *planning* layer: what to check before you run those tools.

## When this skill applies

- "How do I upgrade from 7.x to 8.0?"
- "What changed in 8.0 that could break my cluster?"
- "What's the safe upgrade path?"
- "How do I verify the upgrade worked?"
- "What's the cluster compatibility version?"
- "Do I need EE for 8.0 defaults?"

## Supported upgrade paths

Couchbase supports upgrading one major version at a time:

| From | To | Supported |
|---|---|---|
| 7.0 / 7.1 / 7.2 / 7.6 | 8.0 | Yes — rolling upgrade |
| 6.x | 8.0 | No — must go through 7.x first |
| Community Edition | Enterprise Edition | Requires reinstall, not in-place upgrade |

**Always upgrade to the latest patch of your current version before upgrading to the next major version.** Bugs fixed in patch releases can affect the upgrade process itself.

## Pre-upgrade checklist

- [ ] Full cluster backup (cbbackupmgr or Capella managed backup)
- [ ] Verify current cluster is healthy: all nodes `active` + `healthy`, rebalance not in progress, XDCR caught up (`changes_left` ≈ 0)
- [ ] Review breaking changes for the target version (see below for 8.0)
- [ ] Test the upgrade on a staging cluster first
- [ ] Check SDK compatibility: ensure your SDK versions support the target Couchbase version
- [ ] Read the release notes for your specific patch version

## Couchbase 8.0 breaking changes

**1. Magma storage engine is the new default (EE only)**

New buckets created on 8.0 EE use Magma with 128 vBuckets by default, instead of the previous Couchbase storage engine with 1024 vBuckets.

Impact:
- **Existing buckets are not changed** — they keep their current storage engine and vBucket count
- **New buckets created after upgrade** will use Magma 128 vBuckets unless you specify otherwise
- If your deployment scripts create buckets with hardcoded assumptions about 1024 vBuckets, update them
- If you need 1024 vBuckets for compatibility reasons, explicitly set `numVBuckets=1024` and `storageBackend=couchstore` when creating new buckets post-upgrade

Check your bucket creation scripts and IaC templates before upgrading.

**2. Cluster compatibility version gates 8.0 features**

During a rolling upgrade, the cluster runs in "mixed mode" — some nodes at 7.x, some at 8.0. During this window, 8.0-specific features (vector HVI/CVI indexes, new security features, 8.x Eventing APIs) are not available. They activate automatically once ALL nodes are on 8.0 and the cluster compatibility version advances.

Do not try to use 8.0-specific features until the upgrade is fully complete.

**3. EE-only features as defaults**

Some 8.0 defaults require Enterprise Edition:
- Magma storage engine (EE only)
- Hyperscale Vector Index (EE only)
- DARE at-rest encryption enhancements (EE only)

If you're on Community Edition, 8.0 upgrades still work but EE defaults don't apply. Verify your license tier before upgrading.

**4. Index Service memory model changes**

8.0 adds new index types (HVI, CVI) that use the Index Service RAM quota. If you're already near the Index Service memory limit, plan for the additional RAM that vector indexes may consume post-upgrade.

## Rolling upgrade sequence

The MCP tool sequence is in `couchbase-mcp` (operational-runbooks reference). Summary:

1. Confirm backup exists
2. Pick a node to upgrade first (prefer non-orchestrator)
3. Graceful failover the node
4. Upgrade the Couchbase binary on that node
5. Start the Couchbase service
6. Add the node back and rebalance
7. Verify the node is healthy
8. Repeat for each remaining node
9. Verify `cluster_compat_version` has advanced to 8.0 after all nodes are upgraded

**Capella:** upgrades are managed by Couchbase. You don't execute the rolling upgrade yourself. You can request an upgrade window or Couchbase may apply it automatically based on your support tier.

## Post-upgrade verification

```python
# Verify all nodes healthy and on 8.0
admin_cluster_details(cluster="prod")
# Check: all nodes show version 8.0.x, clusterMembership=active, status=healthy

# Verify cluster compat version
admin_cluster_status(cluster="prod")
# Check: cluster_compat_version should show 8.0

# Run a smoke test query
cb_query("SELECT COUNT(*) FROM `your-bucket` WHERE type IS NOT MISSING", cluster="prod")

# Verify XDCR is healthy if applicable
admin_stats_xdcr(cluster="prod")
# Check: changes_left ≈ 0, no errors
```

## SDK compatibility matrix

| Couchbase 8.0 | Python SDK | Java SDK | Node.js SDK | Go SDK | .NET SDK |
|---|---|---|---|---|---|
| Minimum version | 4.2+ | 3.4+ | 4.2+ | 2.6+ | 3.4+ |

Older SDK versions can connect to 8.0 clusters for basic operations but won't support 8.0-specific features (vector indexes, new security APIs). Update SDKs after the cluster upgrade.

## Related skills

- `couchbase-mcp` — rolling upgrade tool sequence (operational-runbooks reference)
- `couchbase-backup-restore` — pre-upgrade backup procedure
- `couchbase-magma` — Magma storage engine behavior in depth
- `couchbase-ai-applications` — 8.0 vector index types available post-upgrade
