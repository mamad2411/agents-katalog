---
name: multi-subagent-execution
description: 'Execution protocol for launching multiple subagents in sequential or parallel modes with conflict checks, merge strategy, and completion reporting.'
---

# Multi Subagent Execution

Operational guidance for running multiple subagents from the orchestrator.

## When To Use This Skill

- Request contains two or more specialist tasks.
- User explicitly asks for concurrent or parallel execution.
- Workflow needs consolidated outcomes from multiple specialists.

## Execution Protocol

1. Build task graph with dependencies.
2. Mark each task as `sequential` or `parallel-candidate`.
3. Run conflict check for parallel candidates:
   - file overlap risk
   - shared environment mutation risk
   - ordering dependency risk
4. Propose execution plan and request approval.
5. Launch subagent tasks according to approved plan.
6. Collect results and normalize to common schema.
7. Merge results and report unresolved conflicts.

## Result Schema

Each subagent result should return:

- CorrelationId
- TaskId
- TargetAgent
- Status (`completed`, `blocked`, `failed`)
- Outputs
- Evidence
- Risks
- FollowUps

## Merge Rules

- Prefer deterministic outputs over inferred summaries.
- If two outputs conflict, report both and ask for user decision.
- Never hide failed subagent results.

## Safety Rules

- Do not run parallel steps that edit the same files.
- Do not auto-resolve semantic conflicts between parallel outputs.
- Always include per-subagent status in final summary.
