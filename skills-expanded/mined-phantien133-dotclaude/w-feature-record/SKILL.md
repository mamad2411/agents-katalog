---
description: Phase 5 helper for w-task — create or append features/<feature-name>.md inside the current module doc folder. Tracks per-feature history, design decisions, schema/API, diagrams, and constraints for future features.
argument-hint: <task-slug> <feature-name>
allowed-tools: Bash, Read, Write, Edit
---

# w-feature-record

Persist the feature record file: the long-term, append-aware record of a feature's
design history. One file per feature, named after the user story or capability
(NOT after the ticket ID).

Reads `.claude/workflow.yaml`:
- `workflow.module_docs_root`
- `workflow.feature_records_subdir`

State source: `<state_root>/<task-slug>/{intake,plan,impact}.md` + current `state.yaml`.

---

## Inputs

- `$1` — task slug
- `$2` — feature name (kebab-case, no ticket ID). E.g. `sign-up`, `oauth-google`,
  `chat-persistence`, `rate-limiting`.

If `$2` missing: derive a draft from intake.md title; pause and ask developer to confirm.

---

## Step 1 — Resolve path

Read `state.yaml` for `module` field.
Path: `<module_docs_root>/<NN>-<module>/<feature_records_subdir>/<feature-name>.md`

If `workflow.module_docs_root` is null: abort with "Feature records not configured.
Run /w-setup to enable, or skip Phase 5 doc persistence."

---

## Step 2 — Check existence

- **File exists** → APPEND mode (Step 3a)
- **File does NOT exist** → CREATE mode (Step 3b)

---

## Step 3a — APPEND mode

Append a dated history row, then revise current-state sections (Schema/API,
Diagrams, Design decisions) to reflect the new state. Do NOT remove old sections —
overwrite their content with the post-change state.

```markdown
## <YYYY-MM-DD> — <task-slug>

<one-paragraph summary of what changed and why>
```

In the "Implementation history" table, add:
```
| <date> | <ID or n/a> | <one-line summary of this task's change> |
```

Re-read plan.md + impact.md and rewrite:
- § Design decisions — append new decisions, mark obsolete ones with ~~strikethrough~~
- § Schema / API — replace with current state (do NOT keep old schemas)
- § Diagrams — replace outdated Mermaid blocks with current ones
- § Constraints for future features — append new invariants

---

## Step 3b — CREATE mode

Write full file from template:

```markdown
# <feature-name>

## Summary
<what this feature does and why it exists — written to stay accurate over time>

## Implementation history
| Date | Ticket | What changed |
|------|--------|-------------|
| <YYYY-MM-DD> | <ID or n/a> | <one-line summary> |

## Design decisions
- <non-obvious choice 1> — <reasoning>
- <non-obvious choice 2> — <reasoning>

## Schema / API
<current Prisma models / GraphQL operations / REST endpoints>

## Diagrams
<Mermaid sequence / state machine for current flow>

## Constraints for future features
- <invariant 1>
- <pattern that must not be broken>
- <cross-module contract>
- <known deferred items>
```

Fill from:
- Summary, Schema/API, Diagrams ← plan.md + impact.md
- Design decisions ← questions.md answers + plan.md "Implementation approach"
- Constraints ← impact.md "Risks" + plan.md "Out of scope"

---

## Step 4 — Confirm

Print to chat:
```
Feature record written: <module_docs_root>/<NN>-<module>/features/<feature-name>.md
Mode: <CREATE | APPEND>
Sections updated: <list>

Review the file before /w-task advances Phase 5.
```

---

## Naming guidance

When developer is unsure, suggest:
- One feature per capability, not per ticket
- Use the user story slug if available
- Strip filler words ("add", "for", "the", "api")
- Examples:
  - "Add API for user sign-up" → `sign-up`
  - "Implement OAuth via Google" → `oauth-google`
  - "Add rate limiting to mutations" → `rate-limiting`

If multiple tasks plausibly belong to the same feature, ALWAYS reuse the existing
file rather than create a duplicate.
