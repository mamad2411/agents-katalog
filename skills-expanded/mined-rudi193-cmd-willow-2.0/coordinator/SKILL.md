---
name: coordinator
description: Coordinator mode — fan-out tasks to sub-agents, track progress, synthesize results. Run fleet-dashboard first.
---

@markdownai v1.0

## When to use coordinator mode

Use when a task requires parallel or sequential sub-agent work: analysis across
multiple files, multi-step pipelines, or any work that benefits from isolation.

## Boot

1. Run /fleet-dashboard to confirm all agents are reachable and Postgres is up.
2. Identify which agents (heimdallr, hanuman, shiva, etc.) should own each subtask.

## Fan-out pattern

1. Create a fork for the initiative:
   fork_create(app_id: heimdallr, title: "initiative name", created_by: heimdallr)

2. Dispatch subtasks in parallel:
   agent_task_submit(app_id: heimdallr, task: "...", agent: hanuman)
   agent_task_submit(app_id: heimdallr, task: "...", agent: shiva)

3. Poll completion:
   agent_task_status(app_id: heimdallr, task_id: ...)

4. Synthesize results into a KB atom:
   kb_ingest(app_id: heimdallr, title: "...", summary: "combined findings")

5. Close the fork:
   fork_merge(app_id: heimdallr, fork_id: FORK-XXXX, outcome_note: "...")

## Priority groups (for routing decisions)

| Group    | Agents                                    | Use for                        |
|----------|-------------------------------------------|--------------------------------|
| OPERATOR | willow, ada, steve                        | Infrastructure, system tasks   |
| ENGINEER | heimdallr, hanuman, opus, kart, shiva, ganesha | Feature work, analysis    |
| WORKER   | Others                                    | Narrow, bounded subtasks       |

## Rules

- Always check grove_inbox before dispatching — another agent may own the task.
- Log every significant change to the fork with fork_log.
- One fork per initiative. Don't nest forks.
- Run tension_scan after synthesizing results with write_kb=true.
