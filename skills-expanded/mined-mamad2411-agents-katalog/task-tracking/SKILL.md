---
name: task-tracking
description: File-based to-do tracking for multi-step and multi-session work.
usedBy: [all]
version: 0.1.4
lastUpdated: 2026-09-12
---

## Purpose

Agents working on multi-step tasks need a way to track progress that survives session boundaries. A task that spans hours or days will be picked up by an agent with no memory of what was already done. This skill defines a file-based to-do format that any persona can create, update, and resume — so the next session starts where the last one stopped.

## Procedure

1. **Check for an existing to-do.** Run `ls .memory/todo/ 2>/dev/null` to list existing to-do files. If a to-do file for the current task already exists, read it and resume from the first unchecked item. Do not recreate.

2. **Create a to-do from the plan or task brief.** If no existing to-do matches, run the following command to create the file — replace the placeholders with real values:

   ```bash
   mkdir -p .memory/todo && cat > .memory/todo/YYYY-MM-DD-<prefix>-<slug>.md << 'TEMPLATE'
   # <Task Title>

   **Slug:** <prefix>-<slug>
   **Source:** plan | task-brief
   **Created:** YYYY-MM-DD
   **Updated:** YYYY-MM-DD

   ## Items

   - [ ] First item
   - [ ] Second item

   ## Log

   - YYYY-MM-DD: Created from plan/task-brief.
   TEMPLATE
   ```

   Then populate the items from `impl.md` epics and file lists, or from the task brief's acceptance criteria. Each item must be a concrete, verifiable action — not a vague category.

   **Target directory:** `.memory/todo/` — always at the project root, never anywhere else.

   **Naming convention:** The filename uses the pattern `YYYY-MM-DD-<prefix>-<slug>.md`, where `<prefix>` is the conventional-commit type and `<slug>` is a short kebab-case summary — the same convention used for branch names (follows: `rules/git.md`). Examples: `.memory/todo/2026-02-18-feat-user-auth.md`, `.memory/todo/2026-02-18-fix-login-redirect.md`. If a git branch already exists for this work, derive the prefix and slug from the branch name.

3. **Update as you go.** After completing each item, mark it `[x]` and add a log entry if the outcome was notable (unexpected decision, deviation from plan, blocker encountered). Do not batch updates — mark items done as they finish.

4. **Handle blockers.** If an item cannot be completed, mark it `[-]` with a reason in the log. Continue with unblocked items. If nothing can proceed, stop and note the blocker in the log.

5. **Close the to-do.** When all items are done (or skipped with reason), truncate the to-do file with `: > .memory/todo/<filename>`. The handoff summary is the permanent record — the to-do is a working document, not an archive.

## Schema

```markdown
# <Task Title>

**Slug:** <prefix>-<topic>
**Source:** plan | task-brief
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

## Items

- [x] Completed item
- [ ] Pending item
- [-] Skipped item

## Log

- YYYY-MM-DD: Notable event, decision, or blocker.
```

## Schema notes

- **Slug** matches the `<prefix>-<topic>` portion of the filename and follows the git branch prefix convention.
- **Source** identifies whether items came from an architect plan or a task brief.
- **Updated** changes every time an item is checked off or a log entry is added.
- Items use standard checkbox syntax: `[x]` done, `[ ]` pending, `[-]` skipped.
- Log entries are chronological. Keep them terse — one line per event.

## Guardrails

- To-do files live exclusively in `.memory/todo/` at the project root. Never create them anywhere else.
- Never start implementing without first creating or locating an existing to-do.
- Never let the to-do drift from reality. If you completed something, mark it now, not later.
- Never delete a to-do with unchecked items unless the task has been explicitly cancelled.
