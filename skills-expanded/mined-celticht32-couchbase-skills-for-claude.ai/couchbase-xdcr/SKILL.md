---
name: couchbase-xdcr
description: "Design and operate Couchbase XDCR (Cross-Datacenter Replication). Use whenever the user asks about XDCR, cross-datacenter replication, multi-region replication, active-active replication, active-passive replication, XDCR topology, XDCR references, XDCR replications, XDCR filtering, conflict resolution, last-write-wins, custom conflict resolution, XDCR conflict logging (8.x), admin_xdcr_* tools, replication lag, changes_left, or 'how do I replicate data between clusters / regions.' Distinct from couchbase-app-integration (application-layer XDCR-aware patterns) and couchbase-migration-execution (one-time data migration). Use proactively for disaster recovery planning, multi-region active-active architecture, read-local write-global patterns, and XDCR performance diagnosis."
license: MIT
---

# Couchbase XDCR

A skill for *designing and operating* Cross-Datacenter Replication between Couchbase clusters.

Distinct from:
- `couchbase-app-integration` — application code patterns for XDCR-aware reads and writes
- `couchbase-migration-execution` — one-time migration, not ongoing replication

If the conversation is "I need data in multiple regions" or "how do I keep two clusters in sync," this is the right skill.

## When this skill applies

- "How do I replicate between two clusters?"
- "Active-active vs active-passive — which should I use?"
- "How does conflict resolution work in XDCR?"
- "How do I filter which documents get replicated?"
- "How do I monitor XDCR lag?"
- "XDCR replication is behind — how do I diagnose it?"
- "What's the XDCR conflict log in 8.x?"

## Pick the right reference

| Question | Read |
|---|---|
| "Active-active vs active-passive — topology decision" | `references/topology.md` |
| "How do I create references and replications, filter docs, tune performance?" | `references/configuration.md` |
| "Conflict resolution — LWW, custom, 8.x conflict logging" | `references/conflict-resolution.md` |
| "Replication is lagging / errors / mismatched counts" | `references/troubleshooting.md` |

## Three core principles

**Principle 1 — Active-active means accepting eventual consistency and conflict potential.**
In active-active (bidirectional) XDCR, both clusters accept writes independently. When the same document is written on both sides before replication catches up, a conflict occurs. Couchbase resolves it automatically (last-write-wins by default in 7.x; custom resolution in 8.x), but the losing write is silently dropped. If you can't accept silent drops for any write, active-active is not the right topology.

**Principle 2 — XDCR is bucket-to-bucket, not cluster-to-cluster.**
A replication runs between a specific source bucket and a specific destination bucket. If you have 5 buckets, you need 5 replication configurations. Plan this explicitly — it's common to accidentally replicate only some buckets and have inconsistent DR coverage.

**Principle 3 — Filtering early costs less than filtering late.**
XDCR filtering (by key pattern, collection, or document expression) reduces the bandwidth and CPU of replication. Define your filter at creation time. Changing a filter on a running replication restarts replication from the checkpoint — which can cause a brief duplication of already-replicated documents on the destination.

## Quick tool map

| Task | Tool |
|---|---|
| List remote cluster references | `admin_xdcr_list_references` |
| Create a remote cluster reference | `admin_xdcr_create_reference` |
| Update a reference | `admin_xdcr_update_reference` |
| Delete a reference | `admin_xdcr_delete_reference` |
| List replications | `admin_xdcr_list_replications` |
| Create a replication | `admin_xdcr_create_replication` |
| Update replication settings | `admin_xdcr_update_replication` |
| Delete a replication | `admin_xdcr_delete_replication` |
| Get replication stats | `admin_stats_xdcr` |
| 8.x conflict log | `admin_xdcr_get_conflict_log` |

## Version notes

- **7.x:** XDCR references and replications, collection-aware replication (7.1+), LWW conflict resolution, expression-based filtering.
- **8.0+:** Custom conflict resolution functions (JavaScript), conflict logging via `admin_xdcr_get_conflict_log` — conflicts are captured rather than silently dropped, enabling audit and manual resolution workflows.

## Related skills

- `couchbase-app-integration` — application code for XDCR-aware reads, write conflicts, and active-active patterns
- `couchbase-sizing` — XDCR bandwidth estimation
- `couchbase-mcp` — the `admin_xdcr_*` tools
