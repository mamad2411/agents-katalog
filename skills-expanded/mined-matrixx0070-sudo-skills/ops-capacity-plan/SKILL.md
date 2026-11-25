---
name: ops-capacity-plan
version: 1.0.0
description: Build a resource capacity plan that turns a demand forecast into add/reallocate/defer decisions with trigger thresholds.
author: matrixx0070
tags: [operations, capacity, forecasting, planning, resources, headroom]
capabilities: []
---

# Capacity Plan

## When to use
Use this when you must decide whether current resources (people, compute, budget, throughput) will meet projected demand, or when planning hiring, procurement, or scaling ahead of a known growth curve or seasonal peak.

**Not for:** one-off "do we have room right now" checks (just read current utilization), or budgeting exercises with no capacity constraint. If demand has no measurable driver, stop and instrument first.

## Method
1. **Define the resource and unit.** Name what you size (engineers, CPU cores, tickets/day) and the measurable capacity unit per resource.
2. **Baseline current state.** Record total capacity, current demand, and utilization % (demand / capacity). Flag anything already above 80%.
3. **Gather demand drivers.** Identify what moves the workload (users, transactions, releases) and pull 3-6 periods of history. *Decision:* fewer than 3 periods, or high variance? Use a range, not a point estimate.
4. **Forecast demand.** Project each driver using growth rate, seasonality, and known events. State the model and assumptions.
5. **Compute the gap.** Per future period, calculate required vs. available capacity, applying a target headroom buffer (default 20%). *Decision:* spiky/latency-sensitive load takes a larger buffer; steady batch load a smaller one.
6. **Recommend actions.** For each gap, propose add / reallocate / defer with lead time and cost, and set the trigger threshold that forces the action.

## Example
Support team: 5 agents, each 40 tickets/day = 200 capacity. Current demand 170 (85% — already flagged). Tickets grew 8%/month over 4 months. Forecast month 3 demand = 170 x 1.08^3 = 214. With 20% headroom, required capacity = 257, i.e. 6.4 agents. **Gap: hire 2 agents; trigger = sustained utilization >85% for 2 weeks; lead time 6 weeks, so start recruiting now.**

## Pitfalls
- **Sizing to average, not peak.** Averages hide the Tuesday-9am spike that actually breaks you. Plan to the peak percentile.
- **Zero headroom.** Running at 100% has no slack for variance or failure; queues explode long before capacity is "full."
- **Forecasting the metric, not the driver.** Project the underlying driver (users, orders), then derive load — don't extrapolate the load line blindly.
- **No trigger thresholds.** A gap with no "act when X" is a prediction, not a plan.

## Output format
```
Summary:        resource, horizon, verdict (adequate | gap in period X)
Baseline:       capacity | demand | utilization %
Forecast table: period | projected demand | required cap | available | surplus/deficit | util %
Assumptions:    growth rate, buffer %, model used
Recommendations: action (add/reallocate/defer) | timing | cost | trigger threshold
Risks:          what invalidates the forecast
```
