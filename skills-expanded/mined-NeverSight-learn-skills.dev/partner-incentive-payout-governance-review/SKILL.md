---
name: partner-incentive-payout-governance-review
description: Design and audit partner incentive payout governance for referral, reseller, implementation, marketplace, affiliate, MDF, rebate, bounty, and SPIF programs covering eligibility, attribution, quality gates, payout calculation, approval, invoicing, tax, clawbacks, disputes, fraud controls, partner communication, and ROI. Use when incentives can drive growth, channel conflict, or payout abuse.
---

# Partner Incentive Payout Governance Review

Use this skill to convert partner incentive, referral payout, reseller rebate, marketplace bounty, affiliate commission, MDF, SPIF, payout dispute, clawback, attribution, and channel incentive governance questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify partner type, incentive objective, eligible actions, attribution source, payout formula, quality gate, approval authority, invoice/tax path, clawback rule, dispute route, fraud signals, and ROI measurement.
2. Read `references/partner-incentive-payout-governance-patterns.md`.
3. Classify the situation as referral commission, reseller rebate, implementation bonus, marketplace bounty, affiliate payout, marketing development fund, sales SPIF, renewal incentive, or disputed payout.
4. Define eligibility rules, attribution model, calculation source, payout approval, evidence requirements, quality/retention gates, clawback policy, dispute workflow, fraud controls, partner communication, and performance review.
5. Produce partner incentive governance review, state machine, decision table, event schema, payout checklist, dispute policy, and ROI monitoring plan.

## Guardrails

- Do not pay incentives for activity that creates low-quality customers, channel conflict, policy violations, or support burden.
- Do not let sales notes, spreadsheets, and partner claims override the payout source of truth.
- Do not hide clawback, dispute, tax, invoicing, or eligibility conditions from partners until payout time.
- Do not optimize partner incentives only for booked revenue without retention, customer outcomes, margin, and trust checks.

## Output format

```text
Partner incentive context:
Audience / source of truth / risk boundary:

Payout governance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Eligibility, attribution, payout formula, approvals, clawbacks, disputes, fraud controls, and ROI:
- <trigger> -> <policy, metric, edge case, support note>
```
