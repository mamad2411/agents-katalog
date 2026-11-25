---
name: customer-success-health-review
description: Design and audit customer health scoring, onboarding success, adoption, renewal risk, expansion readiness, support signals, QBRs, lifecycle playbooks, and account success operations for SaaS, developer tools, marketplaces, and B2B products. Use when building customer success dashboards, health scores, churn risk reviews, renewal playbooks, or expansion motions.
---

# Customer Success Health Review

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Identify account segment, buyer, users, promised outcome, adoption milestones, renewal date, support history, and expansion path.
2. Read `references/customer-health-patterns.md`.
3. Separate leading indicators, lagging outcomes, sentiment, support burden, commercial risk, and data quality.
4. Design a health score that maps to actions, not just dashboard colors.
5. Produce account states, playbooks, events, and review cadence.

## Guardrails

- Do not treat raw usage volume as health without outcome context.
- Do not hide missing data behind a confident score.
- Keep renewal risk, product adoption, and expansion readiness separate dimensions.
- Avoid manipulative save tactics; success motions should restore value.

## Output format

```text
Customer/account context:
Outcome promised:

Health model:
| Dimension | Signal | Weight | Data quality | Action |
| --- | --- | --- | --- | --- |

Account state and playbook:
- <state> -> <owner/action/message/proof>

Metrics/events:
- <event or review cadence>
```
