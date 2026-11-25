---
name: arangodb-multi-model-database-operations
description: >
  Covers operating ArangoDB, a multi-model database combining document,
  graph, and key-value collections in a single engine with a unified
  query language (AQL): collection type selection, graph traversal via
  AQL, and cluster configuration (coordinators, DB-servers, agency).
  Use when the user asks to "write an AQL query," "should I use a
  document or edge collection in ArangoDB," "set up an ArangoDB
  cluster," "why is this AQL graph traversal slow," or "choose between
  ArangoDB and a single-purpose database for a mixed graph/document
  workload."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# ArangoDB Multi-Model Database Operations

## Purpose

ArangoDB's distinguishing architectural bet is **multi-model in one
engine**: document collections, key-value access, and graph data
(via edge collections connecting document vertices) all live in the
same database, queried through a single language — **AQL** (ArangoQL) —
rather than requiring separate document, graph, and key-value systems
stitched together at the application layer. This is a materially
different trade-off than a graph-only engine like
[neo4j-graph-database-operations](../neo4j-graph-database-operations/SKILL.md):
ArangoDB is the right choice when a workload genuinely needs both
general document storage and graph traversal against the same data
without operating two databases, at the cost of graph traversal
performance that (for very deep or very high-fan-out traversals)
doesn't match a purpose-built graph engine's native storage layout.
This skill covers AQL fundamentals for ops, collection-type selection,
and cluster configuration (coordinators, DB-servers, the Raft-based
agency) — the operational core for running ArangoDB reliably at scale.

## When to use

- Deciding whether a new collection should be a document collection,
  an edge collection (for graph relationships), or accessed purely as
  key-value, and modeling accordingly.
- Writing or debugging an AQL query, especially a graph traversal
  (`FOR v, e, p IN ... GRAPH`) that's slow or returns unexpected results.
- Setting up or troubleshooting an ArangoDB cluster: coordinators,
  DB-servers (the actual data-holding shards), and the agency (Raft-
  based cluster metadata/consensus layer).
- Choosing sharding keys for a document collection, or a graph's vertex
  collections, to avoid an unevenly loaded cluster.
- Evaluating ArangoDB against running separate document/graph/key-value
  systems for a workload that genuinely spans all three access
  patterns.

## Prerequisites & environment

- ArangoDB 3.11+ assumed for the AQL syntax below; note that
  SmartGraphs (sharded graphs with locality-aware placement, an
  Enterprise Edition feature) require the Enterprise Edition, while
  standard (non-Smart) graphs and cluster mode itself are available in
  the Community Edition.
- For cluster mode: at least 3 **agency** nodes (Raft consensus for
  cluster metadata — the same odd-quorum requirement as any Raft-based
  system elsewhere in this repo), at least 1 **coordinator** (stateless
  query-routing/aggregation layer that clients connect to), and at
  least 2 **DB-servers** per shard's replication factor (the nodes that
  actually store shard data).
- `arangosh` (the ArangoDB shell) or the HTTP API for administrative
  operations; a user with the `Administrate` database access level for
  collection/index/graph management.
- Familiarity with the workload's actual access pattern (pure document
  lookups vs. genuine multi-hop graph traversal vs. a mix) before
  choosing collection types and sharding keys — like Cassandra
  partition-key design, this is a decision that's expensive to change
  after data and shard layout are established.

## Step-by-step guidance

### 1. Choose collection type deliberately: document, edge, or both via a named graph

```aql
// Document collections hold vertices (or standalone documents with no graph role)
db._create("users");
db._create("products");

// Edge collections hold relationships — _from/_to reference other collections' documents
db._createEdgeCollection("purchased");
```
```aql
// A named graph ties vertex and edge collections together for traversal queries
db._createGraph("shopping_graph", [
  { collection: "purchased", from: ["users"], to: ["products"] }
]);
```
Use a plain document collection for data with no relationship-traversal
need (most application entities); use an edge collection specifically
for relationships you intend to traverse via graph queries — an edge
collection's documents are ordinary JSON documents that additionally
carry mandatory `_from`/`_to` fields pointing at other documents' `_id`
values. A named graph is metadata that groups edge/vertex collections
for AQL's graph-traversal syntax — it doesn't change how the underlying
collections store data, only how traversal queries can reference them.

### 2. Write and diagnose AQL graph traversals

```aql
FOR v, e, p IN 1..3 OUTBOUND 'users/42' purchased
  FILTER v.category == 'electronics'
  RETURN { product: v.name, path_length: LENGTH(p.edges) }
```
`1..3 OUTBOUND` bounds the traversal depth (1 to 3 hops) and direction
explicitly — as with Neo4j's Cypher, an unbounded depth
(`1.. OUTBOUND`) on a densely connected graph can expand
combinatorially, so always set an explicit upper bound unless graph
connectivity is known to be sparse. Diagnose a slow traversal with
`EXPLAIN`:
```aql
db._explain(`FOR v, e, p IN 1..3 OUTBOUND 'users/42' purchased
  FILTER v.category == 'electronics' RETURN v`);
```
Look for whether the traversal's starting vertex lookup uses an index
(`primary index` on `_key`/`_id` is automatic; a filter on a non-key
property needs an explicit index, same as any document query) and
whether `FILTER` conditions inside the traversal are pushed down to
prune paths early versus evaluated only after the full traversal
completes — a filter that can't be pushed down forces the traversal to
explore paths it will discard anyway, which is far more expensive on a
high-fan-out graph.

### 3. Manage indexes for both document and graph access patterns

```aql
db.users.ensureIndex({ type: "persistent", fields: ["email"], unique: true });
db.products.ensureIndex({ type: "persistent", fields: ["category", "price"] });
```
Every collection has an automatic primary index on `_key` and (for edge
collections) automatic edge indexes on `_from`/`_to` — these make
direct-key lookups and one-hop traversal starts fast without any
additional configuration. Persistent (skiplist-backed) indexes on other
properties must be created explicitly, matching real query filter
patterns — the same "match the index to the actual dominant filter, not
a guess" discipline as any other engine covered elsewhere in this repo.
For full-text search over document fields, use a dedicated inverted
index (ArangoDB's `arangosearch`/`search-alias` view types) rather than
relying on a persistent index, which doesn't support tokenized text
search.

### 4. Design cluster sharding keys deliberately

```aql
db._create("orders", { numberOfShards: 6, shardKeys: ["customerId"] });
```
`shardKeys` determines which DB-server shard holds a given document —
choosing a shard key with poor cardinality (too few distinct values) or
one that's monotonically increasing for the dominant write pattern
creates the same class of hot-shard problem covered for MongoDB's shard
key selection in
[mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md)
and Cassandra's partition key design in
[cassandra-wide-column-database-operations](../cassandra-wide-column-database-operations/SKILL.md).
For a graph whose vertex and edge collections are sharded independently,
non-matching shard keys between them force cross-shard traversal hops
(a network round-trip per hop instead of a local shard lookup) — the
Enterprise-only **SmartGraphs** feature addresses this by co-locating a
vertex's edges on the same shard using a designated "smart" attribute,
at the cost of requiring that attribute to be chosen deliberately up
front, since it can't be changed without a full data migration.

### 5. Configure and monitor the cluster's three node roles

```bash
# Agency (cluster metadata, Raft consensus) — run 3 or 5 nodes
arangod --server.endpoint tcp://0.0.0.0:8531 --agency.activate true \
  --agency.size 3 --agency.my-address tcp://<AGENCY_NODE_IP>:8531

# DB-server (actual data storage)
arangod --server.endpoint tcp://0.0.0.0:8529 --cluster.my-role DBSERVER \
  --cluster.agency-endpoint tcp://<AGENCY_NODE_IP>:8531

# Coordinator (stateless query routing/aggregation — clients connect here)
arangod --server.endpoint tcp://0.0.0.0:8529 --cluster.my-role COORDINATOR \
  --cluster.agency-endpoint tcp://<AGENCY_NODE_IP>:8531
```
Applications connect to a coordinator (or a load balancer in front of
several coordinators), never directly to a DB-server — coordinators are
stateless and can be scaled independently for query-routing/aggregation
throughput, while DB-servers hold the actual shard data and must be
scaled with the replication factor and sharding strategy in mind.
Monitor shard distribution and replication health via the web UI or:
```bash
curl -u <USER>:<PASSWORD> http://<COORDINATOR_HOST>:8529/_admin/cluster/health
```

## Best practices

- Choose collection types (document vs. edge) based on whether the data
  genuinely needs graph traversal, not by defaulting everything to
  document collections and bolting on ad hoc relationship fields —
  edge collections' automatic `_from`/`_to` indexing is specifically
  what makes traversal queries fast.
- Always bound traversal depth explicitly (`1..n OUTBOUND`) unless graph
  connectivity is provably sparse — the same discipline as bounding
  variable-length patterns in Cypher.
- Design sharding keys around the dominant access pattern and expected
  cardinality up front — like MongoDB and Cassandra key design
  elsewhere in this repo, this is far more disruptive to change after
  data has accumulated across shards than to get right initially.
- Use `EXPLAIN`/query profiling on graph traversals specifically, since
  a traversal that looks reasonable can hide unpushed filters that
  force exploring far more of the graph than the final result needs.
- Run an odd number of agency nodes (3 or 5) for the same Raft-quorum
  reasoning as any consensus-based cluster metadata layer, and scale
  coordinators and DB-servers independently based on which is actually
  the bottleneck (query routing/aggregation vs. data volume/shard
  count).
- Evaluate ArangoDB against running separate purpose-built systems
  honestly — multi-model convenience is a real advantage for genuinely
  mixed workloads, but a workload that's overwhelmingly one access
  pattern (pure graph, or pure document) may still be better served by
  a purpose-built engine for that pattern specifically.

## Common pitfalls

- **Symptom:** A graph traversal query with a `FILTER` clause is much
  slower than expected, exploring far more of the graph than the final
  filtered result would suggest.
  **Fix:** The filter condition isn't being pushed down into the
  traversal itself (common with filters referencing the path variable
  `p` in complex ways, or filters on computed expressions), so the
  traversal explores the full unfiltered breadth before filtering.
  Check `db._explain()` for whether the filter appears as part of the
  traversal node or as a separate downstream filter step, and simplify
  the filter expression (or restructure the query) so it can be
  evaluated during traversal rather than after.

- **Symptom:** One DB-server shard consistently shows much higher load
  than its peers, and the imbalance worsens as data grows.
  **Fix:** The collection's `shardKeys` has poor cardinality or is
  monotonically increasing for the dominant write pattern — the same
  hot-shard failure mode as a poorly chosen MongoDB shard key or
  Cassandra partition key. Redesign the shard key around a
  higher-cardinality, non-monotonic attribute; this requires recreating
  the collection with new shard settings and reloading data, so
  validate the choice against real access patterns before the
  collection accumulates significant data.

- **Symptom:** A graph traversal across vertex and edge collections
  that are sharded independently is slower in cluster mode than the
  same query was in single-server testing.
  **Fix:** Non-matching shard keys between the vertex and edge
  collections force cross-shard network hops for each traversal step.
  Either align shard keys deliberately across the related collections,
  or (Enterprise Edition) use a SmartGraph with a co-location attribute
  chosen up front to keep a vertex's edges on the same shard.

- **Symptom:** The cluster's agency (metadata layer) becomes unavailable
  after a routine restart of what was assumed to be a single expendable
  node.
  **Fix:** The agency was running with only 1 or 2 nodes (below the
  minimum 3-node Raft quorum for real fault tolerance), or two agency
  nodes were restarted concurrently, dropping the surviving set below
  quorum. Always run 3 (or 5) agency nodes and restart them strictly
  one at a time, verifying cluster health returns to fully healthy
  before touching the next node.

- **Symptom:** Someone runs `db._drop("collection_name")` or
  `db._dropDatabase()` directly against production intending to clear
  test/staging data.
  **Fix:** Both are immediate, irreversible operations with no
  confirmation step and no built-in undo.
  > **Warning — destructive action.** Always independently confirm the
  > target collection/database (via `db._name()` and an explicit listing
  > of collections) before any drop operation, take a verified backup
  > first (`arangodump`), and restrict `_drop*` operations via
  > ArangoDB's database-level access control to a narrow admin role
  > rather than general application credentials — see
  > [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md)
  > for restore-testing discipline that should back this up.

## Worked example

**Scenario:** A retail platform wants to add a "customers who bought
this also bought" recommendation feature and a general product catalog,
currently split across a document-only MongoDB deployment for the
catalog and an ad hoc application-side join for "also bought" logic
that's become slow and hard to maintain. The team evaluates ArangoDB as
a single multi-model replacement.

1. Model the catalog as document collections (`products`, `customers`)
   and the purchase relationship as an edge collection:
   ```aql
   db._create("products");
   db._create("customers");
   db._createEdgeCollection("purchased");
   db._createGraph("retail_graph", [
     { collection: "purchased", from: ["customers"], to: ["products"] }
   ]);
   ```
2. Write the "also bought" traversal as a bounded 2-hop AQL query
   (customer → product → other customers who bought it → their other
   products):
   ```aql
   FOR c IN customers FILTER c._key == @customerId
     FOR v, e, p IN 2..2 OUTBOUND c purchased, INBOUND purchased
       FILTER v._id != @excludeProductId
       COLLECT product = v WITH COUNT INTO score
       SORT score DESC LIMIT 10
       RETURN product
   ```
3. Profile with `db._explain()`, confirm the traversal starting point
   uses the automatic primary index on `customers._key`, and add a
   persistent index on `products.category` to support the catalog's
   existing category-browse queries that remain plain document
   lookups.
4. Choose `shardKeys: ["customerId"]` for `customers` and `purchased`
   consistently (aligning them to minimize cross-shard traversal hops),
   validated against expected customer-ID cardinality (millions of
   distinct customers, good distribution) before migration.
5. Migrate catalog data from MongoDB via `arangoimport`, run both
   systems in parallel during a validation window, and cut the
   recommendation feature over to the new AQL traversal once query
   latency and result correctness are confirmed against the old ad hoc
   join logic.

## Cross-references

- [neo4j-graph-database-operations](../neo4j-graph-database-operations/SKILL.md) — a graph-only architecture, useful as a direct contrast when a workload is overwhelmingly graph-traversal-heavy and doesn't need ArangoDB's document/key-value multi-model flexibility.
- [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md) — comparable document-collection sharding-key design trade-offs, relevant when comparing ArangoDB's document model against MongoDB's.
- [cassandra-wide-column-database-operations](../cassandra-wide-column-database-operations/SKILL.md) — comparable partition/shard-key hot-spotting failure mode, useful as a conceptual parallel to ArangoDB's `shardKeys` design.
- [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md) — `arangodump`/`arangorestore` tooling and restore-testing discipline for ArangoDB backups.
