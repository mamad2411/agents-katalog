---
name: live-event-ops-review
description: Design and audit live event operations for mobile games, PC games, apps, SaaS communities, marketplaces, launches, seasonal campaigns, limited-time offers, reward calendars, challenges, tournaments, content drops, promotions, and lifecycle events. Use when planning event calendars, segmentation, eligibility, economy impact, rollout, observability, support, compensation, rollback, or post-event learning.
---

# Live Event Ops Review

Use this skill to run live events as controlled product operations, not calendar-driven chaos.

## Workflow

1. Identify event objective, audience, duration, eligibility, reward/offer, dependencies, and blast radius.
2. Read `references/live-event-ops-systems.md`.
3. Map event configuration, rollout, eligibility, inventory/rewards, notifications, monitoring, support, compensation, and shutdown states.
4. Separate engagement goal, monetization goal, economy impact, fairness, operational risk, and trust risk.
5. Produce an event runbook with go/no-go, metrics, rollback, support macros, and post-event review.

## Guardrails

- Do not launch an event without monitoring, support route, and rollback/compensation plan.
- Do not create rewards or offers that destabilize economy, pricing, or fairness without explicit mitigation.
- Avoid fake scarcity, unclear eligibility, and invisible rule changes.

## Output format

```text
Event context:
Objective and audience:

Runbook:
- setup:
- launch:
- monitor:
- support:
- end/settle:

Risks:
- <risk> -> metric, rollback, compensation

Post-event learning:
- decision, data, follow-up
```
