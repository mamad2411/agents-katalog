---
name: status
description: Refresh docs/STATUS.md from the current git state and the PLAN checklist so the next agent can resume without re-explaining. Use at the end of a work unit, before a commit, or when the user says "update status", "وضعیت رو آپدیت کن", "تا کجا رفتیم".
---

# status

Keep `docs/STATUS.md` truthful. Protocol: `.claude/rules/docs-protocol.md`.

## Steps

1. Run `git status --short` and `git diff --stat` (and `git log --oneline -5`) to see what changed since the last update.
2. Read `docs/STATUS.md` and the current phase in `docs/PLAN.md`.
3. Update STATUS: **Now** (phase + current task), **Done** (add verified items with today's date — only things that ran/rendered), **Next up** (ordered, remove finished), **Blocked / open questions**, **How to resume** (commands + read order), footer date + agent name.
4. Tick PLAN checkboxes whose acceptance criteria now hold; never tick on intent.
5. If a decision was made, add it to `docs/DECISIONS.md`; if a lesson was learned, add it to `memory/lessons.md`.
6. Reply with the diff summary of STATUS (3 lines max).
