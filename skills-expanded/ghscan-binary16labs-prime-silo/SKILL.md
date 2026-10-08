---
name: prime-silo-neo4j
description: Queries Neo4j for Prime-Silo run lineage, memory graphs, and session states.
---

# Prime-Silo Neo4j Graph Skill

Use this skill to fetch highly specific subgraphs of the Prime-Silo execution lineage or Memo-Ray sessions without pulling large amounts of JSON data.

## Instructions

1.  **Locate Database**: Ensure Neo4j is running. Typically accessible via `bolt://localhost:7687` with default credentials setup in `prime-silo.config.json` or `.env`.
2.  **Query Run Lineage**:
    To query what files a run touched:
    ```cypher
    MATCH (r:Run {id: $runId})-[:MODIFIED]->(f:File)
    RETURN f.path
    ```
3.  **Query Session State**:
    To get the context of an agent's drafting session:
    ```cypher
    MATCH (s:Session)-[:CREATED]->(d:Draft)
    WHERE s.active = true
    RETURN d.title, d.path
    ```
4.  **Format Output**: Return only the essential path strings or small JSON metadata blocks to conserve token limits during agent execution.
