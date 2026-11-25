---
name: plan-implementation
description: Create the minimum execution contract needed to implement accepted product intent.
---

# Plan implementation

Use this skill when the user explicitly requests operational planning or re-planning.

Do not invoke this skill merely because implementation needs a lightweight internal plan.

## Start

- Read every file in `docs/concept/`.
- Inspect the existing implementation.
- Inspect the existing execution contract.
- Inspect the latest verified state.
- Require accepted concept intent.
- Identify unresolved product decisions.
- Return unresolved product decisions to the user.
- Resolve reversible technical choices during planning.
- Preserve accepted implementation evidence during re-planning.
- Preserve completed history during re-planning.
- Change only the approved planning scope.

## Plan by objective

- Define objectives as observable product outcomes.
- Prefer a complete vertical feature over technical-layer phases.
- Include every required product layer in the objective.
- Include the natural-entry playtest path in an interaction objective.
- Define the completion condition for each objective.
- Define the required validation boundary for each objective.
- Record material dependencies between objectives.
- Avoid prescribing the number of agents.
- Avoid prescribing the execution order when dependencies do not require one.
- Avoid creating implementation packets for minor mechanical steps.
- Let the Leader decompose an approved objective during execution.

## Execution contract

- Keep Project Specifics limited to stable repository rules.
- Record exact supported commands in Project Specifics.
- Record required validation gates in Project Specifics.
- Record material architecture boundaries in Project Specifics.
- Record material security boundaries in Project Specifics.
- Record material external-operation gates in Project Specifics.
- Avoid copying product intent into Project Specifics.
- Avoid copying the execution plan into Project Specifics.

## State

- Create `BUILD_STATE.md` when implementation needs durable continuity.
- Keep `BUILD_STATE.md` focused on current verified truth.
- Record one current objective in `BUILD_STATE.md`.
- Record one next meaningful action in `BUILD_STATE.md`.
- Record active ownership in `BUILD_STATE.md`.
- Record material decisions in `BUILD_STATE.md`.
- Keep completed detail in git history.
- Avoid turning `BUILD_STATE.md` into a task transcript.

## Conditional artefacts

- Create `EXPERIENCE.md` only when cross-feature interaction behaviour needs a durable contract.
- Keep journey mechanics out of `EXPERIENCE.md` when tests express them clearly.
- Create `DESIGN.md` only when presentation direction needs a durable contract.
- Include component-selection guidance in `DESIGN.md` for interface products.
- Include representative component patterns in `DESIGN.md` for interface products.
- Create `GOVERNANCE.md` only when the user approves a named delivery claim.
- Create `ROADMAP.md` only when multiple objectives have material dependencies.
- Keep live worker assignments out of `ROADMAP.md`.
- Keep completed execution logs out of `ROADMAP.md`.
- Omit every conditional artefact that does not earn a distinct responsibility.

## Readiness

- Verify every declared command against the repository.
- Verify every objective has an observable completion condition.
- Verify every objective has a validation boundary.
- Verify every interaction objective has a natural-entry playtest path.
- Verify every unresolved external dependency is explicit.
- Verify `BUILD_STATE.md` identifies the current objective.
- Verify `BUILD_STATE.md` identifies the next meaningful action.
- Verify conditional artefacts do not duplicate one another.
- Verify the execution contract does not prescribe runtime orchestration choices.

## Delivery

- Show the user the resulting execution contract.
- Show the user the resulting objective plan.
- Report every omitted conditional artefact.
- Report every unresolved product decision.
- Report the exact repository status.
- Continue into implementation when the approved objective includes implementation.
- Stop before implementation when the user requested planning only.
- Avoid creating a separate kickoff prompt.

## Boundaries

- Avoid product code during planning-only work.
- Avoid dependency installation during planning-only work.
- Avoid deployment during planning.
- Avoid committing planning-only work without approval.
- Avoid changing accepted product intent.
- Use `shape-concept` when accepted product intent must change.
