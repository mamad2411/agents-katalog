---
name: orchestrator-master
description: Coordinate multi-agent work with pi-agent-orchestrator. Use for complex tasks that benefit from parallel research, explicit handoffs, swarm coordination, independent review, or quota-aware execution. Do not use for small linear tasks that one agent can complete directly.
---

# Orchestrator Master

Use the smallest execution topology that can complete the task reliably.

## Decide the topology

- Use one agent for narrow, linear work with one clear output.
- Use parallel agents only for independent lanes with no overlapping writes.
- Use a structured crew for planner, implementer, and reviewer responsibilities.
- Use a swarm when membership must change dynamically or multiple related discoveries must be consolidated continuously.
- Prefer `smart` join mode unless deterministic group completion or immediate asynchronous delivery is required.

## Plan before spawning

1. Read current session limits and active fleet state.
2. Split the task into outputs with explicit ownership.
3. Mark each lane as read-only or write-capable.
4. Prevent multiple agents from editing the same files or resources.
5. Assign the lowest sufficient thinking level.
6. Define acceptance evidence before execution.

## Thinking levels

- `low`: formatting, mechanical edits, bounded lookups.
- `medium`: normal implementation, tests, routine debugging.
- `high`: architecture, ambiguous root-cause analysis, risky migrations, cross-system review.

Do not ask the user to choose a thinking level when the task itself makes the choice clear.

## Handoffs

A handoff must state:

- objective and current status;
- files, systems, or evidence inspected;
- decisions already made and their rationale;
- exact remaining work;
- blockers, risks, and validation commands;
- whether the next agent may write and which scope it owns.

Never hand off hidden assumptions as facts.

## Parallel and swarm safety

- Partition writes by file, module, branch, or external resource.
- Keep shared-state mutations in one coordinator lane.
- Consolidate findings before spawning follow-up implementers.
- Stop duplicate or stale lanes instead of letting them race.
- Respect quotas, circuit breakers, concurrency, spawn, and turn limits.

## Evaluation loop

After each wave:

1. Verify outputs against the acceptance evidence.
2. Reconcile contradictions using source-grounded facts.
3. Run focused tests or checks for changed scope.
4. Spawn follow-up work only for unresolved defects.
5. Close completed lanes and summarize residual risk.

## Failure handling

- Retry only transient failures.
- For structural failures, change the plan, model, scope, or isolation strategy.
- Do not multiply agents to compensate for a broken dependency or unavailable CI system.
- Report infrastructure-level validation gaps separately from code-level failures.
