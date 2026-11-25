---
name: daily
description: Runs the daily review — overdue, due-today and doing tasks, each project's next action, today's focus and a suggested plan — into today's journal node. Use for "مرور روزانه", "روزم رو شروع کن", "برنامه‌ی امروز", "امروز چی مهمه", "daily review", "plan my day", "start my day", "what matters today", or the Daily review button.
---

# daily

Index first: `index/INDEX.md` already lists overdue tasks, tasks due today and every active project with its next action. Open `index/by-type/task.md` only for the `doing` tasks. Never read node files for this review.

## Steps

1. Read `index/INDEX.md`; collect the overdue tasks, the tasks due today, and each active project's `next:` task (or none). Read `index/by-type/task.md` and collect the `doing` tasks. Read `memory/focus.md` when it exists: the full review's **Now** order leads today's focus.
2. Compose the entry per [references/format.md](references/format.md): only non-empty sections, one `[[Title]]` per line, the day's suggested plan, then one specific journal prompt.
3. Append it to today's journal node `nodes/journal/YYYY-MM-DD.md` (date from **Now** in the runtime context) under `## HH:mm — Daily review`; create the node per `.claude/rules/journal.md` when missing.
4. Refresh the node's frontmatter in the same edit: replace `summary` with one quoted line (≤ 160 chars) that keeps what the day already said and ends with the review's counts (see the summary rule in [references/format.md](references/format.md)), and set `updated` to **Now**. A journal whose `summary` does not mention the review is not finished.
5. Reply with the same entry in the user's language. Change nothing else: the review observes, the user decides.
