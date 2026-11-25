---
name: unit-economics
description: Unit economics for growth and acquisition — CAC and blended CAC, LTV and cohort lifetime value, payback period, LTV:CAC ratio, contribution margin, breakeven CPI, and profitability by channel. Use when deciding what CPI is still profitable, whether to scale a channel, or building a budget business case.
---

# Unit Economics (CAC, LTV, payback, breakeven CPI)

## Definitions — state them or the numbers are meaningless

```
CAC_paid     = paid spend / new customers acquired BY THAT SPEND
CAC_blended  = paid spend / ALL new customers (incl. organic)
LTV(h)       = cumulative NET revenue per user through horizon h × contribution margin
payback      = months until cumulative net revenue per cohort ≥ CAC
breakeven CPI(h) = LTV(h)   ← at the same horizon and the same margin basis
```

Two rules that catch most broken analyses:

1. **Always carry a horizon.** "LTV = $12" is not a number; "D180 LTV = $12" is. Comparing a D30
   LTV to a fully-loaded CAC understates payback and greenlights unprofitable scale.
2. **Never mix blended with paid.** Blended CAC vs paid LTV (or vice versa) silently books organic
   users as a return on ad spend. Pick one basis and label it.

## Net, not gross

Contribution margin must strip: app store commission (typically 15–30%), payment/processing fees,
refunds and chargebacks, VAT/withholding where applicable, and the variable serving cost per user
(bandwidth, infra, support contacts). Marketing decisions made on gross revenue overstate headroom
by roughly the store cut alone.

## Cohorts, not aggregates

- Compute per install-cohort (weekly or monthly) and read the curve, never the pooled average:
  pooled ARPU mixes mature cohorts with fresh ones and drifts as spend grows.
- Extrapolating the LTV curve: fit on the observable window, cap the extrapolation (e.g. never
  claim beyond ~2× the observed horizon), and show the fit alongside the actuals. State the
  assumed shape; a curve that keeps rising forever is an artifact, not a finding.
- Survivorship: the users still spending at D180 are not the cohort — divide by the original
  cohort size, always.

## Decision rules

- **Scale a channel** when marginal (not average) CAC still clears the payback bar. Average CAC
  hides that the next dollar is more expensive than the last.
- **Payback bar** comes from cash constraints, not taste: how long can the business fund the gap?
  Faster payback beats a better LTV:CAC ratio when cash is tight.
- **LTV:CAC** is a sanity ratio, not a target to optimize; a high ratio with 18-month payback can
  still kill the company.
- **Channel comparison** requires the same horizon, the same margin basis, and attribution overlap
  removed — otherwise two channels both "own" the same install.

## Failure modes

- Comparing D7 revenue against a full CAC and calling it a loss (or D360 LTV against CAC and
  calling it a win).
- Counting organic uplift from paid brand spend as free (or as fully attributable — both are wrong;
  it needs a holdout).
- Ignoring the discount rate on revenue collected a year out.
- Currency mixing and pre/post-tax mixing across markets.
- Treating a single blended number as the answer when the spread across geos is 3–5×.

## Reviewer checklist

- [ ] Every LTV/CAC figure carries a horizon and a basis (paid vs blended, net vs gross)
- [ ] Contribution margin itemized, store cut included
- [ ] Cohort-based, divided by original cohort size
- [ ] Extrapolation capped, fit shown next to actuals
- [ ] Scale decisions use marginal, not average, cost
- [ ] Payback stated in months against an explicit cash constraint

## Provenance

Standard SaaS/mobile unit-economics practice. Percentage ranges (store commission, extrapolation
cap) are **derived, unverified** defaults — replace with the product's real contract terms and the
company's own cohort history before deciding anything.
