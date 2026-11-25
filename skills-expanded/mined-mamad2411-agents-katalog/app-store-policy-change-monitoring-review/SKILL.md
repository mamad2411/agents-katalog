---
name: app-store-policy-change-monitoring-review
description: Design and audit app store policy change monitoring for Apple App Store, Google Play, Steam, Microsoft Store, marketplace policies, privacy labels, payments, subscriptions, ads, user-generated content, age ratings, review guidelines, deadlines, impact triage, remediation owners, release timing, and evidence. Use when policy drift can block launches or revenue.
---

# App Store Policy Change Monitoring Review

Use this skill to convert app store policy monitoring, review guideline change, platform deadline, subscription policy, privacy label change, UGC policy, age rating, and remediation-planning questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify store, policy source, effective date, affected products, feature areas, commerce/privacy/content impact, owner, evidence, remediation deadline, and release risk.
2. Read `references/app-store-policy-change-monitoring-patterns.md`.
3. Classify the situation as privacy policy change, payment/subscription change, content or UGC policy, ads policy, age-rating change, metadata requirement, technical requirement, review-process change, or enforcement trend.
4. Define monitoring cadence, impact triage, owner routing, remediation plan, release sequencing, evidence package, reviewer note, and executive/customer communication.
5. Produce policy monitoring plan, state machine, decision table, event schema, impact checklist, remediation tracker, and review-readiness evidence.

## Guardrails

- Do not wait for a rejection to discover a policy change that had a published deadline.
- Do not assume one store policy maps cleanly to another store or region.
- Do not update metadata, privacy labels, payments, or age ratings without product behavior evidence.
- Do not let policy monitoring live with one person without owner routing and recurring review.

## Output format

```text
Store policy context:
Audience / source of truth / risk boundary:

Policy monitoring plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Source, deadline, impact, owner, remediation, evidence, and release timing:
- <trigger> -> <policy, metric, edge case, support note>
```
