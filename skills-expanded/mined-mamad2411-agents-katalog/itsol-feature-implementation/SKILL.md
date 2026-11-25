---
name: itsol-feature-implementation
description: "Implement authorized ITSOL features or refactors with proportionate verification and review."
---
# ITSOL Feature Implementation

Validate `itsol-workflow-mode` before production changes and preserve all seven fields.

## Authorization and loop

- `governed`: specific Business and Technical Plans must be user-approved with `artifact_state: approved`;
- `autonomous-planned`: reviewed plans must be `ready-for-execution`, never user-approved by implication;
- `direct`: use `artifact_state: not-required` and require no plan, approval, Decision Gate, or execution-mode artifact.

Reject missing, inconsistent, or restriction-conflicting state. Apply `.itsol.md`, inspect existing patterns, and map permissions, data/contracts, cache/events/jobs, deployment, and rollback impact. Implement the smallest coherent change, use the router's risk-proportionate verification contract, and finish with `itsol-self-review`. TDD is optional only on explicit user request; do not require a failing test, RED/GREEN evidence, or a TDD exception before editing. Use `itsol-subagent-workflow` only when the resolved `execution_mode` requires it.

Load `itsol-execution-policy` when resource, stop, delegation, or completion state matters. It owns budgets/evidence; never use `maxTurns` or termination as completion. Preserve `partial`, `blocked`, and `failed`.

## Focused references

- [01-overview.md](./references/01-overview.md) — feature process and plan implementation.
- [02-praca-nad-nowa-funkcjonalnoscia.md](./references/02-praca-nad-nowa-funkcjonalnoscia.md) — new-feature workflow.
- [03-pytania-do-gumowej-kaczki-przy-nowej-funkcjonalnosci.md](./references/03-pytania-do-gumowej-kaczki-przy-nowej-funkcjonalnosci.md) — material questions and checklist.
- [04-proces-myslowy-przyklad-nowej-funkcjonalnosci.md](./references/04-proces-myslowy-przyklad-nowej-funkcjonalnosci.md) — worked example and edge cases.
- [05-nawyki-dobrego-dewelopera.md](./references/05-nawyki-dobrego-dewelopera.md) — completion and verification habits.
