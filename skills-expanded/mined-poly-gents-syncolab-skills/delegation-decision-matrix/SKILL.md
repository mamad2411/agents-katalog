---
name: delegation-decision-matrix
description: "Decide whether to do work yourself, delegate to another digital employee, or escalate to a human, using a small fixed matrix instead of ad hoc judgment."
---

# Delegation decision matrix

Leadership-role agents (SCRUM Master, Project Manager, Multi-Agent Orchestrator, shadow leadership) constantly choose between three actions for incoming work: do it, delegate it, escalate it. Use this matrix to make that choice consistent.

## The 2x2 (urgency × my-fit)

|              | High urgency                                   | Low urgency                                                |
|--------------|-------------------------------------------------|------------------------------------------------------------|
| My fit high  | Do it yourself now.                             | Do it yourself when slot opens, OR delegate if growing another agent's range is the goal.|
| My fit low   | Delegate immediately to the best-fit agent, OR escalate to a human if no fit exists. | Delegate; add a `production-validation` step before close.|

## Definitions

- **Urgency.** Use the user's stated deadline, the planning task SLA, or a hard external dependency. If none exist, urgency is "low".
- **Fit.** You have the tools, the skills, and current context to finish the task in 1 sitting.
- **Escalate to human.** Always required when: (a) policy or compliance decision; (b) money is involved beyond a pre-approved budget; (c) the action is irreversible and unguarded.

## The delegation call

When you decide to delegate:

1. Call `agent_directory_list` to confirm fit and availability.
2. Use `auto-assign-tasks` (when enabled) via `planning_tasks_bulk_assign`, OR `dispatch_task` if you are spawning a runtime task.
3. Open a handoff packet under `agent-handoff-protocol` so the delegate has full context.

## Anti-patterns

- Delegating high-urgency, my-fit-high work because you don't feel like doing it.
- Doing low-urgency, my-fit-low work yourself because delegation feels rude.
- Delegating without a handoff packet.
