---
description: "Quick maintenance cycle: discover-tasks → auto-task → update-docs. No team agents, no review."
---

# Quick

Use the **workflow-quick** agent for this task.

Delegate all work to the `workflow-quick` agent now.

## What it does

1. **SAFETY CHECK** — Scan tasks.md for security/sql-injection/data-integrity tags → refuse if found, suggest `/sprint`
2. **DISCOVER** — `discover-tasks` (single agent, lightweight)
3. **IMPLEMENT** — `auto-task` (batch execute) → PR + merge
4. **DOCS** — `update-docs` → sync documentation

## When to use

- Small improvements, tech debt cleanup, documentation
- Tasks that don't touch text-to-SQL, database schema, or API keys

## When NOT to use

- Any work involving text_to_sql.py, database schema, API key handling
- Use `/sprint` or `/fix` instead for those

## Output

Quick cycle summary with completed task count.
