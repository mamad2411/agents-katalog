---
name: pick-up-task
description: Pick up or resume a task from `_dev/TODO.md` — marks `[WIP]`, creates or switches to the task's feature branch, rebases with main. Use when the user invokes `/pick-up-task` or asks to grab/resume a pastiche task.
---

# pick-up-task

Harness conventions: `_dev/docs/harness.md`. Run from the pastiche repo root.

## Workflow

1. **Identify the task.** Read `_dev/TODO.md`. Tasks are numbered lines (`- [ ] **N.** Name — …`) under version-group headings. If the user named a task, use it; otherwise list unchecked, non-`[WIP]` tasks and ask. Respect group order — earlier groups first unless the user overrides.

2. **New or resume?** A task already marked `[WIP]` whose feature branch exists → resume. Otherwise → new.

3. **New task:**
   - Edit `_dev/TODO.md`: insert `[WIP] ` after `- [ ] ` on the task line.
   - Branch off main: `git checkout main && git pull && git checkout -b <version>/<task-name>` — `<version>` from the group heading (e.g. `1.1.0`), `<task-name>` kebab-cased short name (e.g. `1.1.0/codex-support`).
   - Tell the user the next step is `grill-me` → `grill-to-spec` → `divide-task`. Do not start it yourself.

4. **Resume:**
   - If the current branch is not the task's feature branch, switch to it.
   - Always run the `rebase-feat-with-main` skill (absorbs any hotfixes).
   - Report where the task stands (spec present at `_dev/docs/<branch>/`? sub-tasks divided?).

5. **Stop.** Pickup ends here; the user drives what happens next.

## Notes

- `[WIP]` is a soft lock across parallel sessions — never strip another session's marker.
- For live parallel work on sub-tasks, create a worktree off the feature branch instead of switching branches; skip the worktree when the user says to work directly on the current branch.
- Completion (not this skill's job): checkbox ticked, `[WIP]` removed, and parent issue closed when the feature branch merges to main.
