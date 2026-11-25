---
name: logistics-dispatch
description: Plans governed truck-load chains and dispatch options using supplied or authorized load-board data, equipment, driver location, cost-per-mile, deadhead, appointment, Hours-of-Service, and risk constraints. Use for dispatcher work, lane planning, load comparison, or multi-load route proposals.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source: LeeWay DISPATCH_LOGISTICS_PACK.md normalized from E-drive capability inventory
  source-skill: logistics.dispatch.triangulate_loads
---

# Logistics Dispatch

## Contract

Never claim live load availability, guaranteed profit, legal HOS compliance, broker acceptance, or booked freight unless the authorized systems returned current evidence and the responsible human approved the action.

Collect truck/equipment, current location and time, driver clocks, operating authority, target region, appointments, rate, loaded and deadhead miles, tolls, fuel, accessorials, probability of reload, and cost-per-mile assumptions. Mark missing fields.

## Workflow

1. Retrieve candidate loads only through an authorized load-board or broker adapter.
2. Normalize origin/destination, pickup/delivery windows, equipment, weight, rate, miles, commodity, and constraints.
3. Reject infeasible equipment, appointment, HOS, authority, or safety combinations.
4. Build candidate chains and calculate loaded miles, deadhead, gross, estimated variable cost, estimated margin, revenue per total mile, and revenue per planned hour.
5. Stress-test delay, detention, cancellation, and reload uncertainty.
6. Present ranked options with assumptions and callouts for human dispatch approval.

Use `deadhead / total miles` for the deadhead ratio. Treat the source pack's 15% target as a preference, not a universal law.

## Evidence

For every proposal preserve quote/load identifiers, observation time, source, calculation inputs, exclusions, HOS data age, adapter state, and whether any booking actually executed.
