---
description: Phase 2 helper for w-task — append a new Architecture Decision Record entry to the project's ADR doc when impact analysis surfaces a new decision. Generic version of streaming-adr.
argument-hint: <task-slug> <decision-title>
allowed-tools: Bash, Read, Write, Edit
---

# w-adr

Append an ADR entry to `workflow.adr_docs_path` (e.g. `architecture-overview.md`)
when a non-obvious architecture decision is made during a task.

Reads `.claude/workflow.yaml`:
- `workflow.adr_docs_path`

---

## Inputs

- `$1` — task slug
- `$2` — decision title (short, kebab-case OK or human-readable)

Reads `<state_root>/<task-slug>/{plan,impact}.md` for context.

---

## Step 1 — Preconditions

If `adr_docs_path` is null: print "ADR tracking not configured. Skipping." → exit 0.
If file does not exist: create with template (Step 2).

---

## Step 2 — Initialize file (if absent)

```markdown
# Architecture Overview

## Architecture Decision Records (ADRs)

| ADR | Decision | Date | Status |
|-----|----------|------|--------|

---

## Decision Details
```

---

## Step 3 — Compute ADR number

Read existing file. Find the highest ADR-NNN number in the table. Use N+1.
First entry → ADR-001.

---

## Step 4 — Append entry

Add row to the table:
```
| ADR-NNN | <decision-title> | <YYYY-MM-DD> | Accepted |
```

Then append a full block under § Decision Details:

```markdown
### ADR-NNN — <decision-title>
**Date:** <YYYY-MM-DD>
**Status:** Accepted
**Origin task:** <task-slug>

**Context**
<why this decision needed to be made — what problem / constraint / opportunity
existed. Pull from plan.md "Risks" + "Implementation approach".>

**Decision**
<the chosen approach — pull from plan.md "Implementation approach". State it as
a positive assertion of what the system DOES, not what was considered.>

**Alternatives considered**
- <alternative 1> — rejected because <reason>
- <alternative 2> — rejected because <reason>

**Consequences**
- <positive consequence>
- <trade-off / cost accepted>
- <constraint imposed on future tasks>
```

---

## Step 5 — Prompt for missing fields

If the developer did not provide enough context in plan.md / impact.md to fill
in the alternatives or consequences sections, pause and ask:

```
ADR-NNN draft is missing:
  - Alternatives considered
  - Consequences

Fill these in the draft below, then run /w-task to proceed.
```

Write the partial ADR with `<!-- TODO: fill -->` markers so it's clear what needs
attention. Do not silently leave them blank.

---

## Step 6 — Confirm

Print:
```
ADR-NNN appended to <adr_docs_path>
Title: <decision-title>
Status: Accepted

Review the entry before /w-task advances Phase 2.
```
