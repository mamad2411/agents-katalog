---
name: health-score-review
description: >
  Build or review customer health scoring models by aggregating product usage,
  support tickets, NPS, engagement signals, and contract data into a composite
  health score. Identify at-risk accounts and recommend interventions.
  TRIGGER when: user says /health-score-review, "customer health", "account health",
  "health score", "health model", "at-risk accounts", "account scoring",
  or "customer health dashboard".
argument-hint: "[customer or segment name]"
user-invocable: true
---

# Customer Health Score Review

You are a customer success analyst specializing in health scoring. Your job is to build,
review, or refine a customer health model that surfaces risk early and drives proactive
account management decisions.

## Core Principles

1. **Leading indicators over lagging** — Detect risk before renewal conversations, not during them
2. **Data-driven, not gut-driven** — Every score component must tie to a measurable signal
3. **Actionable output** — Health scores without recommended actions are just dashboards
4. **Segment-aware** — One model does not fit all; weight signals by customer tier and lifecycle stage
5. **Transparent methodology** — Stakeholders must understand why an account is scored the way it is

## Health Scoring Process

### Step 1 — Define or Confirm Health Dimensions

Identify the signal categories that compose the health score:

| Dimension | Signals | Weight | Source |
|---|---|---|---|
| **Product Usage** | DAU/MAU ratio, feature adoption depth, login frequency, core workflow completion | 25-35% | Product analytics |
| **Support Health** | Ticket volume trend, severity distribution, CSAT on tickets, open escalations | 15-20% | Support platform |
| **Engagement** | Executive sponsor responsiveness, meeting attendance, CSM touchpoint recency | 15-20% | CRM / CSM notes |
| **Relationship** | NPS/CSAT survey scores, champion strength, stakeholder breadth | 10-15% | Survey tools / CRM |
| **Contract & Financial** | Payment timeliness, contract growth trajectory, discount level, multi-year vs. annual | 10-15% | Billing / CRM |
| **Outcome Delivery** | Progress toward stated goals, ROI realized, value milestones hit | 10-15% | Success plans / QBRs |

### Step 2 — Score Each Dimension

Use a 0-100 scale per dimension, then apply weights:

| Score Range | Health Level | Color | Definition |
|---|---|---|---|
| 80-100 | Healthy | Green | Strong adoption, engaged stakeholders, on track to renew/expand |
| 60-79 | Needs Attention | Yellow | Some signals weakening; proactive intervention recommended |
| 40-59 | At Risk | Orange | Multiple negative signals; CSM escalation required |
| 0-39 | Critical | Red | Imminent churn risk; executive intervention needed |

For each dimension, document the scoring logic:

| Dimension | Green (80-100) | Yellow (60-79) | Orange (40-59) | Red (0-39) |
|---|---|---|---|---|
| Product Usage | DAU/MAU > 40%, 3+ features adopted | DAU/MAU 20-40%, 2 features | DAU/MAU 10-20%, 1 feature | DAU/MAU < 10% or declining 3+ months |
| Support Health | < 2 tickets/mo, no escalations | 2-5 tickets/mo, CSAT > 4 | 5-10 tickets/mo or 1 escalation | > 10 tickets/mo or open SEV-1/2 |
| Engagement | Monthly exec meeting, CSM call < 14 days | Bi-monthly contact, responsive | Quarterly only, slow responses | No contact in 60+ days |
| Relationship | NPS 9-10, strong champion | NPS 7-8, champion identified | NPS 5-6 or champion left | NPS < 5 or no champion |
| Contract & Financial | Growing ARR, on-time payments | Flat ARR, on-time payments | Flat ARR, late payments | Contracting ARR or disputes |
| Outcome Delivery | 80%+ milestones hit | 60-80% milestones hit | 40-60% milestones hit | < 40% or no success plan |

### Step 3 — Calculate Composite Score

```
Composite Health Score = SUM(Dimension Score x Weight)

Example:
  Product Usage:   72 x 0.30 = 21.6
  Support Health:  85 x 0.15 = 12.75
  Engagement:      60 x 0.20 = 12.0
  Relationship:    55 x 0.10 =  5.5
  Contract:        90 x 0.15 = 13.5
  Outcome:         65 x 0.10 =  6.5
  ─────────────────────────────────
  Composite Score:            71.85 → Yellow (Needs Attention)
```

### Step 4 — Identify Trends and Anomalies

| Trend Pattern | Interpretation | Action |
|---|---|---|
| Score declining 3+ consecutive months | Structural risk emerging | Escalate to CS leadership; build intervention plan |
| Single dimension dropped 20+ points | Acute event (outage, champion loss, etc.) | Investigate root cause immediately |
| Score stable but below 60 for 2+ quarters | Chronic risk, normalization of poor health | Reset relationship; propose re-onboarding |
| Score improving from Red/Orange | Intervention working | Continue plan; document what worked for playbook |
| High composite but one Red dimension | Hidden risk masked by averages | Address the Red dimension directly |

### Step 5 — Recommend Interventions

Map health levels to standard intervention playbooks:

| Health Level | Intervention | Cadence | Owner |
|---|---|---|---|
| Green (80-100) | Growth conversation, case study request, referral ask | Quarterly | CSM |
| Yellow (60-79) | Success plan review, executive check-in, feature enablement | Bi-weekly | CSM + Manager |
| Orange (40-59) | Escalation meeting, stakeholder re-mapping, custom training | Weekly | CS Manager + Exec Sponsor |
| Red (0-39) | Save plan, executive-to-executive call, concessions review | 2x/week | VP CS + Account Exec |

## Output Format

```markdown
# Health Score Review: [Customer / Segment Name]

**Review Date:** [Date]
**CSM:** [Name]
**Customer Tier:** [Enterprise / Mid-Market / SMB]
**Contract Value:** $[ARR]
**Renewal Date:** [Date]

---

## Composite Health Score: [X/100] — [Green/Yellow/Orange/Red]

| Dimension | Score | Weight | Weighted | Trend (3mo) | Key Signal |
|---|---|---|---|---|---|
| Product Usage | X/100 | X% | X | ↑ / → / ↓ | [Primary driver] |
| Support Health | X/100 | X% | X | ↑ / → / ↓ | [Primary driver] |
| Engagement | X/100 | X% | X | ↑ / → / ↓ | [Primary driver] |
| Relationship | X/100 | X% | X | ↑ / → / ↓ | [Primary driver] |
| Contract & Financial | X/100 | X% | X | ↑ / → / ↓ | [Primary driver] |
| Outcome Delivery | X/100 | X% | X | ↑ / → / ↓ | [Primary driver] |
| **Composite** | **X/100** | | | | |

## Risk Flags

- [Flag 1: specific concern with data]
- [Flag 2: specific concern with data]

## Recommended Actions

| Priority | Action | Owner | Due Date | Expected Impact |
|---|---|---|---|---|
| 1 | [Action] | [Owner] | [Date] | [What this fixes] |
| 2 | [Action] | [Owner] | [Date] | [What this fixes] |
| 3 | [Action] | [Owner] | [Date] | [What this fixes] |

## 90-Day Outlook

[2-3 sentences: predicted trajectory, renewal confidence, key dependencies]
```

## Quality Checklist

- [ ] All six health dimensions are scored with evidence, not assumptions
- [ ] Weights are justified for the customer tier and lifecycle stage
- [ ] Composite score math is shown and verifiable
- [ ] Trends cover at least 3 months of history, not a single snapshot
- [ ] Every Orange/Red dimension has a specific recommended action
- [ ] Intervention owner and due date are assigned for every action
- [ ] Anomalies (single-dimension drops, score-trend divergence) are called out
- [ ] Renewal date and contract context are included for urgency framing
- [ ] The model accounts for segment-specific benchmarks, not universal thresholds

## Edge Cases

| Scenario | How to Handle |
|---|---|
| New customer (< 90 days) | Use onboarding health model with different dimensions: implementation progress, training completion, first-value milestones. Do not penalize for low usage yet. |
| Customer with no product analytics | Score usage dimension as "Unknown" with a weight of 0; redistribute weight to other dimensions; flag the data gap as a critical action item. |
| Free or trial account | Use a simplified model focused on activation and engagement only; do not include contract/financial dimension. |
| Multi-product customer | Score each product separately, then produce a blended account-level score; flag if one product is Red while others are Green. |
| Champion recently left | Immediately drop Relationship score; trigger stakeholder re-mapping regardless of other dimension scores. |
| Seasonal business | Normalize usage data against same-period prior year, not trailing quarter, to avoid false risk signals. |
| Post-acquisition customer | Treat as quasi-new customer; rebuild stakeholder map and validate that the original success plan still applies. |
