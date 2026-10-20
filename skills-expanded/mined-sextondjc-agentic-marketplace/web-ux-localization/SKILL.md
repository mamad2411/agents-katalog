---
name: web-ux-localization
description: Use when implementing or reviewing web UX localization outcomes with deterministic locale, formatting, and layout-adaptation checks and evidence-backed release recommendations.
---

# Web UX Localization

## Specialization

Use this skill to produce expert-level, agent-usable localization and internationalization outcomes for web UX surfaces.

## Objective

Reduce locale-specific UX failures by validating content expansion, formatting correctness, and layout behavior across target locales.

## Trigger Conditions

- A release adds or updates locale-specific UI content.
- Teams require objective checks for locale formatting and layout adaptation.
- Quality gate decisions require localization evidence before sign-off.

## Scope Boundaries

In scope:

- Text expansion impact, locale-aware dates/numbers/currency, and directionality behavior.
- Locale-specific truncation, overflow, and interaction regressions.

Out of scope:

- Full linguistic translation quality certification.

## Inputs

- Target locales and market priorities.
- In-scope journeys and UI surfaces.
- Localization policy and formatting requirements.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Localization findings with severity and user-impact rationale.
- Locale evidence matrix for formatting and layout adaptation checks.
- Prioritized remediation backlog for locale blockers.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock target locales and in-scope journeys.
2. Define formatting and layout pass/fail checks by locale.
3. Validate date, number, currency, and pluralization behavior.
4. Validate text expansion, truncation, and directionality behavior.
5. Classify findings by severity and market risk.
6. Assign remediation disposition with owner and due date.
7. Publish evidence artifacts and final recommendation.

## Localization Gate Checklist

- [ ] Locale formatting is correct for dates, numbers, and currency.
- [ ] Text expansion does not break task-critical UI.
- [ ] Directionality behavior is correct for affected locales.
- [ ] Locale switching preserves task context where required.
- [ ] High and critical localization issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: target-locale users cannot complete core tasks.
- High: major locale UX friction likely to cause abandonment.
- Medium: measurable locale inconsistency with recoverable path.
- Low: minor locale polish issues.

## Evidence Contract

- `.docs/changes/<workstream-id>/localization-findings.md`
- `.docs/changes/<workstream-id>/localization-evidence-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when target locale checks are complete, high and critical issues are resolved or dispositioned, and final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

