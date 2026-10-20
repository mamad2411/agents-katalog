---
name: business-brief-to-tasks
description: "Turns a business brief or raw assignment into atomic tasks in a folder (including EPIC and sub-tasks)"
---

# From business brief to task folder

Input: **one or more files** (business description, Jira export, meeting notes) — usually under `Agent_reports/...` in the project or a user-specified path.  
Output: **structured task files** in the target directory (recommended: **`Agent_reports/Tasks/To-Do/`**), ready for processing with the **`/process-task-board`** workflow.

---

## Objective

- Break down a bulky requirement into **actionable** units.
- Allow **EPIC** level: one large chunk = one `type: epic` file + subfolder `epic-<id>/` with sub-tasks *or* separate files prefixed `[EPIC-PROJ-1]`.
- Preserve traceability: where a sentence came from → briefly reference the brief paragraph or Jira key.

---

## Reading input

1. Read all `.md`, `.txt`, and (if present) `.csv` files in the given folder that look like tasks or requirements.
2. Jira CSV / export: each row may become `id` and `title`; the description column remains the task body.

---

## Creation rules

### Task size

- **Task:** 0.5–3 days of dev/analysis work (guideline); if larger → **EPIC** or split.
- **EPIC:** if the work spans multiple sprints or needs several teams / sequential phases — create:
  - root file `EPIC-<id>-<slug>.md` with frontmatter `type: epic`, and
  - subfolder `EPIC-<id>-<slug>/tasks/` containing `T-01-....md`, `T-02-....md`, … **or** add everything flat under `To-Do/` with filenames like `PROJ-epic1-sub1.md`.

### Frontmatter for each new task

```yaml
---
id: <project or Jira key or generated T-01>
jira_id: <Jira key, e.g. VAHE-3174; empty if missing>
type: code | analysis | validation | breakdown | epic
code_workflow: ""   # optional: implement-feature | fix-bug | refactor (for type: code)
title: <short title>
source: business-brief
epic_of: <epic id or empty>
status: open
depends_on: []
---
```

### Jira reference rule (`jira_id`)

- If the input contains a Jira key (pattern `ABC-123`, e.g. `VAHE-3174`), add it **always** to the `jira_id` frontmatter field.
- If the input has several Jira keys:
  - the primary / requester ticket goes to `jira_id`,
  - add the rest in the task body under `## Notes / open questions` as a bullet `Related tickets: ...`.
- If no Jira key is found, leave `jira_id` empty (`jira_id: ""`) or ask the user for clarification.
- If `id` is not a Jira key (e.g. internal `T-01`), `jira_id` remains a separate field.

### Body structure (recommended)

```markdown
## Context
[1–3 sentences]

## Acceptance criteria
- [ ] ...

## Notes / open questions
- ...
```

---

## Output layout

The user specifies the **target directory** (recommended: `<project>/Agent_reports/Tasks/To-Do/`).

1. Write files there; do not overwrite existing same-name files — if conflict, add suffix `-2`.
2. If an EPIC structure was created, add `To-Do/EPIC-.../README.md` with a short map of sub-tasks.

---

## Summary for the user

At the end, present:

- List of created files and `type` values.
- EPICs and their sub-task counts.
- Suggested next step: **`/process-task-board`** input = this `To-Do/`, output = `To-Validate/` (or directly `Done/`, if agreed).

---

## References

- Task execution: **`/process-task-board`**
