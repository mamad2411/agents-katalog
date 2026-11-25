---
name: csharp-release-quality-gate
description: Use when C# release candidates need one expert, evidence-first go or no-go decision that consolidates language, async, architecture, testing, and data-access quality outcomes.
---

# C# Release Quality Gate

## Specialization

Use this skill to deliver a unified C# release decision by consolidating quality evidence across language integrity, async behavior, architecture boundaries, testing adequacy, and data-access safety.

This skill is specialized for final quality synthesis and release disposition. It does not implement product features.

## Objective

Produce one deterministic C# release recommendation with explicit gate status, residual-risk accounting, and approval-ready evidence.

## Trigger Conditions

- A C# change set is a release candidate requiring final quality disposition.
- Multiple quality assessments exist and need one unified decision.
- Teams need an auditable go or no-go artifact before promotion.

## Scope Boundaries

In scope:

- Consolidation of quality findings into one release decision.
- Gate status evaluation across language, async, architecture, testing, and data-access evidence.
- Residual-risk, owner, and due-date accounting for unresolved items.

Out of scope:

- New feature implementation.
- Deep specialist investigation of unresolved findings.
- Deployment execution.

## Inputs

- Evidence artifacts and findings summaries for all in-scope quality dimensions.
- Release policy thresholds and exception rules.
- Candidate build metadata and target environment.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Unified gate matrix with pass/fail/conditional status per quality dimension.
- Consolidated findings table with severity, owner, and due date.
- Residual-risk summary and exception log.
- Final recommendation: go, go-with-exceptions, hold, or no-go.

## Deterministic Workflow

1. Confirm the release scope and required quality dimensions.
2. Validate that each required dimension has current evidence artifacts.
3. Normalize severity and disposition semantics across findings.
4. Build one gate matrix assigning status per dimension.
5. Identify unresolved risks and verify ownership with due dates.
6. Apply policy thresholds and exception rules to derive one recommendation.
7. Publish an approval-ready decision artifact with residual risks.

## Decision Rules

- `go`: all required dimensions pass or are formally waived with acceptable risk.
- `go-with-exceptions`: limited medium or low risks remain with approved exceptions.
- `hold`: at least one high-risk item is open but remediable in-cycle.
- `no-go`: unresolved critical risk, or unresolved high risk without approved exception.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Unified release decision | Deterministic Workflow |
| Deterministic quality synthesis | Decision Rules |
| Auditable cross-dimension evidence | Required Outputs |
| Cross-project release portability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Final release confidence requires consolidated rather than fragmented quality decisions.
- Residual-risk transparency is required for safe promotion governance.

Trade-offs:

- Strong synthesis improves decision quality but requires complete input evidence.
- Fast decisions with incomplete evidence increase release risk.

Open blockers:

- Missing evidence from any required dimension blocks reliable synthesis.
- Inconsistent severity semantics across inputs can distort decision outcomes.

Recommendation:

- Use this gate for every release-bound C# slice with cross-capability changes.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when every required dimension has a gate status, unresolved risks have explicit owner and due date, and one final recommendation artifact is published.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.
