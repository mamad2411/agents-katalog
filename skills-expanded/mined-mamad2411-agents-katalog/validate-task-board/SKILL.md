---
name: validate-task-board
description: "Second-pass review — moves To-Validate tasks to Done or back to To-Do with clarifying notes (suited to running with a stronger model)"
---

# Task validation (To-Validate → Done / To-Do)

**Goal:** Review tasks that have **already been completed** in the **first pass** (usually with a faster/lighter model) and sit in the **`To-Validate`** folder.  
Running with a stronger or more capable model improves the chance of catching logic errors, gaps, or mismatches with acceptance criteria.

> **Varies by project:** By default this assumes the structure `Agent_reports/Tasks/{To-Do,To-Validate,Done}`. If the user provides different paths, use those.

---

## When to use

- After **`/process-task-board`**, when finished work was placed under **`To-Validate`** (not straight into `Done`).
- When a human (you) wants an **automatic “second pair of eyes”** before marking something `Done`.

**Model choice:** In the IDE, run this workflow in a chat where a **stronger / more capable model** is selected (if you have a choice), to reduce superficial approval.

---

## Input and output

| Role | Default path (customizable) |
|------|-----------------------------|
| Tasks to review | `<project>/Agent_reports/Tasks/To-Validate/` |
| If approved | `.../Done/` |
| If fixes needed | `.../To-Do/` |

If the user **does not provide paths**, assume these three folders from the project root.  
The user may give absolute paths, e.g. `~/project/Agent_reports/Tasks/To-Validate`.

---

## Task file state after review

You may update frontmatter (if you use YAML):

```yaml
validation_status: approved   # approved | needs_revision
validated_at: "2026-03-23T14:00:00+02:00"   # ISO 8601
reviewer: agent-second-pass    # human may replace with their initials
```

If there is no frontmatter: add the review summary at the **beginning** or **end** of the file with a consistent heading (see below).

---

## Review protocol

For each file or task folder (`To-Validate/<id>-<slug>/`):

### 1. Read completely

- Task description and **acceptance criteria** (if present).
- The full outcome: `.md` body, adjacent artifacts, `README.md` in the folder.

### 2. Evaluation checklist

1. **Completeness:** Are all criteria covered or justified if not?
2. **Internally consistent:** Do conclusions match assumptions and data?
3. **Code tasks:** Are changes aligned with project rules; are tests / lint mentioned or visibly missing (note risk)?
4. **Analysis / documents:** Are conclusions overstated without evidence; are alternatives reasonably considered?
5. **Security and data:** Does anything suggest risk of secret or PII leakage in documentation?
6. **`type: code` tasks:** Does the work show a full cycle was followed (at least references to branch, tests, commit), not only “code changed”? If the task expected **`/implement-feature`** or **`/fix-bug`** but tests/commit are missing without a user exception → prefer **`needs_revision`** and list missing steps.

If the task is a **partner proposal** type, you may additionally reference the **`/validate-external-proposal`** workflow logic (you do not need to rerun the whole flow if the content is already complete).

### 3A. Approve → `Done`

1. Update frontmatter (or append a **Validation summary** section — short positive confirmation).
   - required fields:
     - `validation_status: approved`
     - `status: done`
2. Move the **entire task folder or file** from `To-Validate` → `Done` (same relative structure: if it was `To-Validate/PROJ-1/report.md` + subfiles, keep them together).
3. Do not leave duplicates under `To-Validate`.

### 3B. Fixes needed → `To-Do`

1. Append to the task file (or a separate `REVIEW.md` in the same folder if the file is very long — prefer one place for clarity):

```markdown
## Review feedback (validation pass)

**Status:** needs_revision  
**Date:** YYYY-MM-DD

### Must fix
- [ ] ...

### Suggestions (optional)
- ...

### Notes
- ...
```

2. Update frontmatter: `validation_status: needs_revision`, `status: open`.
3. Move the task (or entire subfolder) from `To-Validate` → `To-Do`.
4. If artifacts are stale or misleading, note in the review **which files should be rewritten or deleted** — do not delete aggressively without user policy; prefer notes.

### 3C. If a new dependent task is needed

If validation shows that completing the current task requires a separate new task:

1. Create a new task in **To-Do** in the correct format (new `id`, clear scope, acceptance criteria).
2. Add a reference in the original task’s review (`follow_up_tasks` or a clear ID list).
3. Do not mark the original task `done` by mistake if the dependency is open:
   - use `needs_revision` or split scope and document which part was considered done.

---

## Report

At the end, provide a summary:

| Task | Decision | Target folder |
|------|----------|---------------|
| … | approved / needs_revision | Done / To-Do |

---

## References

- Task execution: **`/process-task-board`**
