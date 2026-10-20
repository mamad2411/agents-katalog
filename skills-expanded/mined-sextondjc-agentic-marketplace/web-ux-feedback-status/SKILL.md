---
name: web-ux-feedback-status
description: Use when implementing or reviewing web UX feedback-state outcomes with deterministic loading, success, empty, warning, timeout, and recovery checks and evidence-backed release recommendations.
---

# Web UX Feedback Status

## Specialization

Use this skill to produce expert-level, agent-usable feedback-state outcomes for web flows across different product types.

## Objective

Reduce uncertainty and recovery friction by validating system feedback quality across loading, success, empty, warning, error, timeout, and retry states.

## Trigger Conditions

- A release affects user-facing status states or async interactions.
- Teams need objective feedback-state evidence before sign-off.
- Core user tasks include waiting, retrying, or recovering from failure.

## Scope Boundaries

In scope:

- Loading, pending, success, warning, empty, timeout, error, and retry states.
- Visibility, timing, clarity, and recovery guidance for state transitions.

Out of scope:

- Deep performance optimization without state-quality review.

## Inputs

- In-scope journeys and async interaction points.
- Intended state models and transition behavior.
- Recovery expectations and timeout rules.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Feedback-state findings with severity and user-impact rationale.
- State coverage matrix by task and state type.
- Prioritized remediation backlog for unclear or missing states.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope tasks and user-visible state transitions.
2. Define pass/fail checks for each relevant state type.
3. Validate visibility, timing, wording, and recovery guidance for each state.
4. Classify findings by severity and recovery risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Feedback Status Gate Checklist

- [ ] Loading and pending states confirm progress or expected wait.
- [ ] Success states confirm outcome and next action where needed.
- [ ] Empty states explain absence and offer a path forward.
- [ ] Error and timeout states include actionable recovery guidance.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users cannot understand system state and cannot recover core tasks.
- High: missing or misleading states create substantial task failure risk.
- Medium: feedback exists but creates notable hesitation or confusion.
- Low: minor state-quality improvement opportunities.

## Evidence Contract

- `.docs/changes/<workstream-id>/feedback-status-findings.md`
- `.docs/changes/<workstream-id>/feedback-status-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when in-scope feedback states are validated, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

