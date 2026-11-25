---
name: financial-modeling
description: >
  Build financial models — assumption documentation, revenue/cost drivers,
  scenario toggles, sensitivity tables, and model validation.
  TRIGGER when: user says /financial-modeling, needs to build a financial model,
  or asks about forecasting and scenario analysis.
argument-hint: "[business or project to model]"
user-invocable: true
---

# Financial Modeling

## Process

### Step 1: Define Model Purpose
| Purpose | Type | Complexity |
|---------|------|-----------|
| Fundraising | 3-statement + projections | High |
| Project evaluation | DCF / NPV | Medium |
| Budget planning | Revenue + expense forecast | Medium |
| Scenario analysis | Toggle-based projections | Medium |

### Step 2: Document Assumptions
| Category | Assumption | Source | Sensitivity |
|----------|-----------|--------|------------|
| Revenue growth | X% YoY | Historical + market | High |
| Gross margin | X% | Last 4 quarters | Medium |
| CAC | $X | Last 12 months | High |
| Churn rate | X% monthly | Cohort analysis | High |

### Step 3: Build Revenue Model
| Driver | Formula | Y1 | Y2 | Y3 |
|--------|---------|-----|-----|-----|
| New customers | Spend / CAC | X | X | X |
| Churned | Base × churn | X | X | X |
| Revenue | Customers × ARPU | $X | $X | $X |

### Step 4: Build Cost Model
| Category | Type | Driver | Y1 | Y2 | Y3 |
|----------|------|--------|-----|-----|-----|
| COGS | Variable | Revenue × margin | $X | $X | $X |
| Engineering | Semi-fixed | Headcount × salary | $X | $X | $X |
| S&M | Variable | CAC × new | $X | $X | $X |

### Step 5: Add Scenarios
| Scenario | Growth | Churn | Burn Rate |
|----------|--------|-------|-----------|
| Bear | X% | X% | $X/mo |
| Base | X% | X% | $X/mo |
| Bull | X% | X% | $X/mo |

### Step 6: Validate
| Check | Method |
|-------|--------|
| Formula audit | Trace to source |
| Sense check | Match industry benchmarks |
| Stress test | Extreme inputs |
| Historical fit | Replicate actuals |

## Output Format
```markdown
## Model: [Name]
### Assumptions: [table]
### Projections: [3-5 year summary]
### Scenarios: [Bear/Base/Bull]
### Sensitivity: [key drivers]
```

## Quality Checklist
- [ ] Assumptions documented with sources
- [ ] Formulas reference assumptions (no hardcoded numbers)
- [ ] Scenarios toggleable
- [ ] Stress-tested
- [ ] Balance sheet balances (if applicable)

## Edge Cases
- For SaaS, model MRR/ARR with cohort-based churn
- For marketplaces, model both supply and demand sides
- For fundraising, include dilution impact
