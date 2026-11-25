---
name: paper-reflect
description: Generate a lightweight structured reflection JSON for a single paper record.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"] }
      },
  }
---

# paper-reflect

Use this skill when the user wants structured extraction from a paper record.

Workflow
- Run `python3 /root/openclaw-dev/workspace/scripts/reflect_paper.py <paper_json_path>`
- Read the saved reflection JSON under `/root/openclaw-dev/workspace/data/reflections/`
- Treat this as a stable MVP skeleton, not a final Deep Reflection implementation

Outputs
- entities
- claims
- gaps
- placeholder arrays for methods, problems, datasets, metrics, baselines
