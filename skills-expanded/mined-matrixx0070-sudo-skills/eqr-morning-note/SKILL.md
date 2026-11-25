---
name: eqr-morning-note
version: 1.0.0
description: Write a concise pre-market morning note — overnight moves, coverage news, changes, and the day's watch items — that a busy reader can act on in two minutes.
author: matrixx0070
tags: [equity-research, morning-note, desk, summary, monitoring]
capabilities: []
---

## When to use

Use this before the open to brief a reader on what changed overnight and what matters today across your coverage or watchlist. A morning note is triage, not analysis: it surfaces the few things worth attention, links to depth elsewhere, and states any action or view change crisply.

**Not for:** full analysis of a single event (use `eqr-earnings-analysis` or `eqr-earnings-preview`), a new thesis (use `eqr-initiating-coverage`), or the events calendar itself (use `eqr-catalyst-calendar` — the note draws from it). Outputs are research and education, not personalized investment advice.

## Method

1. **Set the tape.** Overnight and pre-market context in one or two lines: indices, futures, rates, commodities/FX only if relevant to coverage. No macro essay.
2. **Scan coverage for news.** Earnings, guidance, upgrades/downgrades, M&A, management or regulatory items on your names since the last note. *Decision point:* include only what a reader would act on or ask about — kill the rest.
3. **Rank by relevance to the reader**, not by news size. A small move on a top holding beats a big move on a name nobody owns.
4. **For each item, give the read.** One line of what happened + one line of what it means (confirms/challenges the view, action or none).
5. **Flag your own changes.** Any estimate, rating, or target changes going out today, with a link to the full note.
6. **List today's watch items.** Prints, data, and events due today from the catalyst calendar, with expected direction where you have one.
7. **Keep it two minutes.** If it can't be read before the open, it fails. Link to depth; don't inline it.

## Example

Tape: futures +0.3%, 10Y +4bps, oil -1%. Coverage: (1) NVAX beat and raised, stock +6% pre-market — confirms the demand-inflection view, no action, full note out 8:30; (2) peer FLEX guided down, read-across negative for our HOLD on JBL, watching for sympathy weakness; (3) we're cutting XYZ estimates 4% on FX today (link). Watch today: CPI 8:30 (rate-sensitive names), ACME prints AMC (previewed — expect in-line, guide is the swing).

## Pitfalls

- **Dumping the newswire.** Volume isn't value; include only what the reader would act on.
- **News ranked by size, not relevance.** A macro headline over a top-holding data point wastes the reader's scarce attention.
- **What without so-what.** Reporting a move without the read forces the reader to do the work you were meant to do.
- **Too long.** A morning note that takes ten minutes gets skipped. Enforce the two-minute rule; link out.
- **Burying your own changes.** Rating/estimate changes are the highest-value lines — flag them, don't hide them.

## Output format

```
MORNING NOTE — <date> | coverage: <sector/list>
TAPE: futures | rates | commodities/FX (only if relevant)
COVERAGE NEWS (ranked by reader relevance)
  <ticker>: what happened — what it means (action/none) [link]
OUR CHANGES TODAY: <ticker> est/rating/target — [full note link]
WATCH TODAY: <event/time> — expected read
Read time target: <= 2 min
Note: research/education, not personalized investment advice.
```

## Reference

Research process: treat the morning note as triage — a tape line, only reader-actionable coverage news ranked by relevance rather than headline size, a one-line read on each item, your own same-day changes flagged, and today's watch items pulled from `eqr-catalyst-calendar`. Modeling: the note references estimate/rating/target changes but links to `eqr-model-update` and full notes for the underlying work rather than reproducing it. Disclosure: a morning note is a research and education summary, its overnight and pre-market figures are point-in-time, and it is not personalized investment advice or a recommendation to transact.
