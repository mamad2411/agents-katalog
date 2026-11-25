---
name: demand-forecast
description: Model capacity demand — growth (linear/compound/seasonal), translate to resource needs + headroom, and flag the lead time before a saturation breach.
---

# demand-forecast

> Capacity planning fails on lead time, not math: you saw the trend but couldn't provision before the wall. Forecast far enough ahead to act, and state the date you run out.

## When to use

- Projecting whether current capacity survives expected growth or a known event (launch, sale, season).
- Turning a usage trend into a provisioning decision with a deadline.
- A workflow invokes `polymath-sre:demand-forecast`.

Not this when: you are setting reliability targets (`polymath-sre:slo-design`) or the current point-in-time capacity recommendation (`polymath-sre:capacity-plan`). This skill projects demand forward in time.

## Inputs

- Historical usage of the driving metric(s) (RPS, storage, connections), and the resource each consumes.
- Known future events and their expected multiplier; the provisioning lead time.

## Procedure

1. **Pick the driver metric(s)** that actually gate capacity (often RPS, concurrent users, data volume, queue depth) — forecast the driver, then map to resources, not the other way around.
2. **Choose a growth model from the data**: linear (steady adds), compound/exponential (% growth — the one teams underestimate), or seasonal/cyclical (day-of-week, holidays, campaigns). Fit to history; don't assume linear because it's easy.
3. **Overlay known events**: launches, marketing, seasonal peaks — apply explicit multipliers on top of the baseline trend.
4. **Translate demand → resources**: use the measured resource-per-unit (from `capacity-plan` / load tests) to convert forecasted driver units into CPU/memory/storage/instances. State the conversion.
5. **Apply a headroom target**: provision to a utilization ceiling (e.g. 60–70% at peak) so you have burst room and time to react — not 100%.
6. **Compute the lead-time-to-breach**: given the trend + headroom + provisioning lead time, the date you must act by. This is the output that matters.
7. **State assumptions + confidence + refresh cadence**: forecasts decay — say when to re-run and what would invalidate it (a step-change in growth).

## Output

- A one-page forecast: the driver metric + growth model, the demand projection with event overlays, the resource translation, headroom target, and the must-provision-by date with confidence + refresh cadence.

## Quality bar

- The growth model is fit to history, not assumed linear; compounding is checked.
- Demand is converted to resources via a measured per-unit cost, with headroom.
- The output names a concrete must-act-by date accounting for provisioning lead time.
- Assumptions, confidence, and a refresh cadence are stated.
