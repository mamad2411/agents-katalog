---
name: cost-analysis
description: "Performs cost-of-goods-sold and cost-per-unit analyses with margin calculations and optimization recommendations. Use when analyzing product or service costs."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Cost Analysis

## When to Use This Skill

Use this skill when you need to:
- Calculate the true cost to produce and deliver a product or service
- Determine per-unit costs, gross margins, and contribution margins
- Identify cost reduction opportunities without sacrificing quality
- Build a cost structure for pricing decisions or investor presentations

**DO NOT** use this skill for budgeting (use budget-planner), pricing strategy (use pricing-strategy), or financial projections. This is specifically for understanding and optimizing your cost structure.

---

## Core Principle

YOU CANNOT OPTIMIZE WHAT YOU HAVE NOT MEASURED — EVERY COST MUST BE IDENTIFIED, CATEGORIZED, AND ASSIGNED TO A UNIT BEFORE MARGIN IMPROVEMENTS ARE POSSIBLE.

---

## Phase 1: Cost Inventory

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product/service** | "What product or service are we analyzing costs for?" | No default — must be provided |
| **Selling price** | "What do you sell it for?" | No default — must be provided |
| **Monthly units sold** | "How many units do you sell per month?" | No default — must be provided |
| **Known direct costs** | "What costs go directly into making/delivering this? (materials, labor, tools)" | No default — list all |
| **Overhead costs** | "What are your monthly fixed business costs? (rent, software, insurance)" | Will estimate if unknown |

**GATE: Do not proceed without the product, selling price, and at least some cost data.**

---

## Phase 2: Cost Breakdown

### Direct Costs (COGS)

```
## Direct Cost Analysis: [Product/Service]

| Cost Component | Cost Per Unit | % of Price | Notes |
|---------------|--------------|-----------|-------|
| [Raw materials / supplies] | $[X] | [X]% | |
| [Direct labor (hours x rate)] | $[X] | [X]% | |
| [Platform/transaction fees] | $[X] | [X]% | |
| [Packaging / delivery] | $[X] | [X]% | |
| [Third-party services] | $[X] | [X]% | |
| **Total Direct Cost** | **$[X]** | **[X]%** | |
```

### Indirect Costs (Overhead Allocation)

```
## Overhead Allocation

| Overhead Category | Monthly Cost | Per Unit (÷ monthly units) |
|------------------|-------------|--------------------------|
| [Software/tools] | $[X] | $[X] |
| [Workspace/rent] | $[X] | $[X] |
| [Insurance] | $[X] | $[X] |
| [Marketing (allocated)] | $[X] | $[X] |
| [Admin/bookkeeping] | $[X] | $[X] |
| **Total Overhead/Unit** | | **$[X]** |
```

### Margin Calculations

```
## Margin Analysis

| Metric | Amount | Percentage |
|--------|--------|-----------|
| Selling price | $[X] | 100% |
| Direct costs (COGS) | $[X] | [X]% |
| **Gross profit** | **$[X]** | **[X]%** |
| Overhead per unit | $[X] | [X]% |
| **Net profit per unit** | **$[X]** | **[X]%** |

### At Current Volume ([X] units/month)
| Metric | Monthly | Annual |
|--------|---------|--------|
| Revenue | $[X] | $[X] |
| Total COGS | $[X] | $[X] |
| Gross profit | $[X] | $[X] |
| Total overhead | $[X] | $[X] |
| **Net profit** | **$[X]** | **$[X]** |
```

---

## Phase 3: Optimization

### Cost Reduction Opportunities

```
## Cost Optimization Recommendations

| Opportunity | Current Cost | Potential Cost | Savings/Unit | Effort |
|------------|-------------|---------------|-------------|--------|
| [Bulk purchasing] | $[X] | $[X] | $[X] | Low |
| [Supplier negotiation] | $[X] | $[X] | $[X] | Medium |
| [Process automation] | $[X] | $[X] | $[X] | High |
| [Material substitution] | $[X] | $[X] | $[X] | Medium |
```

### Volume Sensitivity

Show how costs change at different volumes:

```
## Volume Impact on Unit Economics

| Volume | Direct Cost/Unit | Overhead/Unit | Total Cost/Unit | Margin |
|--------|-----------------|---------------|----------------|--------|
| [Current] | $[X] | $[X] | $[X] | [X]% |
| [2x current] | $[X] | $[X] | $[X] | [X]% |
| [5x current] | $[X] | $[X] | $[X] | [X]% |
```

---

## Phase 4: Deliverable

Present the complete cost analysis with a summary recommendation.

```
## Summary

**Product:** [Name]
**True cost per unit:** $[X] (including overhead allocation)
**Current margin:** [X]%
**Target margin:** [X]%
**Top 3 cost reduction actions:**
1. [Action] — saves $[X]/unit
2. [Action] — saves $[X]/unit
3. [Action] — saves $[X]/unit
```

---

## Example: Online Course

**Price:** $197. **Direct costs:** $3.50/sale (payment processing $5.91, hosting $0.50, email delivery $0.09, amortized creation cost $3/sale over 1,000 sales). **Overhead/unit:** $12 (based on $1,200/month overhead at 100 sales/month). **Total cost:** $15.50. **Margin:** 92%.

**Insight:** At 92% margin, focus on volume growth over cost reduction. The amortized creation cost drops as volume increases.

---

## Anti-Patterns

- **Ignoring time costs** — your time has a dollar value. If you spend 2 hours per unit and your time is worth $100/hour, that is $200 in cost.
- **Forgetting transaction fees** — payment processors, platform fees, and marketplace cuts are real costs. Include them.
- **Amortizing incorrectly** — one-time costs (product creation, equipment) should be spread over expected lifetime units, not charged to the first sale.
- **Overhead allocation without volume context** — overhead per unit changes dramatically with volume. Always show the volume assumption.
- **Optimizing costs that do not move the needle** — a $0.10/unit savings matters at 100K units. At 100 units, focus on margin and pricing instead.

---

## Recovery

- **User does not know all their costs:** Walk through each delivery step and identify costs at each stage. Hidden costs usually live in time, fees, and tools.
- **Negative margins:** Flag immediately. Show which costs must be reduced or what price increase is needed to reach positive margin.
- **Service business (hard to quantify per unit):** Define the "unit" as one client engagement, one project, or one month of service. Calculate costs against that unit.
- **Multiple products sharing overhead:** Allocate overhead proportionally by revenue or by units — state the method and be consistent.
