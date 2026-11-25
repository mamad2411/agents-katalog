---
name: winback-campaign-review
description: Design and audit win-back, reactivation, churn recovery, cancellation follow-up, dormant-user, lapsed-subscriber, lifecycle offer, and re-engagement campaigns for SaaS, apps, games, marketplaces, and developer tools. Use when trying to recover churned users, reactivate dormant accounts, or build ethical promotion flows with segmentation, offers, messaging, and metrics.
---

# Winback Campaign Review

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Identify churn definition, segment, lifecycle stage, prior value moment, consent, channel, and economics.
2. Read `references/winback-campaign-patterns.md`.
3. Separate dormant, cancelled, failed-payment, seasonal, competitor-lost, and bad-fit users.
4. Design message, offer, timing, frequency caps, landing path, support handoff, and measurement.
5. Produce a campaign matrix with guardrails, events, and stop criteria.

## Guardrails

- Do not use dark patterns, fake scarcity, or punitive cancellation copy.
- Do not discount users back into a product that has not fixed their churn reason.
- Respect consent, unsubscribe, quiet periods, and sensitive churn contexts.
- Measure retained recovery, margin, and support load, not opens alone.

## Output format

```text
Win-back context:
Churn reason / segment:

Campaign matrix:
| Segment | Trigger | Message | Offer | Landing path | Guardrail | Metric |
| --- | --- | --- | --- | --- | --- | --- |

State flow:
- <state> -> <campaign action> -> <stop/next action>

Experiment plan:
- <hypothesis, metric, duration, stop condition>
```
