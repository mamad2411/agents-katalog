---
name: churn-intervention
description: >
  Design churn prevention and winback campaigns for fintech and super apps.
  Use when the user needs to reduce churn, design save offers, create
  cancellation flows, plan re-engagement campaigns, or analyze churn reasons.
  Supports both proactive (predictive) and reactive (post-churn) strategies.
metadata:
  author: thaolst
  version: "1.0"
  license: MIT
  related_skills:
    - retention-analyzer
    - growth-mcp-connect
    - campaign-brief
    - voucher-mechanic-designer
---

# Churn Intervention Specialist

> Checks `.agents/product-marketing-context.md` for user segment profiles.
> Checks `.agents/growth-metrics-context.md` for churn baselines.
> If growth-mcp connected, uses `predict_churn_risk` for real predictions.

## Churn Types in Fintech

| Type | Signal | Best Intervention |
|------|--------|------------------|
| Transaction dormancy | No tx in 14-30 days | Nudge + small voucher |
| Balance zero-out | Withdrew all funds | Reason survey + winback offer |
| Feature abandonment | Stopped using key feature | Re-onboarding flow |
| Competitor switch | Known competitor activity | Price match or exclusive benefit |
| Seasonal churn | Post-holiday drop | Streak reward, loyalty tier |

## Save Offer Framework

### Tier 1: Light nudge (no cost)
- Push notification with personalized message
- "We miss you" email with feature highlight
- In-app banner with trending feature

### Tier 2: Small incentive (low cost)
- Time-limited voucher (e.g., 10% off next transaction)
- Bonus points on next action
- Free transaction fee waiver

### Tier 3: Strong intervention (medium cost)
- High-value cashback on next 3 transactions
- Exclusive tier upgrade for 30 days
- VIP customer support access

## Winback Sequence (Recommended)

| Day | Channel | Message | Cost |
|-----|---------|---------|------|
| D0 (dormancy detected) | Push | "You have X points expiring" | Free |
| D3 | Push | "Trending near you: [popular mechanic]" | Free |
| D7 | In-app + Email | "Here's 10% off your next [action]" | Low |
| D14 | SMS | "Special offer: [exclusive cashback]" | Medium |
| D21 | Push | "Your [feature] is waiting" | Free |
| D30 | Survey | "Help us improve" + reason dropdown | Free |

## Metrics to Track

- Save offer redemption rate
- Reactivated user D7/D30 retention
- Cost per reactivated user
- Incremental transactions from saved users
- Winback sequence conversion by step

## Related Skills

- [retention-analyzer](../retention-analyzer/) — diagnose churn root cause
- [growth-mcp-connect](../growth-mcp-connect/) — pull churn predictions
- [campaign-brief](../campaign-brief/) — write reactivation campaign brief
- [voucher-mechanic-designer](../voucher-mechanic-designer/) — design winback mechanics
