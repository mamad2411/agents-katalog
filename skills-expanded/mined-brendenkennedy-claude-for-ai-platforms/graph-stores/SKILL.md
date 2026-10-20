---
name: graph-stores
description: >
  Graph databases and knowledge graphs — Neo4j/Cypher, Apache AGE inside Postgres, and property-graph
  vs RDF. Carries: **when a graph actually earns itself over a relational join** (variable-depth
  traversal, path-finding, relationship-first queries) and when it doesn't, modelling nodes vs
  properties vs relationships, Cypher patterns, index-free adjacency and what it does and doesn't
  buy, supernode blowups, GraphRAG and its real ingestion cost, and traversal scoping as the tenancy
  control. Load when modelling connected data, deciding whether a graph store is warranted, writing
  a traversal, or building a knowledge graph for retrieval. Triggers: graph database, Neo4j, Cypher,
  Apache AGE, Gremlin, RDF, SPARQL, knowledge graph, GraphRAG, entity resolution, relationship,
  traversal, shortest path, multi-hop, recursive CTE, supernode, ontology, triple store. Relational
  modelling is `relational-stores`; vector retrieval is `vector-stores`; RAG scoring is
  `agent-evaluation`.
---

# graph-stores — connected data, and the honest test of whether you need one

**Pinned:** neo4j, apache-age — unpinned · authored 2026-07 · run `/skill-update graph-stores` once a
store is chosen. Cypher is largely portable between Neo4j and AGE; the operational surface is not.

> On-demand: load this when the data is relationship-heavy or someone proposes a knowledge graph.
> Tabular modelling is `relational-stores`; embedding-based retrieval is `vector-stores`; whether a
> GraphRAG system actually answers better is `agent-evaluation`. Corpus governance applies to a
> knowledge graph exactly as to any other retrieval store (`data-governance.md` `D7`, `D8`).

## When this applies

Modelling connected data. Deciding whether to add a graph store. Writing a traversal. Building a
knowledge graph for retrieval.

## First: does a graph earn itself?

A graph database is a system to operate, back up, secure, staff, and pay for. Most "we need a graph"
instincts are a well-indexed join table in disguise. The honest test:

**A graph earns itself when your queries are about paths of unknown length.**

| Query shape | Where it belongs |
|---|---|
| "Who reports to Alice?" | Relational. One join |
| "Everyone in Alice's reporting chain, any depth" | **Graph** — variable-depth traversal |
| "Shortest path between these two entities" | **Graph** |
| "All entities within 3 hops, filtered by relationship type" | **Graph** |
| "Users who bought X also bought…" | Relational, or a recommender. Not a graph problem |
| "Everything connected to this incident" | **Graph**, if the connections are heterogeneous |

Two honest middle options before committing:

- **Postgres recursive CTEs** (`WITH RECURSIVE`) do fixed and variable-depth traversal. They are
  clunky and get slow at depth, but they work, and they need no new system. Try this first.
- **Apache AGE** puts openCypher *inside* Postgres. You get graph queries alongside your relational
  data, in one backup, one restore drill (`D10`), one network posture (`P11`), one credential set.
  For most projects that reach for a graph, **this is the right answer** — and it composes with
  `pgvector` in the same database for hybrid graph+vector retrieval.

Reach for **Neo4j** when traversal is the dominant workload, at depth, at scale, and the operational
cost is justified by that.

## Property graph vs RDF

| | Property graph (Neo4j, AGE) | RDF triple store |
|---|---|---|
| Model | Nodes + relationships, both with properties | Subject–predicate–object triples |
| Query | Cypher / Gremlin | SPARQL |
| Strength | Ergonomic, fast traversal, natural for application data | Formal semantics, ontologies, reasoning, federation |
| Pick when | You are building an application | You need interoperability, standards, or inference |

Most AI-platform work wants a property graph. RDF earns itself when you must exchange the graph with
someone else's, or when formal ontology and inference are the point rather than an aspiration.

## Modelling

The recurring question is **node, property, or relationship?**

- **Node** if it has its own identity, its own relationships, or you'll query *for* it.
- **Property** if it only ever describes its parent and you'd never traverse to it.
- **Relationship** for the verb — and put properties on it (`since`, `weight`, `confidence`), which
  is exactly what a relational join table makes awkward.

Relationship *types* are the graph's schema; keep them few and meaningful. A graph with 200
relationship types is usually a modelling failure.

```cypher
// Variable-depth traversal — the thing SQL makes painful
MATCH path = (start:Service {name: $name})-[:DEPENDS_ON*1..5]->(dep:Service)
WHERE dep.tier = 'critical'
RETURN dep.name, length(path) AS hops
ORDER BY hops;

// Shortest path
MATCH (a:Entity {id: $from}), (b:Entity {id: $to}),
      p = shortestPath((a)-[:RELATED*..8]-(b))
RETURN p;
```

**Always bound the depth** (`*1..5`, never `*`). An unbounded traversal on a connected graph will
attempt to walk the entire dataset.

## Tenancy and scoping

Canon `D8` applies here too, and graphs make it easier to get wrong: **a traversal that starts inside
one tenant can walk out of it** through a shared node.

- Root every traversal in a node the caller is authorized for, and **filter relationship traversal by
  tenant on every hop** — not just on the start node.
- Prefer separate databases or graph namespaces per tenant where the store supports it. Physical
  separation beats a predicate you must remember on each hop.
- Watch for shared entities (a common vendor, a public document) that legitimately connect tenants —
  those are the bridges an unbounded traversal crosses. Decide deliberately whether they are
  traversable, and record it.

## GraphRAG — real, and more expensive than it looks

Building a knowledge graph from documents (entity extraction → relationship extraction → resolution
→ graph) genuinely helps a class of question that vector search handles badly: *multi-hop* and
*global* questions — "how does A relate to C?", "what themes run across this corpus?" — where the
answer exists in no single chunk.

The costs to state before committing:

- **Ingestion is LLM-heavy and slow.** Extraction over a large corpus is a real bill, and it recurs
  whenever the extraction prompt or model changes (`model-governance.md` `M15`).
- **Entity resolution is the hard part.** "Acme Corp", "Acme", "ACME Inc." must merge, or the graph
  fragments and answers get worse than plain retrieval.
- **Extraction errors compound.** A wrong relationship is asserted with the same confidence as a
  right one, and it is now a fact the system reasons from.
- **The graph is a retrieval corpus** — `D7` in full: per-document provenance on every extracted
  edge, so a wrong fact can be traced and removed, and so `D10` deletion reaches it.

**Measure it against a plain vector baseline before adopting it** (`agent-evaluation`). GraphRAG is
frequently proposed and rarely A/B'd; on single-fact lookup it often loses.

Hybrid is usually the strongest shape: vector search for "which documents", graph traversal for "what
connects them" — which is another argument for AGE + pgvector in one Postgres.

## Gotchas

- **Supernodes.** A node with millions of relationships (a "USA" country node, a popular tag) makes
  every traversal through it catastrophic. Detect them, and model around them — bucket, or treat the
  attribute as a property rather than an edge.
- **Unbounded traversal.** `*` with no upper bound. Always bound it.
- **Index-free adjacency is not magic.** It makes *hopping between adjacent nodes* fast. Finding the
  starting node still needs an index — create one on every property you match on, or the fast
  traversal follows a full scan.
- **Modelling everything as a graph.** Attributes that are never traversed belong as properties or
  in a relational table.
- **No schema discipline.** Property graphs let you write anything, which means a year later nobody
  knows what shapes exist. Use constraints, and document the relationship types.
- **A graph nobody validated.** An extracted knowledge graph with no accuracy measurement is a
  confident-looking artifact of unknown quality feeding your answers.
