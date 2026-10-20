---
name: neo4j-graph
description: "Query and traverse graph data using Neo4j's Cypher query language at {{NEO4J_HOST}}:{{NEO4J_PORT}}."
metadata:
  openclaw:
    emoji: "🕸️"
---

# Neo4j Graph Database

Neo4j is available at `http://{{NEO4J_HOST}}:{{NEO4J_PORT}}` within the Docker network.

## Running Cypher Queries

```bash
curl -X POST "http://{{NEO4J_HOST}}:{{NEO4J_PORT}}/db/neo4j/tx/commit" \
  -H "Content-Type: application/json" \
  -u neo4j:$NEO4J_PASSWORD \
  -d '{"statements": [{"statement": "MATCH (n) RETURN n LIMIT 10"}]}'
```

## Creating Nodes and Relationships

```bash
curl -X POST "http://{{NEO4J_HOST}}:{{NEO4J_PORT}}/db/neo4j/tx/commit" \
  -H "Content-Type: application/json" \
  -u neo4j:$NEO4J_PASSWORD \
  -d '{"statements": [{"statement": "CREATE (a:Person {name: $name}) RETURN a", "parameters": {"name": "Alice"}}]}'
```

## Tips for AI Agents

- Use parameterized queries with `$variable` syntax to prevent injection.
- Use `MERGE` instead of `CREATE` to avoid duplicate nodes.
- Use indexes on frequently queried properties: `CREATE INDEX FOR (n:Label) ON (n.property)`.
- The Bolt protocol (port 7687) is preferred for application connections.
