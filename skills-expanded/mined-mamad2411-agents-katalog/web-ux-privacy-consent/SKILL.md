---
name: web-ux-privacy-consent
description: Use when implementing or reviewing web UX privacy and consent outcomes with deterministic disclosure, permission, and revocation checks and evidence-backed release recommendations.
---

# Web UX Privacy Consent

## Specialization

Use this skill to produce expert-level, agent-usable privacy and consent outcomes for web experiences across different product types.

## Objective

Reduce privacy-related UX risk by validating consent quality, disclosure clarity, permission timing, and revocation paths with deterministic evidence.

## Trigger Conditions

- A release changes consent prompts, cookie notices, permission requests, or data-sharing disclosures.
- Teams need objective privacy UX checks before sign-off.
- Product scope includes settings or revocation flows that affect user control.

## Scope Boundaries

In scope:

- Consent wording, permission timing, data-sharing disclosures, preference management, and revocation or opt-out paths.
- User control clarity at the moment of decision.

Out of scope:

- Legal policy drafting or regulatory interpretation.
- Backend data retention implementation.

## Inputs

- In-scope journeys and privacy-affecting actions.
- Product privacy requirements and consent model.
- Target surfaces where disclosures or requests appear.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Privacy and consent findings with severity and user-impact rationale.
- Consent-path evidence matrix by trigger and user choice.
- Prioritized remediation backlog for blocking or deceptive patterns.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope consent and privacy-control surfaces.
2. Define pass/fail checks for disclosure clarity, timing, specificity, and revocation accessibility.
3. Validate consent paths, denial paths, and preference updates.
4. Classify findings by severity and user-control risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Privacy Consent Gate Checklist

- [ ] Consent requests are specific, understandable, and non-coercive.
- [ ] Users can decline or defer where policy allows.
- [ ] Revocation and preference changes are available and discoverable.
- [ ] Data-sharing disclosures are visible at the point of choice.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users cannot make informed or reversible choices about sensitive data use.
- High: consent or disclosure quality is materially misleading or difficult to refuse.
- Medium: user control exists but with notable friction.
- Low: minor improvements in privacy UX clarity.

## Evidence Contract

- `.docs/changes/<workstream-id>/privacy-consent-findings.md`
- `.docs/changes/<workstream-id>/privacy-consent-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when all in-scope privacy and consent paths are validated, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

