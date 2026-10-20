---
name: forecast-delivery
description: Answer "when will this be done" with a probability distribution computed from measured throughput — Monte Carlo over the last 8-12 periods, scope-growth measured rather than assumed away, p50/p85/p95 dates, and a deterministic bracket as a sanity check. Also computes cycle time percentiles, throughput, WIP, ageing work in progress and the DORA four keys. Refuses to emit a single committed date. Use before committing to a deadline, when a stakeholder asks for a date, when setting WIP limits, or when a board is slow for unclear reasons. Not for cost estimation, not for facilitating ceremonies, not for reading a tracker's API.
argument-hint: "[--items 45] [--periods 12] [--trials 10000] [--dora] [--diagnose]"
user-invocable: true
agent: foundry-pmo:flow-analyst
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "tracker-item.v1 + plan.v1 -> review.v1 with a forecast distribution"
license: Apache-2.0
---

# Forecast delivery

Forecasts here come from what the team has actually delivered, never from what it intended to
deliver. The method is deliberately simple, because a simple model over real history beats a
sophisticated model over wishful inputs.

**This skill never emits a single date.** If the caller insists, it returns the p85 date labelled
as the 85th percentile, and states what the other 15% looks like.

## Step 1 — Load measured history

Read `tracker-item.v1[]` from `.foundry/blackboard/<wave>/tracker-operator.json`.

Gate before computing anything:

| Check | If it fails |
|---|---|
| `flow.historyRead` is true on most items | cycle time is unavailable; degrade to lead time and label every figure |
| ≥ 6 complete periods of throughput | forecast anyway, widen the interval, mark `low-confidence` |
| single `provider` in the set | segment by provider; never pool incomparable state models |
| `done` and `cancelled` are distinguishable | stop — pooled closure data inflates throughput and every date derived from it |

Exclude `cancelled` from throughput. This is the most common way a forecast is quietly made
optimistic.

## Step 2 — Describe the present before predicting the future

```
throughput   items reaching done per period, last N periods, as a list not a mean
cycle time   p50, p85, p95 — never the average, the distribution is right-skewed
WIP          sampled daily; report against team size
ageing WIP   now − enteredInProgress for unfinished items, flagged above the p85 line
```

Report the throughput series itself, not just its summary. A team that delivered
`7, 9, 8, 2, 9, 8` has a different risk profile from one that delivered `7, 7, 7, 7, 7, 8`, and
both have a mean near 7.

## Step 3 — Monte Carlo

```
inputs   remaining item count R, throughput history H (8-12 periods), trials T ≥ 10 000
for each trial:
    periods = 0; delivered = 0
    while delivered < R:
        delivered += sample_with_replacement(H)
        periods  += 1
    record periods
report   p50, p85, p95 of the recorded periods, converted to calendar dates
```

Sampling with replacement is what makes this work: it inherits the team's real variability —
the holiday week, the incident, the good run — instead of averaging them into a fiction.

**Measure scope growth and add it.** Count items created in the same window that fall inside the
forecast's scope, express it as items per period, and inflate `R` accordingly. State the measured
growth rate in the output. A forecast that assumes the backlog stops growing is forecasting a
project nobody is working on, and it is wrong in a predictable direction.

Deterministic bracket, run alongside and reported next to it:

```
optimistic  R ÷ p85 throughput
pessimistic R ÷ p15 throughput
```

If the simulation lands outside that bracket, the simulation is wrong. Investigate before
publishing.

## Step 4 — Report

| Percentile | Use |
|---|---|
| p50 | internal planning only, always labelled; half of all outcomes are later |
| p85 | the number given to stakeholders and written into commitments |
| p95 | contractual or regulatory deadlines, where being late has an external cost |

Say what would move the date, in order of measured impact: reducing WIP, reducing scope, removing
the dominant queue state. Do not offer "add people" — it is not measurable from this data and it
is usually false in the short term.

## Step 5 — `--diagnose`

When a board is slow, work this order and stop at the first that explains the data:

1. WIP ÷ team size well above 1 — queueing, not capability.
2. One state dominating cycle time — break it down; `in-review` dominating means review capacity
   or batch size, not development speed.
3. Large items in the tail — correlate size against cycle time; the fix is splitting, via
   `foundry-pmo:groom-backlog`.
4. High `flow.blockedDays` — the constraint is outside the team; emit `risk.v1` for
   `foundry-pmo:risk-manager`.
5. Arrival rate above throughput — the board is overloaded, not slow. No process change fixes
   this; it is a scope or capacity decision.

## Step 6 — `--dora`

Report the four keys only from real deployment and incident data. Mark any key without data as
`unmeasured`; never estimate one. Reporting the two speed keys without the two stability keys
rewards shipping breakage, so report all four or state which are missing and why.

## Refusals

- **A single committed date.** Returns p85 with its label instead.
- **Per-person metrics.** Cycle time measures the queue and the handoffs far more than the
  individual. Ranking people by it optimises for small tickets and hidden work. Offer the team cut.
- **Velocity as productivity, or velocity compared across teams.** Points are a local unit; the
  comparison is meaningless and the pressure inflates them.
- **Forecasting from estimates instead of history** when history exists.

## Degradation

- **No transition history.** Lead time only, labelled; name the tracker permission needed.
- **Fewer than 6 periods.** Forecast with a wide interval marked `low-confidence`. Never withhold
  a forecast for lack of data — silence gets filled by somebody's guess, which is strictly worse.
- **No remaining-item count.** Ask for it, or derive it from `plan.v1`; never assume.

## Progressive disclosure

- `references/monte-carlo.md` — the simulation, worked by hand on a small dataset.
- `references/flow-metrics.md` — definitions, Little's Law preconditions, CFD reading.
- `references/dora.md` — the four keys, their data sources and their misuses.
