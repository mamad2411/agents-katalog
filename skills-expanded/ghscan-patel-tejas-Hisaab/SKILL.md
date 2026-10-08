---
name: quant-statistics
description: >-
  How to read a significance result honestly: bootstrap confidence intervals,
  the multiple-testing problem, deflated Sharpe and PBO, and what sample size
  a Sharpe ratio needs before it means anything. Trigger keywords: significant,
  confidence interval, p-value, bootstrap, deflated sharpe, PBO, luck, random,
  overfitting, is this real.
category: analysis
---

# Reading a statistical result honestly

Adapted from the `quant-statistics` skill in Vibe-Trading (HKUDS, MIT), trimmed
to the tests this engine actually exposes. The engine has no ADF, cointegration,
GARCH or regression-diagnostic tools — do not offer them.

## The two tests available, and which to use

| Question | Tool | Headline field |
|---|---|---|
| Is THIS config distinguishable from luck? | `backtest_significance` | `sharpe_ci.excludes_zero` |
| Does SEARCHING this grid find a real edge? | `validate_parameter_search` | `credible` |

They are not interchangeable. A config the user supplied has no multiple-testing
problem, because nothing was searched. A config found by a grid search does, and
needs the correction.

## Bootstrap confidence intervals

`backtest_significance` resamples the strategy's own daily returns to put an
interval around its Sharpe.

- **`excludes_zero: false` means not significant.** The interval spans zero, so
  the true Sharpe could as easily be negative. Say exactly that.
- A wide interval is itself the finding. On one month, a Sharpe of 0.95 can come
  with an interval of roughly -5.7 to +7.9 — that is not a weak signal, it is no
  information at all.
- `prob_positive` is the share of resamples above zero. Around 0.5 means a coin
  flip; do not report it as "60% likely to be profitable".

Read `sharpe_ci.excludes_zero` as the headline. The permutation p-value
describes the shape of the equity path only — it is **not** an edge test, and
the tool's own note says so.

## The multiple-testing problem

Test 100 things at p < 0.05 and expect 5 false positives. The default grid here
is **320 combinations**, so:

- The best of 320 draws is comfortably positive even when every combination is
  worthless.
- `parameter_search`'s top row is therefore not evidence. It is the maximum of a
  noise distribution.
- `validate_parameter_search` applies the corrections that number needs:
  - **Deflated Sharpe** — compares the winner against the Sharpe the best of N
    reaches by luck alone.
  - **Bootstrap interval** — as above, on the winner.
  - **PBO** (probability of backtest overfitting) — tests whether the *selection
    procedure* generalises, by recombining in-sample/out-of-sample blocks. A PBO
    near or above 0.5 means the procedure is no better than picking at random.
- `credible` is true only when all three come back favourable.

## What sample size a Sharpe needs

The conventional rules of thumb:

- Sharpe > 0.5 with **more than 5 years** of data — may be significant.
- Sharpe > 1.0 with **more than 3 years** — likely significant.
- Sharpe > 2.0 — treat as an overfitting warning, not a triumph.

**This dataset is two months, one of them partial.** No Sharpe computed here
clears any of those bars. State that when asked whether a result is significant:
the honest answer is that the sample is far too short, and it is a stronger
constraint than any single statistic.

## How to report a negative verdict

A strategy failing these checks is a result, not an error. Say what was tested,
what came back, and stop. Do not:

- re-run with a different grid until something passes;
- present a raw `parameter_search` winner as "the best parameters";
- soften "not significant" into "promising but needs more data" — the second
  implies a direction the data does not support.
