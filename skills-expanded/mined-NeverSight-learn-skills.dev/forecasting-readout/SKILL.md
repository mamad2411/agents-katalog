---
name: forecasting-readout
description: Use when projecting a KPI or operating metric and the AI should produce a decision-ready forecast instead of a single-number guess.
source: perlytics-skill
version: 1.0.0
---

# Forecasting Readout

## Purpose

Turn a metric projection into a decision-ready forecast with explicit trend basis, assumptions, and uncertainty bounds - not just a point estimate.

## When to use

Use this skill when:

- asked "what will revenue/users/orders be next quarter/month/year?"
- projecting a metric for planning, budgeting, or target-setting
- presenting a forecast to a stakeholder who will use it to make a decision
- evaluating whether a current trend leads to hitting or missing a target

## When not to use

Do not use this skill when:

- there is insufficient history to support any projection (fewer than 3-4 comparable periods)
- the metric is driven primarily by an upcoming event or decision with no historical analog
- the question is why a metric changed, not where it is going (use `root-cause-analysis`)

## Required thinking discipline

- Never produce a point estimate alone. A single number without a range implies false precision and misleads decision-makers.
- State the basis for the projection explicitly - what pattern does the forecast extrapolate?
- Distinguish extrapolation from causally grounded projection. Trend extrapolation assumes "what has been true will continue." That assumption needs to be named.
- Separate trend from seasonality. Projecting November revenue in July requires handling the seasonal pattern explicitly.
- A forecast is a decision input, not a commitment. State what would need to change for the forecast to be wrong.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Define the metric, entity, and forecast horizon (e.g., net revenue, all markets, next 90 days).
2. Characterize the historical trend basis:
   - Flat (no directional trend)
   - Linear growth or decline
   - Accelerating or decelerating growth
   - Mean-reverting or cyclical
   - Event-driven (spikes around campaigns, holidays, product launches)
3. Identify and separate seasonality: does the metric have known weekly, monthly, or annual periodic patterns? State how seasonality is handled (carried forward, averaged, ignored).
4. List key assumptions the forecast depends on:
   - No major product, pricing, or acquisition strategy changes
   - External environment remains consistent
   - Seasonality pattern from prior years applies
   - Any specific operational assumptions (new market launch, campaign planned)
5. Produce the point estimate plus a scenario range:
   - **Base case:** continuation of recent trend with normal seasonality
   - **Upside case:** trend continues at the favorable end of recent variance
   - **Downside case:** trend continues at the unfavorable end, or a known risk materializes
6. State conditions that would invalidate the forecast - what event or change would require revisiting the projection?

## Output format

- Metric and horizon
- Trend basis (with time period used as foundation)
- Seasonality handling
- Key assumptions
- Point estimate (base case)
- Scenario range (upside / base / downside)
- Invalidation conditions
- Recommended review trigger (e.g., "revisit if weekly actuals deviate more than 10% from base case for two consecutive weeks")

## Good example

Metric: weekly new paid subscriptions. Horizon: next 12 weeks.

> Trend basis: linear growth of approximately +2.8% week-over-week over the past 16 weeks, excluding a one-week spike from a November promotion.
> Seasonality: end-of-year slowdown observed in prior two years (weeks 51-52 run approximately 20% below trend). Applied to base case.
> Key assumptions: no pricing change, current acquisition spend maintained, no major product change.
> Base case: 4,200 new subscriptions in week 12.
> Upside: 4,900 (if acquisition efficiency improves 15% as recently observed in test markets).
> Downside: 3,400 (if the year-end slowdown is stronger than historical average or if acquisition efficiency reverts).
> Invalidation conditions: a pricing change, a shift in paid acquisition budget greater than 20%, or a product change affecting the conversion funnel.
> Review trigger: revisit if actuals fall outside the upside/downside range for two consecutive weeks.

## Bad example

> Revenue will be $2.4M next quarter.

Why this is bad:

- no range or uncertainty - implies false precision
- no trend basis stated - where does $2.4M come from?
- no assumptions - what has to be true for this to hold?
- no invalidation conditions - under what circumstances is it wrong?
- a stakeholder will hold this number as a commitment rather than an estimate

## Practical notes

- The further out the horizon, the wider the uncertainty range should be. A 90-day forecast should have a wider range than a 30-day forecast - if it does not, the uncertainty is being hidden.
- If the metric has high week-to-week variance, communicate that variance explicitly - a "flat" trend with +/-30% weekly swings is very different from a flat trend with +/-5% swings.
- When a forecast is used for planning, recommend what trigger would cause the plan to need revision - this converts a static number into a living decision tool.
- Do not project through a known structural break (pricing change, market entry, acquisition) without stating that the break makes historical extrapolation unreliable.

## Optional variants

- **Operational forecasting (capacity planning):** focus on volume and throughput rather than revenue; add resource requirement translation (headcount, infrastructure).
- **Financial forecasting (budgeting):** be explicit about revenue recognition timing vs. cash timing; add margin assumptions if projecting profit.
- **Growth forecasting:** apply seasonality adjustment explicitly; distinguish organic growth from paid acquisition-driven growth in the trend basis.
