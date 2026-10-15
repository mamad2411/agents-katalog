---
name: orchestrate-tasks
description: "Fan large tasks across parallel agents with planner/worker/verifier roles and structured handoffs. Trigger: 'parallelize', 'fan out', 'orchestrate', or when plan-slice produces 3+ independent slices."
when_to_use: "Activate ONLY when a task is too large for a single agent and has independent parallelizable slices. Do NOT use for single-agent tasks."
argument-hint: "[goal or slice plan to orchestrate]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: orchestration
  ck_mcp_tools: [ck_route, ck_delegate, ck_budget, ck_review_submit, ck_finding, ck_git_diff, ck_memory_record, ck_rollback]
  related_skills: [plan-slice]
---

# Orchestrate Tasks

Fan large tasks across parallel agents with planner/worker/verifier roles. Adapted from Cursor's orchestrate plugin for CK governance.

## Do NOT use when
- Single-agent task (just use `controlkeel-governance`)
- Task has no parallelizable slices
- Budget is tight (orchestration is expensive — multiple delegations)

## Principles

1. **Planners own scope, not code** — decompose, publish tasks, read handoffs, decide next. No file edits.
2. **Workers are isolated** — one task, one agent, one scope. Talk up through handoffs only.
3. **Verifiers check independently** — read worker output, verify against acceptance criteria.
4. **State on disk** — `ck_memory_record` and git, no long-running agent state.
5. **Continuous convergence** — each cycle produces progress. No progress → escalate.

## Workflow

1. Check `ck_budget` — orchestration costs multiple delegations. Stop if insufficient.
2. Decompose into tasks (or use existing `plan-slice` output). Each task: name, type (worker/verifier/subplanner), scoped goal, acceptance criteria, dependencies, paths.
3. Record plan via `ck_memory_record` (type: `decision`, tags: `orchestration-plan`).
4. Submit plan via `ck_review_submit` (review_type: `plan`). **Wait for approval** before spawning.
5. Execute loop:
   - Select ready tasks (dependencies satisfied, not started)
   - Check budget before each delegation
   - Delegate: `ck_route` → `ck_delegate`
   - Collect handoffs
   - Verify completed tasks
   - `ck_rollback` checkpoint after each success
   - Decide: new tasks, retry failures, or completion
6. Synthesize: `ck_git_diff` for total change, `parallel-review` if large.

## Failure recovery

- Worker failure → record `ck_finding`, retry once, escalate if retry fails
- Budget exhaustion → checkpoint state, stop, record for resumption
- Verifier failure → worker output not trusted, fix or escalate

## Output

- Approved orchestration plan
- Delegated tasks with handoffs
- `ck_finding` for failures
- `ck_rollback` checkpoints
- Synthesized result

## Reference

- [Handoff format](references/handoff-format.md)
