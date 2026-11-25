---
name: kanban-schedule-run
description: 'Plan or run explicitly authorized scheduled work on selected Kanban cards. Use when the user requests a scheduled run for specific cards. RU: запланировать задачи, расписание, планировщик.'
---

# Schedule Kanban work

Use when the user requests a scheduled run for specific cards. Discover the board, scheduling and agent capabilities through the current runtime and project interface. This package currently contains a **Claude Code-specific** prototype; consult [its runtime interface and limitations](claude-runtime.md) only when that runtime is actually selected. Do not claim Codex, Hermes, Cursor or Prime execution support from this skill alone.

Before any enqueue, establish the user's intended time and timezone, exact ordered cards, action limits and project acceptance gates. The selected card and each additional card require applicable explicit user authority. Separately authorize any merge, `done`, push, deployment or notification. The current manifest format requests a merge-at-ready permission: do not create it unless that exact action and cards are authorized. A manifest digest protects its bytes, not the origin of approval.

Inspect the complete repository state, current branch, other running work and actual board/helper behavior. The prototype refuses staged, unstaged or untracked repository changes and does not establish exclusion from manual writers. Do not stage, commit, switch branches or remove queued jobs merely to make a scheduled run possible. Use the supported project workflow and preserve unrelated work. Treat a native access, security or approval refusal as a stop.

Check the exact scheduler entry after a permitted enqueue and report its identifier and cancellation interface without changing other jobs. A pending, timed-out, failed or unreviewed run is not completion. Automatic commits and staging are disabled. A card that cannot continue is checkpointed only through `park-task.sh` (a side-branch snapshot that leaves branch, index and worktree untouched; the owner restores the checkout later with `park-task-clean.sh`, never the scheduled agent); otherwise stop on the blocker and preserve everything. More detail: [lifecycle boundaries](lifecycle.md), [scope and safety](reference.md).
