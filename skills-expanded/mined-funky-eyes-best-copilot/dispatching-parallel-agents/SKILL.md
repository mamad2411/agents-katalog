---
name: dispatching-parallel-agents
description: "Use when multiple frozen subtasks have non-overlapping write sets and can be implemented or reviewed in parallel."
---

# Dispatching Parallel Agents

## Preconditions

- Each subtask has goal, files, dependencies, material assumptions or explicit unknowns, acceptance checks, and verification.
- Write sets do not overlap.
- Shared foundation work is already done or assigned as a dependency.
- Fan-in owner is identified.

## Fan-out Packet

Each parallel subtask uses the six-block PM dispatch packet from `core-workflow-contract`. At minimum include:

- `task_intent`: `goal`, `task_type`, `work_mode`
- `frozen_scope`: `files_involved`, `write_set`, `dependencies`, `owner_lane`, `reviewer_lanes`, `review_package_ref`, `diff_ref`
- `execution_contract`: `assumptions`, `tradeoffs`, `simpler_option_considered`, `constraints`, `acceptance_checks`, `verification_budget`, `model_policy`, `model_cost_boundary`, `cost_boundary`, `reviewer_input_boundary`, `reviewer_permission_boundary`, `forbidden_approaches`, `read_before_write_targets` when code edits are planned
- `output_contract`: required skills, `required_artifacts`

Add `sub_task_id` for fan-in tracking.

## Model, Permission, And Token Boundaries

- Every parallel dispatch records the intended `owner_lane`, `reviewer_lane`, `permission_mode`, `write_set`, `review_package_ref` or `diff_ref`, `model_policy`, and `model_cost_boundary`.
- When the runtime supports subagent model selection, choose the cheapest adequate explicit model/tier for each lane instead of inheriting the current session default. If model selection is not enforceable, state that in `model_policy` and `model_cost_boundary.enforcement`.
- Batch fan-out that uses many reviewers, high-tier models, or repeated large context requires PM-visible cost acknowledgement or a cheaper explicit model/context strategy before dispatch.
- Review-only lanes use read-only permission mode and must not run mutating git/workspace commands. Reclassify to fix/implementation before allowing edits.
- Shared diffs, specs, logs, and review packages should be referenced once and reused by path or shard, not pasted into every subagent prompt.

## Fan-in

Adjudicate fan-in using the priority order from `core-workflow-contract` Fan-In Arbitration. Accept only structured handbacks with the required fields. Merge results by dependency order. Re-run integration verification after combining parallel work.
