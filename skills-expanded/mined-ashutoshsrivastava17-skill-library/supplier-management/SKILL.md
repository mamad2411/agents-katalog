---
name: supplier-management
description: >
  Manage supplier relationships through performance scorecards, capacity assessment, risk profiling,
  contract compliance monitoring, and supplier development plans.
  TRIGGER when: user says /supplier-management, "manage suppliers", "supplier scorecard", "vendor management", "supplier review", "supplier performance".
argument-hint: "[supplier-name] [category] [review-period]"
user-invocable: true
---

# Supplier Management

Build resilient, high-performing supplier relationships through structured evaluation, risk management, and continuous development.

---

## Input Gathering

| Input                        | Description                                                    | Required |
|------------------------------|----------------------------------------------------------------|----------|
| Supplier master list         | Name, category, spend tier, location, contact details          | Yes      |
| Purchase order data          | PO history with delivery dates, quantities, quality records    | Yes      |
| Contract terms               | Pricing, SLAs, penalty clauses, renewal dates                  | Yes      |
| Quality data                 | Defect rates, inspection results, CAPA records                 | Yes      |
| Supplier self-assessment     | Financial health, capacity utilization, certifications         | No       |
| Market intelligence          | Alternative suppliers, commodity pricing trends                | No       |
| Strategic priorities         | Innovation goals, sustainability requirements, localization    | No       |

---

## Step-by-Step Process

### Step 1 — Supplier Segmentation

Classify suppliers into tiers to allocate management effort appropriately:

| Tier       | Criteria                                     | Supplier Count | Management Model            |
|------------|----------------------------------------------|----------------|-----------------------------|
| Strategic  | High spend, high impact, few alternatives    | ~5-10%         | Executive sponsorship, QBRs |
| Preferred  | Significant spend, good alternatives exist   | ~15-20%        | Regular reviews, scorecards |
| Approved   | Moderate spend, commodity items              | ~30-40%        | Periodic audits, KPI tracking|
| Transactional | Low spend, easily substitutable           | ~30-50%        | Automated monitoring only   |

Use a 2x2 matrix of supply risk (vertical) vs. profit impact (horizontal) following the Kraljic model to validate segmentation.

### Step 2 — Performance Scorecard

Score each supplier across five dimensions:

| Dimension          | Weight | Key Metrics                                           | Scale   |
|--------------------|--------|-------------------------------------------------------|---------|
| Quality            | 30%    | Defect rate (PPM), first-pass yield, CAPA closure time | 1-5     |
| Delivery           | 25%    | On-time in-full (OTIF), lead time adherence            | 1-5     |
| Cost               | 20%    | Price competitiveness, cost reduction YoY, invoice accuracy | 1-5 |
| Responsiveness     | 15%    | RFQ turnaround, issue resolution time, communication   | 1-5    |
| Innovation         | 10%    | New product contributions, process improvements, patents| 1-5    |

**Scoring guide**:
- 5 = Exceptional (top 10% benchmark)
- 4 = Exceeds expectations
- 3 = Meets expectations
- 2 = Below expectations (improvement plan required)
- 1 = Unacceptable (escalation or exit)

Calculate a weighted composite score. Track trends over 4+ quarters.

### Step 3 — Capacity Assessment

Evaluate each strategic and preferred supplier's capacity:

| Factor                     | Assessment Method                               | Red Flag Threshold        |
|----------------------------|-------------------------------------------------|---------------------------|
| Utilization rate           | Self-reported + on-site verification             | > 85% sustained           |
| Financial health           | Credit reports, financial statements, Z-score    | Z-score < 1.8             |
| Workforce stability        | Turnover rate, key-person dependency             | Turnover > 25%            |
| Capital investment         | CAPEX plans, equipment age, technology roadmap    | No investment in 24 mo    |
| Scalability                | Can they handle 1.5x and 2x current volume?      | Cannot scale 1.5x in 90d |
| Sub-tier dependencies      | Mapping of their critical suppliers               | Single-source sub-tier    |

Flag suppliers approaching capacity ceilings and plan alternatives proactively.

### Step 4 — Risk Profiling

Build a risk register for each strategic supplier:

| Risk Category       | Indicators                                      | Probability | Impact | Score |
|----------------------|-------------------------------------------------|-------------|--------|-------|
| Financial failure    | Declining margins, high leverage, late payments  | L/M/H       | L/M/H  | 1-25  |
| Operational disruption| Single site, aging equipment, labor issues      | L/M/H       | L/M/H  | 1-25  |
| Geographic risk      | Natural disaster zone, political instability     | L/M/H       | L/M/H  | 1-25  |
| Compliance risk      | Regulatory changes, certification lapses         | L/M/H       | L/M/H  | 1-25  |
| Cyber / data risk    | IT maturity, data handling practices             | L/M/H       | L/M/H  | 1-25  |
| Reputational risk    | ESG violations, labor practices, media exposure  | L/M/H       | L/M/H  | 1-25  |

Assign a composite risk score and define risk mitigation actions for any supplier scoring above the threshold.

### Step 5 — Contract Compliance Monitoring

Audit contract adherence systematically:

- **Pricing compliance**: Compare invoiced prices to contracted rates; flag variance > 2%.
- **SLA adherence**: Track OTIF, quality, and responsiveness against contractual minimums.
- **Volume commitments**: Monitor actual spend vs. committed volumes (both buyer and supplier side).
- **Penalty / rebate triggers**: Identify whether penalty or rebate thresholds have been reached.
- **Renewal and termination dates**: Maintain a 12-month forward calendar of contract milestones.
- **Regulatory compliance**: Verify certifications (ISO, FDA, SOC2, etc.) remain current.

### Step 6 — Development Plans and Relationship Governance

For strategic and underperforming suppliers, create a Supplier Development Plan:

| Plan Component            | Detail                                              |
|---------------------------|-----------------------------------------------------|
| Performance gap           | Specific KPIs that need improvement, with targets   |
| Root cause                | Joint analysis of why performance is lagging         |
| Improvement actions       | Concrete steps with owner and due date              |
| Support offered           | Training, process engineering, co-investment         |
| Review cadence            | Weekly for critical gaps, monthly for standard       |
| Exit criteria             | Conditions under which the relationship is terminated|

Establish governance rhythms: quarterly business reviews for strategic suppliers, annual reviews for preferred, audit cycle for approved.

---

## Output Format

```
## Supplier Management Review — [Category/Supplier] — [Period]

### Executive Summary
- Suppliers reviewed: [count] across [categories]
- Average composite score: [X/5] (prior period: [Y/5])
- High-risk suppliers identified: [count]
- Contract compliance rate: [%]

### Supplier Segmentation
| Tier          | Count | Total Spend   | Avg Score |
|---------------|-------|---------------|-----------|
| Strategic     | ...   | ...           | ...       |
| Preferred     | ...   | ...           | ...       |
| Approved      | ...   | ...           | ...       |
| Transactional | ...   | ...           | ...       |

### Performance Scorecards (Strategic Suppliers)
| Supplier | Quality | Delivery | Cost | Responsive | Innovation | Composite | Trend |
|----------|---------|----------|------|------------|------------|-----------|-------|
| ...      | ...     | ...      | ...  | ...        | ...        | ...       | ...   |

### Risk Register (High-Risk Items)
| Supplier | Risk Category | Score | Mitigation Action | Owner | Due Date |
|----------|---------------|-------|-------------------|-------|----------|
| ...      | ...           | ...   | ...               | ...   | ...      |

### Contract Compliance Summary
| Supplier | Pricing | SLA | Volume | Certifications | Overall |
|----------|---------|-----|--------|----------------|---------|
| ...      | ...     | ... | ...    | ...            | ...     |

### Development Plans
- [Supplier A]: [Gap] -> [Target] by [Date]
- [Supplier B]: ...

### Recommendations
1. [Prioritized action items]
```

---

## Quality Checklist

- [ ] Supplier segmentation reflects current spend and risk landscape
- [ ] Scorecard metrics are objective, measurable, and consistently applied
- [ ] Performance data covers at least the trailing 12 months
- [ ] Capacity assessment includes financial health and sub-tier mapping
- [ ] Risk register updated with current geopolitical and market conditions
- [ ] Contract compliance audit covers pricing, SLAs, and certifications
- [ ] Development plans have specific targets, owners, and deadlines
- [ ] Governance cadence defined and calendar invites issued
- [ ] Results communicated to procurement, quality, and operations stakeholders
- [ ] Supplier feedback collected and incorporated into the process

---

## Edge Cases

- **Sole-source supplier with no alternative**: Maintain the relationship carefully; invest in dual-qualification of a backup; negotiate longer-term contracts with performance guarantees and buffer stock agreements.
- **Supplier in financial distress**: Increase monitoring frequency to weekly; secure inventory buffers; accelerate qualification of alternatives; consider advance payments tied to performance milestones.
- **Mergers and acquisitions affecting suppliers**: Reassess capacity, risk, and contract terms post-transaction; validate that certifications and capabilities transfer to the new entity.
- **Supplier in a sanctioned or high-risk country**: Engage legal and compliance teams; ensure trade compliance; evaluate reshoring or near-shoring alternatives.
- **Rapid scale-up requirement**: Pre-negotiate surge capacity clauses; maintain a qualified backup list; consider consignment stock arrangements for critical components.
- **Supplier refusing transparency on sub-tier suppliers**: Escalate through contract provisions; make sub-tier visibility a condition of preferred status; conduct independent supply chain mapping.
