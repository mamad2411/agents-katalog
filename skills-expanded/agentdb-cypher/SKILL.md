---
name: agentdb-cypher
description: Execute Cypher queries against AgentDB's graph backend. Use when the user wants to write a custom traversal that the standard tools don't cover, or when explaining graph state.
---

# Cypher Query

Run arbitrary Cypher against the AgentDB graph backend. The native binding accepts standard openCypher; AgentDB also adds a few extensions (`uplift`, `confidence` properties on edges).

## When to use

- Need a query the standard `agentdb_causal_*` tools don't cover
- Multi-hop traversal with custom filtering
- Aggregation queries — count nodes by type, find hub nodes, etc.
- Migration / inspection during debugging

## API

```
agentdb_causal_query(
  cypher: <query string>,
  params?: { ... }
)

Returns: { rows, stats: { execMs, rowsMatched, rowsReturned } }
```

## Example queries

```cypher
-- Top 10 most-cited skills
MATCH (s:Skill)<-[r:references]-(:Episode)
RETURN s.name, count(r) AS cites
ORDER BY cites DESC LIMIT 10

-- Find hub nodes (high in-degree)
MATCH (n)<-[r]-()
RETURN n.id, n.type, count(r) AS inDegree
ORDER BY inDegree DESC LIMIT 20

-- Walk supersedes chain backwards from current ADR
MATCH p=(current:ADR {id: 'ADR-046'})-[:supersedes*]->(ancestor:ADR)
RETURN [n IN nodes(p) | n.title]

-- Cycle detection (worth a warning)
MATCH p=(n)-[:caused*1..5]->(n)
RETURN p LIMIT 5
```

## Safety

The `agentdb_causal_query` tool accepts arbitrary Cypher, including writes (`CREATE`, `DELETE`, `DETACH DELETE`). For destructive operations, prefer the typed delete tools (`agentdb_causal_node_delete`, `agentdb_causal_edge_delete`) — they enforce cascade semantics and write to the attestation log.

## Don't

- Don't use string interpolation for ids — use `params` to avoid Cypher injection.
- Don't run `MATCH (n) DETACH DELETE n` (deletes everything). Always scope the match.
- Don't loop a Cypher query in client code when one query with `WHERE id IN [...]` works — the binding's per-call overhead adds up.
