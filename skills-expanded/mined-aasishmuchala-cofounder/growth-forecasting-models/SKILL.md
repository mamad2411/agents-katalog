---
name: growth-forecasting-models
description: When the agent needs growth forecasting, demand projections, capacity planning, scenario models, trend extrapolation, or "when do we hit X" questions — forecasts built from drivers and cohorts, delivered with honest uncertainty.
department: Data
source: helm
---

# Growth Forecasting Models

You forecast like the data scientists finance actually invites back: driver-decomposed instead of curve-fit vibes, cohort mechanics doing the heavy lifting, uncertainty shown as ranges — and every forecast scored against reality afterward, because a forecast nobody back-tests is astrology with a spreadsheet.

## Operating principles

1. **Decompose before you extrapolate.** Growth is never one curve; it's the sum of machinery: new acquisition (by channel, each with its own trend + saturation reality) + activation rate + cohort retention curves + expansion − churn. Forecast the COMPONENTS and let the total emerge — a topline curve-fit hides exactly the channel that's dying underneath it. The exception: very short horizons (next 4–6 weeks), where recent run-rate + seasonality honestly beats fancy decomposition.
2. **Cohort curves are the physics engine**: revenue in month N = Σ (each historical cohort's size × its survival/expansion at age N−birth) + new cohorts on the acquisition forecast. This mechanically produces the truths topline models miss: growth slowing while acquisitions hold (aging base), the compounding of NRR > 100%, the cliff hiding in a big cohort's month-12 renewal. Fit the survival curve per segment (SMB and enterprise decay differently) from the retention triangles; extrapolate the curve's SHAPE, not each cohort separately.
3. **Saturation and seasonality are features of reality, not model spoilers**: every channel gets a ceiling assumption (search demand is finite, list quality decays, paid CAC rises with spend — model the rising-CAC curve, not flat) · seasonality from year-over-year patterns where ≥ 2 years exist, from domain knowledge where they don't (B2B dies in December; consumer spikes; India's fiscal-year March matters) — and label which one you used.
4. **Ranges or it's marketing**: base / upside / downside built by flexing the 2–3 drivers that sensitivity analysis says matter (usually: new-acquisition growth rate, early-cohort retention, expansion rate) · state the interval honestly ("March ARR: 82–97L, central 89") · and the horizon discipline — monthly detail to 12 months, quarterly to 24, directional beyond (a 5-year monthly forecast is 60 columns of false confidence).
5. **Forecasts are instruments that get calibrated**: every forecast versioned with its assumptions · actuals vs forecast reviewed monthly (which DRIVER missed, not just the total) · the misses update the assumptions, and the forecast-error trend itself is reported (an org whose errors shrink is learning; one that reforecasts silently is hiding).

## Workflow

1. **Frame**: the decision this forecast feeds (hiring plan? raise timing? capacity?) → horizon + granularity + the tolerance for error that decision can bear.
2. **Build the driver tree** from actuals: acquisition by channel (trend + ceiling), activation, the fitted cohort curves by segment, expansion/contraction rates, churn events (contract renewals as EVENTS on their dates, not smoothed rates, when lumpy).
3. **Assemble the cohort engine** (spreadsheet or code): historical cohorts age forward on the fitted curves; new cohorts arrive per the acquisition forecast; totals roll up.
4. **Scenario-ize**: flex the sensitive drivers with NAMED justifications ("downside = paid CAC +30% as the channel saturates, retention flat"); produce the range + the "what kills the base case" sentence.
5. **Deliver as a decision aid**: the central path + range chart, the driver table with assumptions + sources, the milestone answers ("cross ₹1Cr ARR: Oct–Jan window"), the top sensitivities — and the back-test section comparing the LAST forecast to actuals, driver by driver.

## Output contract

Deliver: framing note (decision, horizon, granularity) · driver tree with fitted values + sources · cohort-engine structure · scenario table with named flexes · the range chart + milestone answers · sensitivity ranking · the calibration section (last forecast vs actuals, error trend).

## Quality bar

- No topline extrapolation without decomposition (short-horizon run-rate exception noted when used).
- Every scenario flex is a named assumption, not ±15% seasoning; renewals modeled as events when lumpy.
- The forecast ships with its predecessor's report card — accuracy is tracked, publicly.
