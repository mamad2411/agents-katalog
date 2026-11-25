---
name: financial-projection
description: "Builds 12-month financial projections with revenue scenarios, expense forecasting, and break-even analysis. Use when planning future revenue and expenses for your business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Financial Projection

## When to Use This Skill

Use this skill when you need to:
- Build a 12-month financial projection for a business
- Model revenue growth scenarios (conservative, base, optimistic)
- Forecast expenses and identify when you reach profitability
- Create projections for investor pitches, loan applications, or strategic planning

**DO NOT** use this skill for monthly budgeting (use budget-planner), real-time financial reporting, or personal finance planning. This is for forward-looking business financial models.

---

## Core Principle

PROJECTIONS ARE NOT PREDICTIONS — THEY ARE STRUCTURED ASSUMPTIONS THAT HELP YOU MAKE DECISIONS TODAY BASED ON WHERE THE NUMBERS COULD GO.

---

## Phase 1: Baseline Data

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Current monthly revenue** | "What is your current monthly revenue?" | No default — must be provided |
| **Revenue model** | "How do you make money? (subscriptions, one-time sales, retainers, hourly)" | One-time sales |
| **Current monthly expenses** | "What are your total monthly expenses?" | No default — must be provided |
| **Growth rate assumption** | "What monthly growth rate do you expect? (or historical growth if available)" | 5-10% month-over-month |
| **Planned investments** | "Any major expenses planned? (hires, equipment, marketing spend)" | None |
| **Projection purpose** | "What is this for? (internal planning, investors, loan, strategic)" | Internal planning |

**GATE: Do not proceed without current revenue, expenses, and revenue model.**

---

## Phase 2: Revenue Projection

### Three Scenarios

Build projections for conservative, base, and optimistic scenarios:

```
## Revenue Projection: 12-Month Outlook

### Assumptions
- Base monthly growth rate: [X]%
- Conservative: [X-2]% monthly growth
- Optimistic: [X+3]% monthly growth
- Starting monthly revenue: $[X]

### Monthly Revenue by Scenario

| Month | Conservative | Base | Optimistic |
|-------|-------------|------|------------|
| Month 1 | $[X] | $[X] | $[X] |
| Month 2 | $[X] | $[X] | $[X] |
| ... | | | |
| Month 12 | $[X] | $[X] | $[X] |
| **Annual Total** | **$[X]** | **$[X]** | **$[X]** |
```

### Revenue Drivers

Break revenue into its component drivers:

```
### Revenue Driver Breakdown (Base Case)

| Driver | Month 1 | Month 6 | Month 12 |
|--------|---------|---------|----------|
| [Product/service 1] units | [X] | [X] | [X] |
| [Product/service 1] revenue | $[X] | $[X] | $[X] |
| [Product/service 2] units | [X] | [X] | [X] |
| [Product/service 2] revenue | $[X] | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** | **$[X]** |
```

---

## Phase 3: Expense Forecast

### Expense Categories

```
## Expense Projection

### Fixed Expenses (Monthly)
| Category | Current | Month 6 | Month 12 | Notes |
|----------|---------|---------|----------|-------|
| [Rent/workspace] | $[X] | $[X] | $[X] | |
| [Software] | $[X] | $[X] | $[X] | |
| [Insurance] | $[X] | $[X] | $[X] | |

### Variable Expenses (Scale with Revenue)
| Category | % of Revenue | Month 1 | Month 6 | Month 12 |
|----------|-------------|---------|---------|----------|
| [COGS] | [X]% | $[X] | $[X] | $[X] |
| [Marketing] | [X]% | $[X] | $[X] | $[X] |
| [Contractors] | [X]% | $[X] | $[X] | $[X] |

### Planned Step-Up Costs
| Investment | Month | Monthly Cost | Purpose |
|-----------|-------|-------------|---------|
| [New hire] | Month [X] | $[X] | [Rationale] |
| [Tool upgrade] | Month [X] | $[X] | [Rationale] |
```

---

## Phase 4: Profit and Loss Summary

### Monthly P&L

```
## Projected Profit & Loss (Base Case)

| | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 |
|--|----|----|----|----|----|----|----|----|----|----|-----|-----|
| Revenue | | | | | | | | | | | | |
| COGS | | | | | | | | | | | | |
| Gross Profit | | | | | | | | | | | | |
| Operating Expenses | | | | | | | | | | | | |
| **Net Profit** | | | | | | | | | | | | |
| Cumulative P&L | | | | | | | | | | | | |

### Break-Even Point
- Break-even month: Month [X] (base case)
- Monthly revenue needed to break even: $[X]
- Monthly units needed to break even: [X]
```

### Key Metrics Over Time

```
### Financial Health Metrics

| Metric | Month 1 | Month 6 | Month 12 |
|--------|---------|---------|----------|
| Gross margin | [X]% | [X]% | [X]% |
| Net margin | [X]% | [X]% | [X]% |
| Monthly burn rate | $[X] | $[X] | $[X] |
| Cash runway (months) | [X] | [X] | [X] |
```

---

## Example: SaaS Product Launch

**Inputs:** Current MRR $2,000, base growth 12%/month, expenses $4,500/month, hiring a VA in month 4 at $2,000/month.

**Result (Base Case):** Break-even at month 5. Month 12 MRR: $6,930. Annual revenue: $48,400. Net profit months 5-12: $11,200.

---

## Anti-Patterns

- **Hockey stick projections without justification** — 50% monthly growth needs a specific driver, not optimism
- **Ignoring step-up costs** — revenue growth triggers new expenses (more support, infrastructure, team). Model these.
- **Single scenario only** — always model at least conservative and base. Stakeholders need to see the range.
- **Projecting revenue without unit economics** — "we will make $100K" is not a projection. Show the units, prices, and conversion rates that produce $100K.
- **Forgetting taxes** — include estimated tax liability in the expense forecast

---

## Recovery

- **Pre-revenue business:** Start with zero revenue and model from first sale. Focus on expense runway — how many months until the money runs out?
- **Highly variable revenue:** Use the lowest 3 months as the conservative base. Model seasonality if applicable.
- **No growth rate data:** Use industry benchmarks or model flat revenue as conservative, 5% as base, 10% as optimistic.
- **Projections for investors:** Add a "key assumptions" section listing every assumption and its source. Investors stress-test assumptions, not numbers.
