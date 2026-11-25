---
name: knowledge-graphs
version: 1.0.0
min_mindforge_version: 10.5.0
status: stable
triggers: knowledge graph design, ontology architecture, graph database modeling, entity resolution system, knowledge extraction pipeline, graph schema design, triple store, semantic relationship, knowledge base construction, graph traversal pattern, entity linking, knowledge graph embedding
compose:
---

# Knowledge Graphs & Ontology Design

## When this skill activates

This skill activates when building knowledge graphs, designing ontologies, implementing entity resolution systems, extracting structured knowledge from unstructured text, or querying graph databases. It applies to any system that represents complex relationships between entities for reasoning, search, or recommendation.

## Mandatory actions when this skill is active

### Before writing any code

1. **Define ontology structure** — Identify entity types (Person, Organization, Product, Event), relationship types (works_for, located_in, purchased, happened_at), and attributes (name, date, value). Document cardinality: one-to-one, one-to-many, many-to-many. Ontology is the schema for your knowledge graph.
2. **Select graph database** — Choose based on scale (thousands vs. billions of nodes), query patterns (simple lookups vs. multi-hop traversals), and ecosystem: Neo4j (property graph, Cypher), Amazon Neptune (supports RDF and property graphs), RDFox (reasoning and inference), or embedded graphs (NetworkX for prototypes). Benchmark query performance on your schema.
3. **Design entity resolution strategy** — Entities from multiple sources must be deduplicated (same person with different names, same product with different IDs). Define resolution rules: exact name match, fuzzy string matching (Levenshtein distance), embedding similarity, or human-in-the-loop confirmation. Test resolution accuracy on labeled data.
4. **Establish schema versioning** — Ontologies evolve as domain understanding improves. Version the schema with semantic versioning (v1.0, v1.1). Define migration paths for schema changes (add new relationship types, rename attributes). Ensure backward compatibility or provide migration scripts.

### During implementation

- **Extract entities and relationships from text** — Use named entity recognition (NER) for entity extraction and relation extraction models for relationships. Validate that extraction recall is high (>80% of entities are found) and precision is acceptable (>70% of extracted entities are correct). Fine-tune models on domain-specific data.
- **Implement entity linking** — Link extracted entities to canonical entities in the graph. Use fuzzy matching, embedding similarity, or knowledge base APIs (Wikidata, DBpedia). Handle ambiguity: "Apple" could be a fruit, a company, or a person's nickname. Disambiguate using context (surrounding words, known relationships).
- **Design relationship inference rules** — Add implicit relationships via rules: if A works_for B and B is_part_of C, then A works_for C (transitive closure). Use graph query languages (Cypher, SPARQL) or inference engines (RDFox, Pellet). Validate that inferred relationships are logically correct.
- **Normalize entity attributes** — Canonicalize names (lowercase, remove punctuation), dates (ISO 8601), and values (currency conversion). Inconsistent attributes break queries: "Microsoft" vs. "microsoft" vs. "Microsoft Corp." should resolve to the same entity.
- **Implement graph traversal optimizations** — Avoid Cartesian product explosions in multi-hop queries. Use query hints (index usage, join order), limit traversal depth (max 3 hops for most use cases), and cache frequent subgraph patterns. Measure query latency and optimize slow queries.
- **Version entities and relationships** — Track temporal validity: relationships have start and end dates (person worked at company from 2020 to 2023). Implement bitemporal modeling if you need to track both valid time (when the fact was true in the real world) and transaction time (when the fact was recorded in the database).

### After implementation

- **Validate graph completeness** — Measure coverage: % of entities from source data that are present in the graph, % of relationships that are captured. Incomplete graphs produce incorrect query results. Identify missing entities and relationships, then backfill.
- **Test query correctness** — Create a test suite of queries with known ground-truth answers. Validate that queries return expected results. Common failure modes: missing relationships, incorrect cardinality, transitive closure errors.
- **Measure query performance** — Benchmark query latency under realistic load. Target: simple lookups <10ms, multi-hop traversals <100ms. If slower, optimize indexes, limit traversal depth, or denormalize hot paths (precompute frequent traversals).
- **Audit for duplicate entities** — Run entity resolution on the entire graph post-construction. Identify entities that should be merged (similar names, same attributes). Merge duplicates and redirect relationships to canonical entities.

## Self-check before task completion

- [ ] Ontology defines entity types, relationship types, attributes, and cardinality constraints
- [ ] Graph database is selected and benchmarked on schema-specific query patterns
- [ ] Entity resolution strategy is defined and tested on labeled data (precision/recall metrics)
- [ ] Schema versioning is implemented with migration paths for schema changes
- [ ] Entity extraction achieves >80% recall and >70% precision on domain data
- [ ] Entity linking disambiguates entities using context and canonical knowledge bases
- [ ] Relationship inference rules are implemented and validated for logical correctness
- [ ] Entity attributes are normalized (names, dates, values) for consistent queries
- [ ] Graph traversal queries are optimized with indexes, depth limits, and subgraph caching
- [ ] Temporal validity is tracked with start/end dates for time-sensitive relationships
- [ ] Graph completeness is measured (% entities and relationships captured from source data)
- [ ] Query correctness is validated with ground-truth test suite
- [ ] Query latency is benchmarked (simple lookups <10ms, multi-hop <100ms)
- [ ] Duplicate entities are audited and merged with canonical entity resolution
