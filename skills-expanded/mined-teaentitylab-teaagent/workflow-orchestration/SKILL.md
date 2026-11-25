---
name: workflow-orchestration
description: Execute a multi-step workflow plan with per-step validation, self-correction, and undo journaling. Documents the deterministic orchestration owned by the harness.
---

# Workflow Orchestration

Reviewed procedure asset for `teaagent.domain.workflow_engine` (ADR-0041
Phase 2). Workflow orchestration is **governance-adjacent** — it owns step
sequencing, validation gates, the `UndoJournal`, and audit wiring — so it
remains in the harness per ADR-0041 ("harness retains `UndoJournal` / audit
wiring only"). This skill documents the procedure as a reviewed asset.

## Procedure

1. **Plan in:** accept a `WorkflowPlan` (from task-classification) of ordered
   `WorkflowStep`s with agents, tools, and dependencies.
2. **Per step:** execute, then validate against the step's validation profile
   (`fast` / `standard` / `strict`).
3. **Self-correct:** on validation failure, generate a correction prompt and
   re-attempt within the step's retry budget.
4. **Journal:** record each write through the `UndoJournal` so the run is
   reversible; emit audit events for every step transition.
5. **Finalize:** report per-step `StepExecution` / `ValidationResult` outcomes.

## Contract

The deterministic engine in `teaagent.domain.workflow_engine` is the source of
truth; the LLM prompt assets it depends on for agent authoring live in the
`agent-prompt-authoring` skill. Undo/audit wiring is a harness responsibility and
is not delegated to a skill.
