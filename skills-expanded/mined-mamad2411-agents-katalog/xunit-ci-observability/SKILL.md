---
name: xunit-ci-observability
description: Use when xUnit pipelines need deterministic evidence capture, flaky-test classification, failure triage ownership, and gate-ready reporting.
---

# xUnit CI Observability

## Specialization

Use this skill to standardize xUnit test evidence and triage outputs in CI so gate decisions are auditable and repeatable.

This skill is specialized for CI test observability and remediation ownership.

## Objective

Produce one deterministic CI evidence contract covering test results, flaky classification, failure ownership, and gate decision outputs.

## Trigger Conditions

- CI test failures are hard to triage or repeatedly unresolved.
- Test evidence artifacts are inconsistent across pipelines.
- Quality gates need explicit pass/fail evidence contracts.

## Scope Boundaries

In scope:

- Test result artifact contract.
- Failure taxonomy and flaky classification policy.
- Triage ownership mapping and escalation rules.
- Gate report outputs for release decisions.

Out of scope:

- Production observability architecture.
- Performance benchmarking workflows.
- Test framework migration implementation.

## Inputs

- CI pipeline topology and test stages.
- Existing artifact formats and retention behavior.
- Failure history and flaky-test signals.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- CI evidence contract (artifacts, schema, retention).
- Failure taxonomy and flaky classification table.
- Triage owner mapping and SLA expectations.
- Gate report template with pass/fail recommendation.
- Final recommendation with unresolved risks.

## Deterministic Workflow

1. Inventory current xUnit CI artifacts and failure signals.
2. Define required evidence artifacts and retention rules.
3. Define deterministic failure taxonomy and flaky classification thresholds.
4. Map failure classes to owners and escalation windows.
5. Define gate-ready report structure and decision criteria.
6. Publish one recommendation with unresolved observability gaps.

## Decision Rules

- Every failing run must emit a durable, parseable result artifact.
- Flaky classification requires explicit criteria, not ad hoc judgment.
- Gate outcomes must cite artifact evidence and named owner dispositions.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert CI evidence posture | Deterministic Workflow |
| Deterministic triage and ownership | Required Outputs |
| Gate-ready reporting | Decision Rules + Required Outputs |
| Cross-project portability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Repeated CI instability is often an evidence and ownership problem, not only a test-authoring problem.
- Durable artifacts enable fast and consistent release decisions.

Trade-offs:

- Richer evidence increases storage and pipeline overhead.
- Lighter evidence improves speed but weakens triage quality.

Open blockers:

- Missing historical run data may reduce initial flaky classification accuracy.
- Incomplete ownership maps can delay remediation.

Recommendation:

- Adopt a minimal-but-strict artifact schema with deterministic failure classes and explicit triage ownership.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Gate artifact template is provided in [ci-test-evidence-template.md](./references/ci-test-evidence-template.md).

## Pragmatic Stop Rule

Stop when artifact contracts, failure classes, and ownership mappings are explicit and gate reports are reproducible.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Evidence and ownership rules are explicit.
- Source catalog is current for this evaluation cycle.
