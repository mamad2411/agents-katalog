---
name: elasticsearch-opensearch-configuration-validation
description: >
  Validates proposed Elasticsearch/OpenSearch index mapping, shard count/
  replica allocation, and ILM/ISM policy settings before production
  indexing begins — checking primary shard count against expected data
  volume and node count, mapping field types against real query
  patterns, and replica/allocation-awareness settings against actual
  failure domains. Use when the user asks to "review this index mapping
  before we start indexing," "validate shard count for this index,"
  "check this ILM policy is safe before we apply it," or "will this
  Elasticsearch/OpenSearch config change require a reindex."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Elasticsearch/OpenSearch Configuration Validation

## Purpose

An Elasticsearch/OpenSearch index's most consequential decisions —
primary shard count and field mapping types — are effectively fixed at
creation time: primary shard count cannot be changed without a reindex
or `_split`/`_shrink` operation, and most mapping field-type changes
require a full reindex rather than an in-place update. That makes
pre-production validation disproportionately valuable here compared to
databases where a config mistake is a quick `ALTER`. This skill is the
validation gate — checking a proposed mapping, shard count, replica
setting, or ILM/ISM policy against real data volume, query patterns,
and failure-domain topology before an index goes live — complementing
the day-2 operational and reindexing guidance in
[elasticsearch-opensearch-cluster-operations](../elasticsearch-opensearch-cluster-operations/SKILL.md).

## When to use

- Before creating a new index (or index template) in production, to
  validate primary shard count against expected data volume and node
  count.
- Before finalizing a mapping for a new index, to validate field types
  match actual query patterns (e.g. `keyword` vs. `text`, whether a
  field needs to be searchable at all) since most mapping changes later
  require a full reindex.
- Before applying a new or modified ILM/ISM policy, to validate rollover
  thresholds and delete-phase retention against the real intended data
  lifecycle.
- Before changing `number_of_replicas` or allocation-awareness
  attributes, to validate the change actually improves the fault
  tolerance it's intended to.
- As a review gate for infrastructure-as-code or index-template
  automation that provisions Elasticsearch/OpenSearch indices.

## Prerequisites & environment

- `monitor` and `manage_index_templates` privileges (read-level) for
  validation queries; write/`manage` privileges only needed to apply a
  validated change.
- Elasticsearch 7.x/8.x or OpenSearch 1.x/2.x assumed for API syntax
  below; note explicitly where the two diverge (ILM vs. ISM policy JSON
  shape) or where a specific version changed default behavior (e.g.
  Elasticsearch's default `number_of_shards` moved from 5 to 1 in
  7.0 — validate the *actual configured* default on the cluster/template
  in question rather than assuming a version-specific default applies).
- Knowledge of expected data volume (documents/day or total corpus size)
  and query patterns (which fields are filtered, sorted, or aggregated
  on) for the index being validated — mapping and shard-count validation
  is meaningless without this context from the owning team.
- Knowledge of the actual cluster's node count, per-node heap size, and
  existing shard distribution (`_cat/allocation`), to validate a
  proposed shard count against real capacity rather than in isolation.
- Access to a staging cluster with a representative (if smaller) node
  topology, to test a mapping/ILM policy against realistic data shape
  before production rollout.

## Step-by-step guidance

### 1. Validate primary shard count against expected data volume and node count

```bash
curl -s "http://<HOST>:9200/_cat/nodes?v&h=name,heap.max,disk.avail"
curl -s "http://<HOST>:9200/_cat/allocation?v"
```
- Primary shard count **cannot be changed after index creation** without
  a `_split` (increase) or `_shrink` (decrease) operation, both of which
  have their own constraints (`_split` requires the original shard count
  to evenly divide into the new one), or a full reindex. Validate the
  proposed count against a real estimate of total data size ÷ target
  per-shard size (a commonly cited healthy range is roughly 10–50GB per
  shard, but validate against your actual node heap/disk rather than
  treating that as a hard rule), not a default carried over from an
  unrelated index.
- Flag a shard count that would leave individual shards very small
  (oversharding) — each shard has a fixed per-shard overhead in cluster
  state and node memory regardless of how little data it holds, and a
  cluster with many tiny shards degrades before it should on pure data-
  volume grounds.
- Flag a shard count of 1 for an index expected to grow well beyond a
  single reasonable shard size with no rollover/ILM policy in place to
  create new backing indices — validate that either the shard count is
  sized for the full expected lifetime volume, or an ILM/ISM rollover
  policy is already wired up so growth is handled by new backing
  indices instead of one shard growing unbounded.

### 2. Validate mapping field types against actual query patterns before data starts landing

```json
GET /<index>/_mapping
```
- `text` fields are analyzed (tokenized) for full-text search but cannot
  be used for exact-match filtering, sorting, or aggregation without a
  `keyword` sub-field or a separate `keyword`-typed field — validate
  that any field intended for exact match/filter/sort/aggregation
  (status codes, IDs, categorical tags) is mapped `keyword`, not `text`,
  from the start.
  ```json
  "status": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } }
  ```
- Validate numeric fields are typed as the smallest sufficient numeric
  type for the actual value range (`integer` vs. `long`, `float` vs.
  `double`) — oversized numeric types waste memory across every
  document at scale with no query benefit if the value range never
  needs it.
- Validate `dynamic` mapping settings deliberately rather than leaving
  the cluster/index default unexamined: fully dynamic mapping
  (`"dynamic": true`, the default) lets an unexpected or malformed field
  in a single document silently create a new mapped field cluster-wide,
  which can bloat cluster state or cause a mapping-type conflict later
  if a differently-typed value for the "same" field name arrives from a
  different source. Consider `"dynamic": "strict"` (reject unmapped
  fields outright) or `"dynamic": "false"` (accept but don't index them)
  for indices with a well-understood, stable schema.
- Validate any field genuinely never queried isn't needlessly indexed
  (`"index": false` on a field only ever retrieved via `_source`, not
  searched/filtered/aggregated) — indexing costs write throughput and
  disk for no query benefit if unused.

### 3. Validate replica count and allocation-awareness against real failure domains

```bash
curl -s "http://<HOST>:9200/_cluster/settings?pretty" | grep -A5 awareness
```
- `number_of_replicas` should be validated against the actual number of
  nodes in the target failure domain(s), not just "at least 1 for
  safety" — a replica configured but with no eligible node available in
  a different failure domain than the primary provides no real fault
  tolerance even though the cluster reports the shard as assigned.
- If `cluster.routing.allocation.awareness.attributes` (e.g. `zone`) is
  configured, validate every relevant node actually carries the
  corresponding `node.attr.zone` setting — a node missing the attribute
  is treated as its own implicit group by the allocator, which can
  produce lopsided shard distribution that isn't obvious from
  `_cluster/health` alone. Cross-check with:
  ```bash
  curl -s "http://<HOST>:9200/_cat/nodeattrs?v"
  ```
- Validate `number_of_replicas` doesn't exceed the number of eligible
  nodes available to host them under the awareness constraints in
  place — this produces a perpetually `yellow` index that will never
  resolve to `green` without either adding nodes or reducing the
  replica count, a common false alarm that wastes on-call time if not
  caught during review.

### 4. Validate an ILM/ISM policy's rollover and retention math against the real intended lifecycle

```json
GET _ilm/policy/<policy-name>
```
- Validate `rollover` conditions (`max_primary_shard_size`, `max_age`,
  `max_docs`) actually align with expected ingest rate — a rollover
  `max_age` set far longer than the realistic time to reach the size
  threshold means rollover is effectively size-only in practice (not
  wrong, but validate that's the intended behavior, not an unexamined
  default).
- Validate `delete.min_age` against the actual, current rollover
  cadence, not a value computed under an earlier or assumed cadence — a
  common source of unintended early deletion is a retention window
  computed as "N rollover periods" when the real rollover interval later
  changed (e.g. from daily to weekly) without updating the ILM policy's
  age-based thresholds to match.
- Validate any `shrink`/`forcemerge` action in a warm/cold phase is
  scheduled with realistic `min_age` relative to real query patterns —
  `forcemerge` is I/O-intensive and should only run once an index is
  genuinely done receiving writes, and a `shrink` action reduces shard
  count (must evenly divide the current count) which affects the same
  per-shard-size considerations validated in step 1.

### 5. Validate a mapping/shard-count change against a staging index with representative data before production

Apply the proposed mapping or shard count to a staging index seeded
with data of the real expected shape and volume (not just row count —
field cardinality and value-length distribution matter for both mapping
memory footprint and shard-size projections), and confirm actual
resulting shard sizes and query latency before committing to the same
config in production, since a reindex to correct a bad choice after
data has accumulated is exactly the expensive operation this validation
step is meant to avoid.

## Best practices

- Treat primary shard count and mapping field types as effectively
  permanent decisions requiring the same review rigor as an
  irreversible schema choice — validate against real expected volume and
  query patterns before the first document is indexed, not after.
- Default new indices to `dynamic: "strict"` (or at minimum `"false"`)
  unless there's a specific, understood reason to allow fully dynamic
  mapping — an uncontrolled dynamic mapping is a common source of
  cluster-state bloat and silent mapping-type conflicts.
- Validate `number_of_replicas` against real, current node/failure-
  domain availability at review time, not against a static "always set
  to 1" policy that might not actually be achievable given the current
  cluster shape.
- Recompute ILM/ISM `delete.min_age` any time the rollover cadence
  changes — treat a cadence change as requiring a retention-math review,
  not an independent, unrelated setting.
- Require a staging validation pass with representative data shape
  before approving a new index's shard count/mapping for production,
  given how expensive a post-hoc correction (full reindex) is compared
  to the validation effort.

## Common pitfalls

- **Symptom:** An index created with a single primary shard grows far
  beyond a healthy shard size within weeks, and query/indexing latency
  degrades steadily with no way to fix it without a full reindex.
  **Fix:** Shard count wasn't validated against realistic growth
  projections, and no ILM/ISM rollover policy was in place to create new
  backing indices as it grew. Validate shard count (or rollover policy
  presence) against expected total lifetime volume at review time, not
  just initial/day-one volume.

- **Symptom:** A field intended for filtering/aggregation
  (`status`, `region`, an ID field) throws an "illegal_argument" /
  "fielddata" error when the application tries to sort or aggregate on
  it, or aggregation results look wrong (split by tokenized terms
  instead of exact values).
  **Fix:** The field was mapped `text` (analyzed/tokenized) instead of
  `keyword`. Since mapping type changes aren't in-place, this requires a
  full reindex to a corrected mapping — validate every field's intended
  query usage (full-text search vs. exact match/filter/sort/aggregate)
  against its mapping type before the index goes live, to avoid this
  reindex.

- **Symptom:** An index stays `yellow` indefinitely no matter how long
  it's given, and `_cluster/allocation/explain` shows a replica simply
  has no eligible node to allocate to.
  **Fix:** `number_of_replicas` was set without validating it against
  the real number of nodes available under the current allocation-
  awareness constraints (e.g. zone awareness configured with replicas
  requested across more zones than actually exist). Validate replica
  count against actual eligible-node availability at review time, not a
  blanket policy value.

- **Symptom:** An ILM policy's delete phase removes data noticeably
  earlier than the team's intended retention period.
  **Fix:** `delete.min_age` was computed assuming a rollover cadence
  that has since changed (e.g. rollover now happens weekly instead of
  daily, but the delete-phase age threshold was never recalculated).
  Validate `delete.min_age` against the *current* rollover cadence
  every time either setting changes, and treat any retention-window
  computation error as effectively irreversible once the delete phase
  has fired, since there's typically no in-cluster restore path.

- **Symptom:** A reviewer approves a new index template with fully
  dynamic mapping (`"dynamic": true`, unexamined default) for a
  high-volume, externally-fed data source, and a malformed upstream
  field later causes a mapping-type conflict that blocks indexing for
  an entire index.
  **Fix:** Fully dynamic mapping let an unexpected field auto-create a
  mapping that a later document's differently-typed value for the "same"
  field name then conflicts with, rejecting those documents outright.
  Validate `dynamic` mapping setting deliberately for any externally-fed
  or loosely-controlled data source — prefer `"strict"` or `"false"` with
  an explicit, reviewed mapping for expected fields, treating an
  unreviewed fully-dynamic mapping as a finding, not an acceptable
  default.

## Worked example

**Scenario:** A team requests review of a new index template for a
customer-events data source, expected to ingest ~50M documents/day, with
a proposed mapping and a 5-primary-shard, 1-replica configuration, no
ILM policy attached yet, and `dynamic: true` left at default.

1. Validate shard count against volume: 50M docs/day at an estimated
   average document size puts daily data volume in a range that would
   overload 5 shards within a couple of weeks at a healthy per-shard
   size target on this cluster's node specs. Flag as needing an ILM
   rollover policy rather than a single static index — recommend
   `max_primary_shard_size: 40gb` / `max_age: 1d` rollover instead of
   relying on shard count alone to absorb the full expected volume.
2. Validate mapping field types: `customer_id`, `event_type`, and
   `region` were mapped `text` by the (unexamined) dynamic default.
   Flag as blocking — the team confirms all three are always used for
   exact filtering/aggregation, never full-text search. Corrected
   mapping specifies `keyword` explicitly for these fields.
3. Validate `dynamic` setting: default `true` risks a malformed upstream
   field (a known-unreliable third-party event source feeds this index)
   creating an unreviewed mapped field or a later type conflict. Flag
   and recommend `dynamic: "strict"` with all expected fields explicitly
   mapped, since the event schema is well-documented and stable.
4. Validate replica/allocation: cluster has 3 nodes across 3 zones with
   zone awareness configured; 1 replica is achievable and provides real
   zone-level fault tolerance — approved as-is.
5. Revised template approved: `keyword` mappings for filter/aggregate
   fields, `dynamic: "strict"`, ILM rollover policy attached at index-
   template creation time (not added retroactively after data has
   already accumulated in an unmanaged single index), `number_of_replicas:
   1` confirmed safe under existing zone topology — validated against a
   staging index seeded with a day's worth of representative sample data
   before the production template is applied.

## Cross-references

- [elasticsearch-opensearch-cluster-operations](../elasticsearch-opensearch-cluster-operations/SKILL.md) — the operational depth (health triage, ILM/ISM mechanics, reindexing procedure) this skill's validation checks are grounded in, and where to go once an index is already live and needs a corrective reindex.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — comparable pre-production configuration validation discipline (restart/rebuild-required changes, capacity math) applied to PostgreSQL, useful as a pattern reference in a polyglot environment.
- [redis-configuration-validation](../redis-configuration-validation/SKILL.md) — comparable validation approach (matching a data-store's config to actual data classification and failure-domain topology) applied to Redis.
