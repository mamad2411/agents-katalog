---
name: couchbase-mcp
description: "Operate Couchbase clusters and Capella v4 through an MCP server. Primary target is celticht32/MCP-Couchbase (167 tools) for full data-plane AND cluster admin; also covers the official Couchbase-Ecosystem/mcp-server-couchbase (narrower, data-plane-only, community-maintained, enterprise-supported via AI Data Plane license) and when to pick which. Use whenever the user mentions Couchbase, buckets, scopes, collections, SQL++ / N1QL, KV ops, subdocument ops, FTS, vector indexes, XDCR, eventing, backup, encryption / KMIP / DARE, user lock/unlock, query performance, Index Advisor, synonyms (8.x), or Capella organizations / projects / clusters / database users / allowed CIDRs / app services. Use proactively for cluster admin (rebalance, failover, recovery, autofailover, autocompaction, logs, alerts, audit, password policy), RBAC design, troubleshooting Couchbase errors, operational runbooks (rolling upgrade, node add/remove, post-failover recovery, backup/restore, credential rotation), and observability."
license: MIT
---

# Couchbase MCP

A skill for operating Couchbase through an MCP server. Two servers cover this space, and they are **not** interchangeable — pick based on how much of the surface you need.

## Which MCP server — read this first

| | **celticht32/MCP-Couchbase** (this skill's primary) | **Couchbase-Ecosystem/mcp-server-couchbase** (official) |
|---|---|---|
| **Maintainer** | Independent (Chris Ahrendt / celticht32) | Couchbase-Ecosystem — community-maintained; NOT covered by Couchbase's support team unless licensed (see below) |
| **Surface** | ~167 tools: full data plane **plus** cluster admin (buckets/scopes/collections, users/RBAC, rebalance/failover/recovery, XDCR, eventing, backup, KMIP/DARE), 8.x features (vector indexes, synonyms, user lock), Capella v4 control plane, perf diagnostics | Deliberately narrow: bucket-scoped data plane only — Cluster Health, Data/Schema, Key-Value, Query, Performance (index list, Index Advisor, slow-query analysis) |
| **Admin ops** (create bucket, rebalance, failover, XDCR, eventing, backup, encryption) | Yes | **No** — not in scope |
| **Capella control plane** (orgs/projects/clusters/allowlists) | Yes (read-only `capella_*` tools) | No |
| **Auth / runtime** | Cluster creds + Capella API key; two server processes | Python 3.10+, PyPI/Docker; `CB_CONNECTION_STRING` + basic auth or mTLS; STDIO or Streamable HTTP; bucket-scoped |
| **Safety** | `CB_MCP_READ_ONLY_MODE` + per-tool `confirm:true` gate | `CB_MCP_READ_ONLY_MODE` / `CB_MCP_READ_ONLY_QUERY_MODE` (read-only query default) |
| **Enterprise support** | None (independent project) | Available by **licensing Couchbase AI Data Plane**, which also entitles Couchbase Agent Memory + Agent Catalog (GA 2026-06-30) |

**How to choose:**
- **Cluster administration, XDCR, eventing, backup, encryption, Capella control-plane inspection, or perf-analysis beyond Index Advisor** → celticht32/MCP-Couchbase. The official server can't do these.
- **Just KV + SQL++ + schema/health/Index-Advisor on a single bucket, want the vendor-tracked package, or need enterprise support via an AI Data Plane license** → the official Couchbase-Ecosystem server.
- Tool names below (`cb_*`, `admin_*`, `capella_*`) are the **celticht32** server's. The official server uses its own (shorter) tool names — check its README when connected to it. The two do not share a namespace.

Note: celticht32 contributed index-management tools upstream to the official server (PR #187). Overlap in the *data-plane* basics is expected; the *admin* surface is unique to celticht32/MCP-Couchbase.

The rest of this skill documents the **celticht32/MCP-Couchbase** server (~167 tools across 17 categories), covering the full Couchbase data-plane and cluster administration surface.

## When this skill applies

Any time the user is working with Couchbase. The MCP server exposes tools across these areas:

- **Data plane**: KV operations (get/upsert/insert/replace/delete, multi-get, subdocument lookup_in/mutate_in), SQL++ queries, FTS search, analytics queries, transactions
- **Cluster admin**: buckets, scopes, collections, sample buckets, indexes (including vector indexes for 8.x), FTS index management, synonyms
- **Operations**: rebalance, failover, recovery, autofailover, autocompaction, logs, alerts, server groups
- **Security**: users, groups, roles, audit, password policy, security settings, lock/unlock (8.x)
- **Cross-datacenter**: XDCR replication, conflict logging (8.x)
- **Advanced services**: eventing functions, backup repositories, encryption (DARE), KMIP key management
- **Diagnostics**: query performance analysis (slowest queries, frequency analysis, covering-index gaps, schema inference, index advisor)
- **Capella v4 control plane**: read-only inspection of organizations, projects, clusters, database users, allowed CIDRs, API keys, app services

If a task touches any of the above, prefer this skill's tools. The list above is the menu — pick from it before reaching for raw REST API calls or another MCP server.

## Quick orientation: pick the right reference

The 167 tools split into a few clusters that share connection settings, conventions, and gotchas. Read the reference that matches the task at hand — don't read all of them upfront:

| Task domain | Read this reference |
|---|---|
| KV CRUD, SQL++, query, subdoc, FTS, transactions, analytics | `references/data-plane.md` |
| Buckets, scopes, collections, users, groups, roles, cluster ops, XDCR | `references/cluster-admin.md` |
| Vector indexes, synonyms, KMIP, user lock/unlock, conflict logging | `references/couchbase-8x.md` |
| Capella organizations, projects, clusters, allowlists, API keys | `references/capella-v4.md` |
| Performance analysis, EXPLAIN, schema inference, index advisor | `references/diagnostics.md` |
| Anything destructive (delete, drop, restore, rebalance) | `references/safety.md` — read this BEFORE writing the call |
| RBAC design, audit strategy, password policy, KMIP-vs-DARE decision, network isolation | `references/security-best-practices.md` |
| Errors and unexpected results (connection failures, auth issues, query/index problems, replication lag, eventing failures) | `references/troubleshooting.md` |
| Multi-step procedures (rolling upgrade, add/remove node, post-failover recovery, restore from backup, credential rotation, enabling DARE) | `references/operational-runbooks.md` |
| Monitoring, alerting, Prometheus integration, what metrics matter | `references/observability.md` |
| "What's the tool name for X?" | `references/tool-index.md` |

Each reference is self-contained. The `tool-index.md` is the fastest path to the exact tool name when you already know what you want to do.

## Two server instances (celticht32 distribution)

Within the **celticht32/MCP-Couchbase** distribution (not the official server), there are **two separate MCP server processes** because they need different credentials and talk to different APIs:

1. **Cluster server** (default) — 151 tools talking to a specific Couchbase cluster via `CB_CONNECTION_STRING`, `CB_USERNAME`, `CB_PASSWORD`. Most tools you'll use.
2. **Capella v4 server** (separate) — 16 read-only tools talking to `cloudapi.cloud.couchbase.com` via `CAPELLA_API_KEY_SECRET` (Bearer auth).

These have **non-overlapping** tool name prefixes:
- Cluster server tools: `cb_*` (data plane) and `admin_*` (cluster admin)
- Capella server tools: `capella_*`

When the user asks about "Capella" they may mean either:
- The **control plane** (the Capella SaaS dashboard concept — orgs, projects, IP allowlists, billing) → use `capella_*` tools
- A **cluster hosted on Capella** (a specific deployment they're querying) → use `cb_*` / `admin_*` tools, just with `couchbases://` connection string and port 18091

If unclear, ask. The blast radius differs: control-plane tools are scoped to one Capella API key, cluster tools are scoped to one deployment's credentials.

## Safety primer (read this even for "simple" tasks)

The MCP server itself enforces two safety mechanisms at the `server.py` layer:

1. **Read-only mode** (`CB_MCP_READ_ONLY_MODE=true`) filters destructive tools out of the tool listing entirely. If the user sets this, you won't even see tools like `admin_bucket_delete` — that's intentional. Don't try to work around it.
2. **Confirmation gate** — destructive tools require `confirm: true` in the arguments. If you call `admin_bucket_delete` without `confirm:true`, the server returns an error explaining what would have happened. Always describe the impact to the user FIRST, get confirmation, THEN pass `confirm:true`.

**Categories of operations to think about twice before calling:**

- **Data destruction**: `cb_delete`, `admin_bucket_delete`, `admin_bucket_flush`, `admin_scope_drop`, `admin_collection_drop`, `admin_index_drop`, `admin_fts_index_delete`
- **Cluster topology changes**: `admin_rebalance_start`, `admin_failover_node`, `admin_recovery_set`
- **Security changes**: `admin_user_delete`, `admin_user_lock`, `admin_security_set`, `admin_audit_set`
- **Replication / backup**: `admin_xdcr_delete_replication`, `admin_backup_restore_run`
- **Encryption rotation**: `admin_encryption_rotate`, `admin_kmip_rotate`

See `references/safety.md` for the full taxonomy of destructive operations and how to surface them to the user.

## Conventions for tool calls

A few patterns repeat across most tools and are worth knowing up front:

**Connection scoping**: Data-plane tools (`cb_*`) take the bucket / scope / collection from arguments when present, falling back to `CB_BUCKET` / `CB_SCOPE` / `CB_COLLECTION` env vars. Admin tools (`admin_*`) typically address cluster-scoped resources by name (e.g., a bucket name string) and don't need a default scope.

**JSON in / JSON out**: All tools return JSON. For tools that wrap REST endpoints, the response usually has a `status` field (`ok` / `error`) and a `data` field with the actual payload. For data-plane tools (`cb_get`, `cb_query`), the response is the document or query result rows directly.

**Capella tools are read-only by design**: There is no `capella_cluster_create` or `capella_user_invite` — those operations are deliberately out of scope. If the user needs to make changes to a Capella deployment, point them at the Capella web UI.

## How to pick a tool when given a task

The naming is consistent enough that you can usually guess. But if you're unsure:

1. **Operation on data?** → `cb_*` (e.g., `cb_get`, `cb_query`, `cb_lookup_in`)
2. **Operation on a Couchbase resource (bucket/index/user)?** → `admin_<resource>_<verb>` (e.g., `admin_bucket_create`, `admin_user_lock`)
3. **Inspection of Capella SaaS structure?** → `capella_<resource>_<verb>` (e.g., `capella_clusters_list`)
4. **Performance analysis?** → `cb_perf_*` family (see `references/diagnostics.md`)
5. **Couchbase 8.x-specific?** → check `references/couchbase-8x.md` first; these tools fail loudly if you're connected to a 7.x cluster

If none of these patterns match the task, the operation may not be supported. Check `references/tool-index.md` for the full listing before concluding the MCP can't do it.

## Examples of correct use

**Example 1 — User asks "show me my buckets":**

The right tool is `admin_bucket_list`. Don't run `cb_query` against `system:keyspaces` to enumerate — there's a direct tool for this.

**Example 2 — User asks "what's slow in my workload?":**

This is a query performance analysis task. Read `references/diagnostics.md` then call `cb_perf_slowest_queries` and `cb_perf_most_frequent` for a starting picture. Optionally follow up with `cb_perf_not_using_covering_index` to find missing-index opportunities.

**Example 3 — User asks "create a vector index on my embedding field":**

This is Couchbase 8.x-specific. Read `references/couchbase-8x.md` to understand the difference between Hyperscale and Composite vector indexes. The Hyperscale variant scales further but costs more; Composite is the default for most workloads. Then call `admin_vector_index_create_composite` or `admin_vector_index_create_hyperscale` with the bucket / scope / collection / field / dimension / similarity arguments.

**Example 4 — User asks "what clusters do I have in Capella?":**

This is the control plane (`capella_*`). Read `references/capella-v4.md` for the resource hierarchy. The walk-down is: `capella_organizations_list` → grab the orgId → `capella_projects_list` with that orgId → grab a projectId → `capella_clusters_list` with both. You can't list clusters without the orgId and projectId — Capella has no global cluster view across organizations.

**Example 5 — User asks "delete bucket X":**

Read `references/safety.md` BEFORE responding. Confirm with the user what they want, describe the impact ("this will delete the bucket and all its data; no recovery without backup"), get explicit confirmation, then call `admin_bucket_delete` with `confirm: true`. If `CB_MCP_READ_ONLY_MODE=true` is set, the tool won't be available — tell the user to either temporarily unset it or do this operation through the Couchbase web console.

## Tool name reference

If you encounter references to older or alternative tool names for common operations, use this mapping:

| Alternative name | Tool name in this server |
|---|---|
| `get_document_by_id` | `cb_get` |
| `upsert_document_by_id` | `cb_upsert` |
| `insert_document_by_id` | `cb_insert` |
| `replace_document_by_id` | `cb_replace` |
| `delete_document_by_id` | `cb_delete` |
| `run_sql_plus_plus_query` | `cb_query` |
| `explain_sql_plus_plus_query` | `cb_explain_query` |
| `get_schema_for_collection` | `cb_get_schema_for_collection` |
| `get_index_advisor_recommendations` | `cb_index_advisor` |
| `list_indexes` | `admin_index_list` |
| `get_buckets_in_cluster` | `admin_bucket_list` |
| `get_cluster_health_and_services` | `admin_cluster_status` |
| `get_longest_running_queries` | `cb_perf_longest_running` |
| `get_most_frequent_queries` | `cb_perf_most_frequent` |
| `get_queries_not_selective` | `cb_perf_not_selective` |
| `get_queries_not_using_covering_index` | `cb_perf_not_using_covering_index` |
| `get_queries_using_primary_index` | `cb_perf_using_primary_index` |
| `get_queries_with_large_result_count` | `cb_perf_large_result_count` |
| `get_queries_with_largest_response_sizes` | `cb_perf_large_response_sizes` |

