---
name: pf-investment-allocation
version: 1.0.0
description: Explain a diversified asset-allocation framework tailored to risk tolerance and time horizon (educational).
author: matrixx0070
tags: [investing, asset-allocation, diversification, risk, personal-finance]
capabilities: []
---

## When to use

Use this when the owner wants to understand how a diversified portfolio is *structured* — the logic of splitting across stocks, bonds, and cash by risk and time horizon. Good for framing a conversation before they meet an advisor, or for understanding a target-date fund's design.

**Not for:** recommending specific securities, tickers, or fund products; timing the market; or telling the owner to buy or sell. You explain frameworks, never issue picks.

This skill provides education and structure, not individualized investment advice. Allocation involves real risk of loss; recommend a licensed fiduciary advisor before the owner commits money.

## Method

1. Establish the goal and its time horizon: short (<3 yr), medium (3-10 yr), or long (10+ yr).
2. Assess risk capacity (can they afford a loss?) and risk tolerance (can they emotionally hold through a 30% drop?). Use the lower of the two.
3. Decision point — set a stock/bond split by horizon and risk. Common educational anchors: long+aggressive ~90/10, long+moderate ~70/30, medium ~50/50, short ~20/80 or all cash.
4. Diversify *within* stocks (domestic + international, broad sectors) and bonds (varied duration/quality) — concentration is the main avoidable risk.
5. Hold an emergency fund (3-6 months expenses) in cash *outside* the invested portfolio so the owner never force-sells in a downturn.
6. Decision point — is any single position >10% of the portfolio (e.g., employer stock)? Flag concentration risk.
7. Set a rebalancing rule: revisit yearly or when a bucket drifts >5 points from target.

## Example

Owner, retirement 25 years out, moderate tolerance. Framework: 70% stocks / 25% bonds / 5% cash. Within stocks: ~45% domestic broad-market, ~25% international. Emergency fund of $18,000 (6 months) held separately. Employer stock is 22% of holdings → flagged as concentration; framework suggests diversifying over time. Rebalance each January.

## Pitfalls

- Confusing risk tolerance with risk capacity — an aggressive personality with an unstable income still needs a buffer.
- Chasing last year's winner; diversification means always owning something underperforming.
- Skipping the emergency fund and being forced to sell investments at the worst time.
- Recommending specific products. Stay at the framework level and defer picks to a licensed professional.

## Output format

```
ALLOCATION FRAMEWORK (educational) — [owner]
Goal: [goal]   Horizon: [x] yrs   Risk: [conservative|moderate|aggressive]

TARGET SPLIT
Stocks  [x]%   (domestic [x]% / international [x]%)
Bonds   [x]%
Cash    [x]%

EMERGENCY FUND: $[x] held separately ([n] months)
CONCENTRATION FLAGS: [position — % — note]
REBALANCE: [yearly / >5pt drift]

This is a framework, not a recommendation. Confirm with a licensed fiduciary before investing.
```

## Reference

Educational frameworks below — general working knowledge, not individualized investment advice. Allocation carries real risk of loss; percentages are teaching anchors, not recommendations.

### Age / horizon-based allocation frameworks

Two classic teaching heuristics for the **stock percentage** of a long-term portfolio:

- **"110 (or 120) minus age"** → stocks. At 30: ~80-90% stocks. At 60: ~50-60%. The bond share is the remainder. The older "100 − age" is now often nudged up to reflect longer lifespans.

Sample split by horizon and risk (stocks / bonds / cash):

| Horizon & profile | Stocks | Bonds | Cash |
|-------------------|--------|-------|------|
| Long (10+ yr), aggressive | ~90 | ~10 | 0 |
| Long, moderate | ~70 | ~25 | ~5 |
| Medium (3-10 yr), moderate | ~50 | ~45 | ~5 |
| Short (<3 yr) or capital-preservation | ~20 | ~50 | ~30 |
| Money needed <1 yr | 0 | 0-some | most/all |

### The glidepath concept

A **glidepath** is the pre-planned drift from higher stock exposure toward more bonds/cash as a goal approaches — exactly what a **target-date fund** automates. Early on it holds mostly stocks for growth; as the target year nears it de-risks so a late-career crash can't force selling at the bottom. "To" glidepaths reach their final conservative mix *at* the target date; "through" glidepaths keep shifting for years *after*. Understanding this explains why a "2055 fund" and a "2030 fund" hold very different mixes today.

### Diversification principles

- **Across asset classes:** stocks, bonds, cash behave differently in a given year; the mix, not any single pick, drives most of the risk/return.
- **Within stocks:** domestic + international, across large/mid/small companies and many sectors. A common educational anchor is roughly 60-70% domestic / 30-40% international of the stock sleeve.
- **Within bonds:** vary duration (short vs long maturities) and credit quality; long bonds swing more with interest rates.
- **Concentration is the main avoidable risk.** Any single position — especially **employer stock** — over ~10% of the portfolio ties your paycheck and your savings to one company. Broad, low-cost index funds are the standard teaching example of instant diversification.

### Risk capacity vs risk tolerance

- **Capacity:** can you *afford* a loss? (income stability, time horizon, other assets)
- **Tolerance:** can you emotionally *hold* through a ~30-50% drawdown without selling?

Use the **lower** of the two. Selling in a panic at the bottom does more damage than any allocation error.

### Cost, tax location, and rebalancing

- **Costs compound against you.** A 1% annual fee can erode a large share of lifetime returns; expense ratios and trading costs matter as much as picks. This is the case for low-cost broad-market funds in most teaching material.
- **Emergency fund first:** hold 3-6 months of expenses in cash *outside* the invested portfolio so a shock never forces selling investments at a low.
- **Rebalancing:** restore targets on a schedule (e.g., yearly) or when any bucket drifts more than ~5 percentage points. Rebalancing mechanically trims winners and adds to laggards — buying low, selling high, without prediction.

### Concepts worth knowing (not picks)

Dollar-cost averaging (investing fixed amounts on a schedule), sequence-of-returns risk (bad early-retirement years hurt more than bad late ones), and the difference between **passive index** and **active** strategies. None of these is a recommendation to buy anything — defer specific securities and products to a licensed fiduciary.
