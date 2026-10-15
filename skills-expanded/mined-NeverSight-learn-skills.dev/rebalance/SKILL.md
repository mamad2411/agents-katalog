---
name: rebalance
description: Portfolio rebalancing — drift analysis, target allocation, tax-aware trade generation. Use when asked to rebalance, fix allocation, or check drift.
context: fork
agent: portfolio-analyzer
---

# Portfolio Rebalancing

## Step 1: Load Portfolio & Target

Load portfolio from `~/.wealthstack/portfolios/`. Check for target at `~/.wealthstack/target-allocation.json`.

If no target, ask the user:
- A) Conservative: 30% Equity / 60% Debt / 10% Gold
- B) Moderate: 60% Equity / 30% Debt / 10% Gold
- C) Growth: 80% Equity / 15% Debt / 5% Gold
- D) Aggressive: 95% Equity / 5% Cash
- E) Custom

Save target to `~/.wealthstack/target-allocation.json`.

## Step 2: Drift Analysis

| Asset Class | Target | Current | Drift | Status |
|------------|--------|---------|-------|--------|

Flag drift >5%.

## Step 3: Rebalancing Strategy

Ask:
- A) Full rebalance (taxable events)
- B) Cash-flow rebalance (new money to underweight only)
- C) Tax-aware (minimize STCG)
- D) Threshold-only (only positions drifting >5%)

## Step 4: Trade Generation

Calculate specific trades. For tax-aware: prioritize selling loss lots, avoid short-term gain positions, flag wash sale concerns.

## Step 5: Post-Rebalance Projection

Show before/after allocation and save plan to `~/.wealthstack/reports/`.
