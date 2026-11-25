---
name: commission-structure
description: "Designs sales commission structures with tiers, accelerators, clawback provisions, and payout schedules. Use when creating or revising compensation plans for sales roles."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Commission Structure

## When to Use This Skill

Use this skill when you need to:
- Design a commission plan for sales representatives or affiliates
- Create tiered commission structures with accelerators
- Define clawback provisions and payout schedules
- Build a compensation plan that aligns incentives with business goals

**DO NOT** use this skill for employee salary planning, freelance rate cards, or affiliate program terms (use affiliate-terms). This is for sales commission design.

---

## Core Principle

A COMMISSION STRUCTURE SHOULD MAKE THE REP'S HIGHEST-EARNING BEHAVIOR IDENTICAL TO THE COMPANY'S HIGHEST-VALUE OUTCOME.

---

## Phase 1: Business Context

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Sales model** | "What are you selling? (SaaS, services, products, one-time, recurring)" | No default — must be provided |
| **Average deal size** | "What is your average sale/contract value?" | No default — must be provided |
| **Sales cycle length** | "How long from first contact to close?" | 30 days |
| **Gross margin** | "What is your gross margin on sales?" | 60% |
| **Target OTE** | "What total compensation (base + commission) should a rep earn?" | $75,000 |
| **Base/variable split** | "What split between base salary and variable commission?" | 50/50 |
| **Quota period** | "Monthly or quarterly quotas?" | Monthly |

**GATE: Do not proceed without sales model, deal size, and target OTE.**

---

## Phase 2: Structure Design

### Commission Model Options

```
## Commission Structure: [Company Name]

### Model Selection

| Model | Best For | Complexity |
|-------|----------|-----------|
| Flat percentage | Simple products, early stage | Low |
| Tiered (increasing %) | Motivating overperformance | Medium |
| Tiered with accelerators | SaaS, enterprise sales | High |
| Revenue share | Recurring revenue, partnerships | Medium |
| Gross margin-based | Services with variable margins | Medium |

### Selected Model: [Tiered with Accelerators]
```

### Commission Table

```
### Commission Rates

| Quota Attainment | Commission Rate | Example Payout |
|-----------------|----------------|---------------|
| 0-50% of quota | [X]% (base rate) | $[X] |
| 51-100% of quota | [X]% (standard rate) | $[X] |
| 101-125% of quota | [X]% (accelerator 1) | $[X] |
| 126-150% of quota | [X]% (accelerator 2) | $[X] |
| 150%+ of quota | [X]% (kicker) | $[X] |

### Quota
- Monthly quota: $[X] in [revenue / bookings / closed deals]
- Quarterly quota: $[X]
- Annual quota: $[X]

### OTE Breakdown
| Component | Amount | % of OTE |
|-----------|--------|---------|
| Base salary | $[X]/month | [50]% |
| Target variable (at 100% quota) | $[X]/month | [50]% |
| **Total OTE** | **$[X]/month** | **100%** |
```

---

## Phase 3: Rules and Provisions

### Clawback and Recovery

```
### Clawback Provisions

| Scenario | Clawback Rule |
|----------|--------------|
| Customer cancels within [30] days | 100% commission clawback |
| Customer cancels within [31-90] days | 50% commission clawback |
| Customer fails to pay | Commission reversed upon chargeback/nonpayment |
| Fraudulent sale | 100% clawback + disciplinary action |

### Payment Schedule
- Commission calculated: [End of each month]
- Commission paid: [15th of the following month]
- Clawback window: [90 days from sale date]
- Minimum payout threshold: $[50]
```

### Special Rules

```
### Additional Provisions

**New rep ramp:** [X]-month ramp with reduced quota
- Month 1: [50]% quota, full commission rate
- Month 2: [75]% quota, full commission rate
- Month 3+: Full quota

**Team deals:** If two reps collaborate, commission is split [50/50 or based on contribution].

**Renewals:** [X]% commission on customer renewals (typically lower than new business rate).

**Upsells/expansion:** Treated as [new business / renewal rate] depending on [criteria].

**Spiffs (bonuses):** $[X] bonus for [specific behavior — multi-year deals, strategic accounts, new product sales].
```

---

## Phase 4: Documentation

### Commission Plan Document

```
## [Company] Sales Commission Plan — [Year]

### Plan Summary
- Effective date: [Date]
- Plan period: [Annual / Quarterly]
- Eligible roles: [List]
- Changes from prior plan: [List or "New plan"]

### Compensation Structure
[Insert tables from Phase 2]

### Rules and Provisions
[Insert from Phase 3]

### Dispute Resolution
Commission disputes must be submitted in writing within [30] days
of the commission statement. Resolution within [15] business days.

### Plan Modifications
Company reserves the right to modify the plan with [30] days notice.
Changes do not affect commissions already earned.

### Acknowledgment
Employee signature: _______________
Date: _______________
```

---

## Example: SaaS Company (ACV $12,000)

**OTE:** $90K ($45K base + $45K variable). Monthly quota: $40K in new ARR.

| Attainment | Rate | Payout on $40K |
|-----------|------|---------------|
| 0-75% | 5% | Up to $1,500 |
| 76-100% | 10% | $1,500-$2,500 |
| 101-125% | 15% | $2,500-$4,375 |
| 125%+ | 20% | $4,375+ uncapped |

At 100% quota: $3,750/month variable = $45K annual. Clawback: 100% if churn in 60 days.

---

## Anti-Patterns

- **Capped commissions** — caps kill motivation once a rep hits quota. Top performers stop selling. Leave upside uncapped.
- **Commissions on revenue without margin consideration** — reps will discount to close. Tie commission to margin or set discount approval thresholds.
- **No clawback provision** — without clawbacks, reps have no incentive to ensure deal quality
- **Changing the plan mid-period** — destroys trust. Only change plans at period boundaries with advance notice.
- **Overly complex structures** — if a rep cannot calculate their own commission on a napkin, the plan is too complex.

---

## Recovery

- **Cannot afford base salary (solo founder):** Use commission-only with higher rates (15-25%). Attract with uncapped earnings potential and leads provided.
- **Reps gaming the system:** Identify which behavior is being incentivized that you did not intend. Adjust the structure to align incentives.
- **High churn on commissioned deals:** Implement or extend clawback windows. Add a quality bonus for deals that retain beyond 6 months.
- **Transition from one plan to another:** Honor all deals in the pipeline under the old plan. New plan applies to new opportunities only.
