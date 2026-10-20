---
name: xunit-traits-and-selection
description: Use when xUnit suites need deterministic trait taxonomy, selective execution strategy, and release-scope test slicing across local and CI runs.
---

# xUnit Traits and Selection

## Specialization

Use this skill to define a stable trait taxonomy and selective execution policy for large xUnit suites.

This skill is specialized for test suite segmentation and execution targeting.

## Objective

Produce one deterministic traits-and-selection contract that defines trait taxonomy, filtering strategy, and release-scope execution slices.

## Trigger Conditions

- Test suites are too large for every-run execution.
- Trait usage is inconsistent or ambiguous across projects.
- CI requires deterministic selective runs for faster feedback.

## Scope Boundaries

In scope:

- Trait taxonomy and naming standards.
- Local and CI filter strategy.
- Mandatory slices for PR, nightly, and release gates.
- Trait drift controls and ownership rules.

Out of scope:

- Runtime performance optimization implementation.
- Product-level test case authoring.
- Non-xUnit trait systems.

## Inputs

- Existing trait usage and command filters.
- Pipeline stages and latency targets.
- Risk policy for release-bound behavior.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Trait taxonomy specification.
- Selection matrix by pipeline stage.
- Command/filter examples for local and CI usage.
- Drift and governance checks for trait changes.
- Final recommendation with residual risk notes.

## Deterministic Workflow

1. Inventory current trait keys, values, and usage patterns.
2. Define canonical taxonomy and deprecate ambiguous variants.
3. Define execution slices for PR, nightly, and release contexts.
4. Define deterministic filter commands per execution context.
5. Define drift controls, ownership, and exception handling.
6. Publish one recommendation and unresolved classification risks.

## Decision Rules

- One canonical taxonomy per repository; aliases must be transitional and time-bounded.
- Every pipeline stage must map to explicit required trait slices.
- Fail closed when release-critical slices are omitted from release gates.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert trait taxonomy | Deterministic Workflow |
| Deterministic selective execution | Required Outputs |
| Release-safe suite slicing | Decision Rules + Required Outputs |
| Cross-project portability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Predictable slicing depends on stable taxonomy and filter contracts.
- Trait drift is a governance issue that causes silent coverage gaps.

Trade-offs:

- Coarse slices simplify operations but reduce targeting precision.
- Fine-grained slices improve speed but increase taxonomy overhead.

Open blockers:

- Legacy inconsistent tags can delay clean cutover.
- Missing ownership for taxonomy updates can reintroduce drift.

Recommendation:

- Establish one canonical taxonomy with explicit stage slices and drift controls before optimizing slice granularity.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Taxonomy template is provided in [traits-taxonomy-template.md](./references/traits-taxonomy-template.md).

## Pragmatic Stop Rule

Stop when canonical taxonomy, stage slices, and filter commands are explicit and drift checks are assigned.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Taxonomy and slice rules are explicit.
- Source catalog is current for this evaluation cycle.
