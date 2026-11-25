---
name: workspai-grounding
description: Load Workspai workspace intelligence reports before diagnosing or changing code
---

# Workspai grounding

Use when the user asks about workspace health, release gates, doctor/pipeline failures, or project structure.

## Workflow

1. Read `.workspai/reports/INDEX.json`
2. Read `.workspai/reports/workspace-context-agent.json`
3. Read fail/warn evidence artifacts listed in the index
4. Propose the smallest safe fix with explicit verification commands

## Refresh stale evidence

```bash
npx workspai workspace agent-sync --write --refresh-context
```
