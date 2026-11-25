---
name: fa-variance-commentary
version: 1.0.0
description: Write defensible variance commentary for a fund — period-over-period or actual-vs-expected moves in NAV, return, income, expenses, or a balance — attributing each material change to a named driver.
author: matrixx0070
tags: [fund-accounting, variance, commentary, attribution, reporting, close]
capabilities: []
---

# Variance Commentary

## When to use
Use this to explain *why* a fund figure moved — NAV or return period over period, income vs prior period, expense ratio vs budget, a balance-sheet line vs last close, or actual vs a forecast — in language an investor, auditor, or board can rely on. It turns a raw delta into a short, sourced narrative with each material piece attributed to a real driver.

**Not for:** proving a balance ties to its source (use fa-gl-recon or fa-nav-tieout) or hunting the transaction behind a difference (fa-break-trace). This *explains* a movement you already trust; it does not prove one.

## Method
1. **Frame the comparison.** State the metric, the two points (current vs prior/budget), the absolute and percentage change, and the materiality threshold you'll comment to.
2. **Confirm the numbers are proven.** Decision point: don't write commentary on an untied figure — an unexplained variance may be an error, not a story. Reconcile first.
3. **Decompose the change** into drivers: for return, use attribution (allocation, selection, FX, income, fees); for a balance, use the roll-forward flows; for expenses, split rate vs volume vs one-offs.
4. **Quantify each driver.** Attach a number and a sign to every contributor; the drivers must sum to the total variance (residual = 0). Decision point: an unattributed residual above threshold means a missing driver — keep decomposing.
5. **Attribute root cause.** Name the *reason* (a position rallied, FX moved, a fee trued up, a subscription diluted), not just the account.
6. **Rank and threshold.** Lead with the largest drivers; net small offsetting items into "other." Comment on everything above threshold, individually.
7. **Write it tight and sourced.** One to three sentences per material driver, each pointing to its evidence; state anything still unexplained plainly rather than hand-waving.

## Example
NAV/unit +1.43% this month vs +0.60% expected. Decompose: equity selection +1.10% (overweight XYZ, +18% on earnings, the single largest contributor); FX +0.20% (EUR book, EUR +1.1% vs base); income +0.04%; management fee −0.11% (routine accrual); a one-off audit-fee true-up −0.03% (invoice above accrual, reset going forward); residual +0.00%. Drivers sum to +1.20% net of the +0.23% base carry = +1.43%, nil residual. Commentary: "Return of +1.43% was driven principally by security selection (+1.10%), notably an overweight position in XYZ following results, with a favorable EUR contribution (+0.20%); a modest audit-fee catch-up (−0.03%) reset the ongoing accrual."

## Pitfalls
- **Commenting on an untied number.** If the figure isn't reconciled, the "variance" may be an error; you'll narrate a bug.
- **Restating the number instead of explaining it.** "Expenses rose because expenses were higher" is not commentary — name the driver and the cause.
- **Leaving a residual.** Drivers that don't sum to the total mean a driver is missing or double-counted; an unexplained residual undermines the whole note.
- **Netting away a material offset.** A big positive and big negative that net small each deserve their own line — burying them hides risk and effort.
- **False precision or vague causation.** Don't attribute to two decimals when the source is an estimate, and don't say "market conditions" when you can name the position, rate, or fee.

## Output format
```
Metric: <...> | Current: <> vs prior/budget: <> | Δ abs: <> | Δ %: <> | Threshold: <>
Numbers proven: Y/N (source)
Driver attribution:
  | driver | contribution | sign | root cause | evidence |
  ... (largest first)
  residual: <should be 0>
Commentary (prose):
  <1–3 sentences per material driver, sourced>
Unexplained / to investigate: <...>
```

## Reference

### Variance vs attribution
A **variance** is the raw delta (this − that). **Attribution** decomposes it into additive drivers that sum back to the delta with no residual. Good commentary is attribution written in prose: every material dollar or basis point of the variance is assigned to a named driver, and the reader can reconcile the words back to the number.

### Return attribution (Brinson-style)
Decompose active return vs a benchmark into:
- **Allocation** — over/underweighting sectors/regions that out/under-performed.
- **Selection** — picking securities that beat their sector.
- **Interaction** — the cross term of allocation and selection.
- **Currency / FX** — return from currency exposure and hedging.
- **Income vs price** — coupon/dividend yield vs capital movement.
- **Fees** — management, incentive, and other expenses drag.
These sum to the total active return; a residual signals a missing effect (often FX or fees).

### Expense variance: rate vs volume vs one-off
Split an expense change into: **rate** (fee % changed), **volume/base** (AUM or driver changed), and **one-off/timing** (true-ups, catch-ups, non-recurring costs). `Δexpense ≈ (Δrate × base) + (rate × Δbase) + one-offs`. Distinguishing a permanent rate change from a one-time true-up is the whole point — one resets the run-rate, the other doesn't.

### Balance variance via roll-forward
For a balance-sheet line, the drivers *are* the roll-forward flows: `Δbalance = additions − reductions ± adjustments`. Capital moved because of subscriptions, redemptions, P&L, and distributions; investments moved because of buys, sells, and revaluation. Tie commentary to the movement note, not just the two endpoints.

### Materiality and thresholds
Comment to a stated threshold — commonly a fixed dollar amount and/or a percentage (e.g., items > $50k or > 5% of the line, and any driver > a set number of basis points on return). Below threshold, net into "other." The threshold should be documented and applied consistently period to period so the note is comparable and defensible.

### Writing standard
Lead with the largest driver; one to three sentences each; every claim sourced to a reconciliation, attribution run, or schedule. Quantify with the sign, use plain causal language ("driven principally by," "partly offset by"), avoid unfounded macro narration, and state any unexplained residual openly. The test: an auditor can trace every sentence back to a number.
