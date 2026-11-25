---
name: financial-model
description: "Builds financial models for startups with revenue drivers, cost assumptions, and sensitivity analysis. Use when creating detailed financial models for fundraising or planning."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Financial Model

## When to Use This Skill

Use this skill when you need to:
- Build a bottoms-up financial model for a startup or small business
- Create investor-ready financial projections with detailed assumptions
- Model revenue drivers, unit economics, and cash flow
- Run sensitivity analysis on key business assumptions

**DO NOT** use this skill for simple budgets (use budget-planner) or basic revenue forecasts (use revenue-forecast). This is for comprehensive financial models with multiple interconnected assumptions.

---

## Core Principle

A FINANCIAL MODEL IS ONLY AS GOOD AS ITS ASSUMPTIONS — EVERY NUMBER MUST TRACE BACK TO A STATED ASSUMPTION THAT CAN BE CHALLENGED, TESTED, AND UPDATED.

---

## Phase 1: Model Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business model** | "How do you make money? (SaaS, e-commerce, services, marketplace)" | No default — must be provided |
| **Revenue streams** | "What are your revenue sources and pricing?" | No default — must be provided |
| **Current metrics** | "Current MRR, users, conversion rates, churn?" | Pre-revenue if not provided |
| **Cost structure** | "Fixed costs, variable costs, planned hires?" | Will build from scratch |
| **Model timeframe** | "12, 24, or 36 months?" | 24 months |
| **Model purpose** | "Who is this for? (internal planning, seed raise, Series A)" | Internal planning |

**GATE: Do not proceed without business model and revenue stream details.**

---

## Phase 2: Assumptions Sheet

Every model starts with a documented assumptions sheet.

```
## Key Assumptions

### Revenue Assumptions
| Assumption | Value | Source/Rationale |
|-----------|-------|-----------------|
| Starting MRR | $[X] | Current |
| Monthly user growth rate | [X]% | [Based on: historical, benchmark, or target] |
| Conversion rate (trial to paid) | [X]% | [Source] |
| Average revenue per user (ARPU) | $[X] | [Current pricing] |
| Monthly churn rate | [X]% | [Historical or industry benchmark] |
| Expansion revenue rate | [X]% | [Upsell/cross-sell estimate] |

### Cost Assumptions
| Assumption | Value | Source/Rationale |
|-----------|-------|-----------------|
| Customer acquisition cost (CAC) | $[X] | [Current or estimated] |
| Gross margin | [X]% | [Based on COGS breakdown] |
| Monthly fixed costs (current) | $[X] | [Actual] |
| Planned hires | [X] people by month [X] | [Hiring plan] |
| Average fully-loaded salary | $[X]/month | [Market rate] |
| Marketing spend (% of revenue) | [X]% | [Target] |
```

**GATE: Present assumptions to the user for validation before building the model.**

---

## Phase 3: Model Build

### Revenue Model (Bottoms-Up)

```
## Revenue Model

### Monthly Cohort Model
| Month | New Users | Churned | Active Users | MRR | Expansion | Total MRR |
|-------|----------|---------|-------------|-----|-----------|-----------|
| M1 | [X] | [X] | [X] | $[X] | $[X] | $[X] |
| M2 | [X] | [X] | [X] | $[X] | $[X] | $[X] |
| ... | | | | | | |
| M24 | [X] | [X] | [X] | $[X] | $[X] | $[X] |

### Annual Revenue Summary
| | Year 1 | Year 2 |
|--|--------|--------|
| ARR (ending) | $[X] | $[X] |
| Total Revenue | $[X] | $[X] |
| YoY Growth | — | [X]% |
```

### Expense Model

```
## Expense Model

### Monthly Expense Breakdown
| Category | M1 | M6 | M12 | M18 | M24 |
|----------|----|----|-----|-----|-----|
| COGS | $[X] | $[X] | $[X] | $[X] | $[X] |
| Personnel | $[X] | $[X] | $[X] | $[X] | $[X] |
| Marketing | $[X] | $[X] | $[X] | $[X] | $[X] |
| G&A | $[X] | $[X] | $[X] | $[X] | $[X] |
| **Total Opex** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

### Headcount Plan
| Role | Start Month | Monthly Cost | Purpose |
|------|------------|-------------|---------|
| [Role] | M[X] | $[X] | [Why needed] |
```

### Cash Flow and Runway

```
## Cash Flow

| | M1 | M6 | M12 | M18 | M24 |
|--|----|----|-----|-----|-----|
| Revenue | $[X] | $[X] | $[X] | $[X] | $[X] |
| Expenses | $[X] | $[X] | $[X] | $[X] | $[X] |
| Net Cash Flow | $[X] | $[X] | $[X] | $[X] | $[X] |
| Cash Balance | $[X] | $[X] | $[X] | $[X] | $[X] |
| Runway (months) | [X] | [X] | [X] | [X] | [X] |

**Break-even month:** M[X]
**Cash needed to reach break-even:** $[X]
```

---

## Phase 4: Sensitivity Analysis

### Key Variable Sensitivity

```
## Sensitivity Analysis

### Impact of Growth Rate Changes on M24 ARR
| Growth Rate | M24 ARR | M24 Runway |
|------------|---------|-----------|
| [Base - 3%] | $[X] | [X] months |
| [Base rate] | $[X] | [X] months |
| [Base + 3%] | $[X] | [X] months |

### Impact of Churn Rate on M24 ARR
| Churn Rate | M24 ARR | LTV |
|-----------|---------|-----|
| [Base - 1%] | $[X] | $[X] |
| [Base rate] | $[X] | $[X] |
| [Base + 1%] | $[X] | $[X] |

### Unit Economics Summary
| Metric | Value |
|--------|-------|
| CAC | $[X] |
| LTV | $[X] |
| LTV:CAC | [X]:1 |
| Payback period | [X] months |
| Gross margin | [X]% |
```

---

## Example: SaaS Startup Seed Stage

**Inputs:** $5K MRR, $29/mo ARPU, 8% monthly user growth, 3.5% monthly churn, $120 CAC, $8K/mo fixed costs.

**M12 projection:** $14.2K MRR, 490 active users, $10.5K monthly expenses, break-even at month 9.
**M24 projection:** $38.6K MRR, 1,330 active users, $18K monthly expenses (added 2 hires), $12K net monthly cash flow.

**Sensitivity:** If churn increases to 5%, M24 ARR drops 32%. If growth decreases to 5%, M24 ARR drops 41%. Growth rate is the most sensitive variable.

---

## Anti-Patterns

- **Top-down models** — "we will capture 1% of a $10B market" is not a financial model. Build bottoms-up from unit economics.
- **Static assumptions** — costs and growth rates change over time. Model step changes in hiring, pricing, and growth.
- **No assumptions documentation** — every number must have a rationale. Undocumented assumptions cannot be validated.
- **Ignoring churn** — for subscription businesses, churn is the most important variable. A 1% difference in monthly churn dramatically changes 24-month outcomes.
- **Perfect hockey sticks** — real growth is lumpy. Include realistic ramp-up periods for new channels and hires.

---

## Recovery

- **Pre-revenue business:** Model from first customer acquisition. State assumptions clearly and emphasize the sensitivity analysis — investors know the numbers are uncertain.
- **No historical data for assumptions:** Use industry benchmarks and clearly label them. Update the model monthly as real data replaces assumptions.
- **Model too complex:** If the user is overwhelmed, simplify to revenue, expenses, and cash flow. Add complexity as they get comfortable.
- **Numbers do not work:** Show which assumptions need to change for the model to work — higher ARPU, lower churn, faster growth, or lower costs. Let the user decide which lever to pull.
