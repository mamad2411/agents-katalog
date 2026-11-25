---
name: neo4j-graph-database-operations
description: >
  Covers operating Neo4j: Cypher query fundamentals for operational
  diagnosis, causal clustering for HA and read scaling, and index/
  constraint management (property indexes, full-text indexes, uniqueness
  constraints). Use when the user asks to "write a Cypher query for
  this graph traversal," "set up a Neo4j causal cluster," "why is this
  Cypher query slow," "add an index/constraint in Neo4j," or "size a
  Neo4j cluster for read scaling."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Neo4j Graph Database Operations

## Purpose

Neo4j stores data as a **property graph** — nodes and relationships,
both of which can carry properties — and is purpose-built for queries
that traverse relationships (multi-hop "who is connected to whom, and
how" questions) that are expensive or awkward to express as repeated
joins in a relational engine. Its operational model is unusual because
relationship traversal cost in Neo4j is proportional to the number of
relationships actually traversed, not the total graph size — a query
that stays well-indexed at the entry point and traverses a bounded
number of hops stays fast regardless of overall graph size, while one
missing an index or traversing unbounded depth degrades sharply. This
skill covers Cypher fundamentals needed for operational diagnosis,
**causal clustering** (Neo4j's replication/HA mechanism), and index/
constraint management — the operational core that keeps a Neo4j
deployment fast and available as the graph grows. For a distinct
multi-model engine that combines graph with document and key-value
data in one database rather than a graph-only architecture, see
[arangodb-multi-model-database-operations](../arangodb-multi-model-database-operations/SKILL.md).

## When to use

- Writing or debugging a Cypher query for an operational diagnostic
  task (finding orphaned nodes, checking relationship cardinality,
  auditing constraint violations) rather than application feature work.
- A Cypher query that traverses relationships is slow, and the cause
  needs diagnosing (missing index at the traversal's starting point,
  unbounded-depth traversal, a Cartesian product from an unintended
  disconnected pattern).
- Setting up or troubleshooting a causal cluster for high availability
  and read scaling, including diagnosing why a follower isn't catching
  up or why the cluster can't elect a leader.
- Adding, auditing, or troubleshooting property indexes, full-text
  indexes, or uniqueness/existence constraints.
- Planning capacity for a growing graph — deciding whether to scale
  reads via cluster followers or address a data-modeling issue instead.

## Prerequisites & environment

- Neo4j 5.x Enterprise Edition assumed for causal clustering (causal
  clustering itself, along with role-based access control and some
  index types, is an Enterprise-only capability — Community Edition is
  single-instance, no built-in clustering). Cypher syntax below targets
  Neo4j 5.x; note that some clauses and index syntax (e.g.
  `CREATE INDEX ... FOR (n:Label) ON (n.prop)` vs. the newer
  `CREATE INDEX ... FOR (n:Label) ON (n.prop)` unified syntax) changed
  between the 3.x/4.x and 5.x lines — verify syntax against the target
  version before assuming portability.
- For a causal cluster: a minimum of 3 **core** servers (participate in
  the Raft-based consensus that elects a leader and replicates writes)
  for basic fault tolerance, plus any number of **read replica** servers
  (asynchronously replicated, do not participate in the write-consensus
  quorum) for horizontal read scaling.
- `dbms.security` role-based access configured for any multi-user
  deployment — Neo4j Enterprise supports fine-grained, role-based
  privilege grants per label/relationship-type/property.
- Familiarity with the graph's actual traversal patterns (which node
  labels are traversal entry points, typical hop depth) before creating
  indexes — like Cassandra's partition-key design, indexing the wrong
  property or label leaves the most common queries unindexed while
  indexing something rarely queried.

## Step-by-step guidance

### 1. Use Cypher for operational diagnostics, not just application queries

```cypher
// Find nodes with no relationships at all (often orphaned/incomplete data)
MATCH (n:Customer)
WHERE NOT (n)--()
RETURN n.customerId LIMIT 100;
```
```cypher
// Check relationship cardinality distribution for a label — spot a
// "super-node" with disproportionately many relationships
MATCH (n:Customer)-[r:PLACED]->(:Order)
WITH n, count(r) AS orderCount
RETURN avg(orderCount), max(orderCount), percentileCont(orderCount, 0.99);
```
A **super-node** (a single node with an extremely high relationship
count — e.g. a "country" node connected to millions of customer nodes)
is Neo4j's rough equivalent of a Cassandra hot partition or a MongoDB
low-cardinality shard key: any traversal through that node becomes
expensive regardless of indexing, since the traversal must still
enumerate a huge relationship set. Identify and redesign around
super-nodes (e.g. an intermediate grouping node, or reconsidering
whether that relationship should exist at that granularity) rather than
only adding more indexes, since indexing helps find the node, not
traverse through it cheaply.

### 2. Diagnose a slow Cypher query with EXPLAIN/PROFILE

```cypher
PROFILE
MATCH (c:Customer {email: 'user@example.com'})-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
WHERE p.category = 'electronics'
RETURN o.orderId, p.name;
```
`PROFILE` (runs the query and reports actual row counts per operator) is
the Cypher equivalent of PostgreSQL's `EXPLAIN ANALYZE` — use it, not
`EXPLAIN` alone (which only estimates), to find the real bottleneck.
Look for a `NodeByLabelScan` (full label scan, analogous to a `Seq
Scan`) where an index-backed `NodeIndexSeek` is expected — this
typically means the starting property (`email` here) has no index:
```cypher
CREATE INDEX customer_email_idx FOR (c:Customer) ON (c.email);
```
Also watch for an unintended **Cartesian product**: a `MATCH` clause
with two disconnected patterns (no relationship linking them) computes
every combination of both patterns' matches, which can silently
explode result size and cost even though the query "looks" like a
normal traversal — Neo4j's planner will flag this in the query plan
(`CartesianProduct` operator) and, in recent versions, warns about it
explicitly; treat that warning as a real problem to fix, not noise to
suppress.

### 3. Manage relationship direction and bounded-depth traversals deliberately

```cypher
// Bounded-depth traversal — safe, cost scales with actual hop count and fan-out
MATCH (start:Person {id: $id})-[:KNOWS*1..3]-(friend:Person)
RETURN DISTINCT friend;
```
An **unbounded** variable-length traversal (`[:KNOWS*]` with no upper
bound) on a densely connected graph can expand combinatorially — always
set an explicit upper bound unless the graph's connectivity is known to
be sparse enough that unbounded traversal is genuinely safe. Direction
matters for both correctness and performance: `-[:KNOWS]->` (a directed
pattern) can use an index/degree lookup scoped to that direction, while
`-[:KNOWS]-` (undirected, matching either direction) must consider
relationships in both directions — use directed patterns whenever the
underlying relationship is genuinely modeled as directional.

### 4. Set up and monitor a causal cluster

```conf
# neo4j.conf — core server
dbms.mode=CORE
dbms.cluster.discovery.type=LIST
dbms.cluster.discovery.endpoints=core1:5000,core2:5000,core3:5000
dbms.cluster.raft.advertised_address=core1:7000
```
```conf
# neo4j.conf — read replica
dbms.mode=READ_REPLICA
dbms.cluster.discovery.endpoints=core1:5000,core2:5000,core3:5000
```
Core servers use Raft consensus to elect a leader and replicate writes
synchronously enough to guarantee committed writes survive a minority
of core-server failures; read replicas asynchronously catch up from the
cluster and serve read traffic, scaling read throughput horizontally
without adding write-quorum overhead. Verify cluster health and role
assignment:
```cypher
CALL dbms.cluster.overview() YIELD id, addresses, role;
```
A core server showing `role: FOLLOWER` indefinitely with no `LEADER`
present anywhere in the overview indicates the cluster cannot currently
elect a leader — check for a genuine network partition or an
even-numbered core-server count that's landed in a scenario where no
partition holds a strict majority (same quorum-math reasoning as an
odd-node requirement in Galera or Cassandra token-ring topology
elsewhere in this repo).

### 5. Manage indexes and constraints deliberately, matching real query patterns

```cypher
-- Property index for fast lookup by a commonly-filtered property
CREATE INDEX order_status_idx FOR (o:Order) ON (o.status);

-- Composite index for a query commonly filtering on both properties together
CREATE INDEX order_customer_status_idx FOR (o:Order) ON (o.customerId, o.status);

-- Uniqueness constraint (also implicitly creates a backing index)
CREATE CONSTRAINT customer_id_unique FOR (c:Customer) REQUIRE c.customerId IS UNIQUE;

-- Full-text index for free-text search over a property
CREATE FULLTEXT INDEX product_search_idx FOR (p:Product) ON EACH [p.name, p.description];
```
A uniqueness constraint both enforces the invariant at write time
(rejecting a duplicate) and creates a backing index automatically — for
any property that must genuinely be unique, prefer the constraint over
a plain index plus application-level uniqueness checking, since the
latter is racy under concurrent writes while the constraint is enforced
by the database itself. Building an index on a large existing label
population is a background operation but still consumes real I/O and
can take time proportional to node count — schedule for a low-traffic
window on a large graph rather than assuming it's instantaneous.

## Best practices

- Identify and design around super-nodes explicitly (a bounded fan-out
  intermediate node, or reconsidering relationship granularity) rather
  than only adding indexes, since no index makes traversing through an
  already-found super-node cheap.
- Always set an explicit upper bound on variable-length relationship
  patterns (`[:REL*1..n]`) unless the graph's connectivity is provably
  sparse enough for unbounded traversal to be safe.
- Use `PROFILE`, not `EXPLAIN` alone, to diagnose real query cost —
  `EXPLAIN` only estimates, and Neo4j's planner estimates can be
  materially wrong on a skewed graph (e.g. around a super-node).
- Prefer uniqueness/existence constraints over application-level
  invariant checks for any property that must genuinely be unique or
  required — constraints are enforced atomically by the database, not
  racy under concurrent writes.
- Run causal clusters with an odd number of core servers (3 or 5) for
  the same quorum-math reason as any Raft/Paxos-based consensus system,
  and scale reads via read replicas rather than adding more core servers
  than write-availability actually requires.
- Watch for and eliminate `CartesianProduct` operators in query plans —
  a query "looks" like a normal multi-pattern traversal but silently
  computes a full cross-product if the patterns aren't actually
  connected by a relationship.

## Common pitfalls

- **Symptom:** A Cypher query traversing from a specific node type is
  fast for most starting nodes but catastrophically slow for a small
  subset.
  **Fix:** Those specific starting nodes are super-nodes with an
  extremely high relationship count (check with
  `MATCH (n:Label) RETURN n, size((n)--()) AS degree ORDER BY degree
  DESC LIMIT 10`). Redesign the data model around the super-node
  (an intermediate grouping node, or reconsidering whether that
  relationship should exist at that granularity) rather than only
  adding more indexes at the traversal's entry point.

- **Symptom:** A query with two seemingly independent `MATCH` clauses
  returns a much larger and slower-to-compute result set than expected.
  **Fix:** The two patterns aren't connected by any relationship,
  producing an unintended Cartesian product (every combination of both
  patterns' matches). Check the query plan for a `CartesianProduct`
  operator, and either connect the patterns via a shared variable/
  relationship or restructure into separate queries if a genuine
  cross-product wasn't intended.

- **Symptom:** A causal cluster's `dbms.cluster.overview()` shows every
  core server as `FOLLOWER`, with no `LEADER` anywhere, and writes fail.
  **Fix:** The cluster cannot achieve Raft quorum — check for an
  even-numbered core-server count (a genuine network partition can then
  leave no side with a strict majority) or an actual network partition
  between core servers. Always run an odd number of core servers (3 or
  5), and investigate connectivity between them (the
  `dbms.cluster.discovery.endpoints` list and actual network reachability)
  before assuming a software bug.

- **Symptom:** A read replica falls further and further behind the
  cluster's write throughput and never catches up.
  **Fix:** Read replicas replicate asynchronously and can genuinely
  fall behind under sustained high write volume, particularly if
  under-provisioned relative to the core servers. Check replica lag via
  monitoring (transaction ID comparison between replica and leader),
  scale the read replica's resources, or add more read replicas to
  spread read load rather than routing all reads to a single
  overloaded replica.

- **Symptom:** Someone runs `MATCH (n) DETACH DELETE n` (deleting all
  nodes and their relationships) directly against a production database
  intending to clear test data from a specific label only.
  **Fix:** An unscoped `MATCH (n)` matches every node in the entire
  graph, not just the intended label — `DETACH DELETE` then removes all
  of it along with every relationship, irreversibly.
  > **Warning — destructive action.** Always scope a deletion query to
  > the specific label/property intended
  > (`MATCH (n:TestData) DETACH DELETE n`), run the equivalent
  > read-only `MATCH ... RETURN count(n)` first to confirm scope
  > matches intent, and restrict broad delete privileges via Neo4j's
  > role-based access control to a narrow admin role rather than
  > general application credentials.

## Worked example

**Scenario:** A social-recommendation feature's Cypher query — "find
friends-of-friends who follow a shared list of interests" — has become
slow for a small number of accounts, while working fine for the vast
majority of users.

1. Profile the query for a slow account:
   ```cypher
   PROFILE
   MATCH (u:User {id: $id})-[:FOLLOWS]->(:Interest)<-[:FOLLOWS]-(other:User)
   MATCH (u)-[:FRIENDS_WITH*1..2]-(fof:User)
   WHERE fof = other
   RETURN DISTINCT other.id;
   ```
   The plan shows an enormous number of rows processed at the
   `Expand(All)` step for the `:FOLLOWS` relationship from a specific
   `:Interest` node.
2. Check that interest node's degree:
   ```cypher
   MATCH (i:Interest {name: 'photography'})<-[:FOLLOWS]-()
   RETURN count(*);
   -- 2,400,000
   ```
   Confirmed: "photography" is a super-node followed by millions of
   users, and any traversal through it is expensive regardless of
   indexing.
3. Redesign the query to bound the interest-matching side separately
   and intersect result sets in a more selective order, and add a
   composite index supporting the friends-of-friends lookup:
   ```cypher
   CREATE INDEX user_friends_lookup_idx FOR (u:User) ON (u.id);
   ```
   restructuring the query to first compute the (much smaller)
   friends-of-friends set, then filter by shared interest membership,
   rather than starting from the high-degree interest node.
4. Re-profile: the rewritten query's cost now scales with the user's
   actual friend-of-friend count (typically hundreds, not millions),
   and the slow-account latency drops from several seconds to tens of
   milliseconds.
5. Add a standing check for high-degree nodes across all `:Interest`
   and similar "hub" labels as part of routine graph health review, so
   the next emerging super-node is caught before it causes a
   user-visible regression.

## Cross-references

- [arangodb-multi-model-database-operations](../arangodb-multi-model-database-operations/SKILL.md) — a distinct multi-model engine (graph plus document plus key-value in one database) rather than Neo4j's graph-only architecture — relevant when a workload needs both graph traversal and general document storage without running two separate databases.
- [postgresql-high-availability-and-failover](../postgresql-high-availability-and-failover/SKILL.md) — comparable quorum-based leader-election and failover concerns (Raft in Neo4j's causal cluster vs. Patroni/etcd-based failover in PostgreSQL), useful as a conceptual parallel.
- [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md) — backup/restore-testing discipline that should back up any destructive Cypher operation (`DETACH DELETE`, a dropped constraint) against a production graph.
