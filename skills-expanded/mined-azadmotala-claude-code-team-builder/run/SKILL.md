---
name: run
description: Autonomous execution loop for TenantFlow. Plans tasks, assigns agents, validates results, self-heals on failure. Use `/run --plan` to generate a plan without executing. Use `/run` to start or resume execution.
---

# Run

Autonomous execution loop for TenantFlow.

## Usage
- `/run --plan` — decompose project into milestones and tasks, show the plan, don't execute
- `/run` — start or resume execution from current state
- `/run --task m1-t3` — execute a single specific task
- `/run --milestone m2` — execute all tasks in milestone 2

## Execution Loop

The loop is defined once, in `.claude/agents/orchestrator/AGENT.md`. Read that file and follow it yourself, in this session, rather than handing the loop to the orchestrator agent. That way you can pass each task straight to the right agent.

1. **Reconcile State**, under State Management, before anything else
2. **Generate the dashboard**: copy `.claude/skills/dashboard/dashboard.html` to `.claude/workspace/dashboard.html`. Do NOT regenerate it from scratch; it reads `tasks.json` and `progress.log` via fetch.
3. **Plan** if there's no `tasks.json` yet, or with `--plan`: break the project into milestones and tasks using the Task Sizing Rules, and write `tasks.json` in the structure under State Management. With `--plan`, show the plan and stop here.
4. **Run the Execution Loop and the Self-Healing Pipeline** exactly as written there. With `--task` or `--milestone`, run only those tasks.

Don't copy the orchestrator's rules into this file. If the loop needs to change, change it in the orchestrator's file.
