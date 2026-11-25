---
name: gammarips-options-flow
description: Use the GammaRips options-flow data (the nightly liquidity-selected pool of option contracts, point-in-time features, realized MFE/MAE opportunity surfaces, outcome labels, regime, and methodology) to answer questions about US options flow and to help the user find and plan a trade. Use when the user asks about the GammaRips pool, options flow, unusual options activity, a trade idea, or opportunity surfaces.
---

# GammaRips options-flow data

GammaRips gives your agent a ready, high-quality options universe every US
trading night, plus the history to plan the exit. Each night the engine ranks
about 3,500 optionable US stocks, keeps the 100 most liquid, keeps the bullish
names, and selects one out-of-the-money call in each **on contract
liquidity**. The pool holds roughly 40 to 50 contracts with deep books: median
open interest 4,664 and median session volume 1,039, against 906 and 232
before the liquidity rule. In a 60-day study, no-fill at the 10:00 ET entry
fell from 40.5% to 6.1%.

## What to do

- **When the user asks for a trade,** build a plan with them. Use the
  `gammarips-trade-plan` skill if it is available. If not, follow the plan
  steps in `get_playbook(name="start-here")`. Give 1 to 3 candidates with
  entry, target, stop, maximum loss, and size, or a reasoned no-trade.
- **When the user asks for a morning read,** use the `gammarips-morning-brief`
  skill if it is available.
- **When the user asks where to exit,** use the `gammarips-exit-lab` skill if
  it is available, or `get_playbook(name="exit-lab")`.

## Rules

- GammaRips has no pick endpoint. Your agent builds the plan with the user.
  Label it as your analysis of GammaRips data. The user decides.
- Do not state an expected return or a win rate, and do not claim the pool
  returns more than other contracts. Quality claims are about execution:
  liquidity, open interest, volume, and fills.
- Do not answer a trade request with pool-wide averages. They describe every
  contract under one fixed rule, not the plan you build.
- `query_outcomes` views `positions` and `performance` hold the history of a
  retired engine test. Do not use them to judge the pool.
- **Point-in-time discipline.** Features are as of the overnight scan. Outcome
  labels and surfaces arrive after the trade window closes. Never treat a label
  or a surface as a live signal for the same day. If you are not sure when a
  field was knowable, call `get_playbook(name="schema")` or
  `get_playbook(field="<name>")`.
- GammaRips is read-only. It cannot place, change, or cancel an order.
- End each plan or summary with: paper-traded research data, educational only,
  not investment advice.

## Access

The preview pool (`get_pool(view="preview")`), `get_daily_report`,
`get_regime_context`, `get_market_calendar_status`, and `get_playbook` are on
every GammaRips plan. The full pool (`get_pool` with `view="enriched"`, `"raw"`,
or `"features"`), `get_signal`, `get_liquidity`, `query_outcomes`, and
`replay_contract` need GammaRips Pro. A trade plan needs Pro. If a tool returns
`subscription_required`, give the user the tool's message as it is written,
then continue with the tools that work. Do not retry the call.

## Tools

- **Day:** `get_market_calendar_status` (`view="freshness"` before you use the
  pool), `get_daily_report`, `get_regime_context`.
- **Pool:** `get_pool(view="enriched")` for thesis, technicals, catalyst, and
  the selected contract per name. `get_pool(view="features")` for feature
  vectors.
- **One name:** `get_signal(view="detail")`, `get_signal(view="earnings")` for
  the earnings window, `get_liquidity(contract=...)` for fresh open interest
  and volume.
- **History for the exit:** `query_outcomes` with `view="harvest"` (touch
  probabilities), `"surface"` (MFE and MAE), `"exit_rule"` (score a bracket or
  trailing stop), `"labels"` and `"summary"` (reference brackets).
  `replay_contract` returns the price tape.
