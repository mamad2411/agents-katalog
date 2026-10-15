---
name: implement-wrapper
description: Schedule approved plans into dependency-safe, single-slot subagent executions with handoff and conflict routing.
---

# implement-wrapper

Use `implement-wrapper` for approved multi-plan tickets. Wrapper schedules and routes; `implement` subagents implement, verify, review, commit, and update status.

## Schedule

- Read `docs/plans/plans.md` backlinks and each plan's approval, status, dependencies, and shared resources.
- Read `.codex/harness.yaml` first. A `Planned` GitHub Project item or `planned` local ticket with no incomplete blockers is a candidate; dependencies wait for completion in the selected tracker.
- Shared resource conflict or uncertainty means sequential execution; independent plans spawn in parallel.
- Give each plan one execution slot. A slot limits concurrent work; it does not reserve an agent identity or permit an agent to execute another plan. Return `ready_plans`, `waiting_plans`, `parallel_groups`, `single_slot_plan_ids`, and reasons.
- Start every plan ticket with a newly spawned `implement` subagent whose execution context contains no prior plan work. Never reuse a completed, handed-off, or blocked plan's subagent for the next plan.
- Before dispatch, assess whether the plan's next bounded implementation action fits inside the Context Smart Zone: enough remaining context to reload the plan/specs/checkpoint, implement or resolve one code blocker, and run its focused verification. If it does not fit, checkpoint and start a fresh subagent for the same plan.
- Prompt each subagent with repository, exact plan path, `docs/plans/plans.md` backlink, `docs/specs/product-spec.md`, `docs/specs/architecture-spec.md`, `.codex/skills/implement/SKILL.md`, checkpoint, dependency/resource facts, Smart Zone assessment, and exactly one plan/strict scope. Do not implement checkpoint, conflict, or reconciliation in this slice.

## Handoff

Use `docs/plans/.runtime/<plan-id>/checkpoint.md`; it is gitignored and does not replace the official plan status. Include it in every prompt.

```yaml
plan_id: <plan-id>
orchestration_state: running | handoff-required | conflict-paused | priority-routed
attempt: <integer>
last_completed_step: <text>
changed_files: []
tests: <evidence>
blocker: <kind, summary, unblock_condition>
smart_zone: <dispatch | before-next-action | after-action; fits | handoff-required; evidence>
next_action: <text>
handoff_reason: context-threshold | plan-boundary | milestone | retry
updated_at: <timestamp>
```

Before a subagent starts, assess the Context Smart Zone. After every material action, assess the Context Smart Zone again, including after a test failure, code-blocker attempt, milestone, and completion. If the next action would cross the zone, write a checkpoint with `handoff_reason: context-threshold`, stop that agent, and start a new empty-context subagent for the same `in-progress` plan. A handoff resumes the same plan only through that new subagent; the single plan slot resumes as `in-progress`. Read checkpoint, plan, specs, and Git/test state. Actual state is the source of truth; correct the checkpoint.

At every plan boundary, checkpoint the completed plan and dispatch the next eligible plan only to a new empty-context subagent, even when the previous agent has remaining context. Record `handoff_reason: plan-boundary`; a plan boundary is never a reason to continue with the previous agent.

## Conflict / blocker

- Record conflict evidence and affected plan ids in each related plan's checkpoint; stops the related execution slots as `conflict-paused`.
- The wrapper does not automatically merge. Conflict-paused plans cannot resume before the main session makes an explicit priority decision; it selects exactly one affected plan to resume first and remaining plans are re-evaluated.
- Report blocker kind, summary, and exact unblock condition. The implementing subagent owns code blocker resolution inside the Context Smart Zone: diagnose, make the bounded fix, and run focused verification in the active plan slot. A code blocker that would exceed the zone is checkpointed and handed to a new empty-context subagent for the same plan; it is not made official `blocked` merely for a context limit. An external environment, authority, dependency, or decision blocker is official `blocked`.

Canonical ticket statuses are `Planned`, `In Progress`, `Blocked`, `Done` in GitHub Project mode and `planned`, `in-progress`, `blocked`, `completed` in local-markdown mode. Keep `conflict-paused` and `priority-routed` as orchestration states, never tracker status.

## Completion

Delegate completion to `implement`; unresolved review or unresolved blocker must not become `completed`. The wrapper must not edit implementation code or change the official plan status.

After completion, `implement` recalculates dependent tickets only in the selected tracker. An incomplete or unresolved ticket remains waiting. Do not copy status into a second tracker or use triage labels for execution state. Report at least one executable ticket or that the entire graph is blocked.

Do not auto-merge or auto-prioritize. `ui ~ entity` E2E cannot run: missing runtime is an environment blocker; unblock condition is a provisioned UI/entity runtime and backing service. Contract tests are the executable verification.
