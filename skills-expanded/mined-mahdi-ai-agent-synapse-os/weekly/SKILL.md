---
name: weekly
description: Runs the PARA weekly review — inbox to zero, a next action per active project, stale tasks, archive candidates — into today's journal with proposed edits to approve. Use for "مرور هفتگی", "هفته رو مرور کن", "آخر هفته‌ست", "weekly review", "review my week", or the Weekly review button.
---

# weekly

Read-mostly: this skill writes only today's journal node. Every other change is a proposed edit the user approves first (then `/capture`, `/link` or a manual edit applies it).

## Steps

1. Read `index/INDEX.md`, `index/by-type/task.md` and `index/by-type/project.md`. Open at most 5 nodes when a detail is needed (e.g. a project body without **Next action:**).
2. Fill the four sections with the thresholds in [references/checklist.md](references/checklist.md): Inbox · Projects · Stale tasks · Archive candidates.
3. Append the review to `nodes/journal/YYYY-MM-DD.md` (date from **Now** in the runtime context) under `## HH:mm — Weekly review`; create the node per `.claude/rules/journal.md` when missing; update its `summary` and `updated`. End the entry with a **Proposed edits** checklist, one concrete edit per `- [ ]` line.
4. Reply with the review and the checklist in the user's language and ask which edits to apply. Apply none in this run.
