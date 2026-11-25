---
name: forge-blueprint
description: >-
  Break approved design into small tasks with file paths, verification steps,
  and dependencies. Use after forge-isolate baseline is green.
---
# Forge Blueprint

**Activates:** isolated sandbox ready.

## Task sizing

Each task: **2â€“5 minutes** of focused agent work â€” one logical commit worth.

## Plan file

Write `docs-ai/designs/drafts/{slug}-plan.md`:

```markdown
# Blueprint: {slug}

## Task 1 â€” {title}
- **Files:** `path/to/file.ts`, ...
- **Do:** (specific change)
- **Verify:** `npm test -- path/to/test.ts`
- **Done when:** (observable criterion)

## Task 2 â€” ...
```

## Requirements

- Every task lists **exact paths** (no "update the service")
- Every task has a **verify command** (test, lint, or curl)
- Mark tasks that need ADR or phase doc updates
- Order by dependency; flag parallelizable groups for `forge-parallel`

## Prompt cross-ref

`docs-ai/cross-cutting/agent-forge/workflow/prompts/planning/work-breakdown.md`

## Gate

Owner approves blueprint before `forge-execute` begins (explicit or implied "lanjut").
