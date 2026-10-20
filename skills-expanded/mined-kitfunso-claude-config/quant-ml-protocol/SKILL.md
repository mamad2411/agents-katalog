---
name: quant-ml-protocol
description: "Predictive-modelling campaigns with a time axis: a price, spread, freight or crypto forecast, a trading signal, a forecasting competition. Use when starting, running, reviewing or rescuing one, including a baseline, a model-family scout, a tuning study, an error map, a mechanism round, an ensemble, a final read or a forecast ledger."
---

# Quant ML Protocol

A campaign is a *tight* loop. A frozen evaluator scores every run the same way, a
ledger records every run, and the lead spends its time where the error is. Validity
lives in the evaluator's code; this file carries the loop. Breadth and speed find
signal; the evaluator keeps it honest. Both are the job.

The campaign page is `docs/EXPERIMENT-PROTOCOL.md` in the project. Its first line
declares the budget (wall-clock or GPU hours) and the external truth the campaign
answers to (a leaderboard, a judged live read, a decision someone will make). Stage
shares below are defaults; move them with a one-line reason on the page.

**Words.** *Evaluator windows*: the walk-forward windows `evaluate.py` scores.
*Final-read window*: the untouched span read once at stage 5. *Champion*: the best
kept run in the ledger, the naive baseline until something beats it. *Headroom*: the
gain an idea would give if it worked perfectly.

## Build first: the data audit, the evaluator and the ledger

Before the first model.

**Data audit.** Every table in the family, found by prefix and directory. Per source:
span, cadence, observation-date column, provenance grade A to D, the hygiene checks
and the freeze manifest, by `references/data-hygiene.md`. Declare the target family
and its metric by `references/targets-and-metrics.md`.

**`evaluate.py`, frozen.** It owns the split, the purge, the metric and the gate.
Agents and sub-agents read it and never edit it; a change is a new evaluator
version, and every ledger row names the version that scored it.
- The split mirrors how the score that matters is made: the test window's length,
  gap and layout, walk-forward over several windows, with the final-read window held
  back. Purge at least one horizon. Everything fitted (scaler, imputer, encoders,
  feature selection, tuning) is fitted inside the fold, through one pipeline object.
- Per run it writes: the metric per window, the per-anchor paired loss against the
  champion, a paired block-bootstrap interval on the mean difference, and the
  out-of-fold predictions to `oof/<run_id>.parquet`.
- Library first: walk-forward and purge from Nixtla `cross_validation` or skfolio
  `WalkForward(purged_size=...)`; bootstraps, `optimal_block_length`, SPA, StepM and
  MCS from `arch.bootstrap`; deflated Sharpe and PBO from `pypbo`. Hand-roll only
  what no library does, and give it a test.

**`results.tsv`, append-only.** One row per run: run_id, date, branch, the one
change, hypothesis (one line), metric, interval against the champion, verdict
(keep, discard, crash), evaluator version, compute minutes. A run absent from the
ledger did not happen.

**Calibrate once.** After the first two or three external scores, check that the
evaluator ranks them in the same order. A mismatch makes fixing the evaluator the
next task, ahead of any model.

## Stages

Each stage closes on its *done* line. Report every stage as done, partial or
skipped, with the ledger rows that show it.

### 0. Sources and errors (about 10%)
1. **External scan.** Public repos, notebooks, forum threads and papers on this
   exact target. Every external data source they use becomes an idea, with whether
   we can get it. For market targets, add the price reporter's methodology and the
   contract spec (`references/prior-art.md` for the search rings).
2. **Naive baseline through the evaluator.** Random walk, seasonal naive, always-one-
   side, trailing mean: whichever the target admits. For a market target, run the
   carry decomposition: how much of any edge is drift the curve already pays.
3. **Error map.** Where the loss sits: by segment, regime, horizon, calendar and
   tail. Write the share of loss per slice.
4. **Idea pool** (`ideas.md`). Each idea gets its *headroom*, measured by plugging in
   the true value or a best case on the slice it targets. Rank by headroom over
   cost. `references/model-families.md` lists mechanism ideas worth a row.

*Done:* the baseline row in the ledger, the error map on disk, the pool ranked.

### 1. Draft breadth (about 10%)
At least four simple drafts that differ in model class, each untuned and
unensembled, run in parallel by sub-agents:
- a regularised linear model;
- a gradient-boosted tree model (LightGBM or CatBoost);
- a small neural net;
- a foundation-model slot, run locally: Chronos-2 or TimesFM for series, TabPFN for
  tabular. TabPFN-TS runs in `LOCAL` mode only, because its default sends data to
  the vendor's cloud. Check the model's pretraining cutoff against the final-read
  window; overlap makes it a leak.

*Done:* four ledger rows, four OOF files.

### 2. Tune (about 15%)
One bounded study on each of the top one or two drafts (Optuna, or mlforecast
`AutoMLForecast`), capped by time, scored on an inner purged walk-forward, completed
on data before the forecasts it serves. Re-tune when the model family changes;
feature rounds reuse the last study.

*Done:* a ledger row for each study, its best against its defaults.

### 3. Mechanism rounds (about 45%)
The main loop. Each round:
1. Take the top idea from the pool. Order: information first (a new source, a
   driver, a target treatment), then mechanism features, then model shape.
2. Run four or five variants, one base plus single-change variants, in parallel.
3. **Keep rule.** The interval's lower bound above zero makes a new champion. An
   interval that straddles zero keeps the simpler of the two. The interval is the
   gate; an economic minimum belongs on the trading page.
4. Redraw the error map on the champion and re-rank the pool.

**Stagnation**, read off the ledger: a branch is *stagnant* after three runs inside
its best run's interval, or two rounds with no new champion. The next round changes
the construct (a new source, a new mechanism or another model family); a fourth
variant of a stagnant construct waits until the pool is empty.

*Done:* the pool's top headroom sits inside the noise bar, or the share is spent.

### 4. Ensemble (about 10%)
Hill-climb or non-negative least squares over the OOF store; every run, kept or
discarded, is a candidate. Weights come from OOF only. Final members run three seeds;
report the range.

*Done:* the blend's ledger row with its interval against the best single model.

### 5. Final read, then the ledger (about 10%)
Read the champion's metric per evaluator window first: a gain resting on one window
is a flag on the page. Freeze the spec, then read the final-read window once. Report
the metric, its interval and the haircut against the evaluator's number. A
disappointing read is the result; any change it prompts is a challenger that waits
for fresh outcomes. Then the live forecast ledger by `references/daily-read.md`, and
a trading page, when there is one, by `references/trading-layer.md`.

*Done:* the final-read row, the first live ledger rows.

## Multiplicity, sized to the search

Every run is in the ledger, so the search is countable. A claim that the champion
beats the baseline or the last champion after K tries uses SPA or StepM on the T x K
loss matrix from the OOF store; the tie set is MCS. A trading claim reports deflated
Sharpe with N equal to the ledger's row count. Rerunning the whole search under null
worlds is an audit for a real-money decision, priced before it runs
(`references/audit.md`).

## Lead and sub-agents

The lead reads results, decides the next round and writes the briefs. Builds go to
sub-agents: Sonnet for a complete brief, Opus where correctness is a validity
question (the evaluator, the purge, availability timestamps). Width over depth: a
round's variants run in parallel. Before a round closes, the lead reads each run's
ledger row and OOF file against the brief; a summary never closes a round.

## Hard rules

These protect the evaluator's numbers, and each one has a test in the project:
- Features use only data published before the forecast cutoff (`references/data-hygiene.md`
  for availability, PIT grades A to D and the staleness cap).
- The split is chronological; random splits are for non-temporal problems.
- The evaluator and the final-read window change only by a new evaluator version,
  never to pass a run.
- A result better than its idea's headroom, or a jump far past the error map's
  share for that slice, is a suspected leak: the round stops until it is explained.
- Trading rules are chosen on evaluator windows, never on the final read.
- A result resting on a B to D source is "a backtest on vendor-revised history".

## Reporting

- Chat: the champion, its interval against the last one, what the round taught, the
  next idea and why. A null is said first.
- The campaign page carries the budget, the stage list with done, partial or
  skipped, and the pool. The closing report is one HTML page: the ledger, the error
  map before and after, the stage list. `references/steering-bank.md` holds the
  questions to fire at the work before each stage closes.

## References

- `references/prior-art.md`: search rings and the extraction row for stage 0.
- `references/targets-and-metrics.md`: target families, the metric per target,
  calibration.
- `references/data-hygiene.md`: availability, PIT grades, outliers, missing data,
  the freeze manifest.
- `references/model-families.md`: family notes for the drafts, tuning, seeds, and a
  menu of mechanism ideas.
- `references/daily-read.md`: the live ledger and its read rule.
- `references/trading-layer.md`: the trading page.
- `references/physical-diff-addendum.md`: read when the target is a physical
  differential to a PRA benchmark.
- `references/steering-bank.md`: questions that caught what checklists missed.
- `references/audit.md`: the full-search null replay and the other heavy checks of
  the 2026-10-03 version, for a real-money decision only.
