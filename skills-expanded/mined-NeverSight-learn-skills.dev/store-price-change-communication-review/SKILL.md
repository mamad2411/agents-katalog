---
name: store-price-change-communication-review
description: Design and audit App Store, Google Play, Steam, Microsoft Store, and direct subscription price-change communication covering affected products, regions, consent requirements, renewal timing, grandfathering, paywall copy, store metadata, notifications, email/in-app messaging, support macros, refund/cancel paths, analytics, and post-change monitoring. Use when pricing changes can affect trust, churn, or platform compliance.
---

# Store Price Change Communication Review

Use this skill to convert store price change, subscription price increase, regional price update, intro offer ending, grandfathering, consent requirement, renewal timing, paywall copy, support macro, and price-change communication questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify store/channel, product IDs, countries, cohorts, current and new prices, renewal dates, consent rules, grandfathering policy, messaging surfaces, support paths, refund/cancel expectations, and analytics.
2. Read `references/store-price-change-communication-patterns.md`.
3. Classify the situation as price increase, price decrease, regional FX adjustment, intro/trial transition, grandfathering sunset, package migration, store-mandated change, or direct-plus-store mixed channel change.
4. Define cohort map, timeline, consent/notification requirements, user messaging, paywall/store metadata updates, support macros, refund/cancel routes, analytics, and monitoring plan.
5. Produce price change communication plan, state machine, decision table, event schema, cohort checklist, support script, and compliance monitoring plan.

## Guardrails

- Do not hide price increases behind vague product-update language or rely only on store notifications for customer trust.
- Do not change paywalls, screenshots, metadata, and support scripts out of sync with actual store price behavior.
- Do not assume App Store, Google Play, Steam, Microsoft Store, and direct billing consent rules behave identically.
- Do not launch price changes without churn, refund, cancellation, support-contact, and billing-error monitoring.

## Output format

```text
Store price-change context:
Audience / source of truth / risk boundary:

Communication and compliance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Cohorts, channel rules, timeline, copy, support, refund/cancel paths, analytics, and monitoring:
- <trigger> -> <policy, metric, edge case, support note>
```
