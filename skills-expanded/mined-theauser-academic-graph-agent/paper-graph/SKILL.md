---
name: paper-graph
description: Write lightweight graph edges from normalized paper entities into a local graph store.
metadata:
  {
    "openclaw":
      {
        "emoji": "🕸️",
        "requires": { "bins": ["python3"] }
      },
  }
---

# paper-graph

Use this skill after `paper-normalize` when the user wants the paper represented in the lightweight graph layer.

Workflow
- Run `python3 /root/openclaw-dev/workspace/scripts/write_graph.py <normalized_json_path>`
- Read `/root/openclaw-dev/workspace/data/graph/graph.jsonl`

Notes
- This MVP writes idempotent JSONL edges.
- Future versions can replace this with Neo4j.
