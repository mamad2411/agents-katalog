---
name: marketplace-dispute-resolution-review
description: Design and audit marketplace dispute resolution for buyers, sellers, creators, developers, partners, listings, skills, apps, services, payouts, refunds, chargebacks, quality claims, delivery failures, policy violations, appeals, evidence packages, timelines, payout holds, fraud review, communication, and fairness monitoring. Use when marketplace conflicts need consistent resolution without harming trust or incentives.
---

# Marketplace Dispute Resolution Review

Use this skill to convert marketplace dispute, refund claim, payout hold, buyer seller conflict, creator appeal, quality claim, chargeback, evidence package, and dispute policy questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify dispute type, parties, transaction/listing, policy claim, evidence, timeline, payout/refund exposure, fraud risk, communication channel, reviewer role, and appeal path.
2. Read `references/marketplace-dispute-resolution-patterns.md`.
3. Classify the situation as non-delivery, quality mismatch, refund dispute, chargeback, payout hold, policy violation, fraud suspicion, rating/review dispute, moderation appeal, or partner/customer escalation.
4. Define evidence requirements, triage SLA, reviewer independence, temporary actions, payout/refund rules, communication templates, appeal path, abuse controls, fairness metrics, and policy feedback.
5. Produce dispute resolution plan, state machine, decision table, event schema, evidence checklist, communication ladder, and fairness review.

## Guardrails

- Do not optimize dispute cost by silently favoring buyers, sellers, high-revenue creators, or platform margin.
- Do not release payouts, refunds, ratings, or enforcement actions without evidence standards and appeal paths.
- Do not expose fraud-detection signals or reviewer private notes in party-facing messages.
- Do not let unresolved dispute patterns stay outside marketplace quality, ranking, policy, and onboarding improvements.

## Output format

```text
Marketplace dispute context:
Audience / source of truth / risk boundary:

Dispute resolution plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Evidence, temporary action, payout/refund decision, appeal, and fairness monitoring:
- <trigger> -> <policy, metric, edge case, support note>
```
