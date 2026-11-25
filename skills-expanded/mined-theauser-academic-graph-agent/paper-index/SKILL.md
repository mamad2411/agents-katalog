---
name: paper-index
description: Build a lightweight local vector-style index record from normalized paper data.
metadata:
  {
    "openclaw":
      {
        "emoji": "🗂️",
        "requires": { "bins": ["python3"] }
      },
  }
---

# paper-index

Use this skill after `paper-normalize` when the user wants the paper added to the lightweight retrieval index.

Workflow
- Run `python3 /root/openclaw-dev/workspace/scripts/index_paper.py <normalized_json_path>`
- Read `/root/openclaw-dev/workspace/data/index/vector_index.jsonl`

Notes
- This MVP uses deterministic hashed vectors.
- Future versions can replace this with ChromaDB or other embedding backends.
