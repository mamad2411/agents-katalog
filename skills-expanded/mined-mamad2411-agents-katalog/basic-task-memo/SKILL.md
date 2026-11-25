---
name: basic_task_memo
description: Use when creating or updating docs/plan.md, docs/tasks.md, or docs/progress.md, or when asked about plan/todo/progress and next steps.
---

# Basic Task Memo

## Goal

Keep planning, TODOs, and progress logs consistent and actionable without mixing concerns.

## Workflow

1. Read memos

- Open `docs/plan.md`, `docs/tasks.md`, and `docs/progress.md`.
- Summarize the current goals and next actions; do not invent tasks.

2. Update plan (`docs/plan.md`) when scope or strategy changes

- Keep goals and success criteria measurable and short.
- Record decisions, risks, and open questions.
- Avoid task-level detail here; keep it strategic.

3. Update tasks (`docs/tasks.md`) for actionable work

- Use small, checkable items with clear outcomes.
- Keep each item independently completable.
- Remove or check off completed tasks.

4. Update progress (`docs/progress.md`) for completed work

- Append completed, high-signal changes as bullet points.
- Keep entries factual and brief.
- Do not add future work here.

5. Keep files in sync

- When a task completes, mark it in `docs/tasks.md` and add a progress entry.
- When a plan changes, align tasks to match it.

## Optional Template (use only if a file is missing)

```markdown
# Implementation Plan: <short title>

1. Goals and Targets

- Do:
- Target:

1. Success Criteria

-

1. Current State

-

1. Scope

-

1. Approach

-

1. Risks / Open Questions

-
```

## Guardrails

- Keep updates short and free of secrets or tokens.
- Preserve the existing structure when it is already in use.
- Confirm updates in the response and reference the file paths.
