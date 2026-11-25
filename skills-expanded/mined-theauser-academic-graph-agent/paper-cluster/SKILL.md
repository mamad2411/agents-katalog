---
name: paper-cluster
description: "Build, query, and visualize literature relationship clusters using Kuzu and Cypher."
requires:
  bins:
    - /root/openclaw-dev/envs/academic-embed/bin/python
---

# Paper Cluster

Use this skill when the user wants to build or inspect a literature graph, run Cypher over paper and entity relationships, or render a paper cluster visualization.

## Capabilities
- ingest normalized paper JSON into Kuzu
- query the paper graph with Cypher
- render cluster graphs to PNG

## Data Rules
- All runtime data for this skill must stay under `/root/openclaw-dev/data/`
- Kuzu database path: `/root/openclaw-dev/data/kuzu/academic_graph`
- Visualization output path: `/root/openclaw-dev/data/visualizations/`
- Query audit path: `/root/openclaw-dev/data/queries/last_query.json`

## Commands
Ingest one normalized paper:
```bash
/root/openclaw-dev/envs/academic-embed/bin/python /root/openclaw-dev/workspace/scripts/graph_engine.py ingest /root/openclaw-dev/workspace/data/normalized/2312.10793v3.json
```

Run a Cypher query directly:
```bash
/root/openclaw-dev/envs/academic-embed/bin/python /root/openclaw-dev/workspace/scripts/graph_engine.py query "MATCH (p:Paper)-[:MENTIONS]->(e:Entity) RETURN p.id AS paper_id, e.name AS entity LIMIT 10"
```

Render a paper cluster visualization:
```bash
/root/openclaw-dev/envs/academic-embed/bin/python /root/openclaw-dev/workspace/scripts/graph_engine.py visualize "MATCH (p:Paper)-[:MENTIONS]->(e:Entity) RETURN p.id AS source, 'Paper' AS source_label, 'MENTIONS' AS rel_type, e.name AS target, 'Entity' AS target_label LIMIT 50" --output-name paper-cluster-demo.png
```

## Notes
- Entity nodes are rendered in blue.
- Paper nodes are rendered in red.
- `query` expects a Cypher string that has already been produced from user intent.
- `visualize` expects query output columns named: `source`, `source_label`, `rel_type`, `target`, `target_label`.
