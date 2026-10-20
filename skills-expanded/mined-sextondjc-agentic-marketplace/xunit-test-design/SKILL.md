---
name: xunit-test-design
description: Use when designing expert-level xUnit tests with deterministic Fact/Theory selection, data strategy, assertion quality, and boundary coverage.
---

# xUnit Test Design

## Specialization

Use this skill to design maintainable, deterministic, and behavior-focused xUnit tests that scale across projects.

This skill is specialized for test-case design. It does not implement production code.

## Objective

Produce a deterministic xUnit test design package that defines test shapes, data strategy, coverage intent, and assertion standards for a target behavior slice.

## Trigger Conditions

- New tests are needed for a feature, fix, or regression boundary.
- Existing xUnit tests are brittle, unclear, or redundant.
- Teams need consistent cross-project test design standards.

## Scope Boundaries

In scope:

- Fact vs Theory selection.
- Data strategy (`InlineData`, `MemberData`, `ClassData`) decisions.
- Coverage-intent planning for success, failure, and boundary behavior.
- Assertion clarity and determinism checks.

Out of scope:

- Integration test infrastructure provisioning.
- UI or end-to-end workflow automation.
- Non-xUnit framework migration work.

## Inputs

- Target behavior contracts and failure modes.
- Risk profile and defect history for the target slice.
- Data constraints and boundary conditions.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Test shape matrix mapping behavior to `Fact` or `Theory`.
- Data-source strategy map with rationale.
- Coverage-intent matrix across success, failure, and boundary paths.
- Assertion standards checklist.
- Final design recommendation with residual risks.

## Deterministic Workflow

1. Enumerate behavior contracts and failure modes.
2. Choose `Fact` or `Theory` per behavior with one explicit rationale.
3. Select data source strategy based on readability, reuse, and stability needs.
4. Map coverage expectations for happy path, failure path, and boundaries.
5. Define assertion strategy for precision and maintainability.
6. Identify anti-pattern risks and mitigation actions.
7. Publish one design recommendation with unresolved risks.

## Decision Rules

- Use `Fact` when one deterministic scenario validates behavior.
- Use `Theory` when behavior must hold across multiple parameter sets.
- Prefer `InlineData` for compact scalar cases.
- Prefer `MemberData` or `ClassData` for reusable, complex, or generated cases.

## Anti-Pattern Checks

- Test names that describe implementation instead of behavior.
- Overloaded theories with unrelated assertions.
- Assertion bundles that hide the failing intent.
- Data sources with unstable ordering or implicit side effects.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert test-shape decisions | Deterministic Workflow + Decision Rules |
| Deterministic data strategy | Decision Rules |
| Behavior-first coverage planning | Required Outputs |
| Cross-project reusability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Clear behavior contracts produce clearer test design.
- Deterministic data and assertions reduce long-term flakiness.

Trade-offs:

- Highly parameterized tests reduce duplication but can reduce readability.
- Narrow tests improve diagnostics but increase test count.

Open blockers:

- Missing boundary definitions can lead to false confidence.
- Unclear domain invariants can produce low-signal assertions.

Recommendation:

- Start with behavior-focused, minimal tests and expand data-driven coverage only where risk or variability justifies it.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when each target behavior has one explicit test-shape decision, one data strategy decision, and one assertion expectation.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Decision logic is explicit.
- Source catalog is current for this evaluation cycle.
