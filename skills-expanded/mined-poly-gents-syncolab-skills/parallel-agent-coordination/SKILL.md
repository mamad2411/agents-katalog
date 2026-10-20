---
name: parallel-agent-coordination
description: "Spin up multiple sub-agents in parallel for independent sub-tasks while keeping a clear coordinator that aggregates results, breaks ties, and surfaces partial failures back to the user."
---

# Parallel agent coordination

Use this skill when you, as a coordinator role (Multi-Agent Orchestrator, SCRUM Master, Project Manager, or a shadow leadership role), have a piece of work that decomposes into **independent** sub-tasks that can safely run side by side.

Independence is the gate. If two sub-tasks read or write the same file, code path, data row, ticket, or external system, run them sequentially or hand them off — do not parallelize.

## When to use

- Multi-repo scan or audit (each repo is independent).
- Multiple unrelated bug investigations.
- Research + drafting + asset prep for the same launch where each output is consumed by you, not by a peer agent.
- Bulk planning ops where each task lives in a different room or owner.

## When NOT to use

- Anything that mutates shared state (codebase, single document, single Jira board with linked tasks).
- The user explicitly wanted a single chain-of-thought author for the work.
- One sub-task's output is the input to another — use `crew-planner-executor` or `agent-handoff-protocol` instead.

## The loop

1. **Decompose.** Apply `task-decomposition-tree`. Mark each leaf as `independent` or `dependent`. Only `independent` leaves are eligible for parallel execution.
2. **Dispatch.** For each parallel leaf, call `dispatch_task` (or `planning_tasks_bulk_assign` if the targets are clocked-in digital employees) with a tight scope statement, an explicit `do_not_touch` list (paths/rows/tickets you reserve for yourself or another leaf), and a deadline.
3. **Track.** Open `planning_overview` to monitor liveness. Each sub-agent should follow `agent-status-pings` to emit progress signals at least every 5 minutes.
4. **Aggregate.** When all leaves complete, you (the coordinator) read each result, resolve overlaps or conflicts, and produce a single consolidated response or commit.
5. **On partial failure.** If one leaf fails or stalls past its deadline, do NOT cancel the healthy leaves. Record the failed leaf as a planning issue via `report_incident` (when relevant), and either retry that leaf with a smaller scope or sequentially absorb its work yourself.

## Anti-patterns

- Fan-out without a coordinator (each agent posts a separate user-facing reply).
- Parallelizing dependent leaves and racing for the same write.
- Cancelling the whole batch when one leaf fails.
