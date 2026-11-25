---
name: gammarips-exit-lab
description: Test an options exit rule (profit target, stop, trailing stop, holding window) against the realized history of GammaRips pool contracts - touch probabilities, the MFE/MAE opportunity surface, and scoring for a bracket the user chooses. Use when the user asks where to take profit, where to put a stop, how often contracts reached +X%, or wants to score their own exit. Research only, never a promise.
---

# GammaRips exit lab

Help the user test an exit rule against history. The tools score the rule. The
user decides. These tools need GammaRips Pro. If a call returns
`subscription_required`, give the user the tool's message as it is written,
offer `get_playbook(name="exit-lab")` (it is on every plan), and stop.

## Steps

1. **Get the rule.** Ask for, or confirm: target %, stop %, horizon
   (`same_day` or `3d`), and optionally a delta band and a date range. For a
   trailing stop, get `trail_pct` and `activation_pct`.
2. **Start from the two exact labels.** Call
   `query_outcomes(view="summary", horizon="same_day")` (+40% / -30%, flat by
   15:45 ET) and `query_outcomes(view="summary", horizon="3d")` (+80% / -60%,
   3 trading days). These are the only exactly simulated brackets, with real
   fills and slippage. They are the reference points.
3. **Touch probabilities.** Call
   `query_outcomes(view="harvest", targets=[...], stops=[...])` with the user's
   levels. Report the probability of touching each level, with its confidence
   interval, and which day the peak landed on.
4. **The surface.** Call
   `query_outcomes(view="surface", aggregate_only=True, days=<N>)` for MFE and
   MAE quantiles over the same period.
5. **Score the rule.** Call `query_outcomes(view="exit_rule", rule="bracket",
   target_pct=<T>, stop_pct=<S>)`, or `rule="trailing"` with `trail_pct` and
   `activation_pct`. Its default window is 3 trading days. Report `ev_bounds`,
   not one EV number, and report `heuristic_share`.
6. **Slice, then check stability.** If the user wants more, repeat steps 3 to 5
   inside a feature slice (for example a delta band with `delta_min` and
   `delta_max`) and across two or more date ranges. Trust a result only if it
   holds in each range.

## How to report

For every number, give its horizon, its row count (N), and its date range.
Then give these caveats:

- **Never mix horizons.** Same-day and 3-day numbers can point in opposite
  directions. Compare a rule only with numbers from the same horizon.
- **Touches are not fills.** A touch is a bar high or low. Surface and
  exit-rule estimates apply no slippage. Real stop fills land past the stop
  level, and more so on thin contracts. Expect real results below the
  estimate.
- **Heuristic rows.** When both levels were crossed inside the window, the
  order is estimated. If `heuristic_share` is large, say that the score is
  uncertain.
- **Excluded rows.** Rows with no label (illiquid at the entry anchor) are
  excluded, and that group is not random. Quote the exclusion counts from the
  response `meta`.
- **History is not a promise.** A score on history is a research result for
  that rule on past contracts, not an expected return for the next trade.
- Paper-traded research data. Educational only. Not investment advice.

For the full method, call `get_playbook(name="exit-lab")`.
