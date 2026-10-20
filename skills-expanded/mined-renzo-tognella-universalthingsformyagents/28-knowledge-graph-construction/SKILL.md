---
name: Knowledge Graph Construction
description: Use when building, maintaining, or querying the knowledge graph in TheSearch — entity extraction, community detection, incremental updates, Cypher patterns, and graph quality assurance.
---

# Knowledge Graph Construction & Maintenance

## Overview

TheSearch uses Neo4j as its structural memory layer. Memories become nodes (`MemoryItem`, `PRMemory`, `ProceduralMemory`) connected by typed relationships (`IMPLEMENTS`, `EVIDENCES`, `DEPRECATES`). This skill covers how to build and maintain this graph effectively, drawing from GraphRAG, HippoRAG, KG-Agent, and LLM Graph Transformer research.

**Core principle:** The graph must stay accurate through incremental merges, not full rebuilds.

## When to Use

- Adding new entity/relation types to the graph model
- Implementing entity extraction (NER) or relation extraction
- Setting up community detection for hierarchical summarization
- Writing Cypher for graph maintenance (merge, refine, deprecate)
- Validating graph construction quality
- Deciding between incremental update vs full rebuild

## Current Graph Model

```
(Project)-[:HAS_CATEGORY]->(Category)
(Category)-[:HAS_MEMORY]->(MemoryItem)
(Domain)-[:CONTAINS]->(MemoryItem)
(PRMemory)-[:IMPLEMENTS|EVIDENCES|MODIFIES]->(MemoryItem)
(MemoryItem)-[:DEPRECATES]->(MemoryItem)
(MemoryItem)-[:RELATED_TO]->(MemoryItem)
```

**Node properties:** `memory_id`, `title`, `summary`, `details`, `category`, `project`, `effective_weight`, `status`, timestamps.

**Vector dual:** Each `MemoryItem` also has a vector embedding in Qdrant, synced by `memory_id`.

## 1. Entity Extraction Patterns

### LLM-based NER + Relation Extraction

```python
from pydantic import BaseModel, Field

class ExtractedEntity(BaseModel):
    name: str = Field(description="Canonical entity name")
    entity_type: str = Field(description="Person, Technology, Concept, Organization, etc.")
    properties: dict = Field(default_factory=dict)

class ExtractedRelation(BaseModel):
    source: str
    relation_type: str
    target: str
    properties: dict = Field(default_factory=dict)

class GraphExtraction(BaseModel):
    entities: list[ExtractedEntity] = Field(default_factory=list)
    relations: list[ExtractedRelation] = Field(default_factory=list)

EXTRACTION_PROMPT = """Extract entities and relations from the text.
Entity types: Technology, Concept, Person, Organization, Pattern, Domain
Relation types: USES, DEPENDS_ON, IMPLEMENTS, RELATES_TO, PART_OF, SUPERSEDES

Rules:
1. Use canonical names (e.g., "Neo4j" not "neo4j" or "neo4j database")
2. Each relation must connect two extracted entities
3. Prefer specific over generic relations
4. Extract only explicitly stated relations, do not infer
"""

async def extract_graph(content: str) -> GraphExtraction:
    return await structured_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=GraphExtraction,
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": content},
        ],
    )
```

### Integration with Existing ExtractionService

```python
async def extract_candidates_with_graph(
    content: str, project: str
) -> tuple[list[MemoryCandidate], GraphExtraction]:
    candidates = await extraction.extract_candidates(content, project)
    graph = await extract_graph(content)
    return candidates, graph
```

## 2. Community Detection (GraphRAG Pattern)

Microsoft GraphRAG uses Leiden algorithm for community detection, then summarizes each community. In TheSearch:

```python
async def detect_communities(project: str) -> list[dict]:
    query = """
    CALL gds.leiden.stream('memory-graph', {
        nodeLabels: ['MemoryItem'],
        relationshipTypes: ['RELATED_TO', 'IMPLEMENTS'],
        relationshipWeightProperty: 'effective_weight'
    })
    YIELD nodeId, communityId
    WITH gds.util.asNode(nodeId) AS node, communityId
    WHERE node.project = $project
    RETURN communityId,
           collect(node.title) AS memories,
           count(*) AS size
    ORDER BY size DESC
    """
    return await neo4j.run_query(query, project=project)

async def summarize_communities(communities: list[dict]) -> list[dict]:
    summaries = []
    for community in communities:
        if community["size"] < 2:
            continue
        summary = await llm.summarize(
            f"Summarize this group of related memories:\n"
            + "\n".join(f"- {m}" for m in community["memories"])
        )
        summaries.append({
            "community_id": community["communityId"],
            "summary": summary,
            "size": community["size"],
        })
    return summaries
```

**When to run:** Background consolidation job, not in the hot path. See skill `13_consolidation_background`.

## 3. Graph Maintenance: Merge, Refine, Deprecate

### Merge Duplicates

```cypher
// Find potential duplicates by title similarity
MATCH (m1:MemoryItem {project: $project, status: 'active'})
MATCH (m2:MemoryItem {project: $project, status: 'active'})
WHERE m1.memory_id < m2.memory_id
  AND apoc.text.jaroWinklerDistance(m1.title, m2.title) < 0.15
RETURN m1, m2
```

```cypher
// Merge m2 into m1 (keep m1, transfer relations)
MATCH (m1:MemoryItem {memory_id: $keep_id})
MATCH (m2:MemoryItem {memory_id: $merge_id})
// Transfer incoming relations
MATCH (src)-[r]->(m2)
WHERE type(r) <> 'DEPRECATES'
MERGE (src)-[r2:IMPLEMENTS]->(m1)
  ON CREATE SET r2 = properties(r)
// Transfer outgoing relations
MATCH (m2)-[r]->(tgt)
WHERE type(r) <> 'DEPRECATES'
MERGE (m1)-[r2:RELATED_TO]->(tgt)
  ON CREATE SET r2 = properties(r)
// Deprecate merged node
SET m2.status = 'deprecated'
MERGE (m1)-[:DEPRECATES]->(m2)
  ON CREATE SET m1.merged_from = m2.memory_id
DETACH DELETE (SELECT FROM m2 WHERE false)
```

### Incremental Update

```cypher
// Idempotent upsert — core pattern for TheSearch
MERGE (m:MemoryItem {memory_id: $memory_id})
SET m.title = $title,
    m.summary = $summary,
    m.category = $category,
    m.effective_weight = $weight,
    m.updated_at = datetime(),
    m.status = 'active'
WITH m
UNWIND $domains AS domain_name
MATCH (d:Domain {slug: domain_name})
MERGE (d)-[:CONTAINS]->(m)
```

### Deprecate with Replacement Chain

```cypher
MATCH (old:MemoryItem {memory_id: $old_id})
MATCH (new:MemoryItem {memory_id: $new_id})
SET old.status = 'deprecated',
    old.deprecated_at = datetime()
MERGE (new)-[:DEPRECATES]->(old)
  ON CREATE SET new.replaces = $old_id
```

## 4. Quality Assurance for Graph Construction

### Validation Rules

```python
class GraphValidator:
    RULES = {
        "no_orphan_memories": """
            MATCH (m:MemoryItem {status: 'active'})
            WHERE NOT (m)<--(:Category) AND NOT (m)<--(:Domain)
            RETURN m.memory_id, m.title
        """,
        "no_self_relations": """
            MATCH (m:MemoryItem)-[r]->(m)
            RETURN m.memory_id, type(r)
        """,
        "weight_range": """
            MATCH (m:MemoryItem)
            WHERE m.effective_weight < 0 OR m.effective_weight > 1
            RETURN m.memory_id, m.effective_weight
        """,
        "deprecated_still_linked": """
            MATCH (m:MemoryItem {status: 'deprecated'})-[r]->(active:MemoryItem {status: 'active'})
            WHERE type(r) <> 'DEPRECATES'
            RETURN m.memory_id, type(r), active.memory_id
        """,
    }

    async def validate(self) -> dict[str, list[dict]]:
        results = {}
        for rule_name, cypher in self.RULES.items():
            violations = await self.neo4j.run_query(cypher)
            results[rule_name] = violations
        return results
```

### Entity Canonicalization

```python
ENTITY_ALIASES = {
    "neo4j": "Neo4j",
    "qdrant": "Qdrant",
    "python": "Python",
    "mcp": "MCP",
    "react": "ReAct",
    "langchain": "LangChain",
}

def canonicalize(name: str) -> str:
    return ENTITY_ALIASES.get(name.lower().strip(), name.strip())
```

## 5. Incremental vs Full Rebuild

| Scenario | Approach | Rationale |
|----------|----------|-----------|
| New PR memory | Incremental MERGE | Single node, idempotent |
| Bulk category restructure | Batch with transaction | Many nodes, need consistency |
| Entity extraction upgrade | Full rebuild of entity nodes | Schema change |
| Community recalculation | Incremental Leiden | Only affected subgraph |
| Duplicate consolidation | Incremental merge | Targeted by similarity query |

**Rule:** Prefer incremental MERGE. Full rebuild only when schema changes.

## 6. Cypher Quick Reference

```cypher
-- Get full context for a memory (neighbors + relations)
MATCH (m:MemoryItem {memory_id: $id})-[r]-(n)
RETURN m, type(r) AS relation, labels(n)[0] AS neighbor_type, n

-- Find knowledge paths between two concepts
MATCH path = shortestPath(
  (a:MemoryItem {category: $cat_a})-[*..5]-(b:MemoryItem {category: $cat_b})
)
RETURN path

-- Temporal query: what was known at a point in time
MATCH (m:MemoryItem)
WHERE m.created_at <= datetime($point_in_time)
  AND (m.status = 'active' OR m.deprecated_at > datetime($point_in_time))
RETURN m ORDER BY m.created_at DESC

-- Weight-weighted neighbor expansion (for retrieval)
MATCH (center:MemoryItem {memory_id: $id})-[r]-(neighbor:MemoryItem {status: 'active'})
RETURN neighbor.memory_id, neighbor.title, neighbor.effective_weight,
       neighbor.summary, type(r) AS relation
ORDER BY neighbor.effective_weight DESC
LIMIT $limit
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using CREATE instead of MERGE | Always MERGE for idempotent upserts |
| Extracting entities without canonicalization | Normalize names before creating nodes |
| Running community detection on every write | Schedule as background job |
| Forgetting to sync Neo4j + Qdrant on merge | After merge, delete merged vector from Qdrant |
| Querying deprecated nodes | Always filter `status = 'active'` |
| Ignoring graph depth in traversal | Limit `[*..N]` to prevent runaway queries |

## References

- Microsoft GraphRAG: hierarchical summarization via community detection
- Neo4j GraphRAG Python: official KG construction tools
- HippoRAG: hippocampal indexing for KG construction (NeurIPS 2024)
- KG-Agent: autonomous agent for KG interaction
- Graph Chain-of-Thought: reasoning over graph structures (ACL 2024)
- Path-Constrained Retrieval: structural + semantic constraints
- MediGRAF: Text2Cypher + vectors for hybrid graph RAG
- Source: `knogdement/01_graphs_llm_memory.md`, `knogdement/10_thesearch_related.md`
