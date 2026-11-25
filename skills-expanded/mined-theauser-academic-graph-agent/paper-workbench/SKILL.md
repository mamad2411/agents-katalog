---
name: paper-workbench
description: Orchestrate the lightweight academic pipeline by chaining paper-fetch, paper-reflect, and paper-normalize.
metadata:
  {
    "openclaw":
      {
        "emoji": "🛠️",
        "requires": { "bins": ["python3"] }
      },
  }
---

# paper-workbench

Use this skill when the user wants a single entrypoint for the current MVP academic pipeline.

Workflow
- Run `python3 /root/openclaw-dev/workspace/scripts/run_workbench.py "<query>" --max-results <N> --top-n <M>`
- This chains:
  - `paper-fetch`
  - `paper-reflect`
  - `paper-normalize`
- Return the saved JSON paths for each stage

Notes
- This is the orchestration skill for the current MVP.
- It is intentionally lightweight and deterministic.
