---
name: dotnet-refactor
description: Use when modernizing .NET code with this priority order: preserve requested behavior, keep changes small and verifiable, then apply measurable improvements such as nullable adoption and obsolete API cleanup.
---

# .NET Modernization Skill

## Specialization

This skill is specialized for the workflow described in this file and should remain narrowly bounded to that responsibility.

It should not absorb adjacent planning, execution, or review responsibilities that belong to other assets.

## Scope

Apply focused cleanup and modernization passes that improve maintainability and safety without introducing unnecessary architectural layers.

## Rules

- Priority order for tradeoffs: preserve requested behavior first, then correctness and safety, then smallest verifiable change, then measurable modernization gain.
- Preserve behavior unless the user request includes an approved behavior-change requirement.
- Keep changes small and verifiable.
- Prefer measurable improvements over stylistic churn.
- Add or adjust tests when public behavior or public contracts change.

## Typical Tasks

- Remove obsolete patterns and APIs.
- Correct async and cancellation usage.
- Improve nullability annotations.
- Reduce warnings and analyzer findings.
- Replace legacy syntax with modern, readable C# where supported by the target framework.

## Modernization Workflow

1. Inventory the legacy construct or smell being targeted.
2. Confirm the change is behavior-preserving unless the user request includes an approved behavior change.
3. Prefer automated or mechanical refactors in small batches.
4. Re-run tests and compare warnings, analyzer output, or benchmark evidence as appropriate.
5. Escalate to ADR or architecture review when the change stops being purely local modernization.

## Evidence Gates

- Do not introduce `ValueTask`, `Span<T>`, pooling, or similar performance-sensitive changes without measurement.
- Keep before/after evidence when the change claims performance, warning reduction, or modernization benefit.
- If a refactor touches public behavior, tests must prove the preserved contract.

## Trigger Conditions

Invoke this skill when any of the following is true:

- The user wants safe, behavior-preserving .NET modernization work.
- Nullable cleanup, obsolete API removal, or similar refactoring is required.
- A focused modernization pass is needed without broader redesign.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- Code and/or configuration changes that are limited to the requested modernization scope.
- Validation evidence appropriate to the change type (for example tests, warning deltas, analyzer output, or benchmark evidence).
- A short summary of what changed and why the change is behavior-preserving (or explicitly approved as behavior-changing).

## Workflow

1. Gather required context and constraints from the workspace and user request.
2. Execute modernization steps in small, reviewable batches.
3. Produce required outputs and evidence for the applied changes.
4. Validate completeness and consistency with active workspace instructions.

