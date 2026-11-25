---
name: elasticsearch-opensearch-cluster-operations
description: >
  Covers Elasticsearch/OpenSearch shard and index lifecycle management
  (ILM/ISM: hot-warm-cold-delete tiers, rollover), cluster health triage
  (yellow/red status root-causing), and reindexing (mapping changes,
  zero-downtime cutover via aliases). Use when the user asks to "why is
  my Elasticsearch/OpenSearch cluster yellow/red," "set up an ILM/ISM
  policy," "reindex without downtime," "shards are unassigned," "design a
  hot-warm architecture," or "cluster health is degraded, what's the root
  cause."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Elasticsearch/OpenSearch Cluster Operations

## Purpose

Elasticsearch and OpenSearch (a fork sharing the same core architecture
and largely compatible APIs since the 2021 divergence) distribute an
index's data across shards, each of which is a full, independent Lucene
index — which means most day-2 operational problems are really shard
placement, shard sizing, or shard-lifecycle problems wearing a
"cluster health" costume. This skill covers triaging cluster health
(yellow/red status back to its actual root cause), managing an index's
lifecycle from hot ingestion through cold storage to deletion (ILM in
Elasticsearch, ISM in OpenSearch), and reindexing safely when a
mapping needs to change. It is the cluster-operations counterpart to
[elasticsearch-opensearch-configuration-validation](../elasticsearch-opensearch-configuration-validation/SKILL.md),
which validates index mapping and shard allocation settings *before*
production indexing begins rather than operating a cluster already
under load.

## When to use

- Cluster health shows `yellow` or `red` and the root cause isn't
  immediately obvious from the color alone.
- Designing or tuning an ILM/ISM policy: rollover conditions, hot-warm-
  cold tiering, or a delete phase that's either too aggressive or never
  firing.
- Planning a reindex to change a field's mapping (mappings are largely
  immutable once set — most type changes require a full reindex, not an
  in-place update).
- Shards are shown as `UNASSIGNED` and need root-causing before
  deciding on a fix.
- A specific node or the cluster overall is running low on disk and
  watermark-based allocation behavior needs to be understood before
  reacting.
- Planning a zero-downtime index cutover (alias-based) for a mapping
  change or a full data-model migration.

## Prerequisites & environment

- Elasticsearch 7.x/8.x or OpenSearch 1.x/2.x assumed for the API
  syntax below — call out explicitly where the two diverge (ILM vs.
  ISM policy JSON shape differ, though both express the same hot-warm-
  cold-delete phase model; OpenSearch retains the `_cat`/`_cluster` REST
  API surface largely unchanged from its Elasticsearch fork point).
- `monitor` cluster privilege at minimum for health/diagnostic API
  calls; `manage_ilm`/`manage_index_templates` (or OpenSearch's
  equivalent ISM permissions) to create/modify lifecycle policies;
  broader `manage` privilege needed for reindex and allocation-setting
  changes.
- A multi-node cluster (minimum 3 master-eligible nodes for real quorum-
  based master election — a single-node or 2-node cluster has no
  meaningful split-brain protection) for any guidance here about
  replica-driven fault tolerance to actually apply.
- For hot-warm-cold tiering: nodes explicitly tagged by tier (e.g.
  `node.attr.data: hot` / `warm` / `cold`) and index templates/ILM
  policies referencing those attributes — tiering does nothing without
  this node-attribute wiring in place first.
- Sufficient disk headroom below the configured allocation watermarks
  on every data node — the specific watermark percentages are
  version-configurable, so check the actual configured values
  (`cluster.routing.allocation.disk.watermark.*`) rather than assuming a
  specific default percentage.

## Step-by-step guidance

### 1. Triage cluster health by shard state, not the color alone

```bash
curl -s "http://<HOST>:9200/_cluster/health?pretty"
curl -s "http://<HOST>:9200/_cluster/allocation/explain?pretty"
```
- **Yellow**: all primary shards are assigned, but at least one replica
  is not — the cluster is fully readable/writable but under-replicated
  (reduced fault tolerance, not data loss). Common on a single-node
  cluster (nowhere to put a replica) or right after a node drops out
  (replicas being reassigned/rebuilt).
- **Red**: at least one **primary** shard is unassigned — some data is
  currently unavailable for reads/writes on that index. This needs
  immediate root-causing, not just waiting, since it's an active
  availability/data-access problem right now.
- `_cluster/allocation/explain` is the actual diagnostic tool — it
  returns the *specific* reason a given unassigned shard can't be
  allocated (disk watermark exceeded, allocation filtering rule
  excluding all eligible nodes, a shard awaiting a node that hasn't
  rejoined yet, too many shards already on eligible nodes hitting a
  total-shards-per-node limit) rather than requiring guesswork from the
  health summary alone.

### 2. Diagnose the specific unassigned-shard reason before reacting

```bash
curl -s "http://<HOST>:9200/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason"
```
Common `unassigned.reason` values and what each actually means:
- `NODE_LEFT` — the node holding this shard left the cluster; if it
  rejoins within the configured delay
  (`index.unassigned.node_left.delayed_timeout`, default 1 minute),
  Elasticsearch/OpenSearch prefers reusing its existing shard copy over
  a full reallocation/rebuild elsewhere — don't rush to force
  reallocation before that delay window if the node is expected back
  soon, since forcing it now discards a fast recovery path.
- `ALLOCATION_FAILED` — an allocation attempt failed (often a disk
  watermark or a corrupt shard) — check
  `_cluster/allocation/explain` for the specific underlying error.
- `INDEX_CREATED` immediately after creating an index with more replicas
  than there are eligible nodes to host them — expected and resolves by
  adding nodes or reducing `number_of_replicas`, not a fault.

### 3. Understand and respect disk-based allocation watermarks

```bash
curl -s "http://<HOST>:9200/_cluster/settings?include_defaults=true&pretty" \
  | grep -A2 watermark
```
Three thresholds gate shard allocation behavior as a node's disk fills:
low watermark (stop allocating *new* shards to this node), high
watermark (actively try to relocate shards *off* this node), and flood-
stage watermark (force all indices on this node into
`read_only_allow_delete` — writes are rejected outright). A flood-
stage breach is the actual cause behind a confusing "why can't I write
to this index anymore, nothing changed in the mapping" symptom — check
node disk usage before suspecting a mapping/application-side cause.
Recovering from flood-stage requires freeing real disk space (deleting
old indices via ILM, adding capacity) and then explicitly clearing the
read-only block once space is available:
```bash
curl -X PUT "http://<HOST>:9200/<index>/_settings" -H 'Content-Type: application/json' -d '
{ "index.blocks.read_only_allow_delete": null }'
```

### 4. Design an ILM (Elasticsearch) / ISM (OpenSearch) policy around real retention and query-recency needs

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": { "max_primary_shard_size": "50gb", "max_age": "7d" },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": { "set_priority": { "priority": 0 } }
      },
      "delete": {
        "min_age": "90d",
        "actions": { "delete": {} }
      }
    }
  }
}
```
Rollover on a size/age/doc-count threshold (`max_primary_shard_size`
keeps individual shards from growing unboundedly on a single logical
"index," which is really a rolling series of backing indices behind an
alias) rather than a single ever-growing index — this is what allows
older data to be moved to cheaper/warm/cold-tier nodes and eventually
deleted without touching data still being actively written. Set
`delete.min_age` based on the team's actual retention requirement (legal/
compliance minimums, if any, plus operational need), not an arbitrary
number — a delete phase firing too early is silent, irreversible data
loss with no restore path from within the cluster itself.

### 5. Reindex safely when a mapping change is needed

Mappings are largely immutable once a field is created (changing a
field's type, e.g. `text` to `keyword`, is not an in-place operation) —
the standard path is create-new-index, reindex, cut over the alias:
```json
PUT /logs-v2
{ "mappings": { "properties": { "status_code": { "type": "keyword" } } } }
```
```json
POST _reindex
{
  "source": { "index": "logs-v1" },
  "dest": { "index": "logs-v2" }
}
```
```json
POST _aliases
{
  "actions": [
    { "remove": { "index": "logs-v1", "alias": "logs" } },
    { "add": { "index": "logs-v2", "alias": "logs" } }
  ]
}
```
Applications should always read/write through the alias (`logs`), never
a concrete index name, so this cutover is atomic from the application's
perspective — no application redeploy or connection-string change
needed. For a large index still receiving writes during the reindex,
run the initial `_reindex` for the historical bulk, then use a second,
narrower reindex (or dual-write briefly) to catch documents written
during the first pass, before the final alias swap — a single
`_reindex` call is a point-in-time copy and will miss writes that land
on the source index after it starts.

### 6. Monitor shard count and size per node as a standing health check, not just at setup

```bash
curl -s "http://<HOST>:9200/_cat/allocation?v"
```
Too many small shards ("oversharding") wastes cluster overhead (every
shard has fixed per-shard memory/file-handle cost regardless of size);
too few, very large shards make recovery/relocation slow and increase
the blast radius of any single shard's failure. There's no single
universally-correct shard-size target — validate against your actual
cluster's node count, heap size, and query patterns rather than
copying a number from an unrelated deployment, but a large ILM-managed
time-series index growing to tens of GB per primary shard on
undersized nodes is a common early sign to investigate.

## Best practices

- Root-cause `red`/`yellow` health via `_cluster/allocation/explain`
  before taking any corrective action — reacting to the color alone
  (e.g. force-reallocating a shard that would have recovered on its own
  within the `node_left` delay) can make recovery slower, not faster.
- Design ILM/ISM rollover on a size or age threshold that keeps
  individual shards within a sane size range for your cluster's node
  specs, not a single ever-growing index — this is a prerequisite for
  hot-warm-cold tiering and bounded-cost deletion to work at all.
- Always read/write through an alias, never a concrete backing index
  name, so ILM rollover and reindex-based mapping changes are invisible
  to application code.
- Treat disk watermark breaches as a capacity-planning signal to act on
  before flood-stage, not just something to unblock reactively after
  writes start failing — alert on watermark proximity, not only on the
  read-only block itself.
- Validate a reindex's completeness (document counts matching, spot-
  checked field values correct) before cutting the alias over, and keep
  the old index available (not deleted) for a rollback window after
  cutover in case the new mapping surfaces an unexpected issue.

## Common pitfalls

- **Symptom:** Cluster health is `yellow` and stays that way
  indefinitely, with no obvious node failure.
  **Fix:** Often a single-node cluster (or a cluster with more replicas
  configured than there are eligible nodes to host them) — there is
  nowhere to place the replica shard. Check `_cat/allocation` for node
  count vs. `number_of_replicas`, and either add nodes or reduce
  replicas to match actual eligible node count, rather than treating
  perpetual yellow as an unexplained anomaly.

- **Symptom:** Writes to an index suddenly start failing with a
  read-only-related error, with no application or mapping change to
  explain it.
  **Fix:** A data node crossed the flood-stage disk watermark, which
  forces `index.blocks.read_only_allow_delete` on automatically. Check
  node disk usage first, free space (delete old ILM-managed indices,
  add capacity), then explicitly clear the block — it does not clear
  itself just because disk usage subsequently drops.

- **Symptom:** An ILM/ISM delete phase removes data earlier than
  expected, and there's no way to get it back.
  **Fix:** `min_age` in the delete phase was miscalculated (e.g.
  computed from index creation time under the assumption of a rollover
  cadence that later changed, or copy-pasted from a different policy
  with a shorter intended retention). This is an irreversible action —
  always double-check `min_age` against the current, real rollover
  cadence before applying an ILM/ISM policy change, and consider a
  snapshot-based backup policy (via the snapshot lifecycle management
  API) as a safety net independent of the ILM delete phase itself for
  any data with a real retention/compliance requirement.

- **Symptom:** A `_reindex` operation appears to complete successfully,
  but the new index is missing documents that were written to the old
  index during the reindex.
  **Fix:** `_reindex` is a point-in-time copy of the source index as it
  existed when the operation started — any writes to the source after
  that point aren't included. Run a follow-up reindex scoped to
  documents modified after the first pass's start time (via a range
  query on a timestamp field) before the alias cutover, or briefly
  dual-write to both indices during the transition window.

- **Symptom:** Someone runs a broad `DELETE /logs-*` (or an ILM delete
  phase misconfigured to match far more indices than intended) directly
  against production with no prior review.
  **Fix:** This is a destructive, irreversible action against
  potentially many indices at once — wildcard index deletes and ILM
  policy changes affecting a delete phase should go through the same
  review rigor as a database `DROP TABLE`. Always confirm the actual
  index pattern match (`GET /logs-*` to list what would be affected)
  before deleting, and prefer closing an index
  (`POST /<index>/_close`, reversible) over deleting it outright when
  the goal is just "stop it from being actively queried/written," not a
  genuine permanent removal.

## Worked example

**Scenario:** An application-logs cluster (`logs` alias over daily
rolling indices) shows `red` health, and a request to add a
`severity_code` field as a numeric type is also pending, but the field
currently exists as `text` in the mapping from an earlier, less
deliberate rollout.

1. Triage the `red` status:
   ```bash
   curl -s "http://<HOST>:9200/_cluster/allocation/explain?pretty"
   ```
   Output shows a primary shard `UNASSIGNED` with reason
   `ALLOCATION_FAILED`, and the detailed explanation points to the disk
   flood-stage watermark being exceeded on the only node that held that
   shard's data.
2. Free disk space: identify the oldest ILM-managed backing indices
   still present past their intended delete-phase age (an ILM policy
   bug — `delete.min_age` was set relative to index creation but
   rollover had been happening less frequently than assumed, so old
   indices were accumulating past their intended lifetime) and delete
   the confirmed-stale ones after checking the actual index list
   against the intended retention window.
3. Clear the resulting read-only block once space is freed:
   ```bash
   curl -X PUT "http://<HOST>:9200/logs-2026.07.10/_settings" -d '
   { "index.blocks.read_only_allow_delete": null }'
   ```
   Confirm health returns to `green`/`yellow` as expected for the node
   count.
4. Fix the ILM policy's `delete.min_age` to be computed against the
   actual current rollover cadence, preventing recurrence.
5. Handle the `severity_code` mapping change via create-new-index,
   reindex, alias-swap rather than attempting an in-place type change:
   ```json
   PUT /logs-v2
   { "mappings": { "properties": { "severity_code": { "type": "integer" } } } }
   ```
   ```json
   POST _reindex
   { "source": { "index": "logs-v1" }, "dest": { "index": "logs-v2" } }
   ```
   Verify document counts match, spot-check `severity_code` values
   parsed correctly as integers, then swap the `logs` alias — old index
   retained for a rollback window before eventual deletion under the
   (now-corrected) ILM policy.

## Cross-references

- [elasticsearch-opensearch-configuration-validation](../elasticsearch-opensearch-configuration-validation/SKILL.md) — validates index mapping and shard allocation/replica settings before production indexing begins, complementing the operational triage covered here.
- [redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md) — comparable cluster-topology and node-failure-handling concerns (shard/replica placement, quorum-based master election) in a different distributed-systems shape.
- [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md) — comparable sharding and chunk/shard-balancing concerns (shard key selection vs. shard/replica allocation here) if both systems are in the same platform.
