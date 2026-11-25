---
name: pf-retirement-plan
version: 1.0.0
description: Build a personal retirement savings plan and projection from age, savings rate, and target (educational).
author: matrixx0070
tags: [retirement, savings-rate, compounding, projection, personal-finance]
capabilities: []
---

## When to use

Use this when the owner wants to know if they are on track for retirement — projecting a nest egg from current savings, contribution rate, and time, and translating a target income into a savings goal.

**Not for:** choosing specific funds or accounts (see pf-investment-allocation), guaranteeing returns, or giving withdrawal-tax rulings. Projections are estimates, not promises.

This skill provides education and structure, not individualized financial advice. Retirement outcomes depend on markets, inflation, and personal factors — recommend a licensed financial planner before relying on any projection.

## Method

1. Gather inputs: current age, target retirement age, current retirement savings, monthly contribution, and desired annual retirement income.
2. Estimate the target nest egg. Educational rule of thumb: target ≈ desired annual income × 25 (the 4% rule), adjusted for other income sources like pensions/social security.
3. Project growth: compound current savings + contributions to retirement age. Use a conservative real (after-inflation) return assumption, e.g., 5%, and state it explicitly.
4. Decision point — is the projection below target? Increase contributions, delay retirement, or lower the income target; show the gap in dollars and the extra monthly saving needed to close it.
5. Prioritize order: capture any employer match first (free money), then tax-advantaged accounts, then taxable — but keep this account-type guidance educational.
6. Decision point — is retirement <10 years out? Shift the conversation toward capital preservation and sequence-of-returns risk; defer specifics to a professional.
7. Set a yearly review to update inputs and re-project.

## Example

Age 35, retire at 65, $50,000 saved, $600/mo contributions, wants $40,000/yr income. Target ≈ $1,000,000. At 5% real return, $50k grows to ~$216k and 30 yrs of $600/mo adds ~$478k → ~$694k projected. Gap ≈ $306k. Closing it needs roughly +$380/mo (to ~$980/mo). Action: capture full employer match first, then raise contributions gradually. Review yearly.

## Pitfalls

- Using nominal returns and ignoring inflation — the projected number looks great and buys far less.
- Assuming aggressive returns (10%+) that leave no margin for bad decades.
- Leaving employer match on the table; it is an immediate guaranteed return.
- Treating one projection as destiny. Re-run yearly as income and markets change.

## Output format

```
RETIREMENT PROJECTION (educational) — [owner]
Age [x] -> retire [x]   Assumed real return: [x]% (stated, not guaranteed)

TARGET NEST EGG: $[x]  (desired income $[x]/yr × 25, adj. for [pension/SS])
PROJECTED AT RETIREMENT: $[x]
GAP: $[x]   ->  close with +$[x]/mo OR delay [n] yrs OR lower target

PRIORITY ORDER: 1) employer match  2) tax-advantaged  3) taxable
REVIEW: yearly.

Estimate only — confirm with a licensed financial planner before relying on it.
```

## Reference

Educational rules-of-thumb below — general working knowledge, not individualized financial advice. Projections depend on markets, inflation, and personal factors; the numbers are teaching anchors, not promises.

### The 4% rule (and the ×25 target)

A well-known teaching guideline from retirement research: withdrawing about **4% of a portfolio in the first year of retirement**, then adjusting that dollar amount for inflation, historically had a high chance of lasting ~30 years. The mirror image is the savings target:

> **Target nest egg ≈ desired annual spending × 25.**

So $40,000/yr of desired income → ~$1,000,000 (before subtracting other income like pensions or social security, which reduce what the portfolio must cover). The 4% figure is debated — some educators use a more conservative 3-3.5% for longer or earlier retirements. It assumes a diversified portfolio and is a *starting* withdrawal rate, not a guarantee.

### Savings rate → years to financial independence

Because a higher savings rate both grows the pot faster **and** lowers the spending the pot must support, the years-to-FI depends heavily on savings rate. Rough figures (starting from zero, ~5% real return, spending in retirement equal to current spending):

| Savings rate | Approx. years to FI |
|--------------|---------------------|
| 10% | ~40+ |
| 15% | ~35 |
| 20% | ~30 |
| 30% | ~25 |
| 40% | ~20 |
| 50% | ~15-17 |
| 65% | ~10-11 |

The lesson educators draw: the savings *rate* moves the finish line far more than picking investments. Even shifting from 10% to 15-20% can pull retirement in by years.

### Compounding illustration

$500/month invested at ~7% nominal average return:

| Years | Total contributed | Approx. balance |
|-------|-------------------|-----------------|
| 10 | $60,000 | ~$86,000 |
| 20 | $120,000 | ~$260,000 |
| 30 | $180,000 | ~$610,000 |
| 40 | $240,000 | ~$1,310,000 |

Most of the final balance is growth, not contributions — and most of *that* growth arrives in the final decade. This is why **starting early** beats contributing more later: a dollar invested at 25 works far longer than one invested at 40. The "Rule of 72" gives a quick estimate — money doubles roughly every `72 ÷ return%` years (at 7%, about every 10 years).

### Nominal vs real returns (inflation)

Always separate **nominal** (headline) returns from **real** (after-inflation) returns. A 7% nominal return with 2-3% inflation is only ~4-5% real. Project long-term buying power with a conservative **real** return (e.g., ~5%) and state the assumption explicitly — a projection built on 10%+ returns leaves no margin for a bad decade.

### Contribution priority order (teaching sequence)

1. **Employer match** — an immediate, guaranteed return; capture the full match first.
2. **High-interest debt** — paying off 20% debt is a guaranteed 20% "return."
3. **Tax-advantaged accounts** — IRA/401(k)/HSA (see pf-tax-personal and pf-investment-allocation for account and allocation concepts).
4. **Taxable brokerage** — for savings beyond the tax-advantaged limits.

### Sequence-of-returns risk

Poor market returns in the *first few years* of retirement do far more damage than the same returns later, because withdrawals lock in losses. As retirement approaches (roughly <10 years out), the standard teaching shift is toward capital preservation, a cash buffer of 1-2 years of spending, and a de-risking glidepath — defer specifics to a licensed planner.

### Guardrails

- Re-run the projection yearly; one estimate is not destiny.
- Don't leave the employer match on the table.
- Account for social security/pensions as offsets to the target, but don't over-count uncertain future benefits.
