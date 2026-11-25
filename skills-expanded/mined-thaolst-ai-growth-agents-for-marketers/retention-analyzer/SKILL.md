---
name: retention-analyzer
description: >
  Analyze cohort retention, diagnose retention drops, identify at-risk segments,
  and recommend intervention strategies. Use when the user wants to understand
  retention trends, analyze cohort data, diagnose a retention drop, or plan
  retention campaigns. Specialized for fintech and super apps.
metadata:
  author: thaolst
  version: "1.0"
  license: MIT
  related_skills:
    - growth-mcp-connect
    - churn-intervention
    - campaign-brief
    - campaign-planning
---

# Retention Analyzer

> Checks `.agents/product-marketing-context.md` for product context.
> Checks `.agents/growth-metrics-context.md` for baseline retention.
> If growth-mcp connected, pulls real cohort data via `analyze_retention` and
> `predict_churn_risk`. Otherwise, use expert defaults below.

## Fintech Retention Benchmarks (SEA)

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| D1 Retention | > 50% | 30-50% | < 30% |
| D7 Retention | > 30% | 15-30% | < 15% |
| D30 Retention | > 20% | 10-20% | < 10% |
| Monthly Churn | < 15% | 15-30% | > 30% |

## Diagnostic Framework

When retention drops, check:

1. **Seasonal effect** — holiday spending spree → natural D1 dip
2. **Campaign hangover** — big promo → users wait for next promo
3. **Feature regression** — bug, UX change, performance issue
4. **Competitor activity** — competitor launched similar mechanic
5. **Segment shift** — acquired wrong user segment (incentive-driven)

## Intervention Matrix

| Problem | Intervention | Expected Lift |
|---------|-------------|---------------|
| D1 drop (activation) | Onboarding flow fix, welcome voucher | +5-15% |
| D7 drop (habit) | Push nudge series, streak reward | +3-10% |
| D30 drop (churn risk) | Re-engagement campaign, winback voucher | +2-8% |
| General decay | Loyalty program, points economy | +5-20% over 3 months |

## Related Skills

- [growth-mcp-connect](../growth-mcp-connect/) — pull real cohort data
- [churn-intervention](../churn-intervention/) — design save offers
- [campaign-brief](../campaign-brief/) — write retention campaign brief
- [voucher-mechanic-designer](../voucher-mechanic-designer/) — design winback voucher
