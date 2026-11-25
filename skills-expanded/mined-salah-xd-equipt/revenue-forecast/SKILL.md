---
name: revenue-forecast
description: "Projects revenue with multiple scenarios using historical data and market factors. Use when forecasting future revenue for planning or reporting."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Revenue Forecast

## When to Use This Skill

Use this skill when you need to:
- Project revenue for the next 3, 6, or 12 months
- Create conservative, base, and optimistic revenue scenarios
- Forecast revenue by product line, channel, or customer segment
- Build a data-backed revenue plan for budgeting or investor communications

**DO NOT** use this skill for complete financial models (use financial-model), expense forecasting, or pricing decisions. This is focused specifically on revenue projection.

---

## Core Principle

A REVENUE FORECAST IS A RANGE, NOT A NUMBER — PRESENT THREE SCENARIOS AND IDENTIFY WHICH ASSUMPTIONS SEPARATE THEM.

---

## Phase 1: Historical Data

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Monthly revenue (last 6-12 months)** | "Share your monthly revenue for the last 6-12 months." | No default — must be provided |
| **Revenue streams** | "How do you generate revenue? (products, services, subscriptions, one-time)" | No default — must be provided |
| **Seasonality** | "Are there seasonal patterns in your revenue?" | No known seasonality |
| **Growth drivers** | "What is driving growth? (marketing, referrals, new products, expansion)" | Organic growth |
| **Planned changes** | "Any upcoming changes? (new product launch, price increase, new channel)" | None planned |
| **Forecast period** | "How far out? (3, 6, or 12 months)" | 12 months |

**GATE: Do not proceed without at least 3 months of historical revenue data.**

---

## Phase 2: Trend Analysis

### Historical Performance

```
## Revenue Analysis

### Monthly Revenue History
| Month | Revenue | MoM Change | YoY Change |
|-------|---------|-----------|-----------|
| [Month] | $[X] | +/-[X]% | +/-[X]% |
| ... | | | |

### Key Metrics
| Metric | Value |
|--------|-------|
| Average monthly revenue (last 6 months) | $[X] |
| Average monthly growth rate | [X]% |
| Revenue trend | Growing / Flat / Declining |
| Highest month | $[X] ([Month]) |
| Lowest month | $[X] ([Month]) |
| Revenue volatility (std deviation) | $[X] |
```

### Revenue by Stream

```
### Revenue Breakdown by Stream
| Stream | Monthly Avg | % of Total | Growth Rate | Trend |
|--------|-----------|-----------|-------------|-------|
| [Stream 1] | $[X] | [X]% | [X]% | ↑↓→ |
| [Stream 2] | $[X] | [X]% | [X]% | ↑↓→ |
```

---

## Phase 3: Forecast Model

### Three Scenarios

```
## Revenue Forecast: [Period]

### Assumptions

| Factor | Conservative | Base | Optimistic |
|--------|-------------|------|------------|
| Monthly growth rate | [X]% | [X]% | [X]% |
| New stream revenue | $0 | $[X] | $[X] |
| Seasonal adjustment | Yes | Yes | Yes |
| Price change impact | None | None | +[X]% |
| Churn/loss factor | [X]% | [X]% | [X]% |

### Monthly Forecast

| Month | Conservative | Base | Optimistic |
|-------|-------------|------|------------|
| M1 | $[X] | $[X] | $[X] |
| M2 | $[X] | $[X] | $[X] |
| ... | | | |
| M12 | $[X] | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** | **$[X]** |

### Forecast by Revenue Stream (Base Case)

| Month | [Stream 1] | [Stream 2] | [Stream 3] | Total |
|-------|-----------|-----------|-----------|-------|
| M1 | $[X] | $[X] | $[X] | $[X] |
| ... | | | | |
```

### Key Drivers and Risks

```
### What Separates the Scenarios

**Conservative → Base:** [Key assumption difference, e.g., "Assumes new
marketing channel launches on time and produces 20 leads/month by M3"]

**Base → Optimistic:** [Key assumption difference, e.g., "Assumes enterprise
deal closes in Q2 adding $5K/month recurring"]

### Downside Risks
1. [Risk] — Impact: -$[X]/month — Likelihood: [High/Med/Low]
2. [Risk] — Impact: -$[X]/month — Likelihood: [High/Med/Low]

### Upside Opportunities
1. [Opportunity] — Impact: +$[X]/month — Likelihood: [High/Med/Low]
```

---

## Phase 4: Deliverable

```
## Forecast Summary

**Forecast period:** [X] months
**Conservative annual revenue:** $[X]
**Base case annual revenue:** $[X]
**Optimistic annual revenue:** $[X]

**Planning recommendation:** Budget against the conservative scenario.
Target the base case. Celebrate if you hit optimistic.

forecast/
└── revenue-forecast-[YYYY].md
```

---

## Example: Consulting Business ($15K/month Average)

**History:** 6 months of data, $12K-$18K range, average $15K, 4% monthly growth driven by referrals.

**Forecast (12 months):** Conservative $14.5K avg (flat), Base $17.8K avg (4% growth), Optimistic $21K avg (7% growth from adding a new service). Annual totals: Conservative $174K, Base $214K, Optimistic $252K.

**Key driver:** Base case assumes maintaining current referral rate. Optimistic assumes launching a group coaching program in M4 adding $3K/month.

---

## Anti-Patterns

- **Straight-line projections** — revenue rarely grows in a straight line. Account for seasonality, ramp-up periods, and plateaus.
- **Single-number forecasts** — always provide a range. A single number is either a lie or a guess.
- **Ignoring churn and cancellations** — if you have recurring revenue, model churn. Gross new revenue minus churn equals net revenue growth.
- **Forecasting without identifying drivers** — "revenue will grow 10%" is not a forecast. "10 new clients at $1,500/month from LinkedIn ads" is a forecast.
- **Over-optimism bias** — most founders forecast 2-3x what actually happens. Use historical growth rates as the base, not aspirational targets.

---

## Recovery

- **Less than 3 months of data:** Use industry benchmarks and clearly label the forecast as preliminary. Update monthly as data accumulates.
- **Highly variable revenue:** Focus on trailing averages rather than month-to-month growth rates. Widen the gap between conservative and optimistic scenarios.
- **New revenue stream with no data:** Model it separately with a conservative ramp. Do not include it in the base case until you have 2-3 months of actual data.
- **Revenue declining:** Acknowledge the trend. Model scenarios for stabilization and recovery. Identify which actions change the trajectory.
