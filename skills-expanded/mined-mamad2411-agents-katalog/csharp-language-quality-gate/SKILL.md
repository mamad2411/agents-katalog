---
name: csharp-language-quality-gate
description: Use when C# language and API-contract changes need an expert, evidence-first quality decision before merge or promotion.
---

# C# Language Quality Gate

## Specialization

Use this skill to evaluate C# language-level correctness and maintainability for modern syntax adoption, nullability, immutability, and API contract clarity.

This skill is specialized for evidence-first quality decisions. It does not implement product features.

## Objective

Produce one deterministic language-quality recommendation with severity-ranked findings and explicit pass criteria.

## Trigger Conditions

- A change introduces or modifies C# language features.
- A code review flags nullability, API contract, or readability risks.
- A team needs one release-bound decision on language-level quality.

## Scope Boundaries

In scope:

- Language-version compatibility checks.
- Nullability and API contract checks.
- Immutability and data-shape consistency checks.
- Readability and maintainability findings.

Out of scope:

- Runtime performance profiling.
- SQL, infrastructure, or deployment execution.
- Feature implementation.

## Inputs

- Target files or modules.
- Target framework and language-version constraints.
- Review threshold policy.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Findings table with severity, impact, and remediation guidance.
- Language compatibility verdict.
- Nullability and contract-safety verdict.
- Final recommendation: pass, pass-with-conditions, or fail.

## Deterministic Workflow

1. Confirm TFM and language-version compatibility boundary.
2. Inspect nullability context and dereference safety.
3. Verify public API contracts for clarity and intent.
4. Check immutable model usage where domain invariants require stability.
5. Rank findings by severity and map each finding to one remediation.
6. Produce one explicit verdict with residual risks and conditions.

## Severity Rubric

- `critical`: likely production failure or unsafe behavior.
- `high`: significant correctness or maintainability risk.
- `medium`: quality drift that should be remediated before broad rollout.
- `low`: stylistic or clarity improvement with low risk.

## Decision Rules

- `pass`: no critical or high findings and no unresolved medium findings that violate policy.
- `pass-with-conditions`: limited medium or low findings remain with owner and due date.
- `fail`: any unresolved critical finding or unresolved high finding.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert language review | Deterministic Workflow |
| Deterministic quality gate | Decision Rules |
| Auditable findings | Required Outputs + Severity Rubric |
| Cross-project portability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Teams require deterministic language-level review before promotion.
- Nullability and contract clarity are major defect-prevention controls.

Trade-offs:

- Strict gates prevent defects but may slow rapid iteration.
- Looser gates increase throughput but raise long-term maintenance risk.

Open blockers:

- Missing TFM or language-version target blocks compatibility decisions.
- Partial code visibility can hide contract breakage.

Recommendation:

- Use this gate for all public-surface or shared-library C# changes.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when every finding has a severity, one remediation, one owner, and one explicit verdict is published.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.
