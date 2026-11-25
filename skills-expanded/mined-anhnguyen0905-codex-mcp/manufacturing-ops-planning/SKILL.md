---
name: manufacturing-ops-planning
description: Manufacturing operations planning — production capacity planning from demand forecasts, preventive maintenance scheduling and unplanned downtime reduction, shift staffing and rotating rosters, process improvement and lead time reduction (order-to-ship cycle time), OEE, takt time, line utilization. Use for factory capacity plans, maintenance schedules, shift plans, or cycle-time improvement. For job sequencing and bottleneck resolution on a live schedule, prefer production-scheduling.
---

# Manufacturing Ops Planning (capacity, maintenance, shifts, cycle time)

## Definitions — compute these before recommending anything

```
takt time        = available production time / customer demand (units)
required capacity = forecast demand × cycle time per unit / (OEE × available hours)
OEE              = availability × performance × quality      (world-class ≈ 85%, typical 60% — rule of thumb)
availability     = run time / planned production time        (unplanned downtime lives here)
lead time        = order received → order shipped            (measure the whole chain, not one step)
utilization      = scheduled load / demonstrated capacity    (plan ≤ ~85%; 100% planning guarantees lateness)
```

## Capacity planning (quarter/period level)

1. Start from the demand forecast **with its uncertainty**, not the point estimate — plan the
   base case and a ±20% band (or the forecaster's stated range).
2. Convert to required hours per work center using demonstrated (measured) cycle times and
   demonstrated OEE — never nameplate/vendor figures.
3. Compare against available hours after subtracting planned maintenance, holidays, training,
   and changeovers. The gap is the decision: overtime, extra shift, outsourcing, or demand shaping.
4. State the constraint explicitly (which work center is the bottleneck at base and high case);
   capacity added anywhere else is spend without output.

## Preventive maintenance (PM) scheduling

- Classify equipment by criticality: bottleneck/single-point-of-failure machines get
  time-or-usage-based PM; redundant, cheap-to-fail assets can run to failure deliberately.
- PM interval: start from manufacturer guidance, then adjust on failure history
  (shorten after repeated unplanned failures, lengthen only with evidence).
- Schedule PM into the capacity plan (it consumes available hours); PM done "when we have time"
  is PM not done — that is how unplanned downtime returns.
- Track: unplanned downtime hours by machine and cause, MTBF, MTTR, PM compliance %
  (completed on schedule / scheduled). A PM program with <90% compliance is a paper program.

## Shift staffing and rotating rosters

- Coverage math first: required positions × hours of coverage ÷ net hours per operator
  (after breaks, absence rate ~5–8%, leave, training) = headcount. Staffing to gross hours
  understaffs every real week.
- 24/7 coverage needs ≥ 4 crews (3 crews = built-in structural overtime). Common patterns:
  4-crew 8h rotation, 2-2-3 (Panama) 12h. Rotate forward (morning → evening → night);
  backward rotation fights circadian rhythm.
- Fairness is explicit: nights, weekends, and holidays distributed and visible in the roster,
  or the schedule fails socially even when it works mathematically.

## Process / lead-time improvement (order-to-ship)

1. Map the current state end-to-end with times: processing, waiting, transport, rework.
   In most order-to-ship cycles >80% of lead time is waiting, not processing.
2. Attack queues and handoffs first (batching policies, approval waits, information gaps) —
   speeding up a processing step that is 5% of lead time cannot cut lead time 20%.
3. One measurable target per wave ("order-to-ship 10 days → 8 by cutting credit-check queue"),
   with the baseline measured the same way as the result.

## Failure modes — what wrong looks like

- Planning at 100% utilization: queues explode nonlinearly as utilization → 1; late everywhere.
- Nameplate capacity used instead of demonstrated OEE-adjusted capacity: plan overstates ~20–40%.
- PM deferred during busy periods — exactly when failure cost is highest.
- Cutting lead time by expediting (rushing single orders) instead of fixing the queue policy:
  averages worsen while anecdotes improve.
- Shift plan balanced on paper but ignoring absence rate and training time.

## Reviewer checklist

- [ ] Capacity uses demonstrated cycle times and OEE, with a demand band, not a point forecast
- [ ] Bottleneck named; the plan adds capacity or protection there, not elsewhere
- [ ] PM hours appear inside the capacity calculation; compliance % is tracked
- [ ] Roster headcount includes absence/leave/training; night/weekend fairness visible
- [ ] Lead-time work targets waiting/queues with a measured baseline and a numeric goal
- [ ] Every rule-of-thumb figure (OEE 85%, absence 5–8%) labeled as such, not presented as law

Provenance: standard industrial-engineering practice (TPS/lean, TPM, queueing behavior at high
utilization); numeric benchmarks are rules of thumb — derived, unverified for any specific plant.
