---
name: paper-normalize
description: Normalize extracted paper entities into canonical forms with lightweight audit logs.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧩",
        "requires": { "bins": ["python3"] }
      },
  }
---

# paper-normalize

Use this skill after `paper-reflect` when the user wants canonical entities and alias cleanup.

Workflow
- Run `python3 /root/openclaw-dev/workspace/scripts/normalize_entities.py <reflection_json_path>`
- Read the normalized JSON under `/root/openclaw-dev/workspace/data/normalized/`
- Inspect `audit_log` for alias mappings and dedupe actions

Notes
- This MVP uses deterministic rules only.
- Future versions can replace rules with a reviewed LLM normalization step.
