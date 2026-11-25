---
name: task-management
description: >
  Create, update, list, prioritize, and triage tasks.
  TRIGGER when: user says "add task", "todo", "what are my tasks", "mark done",
  "triage", "prioritize", or manages any work item tracking.
argument-hint: "[add|list|done|triage|delete] [task description or ID]"
user-invocable: true
---

# Task Management

A structured, file-based task tracking system. Each task is an individual markdown file with YAML frontmatter, indexed in a central manifest.

## First-Run Setup

Before any operation, ensure the task system exists:

1. Check if `~/.claude/tasks/` exists — if not, create with `mkdir -p ~/.claude/tasks/`
2. Check if `~/.claude/tasks/TASKS.md` exists — if not, create:

```markdown
# Task Index

<!-- Auto-maintained. Do not edit manually. -->

## In Progress

## To Do

## Blocked

## Done
```

## Task Schema

Each task is a file at `~/.claude/tasks/TASK-{NNN}.md`:

```yaml
---
id: TASK-001
title: "Short imperative description (max 80 chars)"
status: todo | in-progress | done | blocked
priority: critical | high | medium | low
created: 2026-04-08
updated: 2026-04-08
due: 2026-04-15          # optional — ISO date
completed: null           # set to ISO date when done
tags: [feature, backend]  # optional — freeform labels
blocked-by: TASK-003      # optional — dependency
source: "gh#45"           # optional — link to GitHub issue, PR, or external ref
---

Detailed description of what needs to be done and why.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
- YYYY-MM-DD: Progress note or context update
```

## Operations

### Add — `$ARGUMENTS` starts with "add" or user describes a new task

1. **Parse input**: Extract title, priority, due date, tags from the user's description. Infer what you can; ask only for what's ambiguous.
2. **Generate ID**: Read existing task files to find the highest ID, increment by 1. Pad to 3 digits (e.g., `TASK-001`).
3. **Normalize dates**: Convert relative dates to absolute ISO format. Use today's date as reference.
4. **Default values**: `status: todo`, `priority: medium`, `created: today`, `updated: today`.
5. **Write task file**: Create `~/.claude/tasks/TASK-{NNN}.md` with full schema.
6. **Update index**: Add entry to the appropriate section in `TASKS.md`:
   `- [TASK-{NNN}](TASK-{NNN}.md) — {title} ({priority}, due {date})`
7. **Confirm**: Show the created task with its ID.

### List — `$ARGUMENTS` starts with "list" or user asks to see tasks

1. Read `TASKS.md` and present grouped by status.
2. **Filtering**: Support filters from `$ARGUMENTS`:
   - `list high` — filter by priority
   - `list blocked` — filter by status
   - `list backend` — filter by tag
   - `list overdue` — due date < today and status != done
3. **Sorting**: Within each status group, sort by: priority (critical > high > medium > low), then due date (soonest first), then creation date.
4. **Output format**:

```
## Tasks (5 total: 1 in-progress, 3 todo, 1 blocked)

### In Progress
- TASK-005: Migrate user table (high, due tomorrow)

### To Do
- TASK-007: Write API docs (medium, no due date)
- TASK-008: Add rate limiting (medium, due 2026-04-20)
- TASK-009: Update onboarding flow (low)

### Blocked
- TASK-006: Deploy auth service — blocked by TASK-005
```

### Done — `$ARGUMENTS` starts with "done" or user marks a task complete

1. Find the task by ID or keyword match. If ambiguous, present options and ask.
2. Update the task file:
   - Set `status: done`
   - Set `completed: {today}`
   - Set `updated: {today}`
3. Move the entry in `TASKS.md` from its current section to `## Done`.
4. If the completed task was blocking other tasks (`blocked-by` references), notify the user and offer to unblock them.
5. Confirm completion.

### Update — user wants to change a task's priority, due date, description, or status

1. Find the task by ID or keyword.
2. Apply the requested changes to the task file frontmatter and/or body.
3. Always set `updated: {today}`.
4. Add a timestamped note under `## Notes` describing the change.
5. Update `TASKS.md` if the status, priority, or title changed.
6. Confirm what was updated.

### Triage — `$ARGUMENTS` starts with "triage" or user asks to review tasks

Triage walks through tasks that need attention:

1. **Identify candidates**:
   - Overdue: `due < today` and `status != done`
   - Stale: `updated` > 7 days ago and `status` is `todo` or `in-progress`
   - Unestimated: no `due` date and `priority` is `high` or `critical`
   - Long-running: `in-progress` for > 14 days
2. **Present each** with context and ask the user to choose an action:
   - **Reprioritize**: change priority
   - **Reschedule**: set or update due date
   - **Close**: mark as done or remove
   - **Skip**: leave as-is for now
3. **Apply changes** as the user decides.
4. **Summary**: After triage, show counts of actions taken.

### Delete — `$ARGUMENTS` starts with "delete" or "remove"

1. Find the task by ID or keyword.
2. **Require explicit confirmation** — show the full task before deleting.
3. Remove the task file.
4. Remove the entry from `TASKS.md`.
5. Check if any other tasks have `blocked-by` referencing this task. If so, warn the user.
6. Confirm deletion.

## Integrity Rules

- **Single source of truth**: Task files are authoritative. `TASKS.md` is a derived index.
- **Index repair**: If `TASKS.md` is out of sync with task files (missing entries, wrong status), rebuild it from the task files.
- **No duplicates**: Before creating, search existing tasks for similar titles. Warn if a near-duplicate exists.
- **ID immutability**: Once assigned, a task ID never changes. Deleted IDs are not reused.
- **Audit trail**: Every status change gets a timestamped note in the task file.
- **Atomic updates**: Always update both the task file AND `TASKS.md` in the same operation. Never leave them inconsistent.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
