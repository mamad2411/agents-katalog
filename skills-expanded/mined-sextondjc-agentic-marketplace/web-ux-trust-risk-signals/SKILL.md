---
name: web-ux-trust-risk-signals
description: Use when implementing or reviewing web UX trust and risk-signal outcomes with deterministic consent, warning, and irreversible-action checks and evidence-backed release recommendations.
---

# Web UX Trust Risk Signals

## Specialization

Use this skill to produce expert-level, agent-usable trust and risk-signal outcomes for web UX flows.

## Objective

Protect user confidence and reduce harmful mistakes by validating consent, warning, and irreversible-action signaling with deterministic evidence.

## Trigger Conditions

- A release includes sensitive actions, consent steps, or irreversible outcomes.
- Teams need objective trust-signal checks before release.
- UX quality gate decisions require explicit risk communication evidence.

## Scope Boundaries

In scope:

- Consent prompts, destructive action warnings, confirmation patterns, and sensitive-state indicators.
- Clarity and timing of risk communication in task flows.

Out of scope:

- Legal policy drafting.
- Security architecture implementation.

## Inputs

- In-scope sensitive journeys and actions.
- Consent and warning requirements.
- Known compliance constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Trust-signal findings with severity and user-impact rationale.
- Risk-signal evidence matrix by sensitive action.
- Prioritized remediation backlog for trust blockers.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope sensitive flows and irreversible actions.
2. Define pass/fail checks for consent clarity, warning timing, and confirmation quality.
3. Validate risk cues before, during, and after sensitive actions.
4. Classify findings by severity and user-harm risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical trust issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Trust-Signal Gate Checklist

- [ ] Sensitive actions have explicit and comprehensible warnings.
- [ ] Consent requests are specific and avoid coercive patterns.
- [ ] Irreversible actions have clear confirmation and recovery guidance.
- [ ] Risk cues are visible at the decision point, not after submission.
- [ ] High and critical trust issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users can trigger harmful or irreversible outcomes without clear warning.
- High: users face significant trust erosion or error risk.
- Medium: notable trust friction with recoverable path.
- Low: minor trust-signal polish issues.

## Evidence Contract

- `.docs/changes/<workstream-id>/trust-risk-findings.md`
- `.docs/changes/<workstream-id>/trust-risk-evidence-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when sensitive-action trust checks are complete, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

