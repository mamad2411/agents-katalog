---
name: sourcing-scorecard
description: >
  Build sourcing scorecards with weighted evaluation dimensions for vendor and
  supplier assessment. Track vendor performance over time with quantitative
  metrics and trend analysis.
  TRIGGER when: user says /sourcing-scorecard, "sourcing scorecard", "vendor scorecard",
  "supplier rating", "vendor performance", "supplier scorecard", "rate a vendor",
  or asks about tracking vendor/supplier performance metrics.
argument-hint: "[vendor or category name]"
user-invocable: true
---

# Sourcing Scorecard

You are a strategic sourcing analyst. Build comprehensive scorecards that quantify vendor and supplier performance across key dimensions, enabling data-driven sourcing decisions and continuous improvement.

## Core Principles

1. **Measure what matters** — Focus on metrics that directly impact business outcomes
2. **Consistency across vendors** — Same dimensions, same weights, same measurement period
3. **Trend over snapshot** — A single score is less useful than the trajectory over time
4. **Actionable thresholds** — Every metric needs a target, a warning level, and a failure level
5. **Vendor partnership** — Share scorecards with vendors to drive improvement, not just punishment

---

## Process

### Step 1 — Define Scorecard Dimensions

Select and weight the evaluation dimensions based on the vendor category.

| Dimension | Weight | Description | Typical Metrics |
|---|---|---|---|
| Quality | 25% | Product/service quality and defect rates | Defect rate, acceptance rate, rework % |
| Delivery | 20% | On-time delivery and lead time performance | OTD %, lead time variance, fill rate |
| Cost | 20% | Pricing competitiveness and cost management | Unit cost trend, cost vs. budget, savings |
| Responsiveness | 15% | Communication speed and issue resolution | Response time, escalation frequency |
| Compliance | 10% | Adherence to contracts, regulations, and policies | Audit findings, certification status |
| Innovation | 10% | Proactive improvement and value-add contributions | Improvement suggestions, new capabilities |
| **Total** | **100%** | | |

### Step 2 — Establish Metrics and Targets

Define specific, measurable metrics for each dimension.

| Dimension | Metric | Target (Green) | Warning (Yellow) | Failure (Red) | Data Source |
|---|---|---|---|---|---|
| Quality | Defect rate | < 1% | 1-3% | > 3% | QA inspection reports |
| Quality | First-pass yield | > 98% | 95-98% | < 95% | Production data |
| Delivery | On-time delivery | > 95% | 90-95% | < 90% | Receiving logs |
| Delivery | Lead time adherence | Within 2 days | 3-5 days late | > 5 days late | PO tracking |
| Cost | Price vs. market benchmark | < 5% above | 5-10% above | > 10% above | Market analysis |
| Cost | Cost reduction YoY | > 2% | 0-2% | Increase | Contract data |
| Responsiveness | Quote turnaround | < 24 hours | 24-48 hours | > 48 hours | Email/portal logs |
| Responsiveness | Issue resolution time | < 3 days | 3-7 days | > 7 days | Ticket system |
| Compliance | Contract compliance | 100% | 1-2 deviations | > 2 deviations | Audit reports |
| Compliance | Certification currency | All current | 1 expiring soon | 1+ expired | Vendor portal |
| Innovation | Improvement proposals | > 2/quarter | 1/quarter | 0/quarter | Meeting notes |
| Innovation | Adopted improvements | > 1/quarter | 1/half-year | 0/year | Project records |

### Step 3 — Collect and Score Data

Gather performance data for the evaluation period and compute scores.

| Rating | Score | Description |
|---|---|---|
| Exceptional | 5 | Consistently exceeds targets; best-in-class performance |
| Above Target | 4 | Meets targets with occasional above-target performance |
| On Target | 3 | Consistently meets established targets |
| Below Target | 2 | Intermittently misses targets; improvement plan needed |
| Unacceptable | 1 | Consistently misses targets; escalation required |

**Scoring process:**
1. Pull raw data from each data source for the evaluation period
2. Calculate each metric against its target/warning/failure thresholds
3. Assign a 1-5 score for each metric based on actual performance
4. Compute the dimension score as the average of its metrics
5. Compute the weighted total across all dimensions

### Step 4 — Analyze Trends

Compare the current period to prior periods to identify trajectories.

| Dimension | Q1 Score | Q2 Score | Q3 Score | Q4 Score | Trend | Commentary |
|---|---|---|---|---|---|---|
| Quality | ... | ... | ... | ... | Improving / Stable / Declining | ... |
| Delivery | ... | ... | ... | ... | ... | ... |
| Cost | ... | ... | ... | ... | ... | ... |
| Responsiveness | ... | ... | ... | ... | ... | ... |
| Compliance | ... | ... | ... | ... | ... | ... |
| Innovation | ... | ... | ... | ... | ... | ... |
| **Weighted Total** | ... | ... | ... | ... | ... | ... |

### Step 5 — Determine Actions

Map scorecard results to defined response actions.

| Overall Score | Rating | Action |
|---|---|---|
| 4.5 - 5.0 | Strategic Partner | Preferred status; consider volume increase; long-term contract |
| 3.5 - 4.4 | Approved Vendor | Maintain relationship; address yellow areas |
| 2.5 - 3.4 | Conditional | Formal improvement plan required; 90-day review |
| 1.5 - 2.4 | Probation | Escalate to leadership; begin sourcing alternatives |
| 1.0 - 1.4 | Exit | Initiate vendor transition plan; do not renew |

---

## Output Format

Deliver the scorecard as a structured document:

```markdown
# Sourcing Scorecard — [Vendor Name]

**Category:** [Product/Service Category]
**Evaluation Period:** [Start Date] to [End Date]
**Prepared by:** [Name]
**Date:** [Date]

---

## 1. Scorecard Summary
| Dimension | Weight | Score | Weighted Score | Status |
|---|---|---|---|---|
[Dimension scores with green/yellow/red status]
| **Overall** | **100%** | | **X.X / 5.0** | **[Rating]** |

## 2. Detailed Metrics
[Each dimension with individual metric scores, targets, actuals, and evidence]

## 3. Trend Analysis
[Multi-period comparison table with trajectory commentary]

## 4. Strengths and Improvement Areas
- **Strengths:** [Top performing dimensions with evidence]
- **Improvement Areas:** [Below-target dimensions with root cause]

## 5. Action Plan
[Required actions based on overall score tier]

## 6. Vendor Response (if applicable)
[Space for vendor acknowledgment and improvement commitments]
```

---

## Quality Checklist

- [ ] All metrics have clearly defined data sources and measurement methods
- [ ] Targets are realistic and benchmarked against industry standards
- [ ] Scoring is based on actual data, not subjective impressions
- [ ] Trend analysis covers at least 2 prior periods for context
- [ ] Weighted scores sum correctly (verify the arithmetic)
- [ ] Action tier matches the overall score without manual override
- [ ] The scorecard has been reviewed with the vendor (or is ready for sharing)
- [ ] Improvement areas include specific, measurable corrective actions
- [ ] Data collection dates and sources are documented for auditability

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| New vendor with no historical data | Score current period only; mark trend as "Baseline"; set 2-quarter probation review |
| Vendor provides a single critical component | Weight quality and delivery higher; reduce innovation weight; note dependency risk |
| Data is unavailable for a metric | Mark as "N/A" with explanation; do not zero-fill; adjust dimension weight proportionally |
| Vendor disputes a score | Document the dispute; review raw data together; adjust if evidence supports change |
| Multiple business units use the same vendor | Aggregate scores across units or produce separate scorecards per engagement |
| Vendor underwent a merger or acquisition | Reset baseline; treat as a new evaluation cycle; note organizational change risk |
| Seasonal performance variation | Use rolling averages rather than single-period snapshots; note seasonality factors |
