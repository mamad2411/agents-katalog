---
name: csharp-architecture-quality-gate
description: Use when C# architectural integrity needs an expert, evidence-first quality decision across boundaries, repository safety, and validation discipline.
---

# C# Architecture Quality Gate

## Specialization

Use this skill to assess C# architectural integrity with deterministic checks for layering, dependency direction, repository boundaries, validation discipline, and testability.

This skill is specialized for architecture-quality findings and does not implement product features.

## Objective

Produce one deterministic architecture-quality recommendation with severity-ranked findings and explicit remediation ownership.

## Trigger Conditions

- A change modifies boundaries between domain, application, and infrastructure concerns.
- A review flags coupling, repository, or validation discipline risks.
- A release-bound C# slice needs architectural sign-off.

## Scope Boundaries

In scope:

- Boundary and dependency-direction checks.
- Repository contract and data-access safety checks.
- Validation-at-boundary and immutability checks.
- Testability and isolation checks.

Out of scope:

- End-to-end product implementation.
- DBA operations and live infrastructure changes.
- Non-C# architecture domains not material to the request.

## Inputs

- Target modules and dependency graph context.
- Repository and validation standards for the workspace.
- Required release constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Boundary findings matrix with severity and impact.
- Repository safety and validation-discipline verdict.
- Testability-risk summary.
- Final recommendation: pass, pass-with-conditions, or fail.

## Deterministic Workflow

1. Map the architectural slice and dependency direction.
2. Verify that boundary responsibilities are explicit and non-overlapping.
3. Validate repository contracts and parameterized data-access safety assumptions.
4. Verify that boundary input validation and immutable model expectations are enforced.
5. Evaluate testability and substitution feasibility at key seams.
6. Rank findings and publish one explicit recommendation.

## Decision Rules

- `pass`: no unresolved critical or high findings.
- `pass-with-conditions`: only medium or low findings remain with owner and due date.
- `fail`: unresolved critical findings, or high findings in core boundaries.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert architecture review | Deterministic Workflow |
| Deterministic gate decision | Decision Rules |
| Auditable findings and ownership | Required Outputs |
| Cross-project portability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Boundary drift is a leading indicator of long-term delivery friction.
- Repository and validation discipline are core reliability controls in cross-project C# work.

Trade-offs:

- Strict architecture gates improve maintainability but can slow short-term delivery.
- Relaxed gates increase short-term speed but raise defect and coupling risk.

Open blockers:

- Incomplete dependency visibility can hide coupling regressions.
- Undefined repository or validation standards weaken recommendation confidence.

Recommendation:

- Use this gate for any change that touches architectural seams, repositories, or boundary validation behavior.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when boundary findings, repository safety, and validation discipline are explicitly assessed and one recommendation is published.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.
