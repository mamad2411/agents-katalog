---
name: crew-manager-pattern
description: "Use the manager-worker pattern: a single manager agent decomposes, delegates, monitors, and aggregates while worker agents execute leaves — applied via your existing planning, assignment, and dispatch tools."
---

# Crew manager pattern

Adapted from CrewAI's manager pattern (`provenance:crewai`). Applies inside PolyGents' existing planning + agent-directory + dispatch tooling — no separate orchestration framework needed.

## When to use

- A planning task with 3+ independent leaves that each fit a known agent template (front-end, back-end, research, ops).
- A user request that arrives at the orchestrator and needs to be broken up and reassigned.
- A sprint where the manager role (SCRUM Master, Shadow Engineering Lead) is doing the distribution.

## The pattern

- **Manager** (you). Owns the user conversation, the planning task tree, and the final synthesis. Never personally edits the same artefacts the workers are editing.
- **Workers.** Each owns a single leaf or a tight set of leaves. They follow `agent-status-pings`, raise blockers via `agent-handoff-protocol` back to the manager, and run `agent-self-check` before declaring leaf done.

## The loop

1. **Decompose.** `task-decomposition-tree`. Each leaf gets an `owner_template` field naming which agent template should pick it up.
2. **Assign.** `agent_directory_list` → `planning_tasks_bulk_assign` with the chosen `digital_employee_id` per leaf.
3. **Brief.** For each worker, post an `agent-handoff-protocol` packet on the task description.
4. **Monitor.** Watch the planning overview + the workers' ping cadence. If a worker goes dark for > 1 cadence, ping or reassign.
5. **Aggregate.** When all leaves are done, the manager synthesizes the final user-facing answer and runs `agent-self-check` over the whole.
6. **Report.** One reply to the user, not N.

## Anti-patterns

- Manager also does worker leaves. Pick one role per turn.
- Workers reporting directly to the user without going through the manager.
- Decomposition that the manager never re-checks for drift.

## Tools

- `agent_directory_list`, `planning_tasks_bulk_assign`, `planning_overview`, `dispatch_task`, `agent-handoff-protocol`, `agent-status-pings`.
