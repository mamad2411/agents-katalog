---
name: dev-flow-planning
description: Use when dev-flow work needs OpenSpec/opsx artifacts and tasks, inline task dependencies, combined planning review, Git assumptions, or an executable verification plan before execution.
---

# dev-flow-planning

Own phase planning before execution. Prepare OpenSpec/opsx with its canonical task artifact, then run one combined planning checker before one Phase Planning Gate. All user-facing replies and persisted Markdown artifacts are written in Chinese.

## Boundary

This skill prepares phase artifacts and plans. It does not implement tasks or make runtime decisions.

## Core Contract

- An explicit request to implement, change, or build authorizes creation of necessary planning artifacts. Ask the user only for genuinely blocking decisions; record non-blocking assumptions and continue.
- Persist dev-flow-state.md beside planning artifacts. Chat memory is not evidence.
- All implementation work requires OpenSpec/opsx artifacts.
- The active OpenSpec task artifact is the only implementation task source. Give every task a stable native ID; add `Depends on: <task-id>` only to tasks with dependencies. Do not create a second task list or separate coordinated test matrix.
- Execute tasks with one writer at a time in stable OpenSpec order, skipping tasks whose dependencies are not yet settled. Phase-level parallelism belongs only to the Loop Phase DAG and Loop Start Gate.
- After OpenSpec artifacts and Git/writer assumptions are ready, use one combined planning checker over them. It checks task coverage, dependency references and cycles, verification intent, feasibility, the Phase's planned write scope, writer safety, and applicable system coverage. Apply the shared bounded-convergence policy from dev-flow-master/references/state-and-gates.md and its max_checker_evaluations budget across this single checkpoint.
- Present one Phase Planning Gate. Loop-authorized work may reuse envelope approval instead of asking again, but the combined checker still runs.
- Keep the confirmed Loop baseline intact; create only phase-level OpenSpec/opsx artifacts and normal dev-flow state.

## References

- Read references/phase-1-documents.md for OpenSpec/opsx preparation and openspec_artifact_ready.
- Read references/openspec-tasks.md for the canonical task format, inline dependencies, runtime scheduling, combined review, and phase_plan_ready.

## Required Signals

- openspec_artifact_ready: artifact readiness and paths, without a checker score.
- phase_plan_ready: OpenSpec task source, task count, planned write scope, planning_checker_score, findings, Git/writer assumptions, and gate readiness.

Persist planning evidence, assumptions, blockers, and the Phase Planning Gate decision in dev-flow-state.md.
