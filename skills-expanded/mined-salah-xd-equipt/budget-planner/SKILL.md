---
name: budget-planner
description: "Creates monthly and annual business budgets with category breakdowns, variance tracking, and adjustment triggers. Use when building or revising a business budget."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Budget Planner

## When to Use This Skill

Use this skill when you need to:
- Create a monthly or annual business budget from scratch
- Organize expenses into categories with allocation targets
- Build variance tracking to compare budget vs. actual spending
- Set up adjustment triggers for when spending goes off track

**DO NOT** use this skill for personal budgets, financial projections (use financial-projection), or investment planning. This is for operational business budgeting.

---

## Core Principle

A BUDGET IS A DECISION-MAKING TOOL, NOT A SPREADSHEET — EVERY LINE ITEM MUST TIE TO A BUSINESS PRIORITY AND HAVE A CLEAR OWNER.

---

## Phase 1: Business Snapshot

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Monthly revenue** | "What is your current or expected monthly revenue?" | No default — must be provided |
| **Business type** | "What type of business? (service, product, SaaS, consulting)" | Service-based |
| **Team size** | "How many people? (just you, contractors, employees)" | Solo with contractors |
| **Top 3 expense categories** | "What are your biggest costs?" | Software, marketing, contractors |
| **Budget period** | "Monthly or annual budget?" | Monthly |
| **Growth goals** | "Any planned investments or growth spending?" | None specified |

**GATE: Do not proceed without monthly revenue and business type.**

---

## Phase 2: Budget Framework

### Category Structure

Build the budget using these standard categories, adjusted for business type:

```
## Budget: [Business Name] — [Month/Year or Annual]

### Revenue
| Source | Budgeted | Notes |
|--------|----------|-------|
| [Primary revenue] | $[X] | |
| [Secondary revenue] | $[X] | |
| **Total Revenue** | **$[X]** | |

### Fixed Costs (Do not change month-to-month)
| Category | Budgeted | % of Revenue | Notes |
|----------|----------|-------------|-------|
| Rent/workspace | $[X] | [X]% | |
| Software/subscriptions | $[X] | [X]% | |
| Insurance | $[X] | [X]% | |
| Salaries (if applicable) | $[X] | [X]% | |
| **Total Fixed** | **$[X]** | **[X]%** | |

### Variable Costs (Scale with revenue)
| Category | Budgeted | % of Revenue | Notes |
|----------|----------|-------------|-------|
| Marketing/advertising | $[X] | [X]% | |
| Contractors/freelancers | $[X] | [X]% | |
| COGS/fulfillment | $[X] | [X]% | |
| Transaction fees | $[X] | [X]% | |
| **Total Variable** | **$[X]** | **[X]%** | |

### Growth Investments (Discretionary)
| Category | Budgeted | % of Revenue | Notes |
|----------|----------|-------------|-------|
| New tools/equipment | $[X] | [X]% | |
| Education/training | $[X] | [X]% | |
| Hiring | $[X] | [X]% | |
| **Total Growth** | **$[X]** | **[X]%** | |

### Summary
| | Amount | % of Revenue |
|--|--------|-------------|
| Total Revenue | $[X] | 100% |
| Total Expenses | $[X] | [X]% |
| **Net Profit** | **$[X]** | **[X]%** |
```

### Benchmark Allocations (Solopreneur/Small Business)

| Category | Healthy Range |
|----------|--------------|
| Fixed costs | 15-30% of revenue |
| Marketing | 5-15% of revenue |
| Contractors | 10-25% of revenue |
| Owner's pay | 30-50% of revenue |
| Profit reserve | 10-20% of revenue |
| Tax reserve | 25-30% of profit |

---

## Phase 3: Variance Tracking

### Monthly Tracking Template

```
## Variance Report: [Month]

| Category | Budgeted | Actual | Variance | % Variance |
|----------|----------|--------|----------|------------|
| [Category] | $[X] | $[X] | +/-$[X] | +/-[X]% |

### Variance Flags
🔴 Over budget by >15%: [List categories]
🟡 Over budget by 5-15%: [List categories]
🟢 On or under budget: [List categories]
```

### Adjustment Triggers

Define when to take action:

```
## Adjustment Triggers

| Trigger | Action |
|---------|--------|
| Revenue drops >10% from plan | Cut discretionary spending, pause growth investments |
| Any category exceeds budget by >20% | Review and reallocate or cut before next month |
| Revenue exceeds plan by >15% | Allocate surplus: 50% profit reserve, 30% growth, 20% owner bonus |
| Cash reserve drops below 2 months expenses | Freeze all non-essential spending |
| Marketing spend exceeds 15% without corresponding revenue increase | Audit campaign ROI, pause underperformers |
```

---

## Phase 4: Deliverable

Present the complete budget document and provide quarterly review reminders.

```
budget/
└── budget-[YYYY].md (or budget-[YYYY-MM].md for monthly)
```

Include: Revenue targets, categorized expenses, percentage benchmarks, variance tracking template, and adjustment triggers.

---

## Example: Solopreneur Consultant ($12K/month Revenue)

| Category | Amount | % |
|----------|--------|---|
| Revenue | $12,000 | 100% |
| Software/tools | $400 | 3% |
| Marketing | $1,200 | 10% |
| Contractors | $1,800 | 15% |
| Transaction fees | $360 | 3% |
| Education | $200 | 2% |
| Tax reserve | $2,400 | 20% |
| Owner's pay | $4,500 | 38% |
| Profit reserve | $1,140 | 10% |

---

## Anti-Patterns

- **Budgeting based on hopes instead of data** — use actual revenue from the past 3-6 months, not best-case projections
- **No tax reserve** — solopreneurs who do not set aside 25-30% for taxes get blindsided at tax time
- **Zero buffer** — always budget 5-10% for unexpected expenses
- **Set and forget** — a budget reviewed quarterly is a suggestion. Review monthly, adjust as needed.
- **Cutting marketing first** — marketing drives revenue. Cut low-ROI marketing, not all marketing.

---

## Recovery

- **Irregular income:** Budget based on the average of the last 6 months. Create a "minimum viable budget" for low months and a "growth budget" for high months.
- **No historical data (new business):** Build a conservative budget based on expected revenue, then update monthly with real data for the first 6 months.
- **Expenses exceed revenue:** Flag immediately. Identify which costs can be cut or deferred, and what revenue increase is needed to break even.
- **Multiple revenue streams:** Break revenue into separate lines but keep expenses consolidated unless they directly tie to one stream.
