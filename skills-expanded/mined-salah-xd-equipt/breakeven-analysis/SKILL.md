---
name: breakeven-analysis
description: "Performs break-even analyses with fixed/variable cost breakdowns, margin calculations, and scenario modeling. Use when determining how many sales you need to cover costs."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Break-Even Analysis

## When to Use This Skill

Use this skill when you need to:
- Calculate how many units or sales you need to break even
- Analyze fixed vs. variable costs to find the break-even point
- Model break-even scenarios for different pricing or cost structures
- Evaluate the viability of a new product, service, or business

**DO NOT** use this skill for full financial projections or pricing strategy. This is specifically for determining the break-even point.

---

## Core Principle

BREAK-EVEN IS THE MINIMUM VIABLE NUMBER — IT TELLS YOU THE FLOOR, NOT THE GOAL. IF YOU CANNOT REACH BREAK-EVEN, THE BUSINESS MODEL NEEDS TO CHANGE BEFORE ANYTHING ELSE.

---

## Phase 1: Cost Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product/service** | "What are we analyzing?" | No default — must be provided |
| **Selling price per unit** | "What do you charge per unit/sale/project?" | No default — must be provided |
| **Variable cost per unit** | "What does each sale cost you? (materials, delivery, fees)" | No default — must be provided |
| **Monthly fixed costs** | "What are your monthly costs that do not change with sales volume?" | No default — must be provided |
| **Time period** | "Analyze monthly or annually?" | Monthly |

**GATE: Do not proceed without price, variable cost, and fixed costs.**

---

## Phase 2: Break-Even Calculation

```
## Break-Even Analysis: [Product/Service]

### Cost Structure
| Category | Amount |
|----------|--------|
| Selling price per unit | $[X] |
| Variable cost per unit | $[X] |
| **Contribution margin per unit** | **$[X]** |
| **Contribution margin %** | **[X]%** |
| Monthly fixed costs | $[X] |

### Break-Even Point
| Metric | Value | Formula |
|--------|-------|---------|
| **Break-even units (monthly)** | **[X] units** | Fixed costs / Contribution margin |
| **Break-even revenue (monthly)** | **$[X]** | Break-even units x Price |
| Break-even units (annual) | [X] units | Monthly x 12 |
| Break-even revenue (annual) | $[X] | Monthly x 12 |
| Units per day needed | [X] | Monthly / 30 |
| Units per week needed | [X] | Monthly / 4.3 |

### Margin of Safety
At current sales of [X] units/month:
| Metric | Value |
|--------|-------|
| Current monthly units | [X] |
| Break-even units | [X] |
| Margin of safety (units) | [X] |
| Margin of safety (%) | [X]% |
```

---

## Phase 3: Scenario Modeling

```
## Scenario Analysis

### Price Sensitivity
| Price Point | Contribution Margin | Break-Even Units | Break-Even Revenue |
|------------|--------------------|-----------------|--------------------|
| $[X] (-20%) | $[X] | [X] | $[X] |
| $[X] (-10%) | $[X] | [X] | $[X] |
| **$[X] (current)** | **$[X]** | **[X]** | **$[X]** |
| $[X] (+10%) | $[X] | [X] | $[X] |
| $[X] (+20%) | $[X] | [X] | $[X] |

### Fixed Cost Scenarios
| Scenario | Monthly Fixed | Break-Even Units | Notes |
|----------|-------------|-----------------|-------|
| Lean (cut non-essentials) | $[X] | [X] | [What gets cut] |
| **Current** | **$[X]** | **[X]** | |
| Growth (add hire/tool) | $[X] | [X] | [What gets added] |

### Variable Cost Scenarios
| Scenario | Variable Cost/Unit | Break-Even Units |
|----------|-------------------|-----------------|
| Optimized (reduce COGS) | $[X] | [X] |
| **Current** | **$[X]** | **[X]** |
| Increased (higher quality) | $[X] | [X] |
```

---

## Phase 4: Action Plan

```
## Recommendations

### Path to Break-Even
- Current monthly sales: [X] units
- Break-even target: [X] units
- Gap: [X] units ([X]% increase needed)

### Fastest Levers
1. **[Lever]** — [Impact on break-even point]
2. **[Lever]** — [Impact]
3. **[Lever]** — [Impact]

### Timeline to Break-Even
At [X]% monthly growth rate: [X] months to reach break-even volume.
```

---

## Example: Online Course ($197 price)

**Costs:** Variable $8/sale (processing + hosting). Fixed $3,200/month (software, ads, contractors). Contribution margin: $189/sale.

**Break-even:** 17 sales/month ($3,349/month revenue). At current 12 sales/month, need 42% more sales. At 10% monthly growth, break-even in 4 months.

**Scenario:** If price increases to $247, break-even drops to 13.4 sales/month — already profitable at current volume.

---

## Anti-Patterns

- **Forgetting hidden variable costs** — payment processing fees, shipping, packaging, and platform commissions are variable costs. Include them all.
- **Treating owner's salary as optional** — if you plan to pay yourself, include it in fixed costs. A "profitable" business that does not pay the owner is not profitable.
- **Static analysis only** — always include at least 3 scenarios (price change, cost change, volume change).
- **Ignoring the timeline** — break-even in 2 months is great. Break-even in 24 months may mean you run out of cash first.
- **Assuming linear scaling** — at high volumes, variable costs may change (bulk discounts or additional infrastructure). Note the volume range where your numbers hold.

---

## Recovery

- **Break-even seems unreachable:** Show which single change (price increase, cost cut, or additional revenue stream) has the biggest impact. Sometimes a 15% price increase changes everything.
- **Multiple products:** Calculate break-even per product, then create a blended analysis using the weighted average contribution margin.
- **Service business (no clear "unit"):** Define the unit as one client, one project, or one month of service. Calculate based on that.
- **Pre-launch (no sales data):** Use the break-even analysis to set targets. "You need X sales/month at $Y price to cover costs" becomes the launch goal.
