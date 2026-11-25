---
name: status
description: Show current project state for TenantFlow. Reports what's done, in progress, blocked, failed, and next. Run any time to see where the project stands.
---

# Status

Reports project state for TenantFlow.

## Workflow

1. **Read state** — load `tasks.json` and `orchestrator_state.json`
2. **Categorize tasks** by `status` (the list is under State Management in `.claude/agents/orchestrator/AGENT.md`):
   - ✅ Done — `done`
   - 🔄 In progress — `in_progress`
   - 🔍 Review — `review`, needs checking again
   - 🚫 Blocked — `pending`, but a task in its `depends_on` isn't `done`
   - ⏳ Pending — `pending` and ready to start
   - 🔴 Failed — `failed`, going through self-healing
   - ⏭️ Skipped — `skipped` after max retries
3. **Show milestone progress** — percentage complete per milestone
4. **Show recent activity** — last 5 entries from `progress.log`
5. **Show next action** — what the orchestrator will do next
6. **Show failures** — any failed or skipped tasks, with `attempts` and the reason

## Output format
Print to console. Group by milestone. Show counts at the top: `Done: X | In Progress: X | Review: X | Blocked: X | Pending: X | Failed: X | Skipped: X`
