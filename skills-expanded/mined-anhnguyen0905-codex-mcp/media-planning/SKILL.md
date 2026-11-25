---
name: media-planning
description: Build a media plan and allocate marketing budget across paid channels — media mix, budget split, marginal CPI and scale ceiling, saturation curves, test reserve, pacing, seasonality and Q4 CPM inflation, geo tiering, and downside scenarios. Use when splitting spend across UA, brand and influencer or planning a quarterly budget.
---

# Media Planning (budget allocation across channels)

## Allocate on marginal return, not average

The only defensible split equalizes **marginal** return across channels: keep moving the next
dollar to whichever channel returns most at its current spend level, until the returns equalize or
the payback bar is hit. Average CPI per channel is the wrong input — it always flatters the small
channel.

```
marginal CPI ≈ Δspend / Δinstalls   (measured between adjacent spend levels of the same channel)
scale ceiling = the spend beyond which marginal CPI exceeds the breakeven CPI (see unit-economics)
```

Every channel saturates. A plan that scales a channel linearly from its current spend is the single
most common planning error — the CPI curve bends upward well before the budget runs out.

## The plan itself

A media plan is a table, not a paragraph. One row per channel × month:

| channel | month | spend | assumed CPI | expected installs | basis of the CPI assumption | confidence |

- Every CPI assumption must name its basis: last quarter's actual at comparable spend, a test
  result, or a vendor estimate (mark vendor estimates as unverified).
- Sum to the actual budget and reconcile: plans that don't add up get discovered in month two.
- Show a **downside scenario** (CPI +20–30%, or the channel not scaling past X) with what gets cut
  first. A plan without a downside branch is a forecast, not a plan.

## Reserve, pacing, seasonality

- **Test reserve**: hold back roughly 10–20% for new channels/creative/geos. Without it the plan
  can only ever re-buy last quarter's mix, and the mix decays.
- **Pacing**: front-load learning (new campaigns need volume to exit the learning phase), then
  flatten. Month-end spend dumps buy the worst inventory of the month.
- **Seasonality**: Q4 and local holiday peaks inflate CPM materially; a plan built on Q2 CPMs
  under-delivers in Q4 at the same budget. Plan the same installs at a higher CPI, or shift timing.

## Channel roles differ — don't compare them on CPI alone

Prospecting UA buys volume, retargeting buys efficiency on existing demand, brand and influencer
buy future demand that shows up as organic/branded search. Comparing brand spend to UA on CPI
guarantees you defund brand; hold brand to a lift/incrementality measurement instead.

## Failure modes

- Linear scaling assumption (no saturation curve).
- Double-counting installs when two channels both claim the same conversion — de-overlap before
  summing, or the plan promises installs that don't exist.
- Planning on blended averages that hide 3–5× geo spread.
- No test reserve, so no new channel is ever proven.
- Treating platform-reported ROAS as incremental for brand/retargeting.
- No downside branch and no named trigger for cutting.

## Reviewer checklist

- [ ] Split justified by marginal return, with the scale ceiling per channel stated
- [ ] Every CPI assumption has a named basis and a confidence level
- [ ] Spend sums to budget and reconciles by month
- [ ] Test reserve carved out explicitly
- [ ] Seasonality/CPM inflation reflected in the assumed CPI, not ignored
- [ ] Downside scenario with an explicit cut order and trigger
- [ ] Brand/retargeting held to lift, not to CPI

## Provenance

Standard media-planning practice (marginal allocation, saturation, test reserve, pacing). The
percentage ranges (10–20% test reserve, +20–30% downside, Q4 CPM inflation) are **derived,
unverified** planning defaults — replace with the account's measured curves before committing spend.
