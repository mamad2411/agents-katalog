---
name: xunit-quality-gate
description: Use when xUnit assets need an expert, evidence-first quality decision with deterministic findings, ownership, and pass-or-fail recommendation.
---

# xUnit Quality Gate

## Specialization

Use this skill to evaluate xUnit test assets and xUnit-focused skill outputs with deterministic quality checks and one explicit recommendation.

This skill is specialized for review and sign-off decisions, not implementation.

## Objective

Produce one deterministic xUnit quality verdict with severity-ranked findings, remediation ownership, and release recommendation.

## Trigger Conditions

- xUnit test changes are merge-bound or promotion-bound.
- xUnit skill outputs need acceptance review.
- Test regressions escaped and quality controls need reinforcement.

## Scope Boundaries

In scope:

- xUnit design quality and behavior coverage adequacy.
- Fixture lifecycle safety and parallelization readiness.
- Async/cancellation test adequacy.
- Moq collaboration-test quality and brittleness risk.
- Analyzer-rule alignment and deterministic execution checks.

Out of scope:

- Product feature implementation.
- Non-test operational release tasks.
- Performance benchmarking outside test-quality scope.

## Inputs

- Target xUnit artifacts and behavior contracts.
- Existing defects, flaky-test history, and risk classification.
- Required quality threshold policy.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Findings table with severity, impact, owner, and remediation.
- Coverage-intent adequacy summary.
- Determinism verdict for flake and nondeterministic risk.
- Final recommendation: pass, pass-with-conditions, or fail.

## Deterministic Workflow

1. Validate behavior coverage intent across success, failure, and boundary conditions.
2. Validate fixture lifecycle and shared-context safety posture.
3. Validate async and cancellation assertion adequacy.
4. Validate mock collaboration boundaries and interaction-verification quality.
5. Validate analyzer-rule and deterministic execution compliance.
6. Rank findings and assign owner/remediation for each.
7. Publish one explicit recommendation with residual risks.

## Decision Rules

- `pass`: no unresolved critical or high findings.
- `pass-with-conditions`: only medium or low findings remain with owner and due date.
- `fail`: unresolved critical findings, or unresolved high findings in release-bound paths.

## Severity Model

- `critical`: direct risk of false confidence in release-bound behavior.
- `high`: material behavior risk or systemic flakiness under common conditions.
- `medium`: meaningful maintainability or coverage gaps with bounded risk.
- `low`: minor clarity or consistency issues with low immediate impact.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert xUnit quality decision | Deterministic Workflow |
| Deterministic pass/fail verdict | Decision Rules |
| Auditable remediation ownership | Required Outputs |
| Cross-project governance fit | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Test quality should be judged by behavior confidence and determinism, not test count.
- Explicit ownership is required for unresolved quality risks.

Trade-offs:

- Strict gates reduce regression risk but increase short-term delivery friction.
- Looser gates increase throughput but risk defect escape and unstable pipelines.

Open blockers:

- Missing behavior contracts reduce confidence in verdict quality.
- Incomplete flaky-test history can hide systemic determinism issues.

Recommendation:

- Apply this gate to all release-bound xUnit changes and reusable xUnit skill outputs.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Operational checklist guidance is captured in [xunit-quality-gate-checklist.md](./references/xunit-quality-gate-checklist.md).

## Pragmatic Stop Rule

Stop when all findings have severity and owner, determinism posture is explicit, and one recommendation is published.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.
