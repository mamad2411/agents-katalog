---
name: spec-driven-archive
description: Archive a completed spec-driven change. Warns on incomplete tasks, moves change to archive/ with a date prefix.
version: 0.1.0
---

You are helping the user archive a completed spec-driven change.

## Steps

1. **Select the change** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify` to list active changes. Ask which change to archive. If already specified, use it.

2. **Check for incomplete tasks** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>
   ```
   If `remaining > 0`, warn the user:
   > "This change has X incomplete tasks. Archiving will preserve them as-is. Are you sure you want to proceed?"
   Wait for confirmation before continuing.

3. **Merge delta specs** — list all files in `.spec-driven/changes/<name>/specs/`:
   - If `specs/` is empty: ask the user to confirm this change has no observable spec impact before continuing.
   - For each delta file (e.g. `specs/install/install-behavior.md`), merge into the corresponding main spec file (e.g. `.spec-driven/specs/install/install-behavior.md`):
     - **ADDED**: append the `### Requirement:` blocks to the target file (create it if it doesn't exist)
     - **MODIFIED**: locate the existing `### Requirement: <name>` block by name and replace it in place
     - **REMOVED**: locate the `### Requirement: <name>` block by name and delete it; remove the file if it becomes empty
   - Briefly summarize what changed in `specs/` after merging.

4. **Update specs/INDEX.md** — after merging, update `.spec-driven/specs/INDEX.md`:
   - Add entries for any newly created spec files (with a one-line description)
   - Remove entries for any deleted spec files
   - Leave existing entries unchanged unless the file's scope changed

5. **Archive the change** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js archive <name>
   ```
   This moves the entire change directory (including questions.md) to the archive.

6. **Confirm** — report the result:
   - Where the change was moved to (e.g. `.spec-driven/changes/archive/2024-01-15-<name>/`)
   - Suggest running `/spec-driven-propose` if there's follow-up work

## Rules
- Always check for incomplete tasks before archiving
- Always merge delta specs before archiving — this is a hard gate, not optional
- Do not skip the incomplete-task warning — let the user make an informed decision
- Do not delete anything — archive only moves, never deletes
