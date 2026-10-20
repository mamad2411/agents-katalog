---
name: eni-github-workflow-hub
description: "Official GitHub workflow source catalog and local tool readiness adapter. Use when selecting upstream methods for reverse engineering, web testing, fuzzing, code security, cloud, mobile, memory, or scraping."
x-alice-class: assist
---

# 小寒 GitHub Workflow Hub

Read references/github-sources.md for the curated source matrix. Use scripts/source_catalog.py to filter sources by workflow and scripts/tool_adapter.py to detect locally available adapters.

    python scripts/source_catalog.py --workflow reverse --json
    python scripts/tool_adapter.py --workflow fuzzing --json

The package records immutable reviewed commits and absorbs method structure only. It does not vendor upstream repositories. Prefer stable releases or immutable commits when installing a tool.
