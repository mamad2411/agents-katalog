---
name: gammarips-trade-plan
description: Build a concrete options trade plan with the user from GammaRips data - shortlist liquid contracts from the nightly pool, check earnings and fresh liquidity, set the target and stop from the realized history of past pool contracts, and size the position to a maximum loss. Use when the user asks for a trade, a good options trade, a trade idea, what to buy or look at today, or a plan for the next session.
---

# GammaRips trade plan

Build the user's own trade plan from GammaRips data. Run the steps in order.
If a step fails, say which one and continue where you can.

## Steps

1. **Session and freshness.** Call `get_market_calendar_status()` and
   `get_market_calendar_status(view="freshness")`. If the market is closed,
   plan for the next session and say when the next pool lands (about 06:00 ET).
2. **Regime.** Call `get_regime_context()`. The rail passes when VIX is at or
   below VIX3M. If it fails, say so. A failed rail makes the default answer a
   no-trade unless the user chooses otherwise.
3. **Risk budget.** Use the user's risk budget per trade. If you do not know
   it, ask one time. If the user does not answer, plan with a maximum loss of 500 USD
   per trade and say that you assumed it.
4. **Pool.** Call `get_pool(view="enriched")`. Note each name's selected
   contract, delta, days to expiration, thesis, and catalyst.
5. **Shortlist.** Use the user's criteria. If the user has none, start with
   |delta| 0.20 to 0.46 (the engine's reference band). Take up to 5 names into
   the checks.
6. **Checks for each name.**
   - Earnings: `get_signal(ticker=..., view="earnings")`. Drop a name with
     earnings before expiration, unless the user wants an earnings trade.
   - Liquidity: `get_liquidity(contract=...)`. Drop a contract with thin
     open interest or no prints today.
   Keep the best 1 to 3 that pass. Say why each one passed.
7. **Exit from history.** Call `query_outcomes(view="harvest",
   targets=[25, 50, 75, 100], stops=[20, 30, 40])` and
   `query_outcomes(view="surface", aggregate_only=True)`. Select a target that
   past pool contracts touched often enough, and a stop outside the normal
   adverse move (the MAE quantiles). Score the pair with
   `query_outcomes(view="exit_rule", target_pct=<T>, stop_pct=<S>)`. Give the
   touch rates with their horizon (3 trading days) and row count.
8. **Size.** Contracts = maximum loss / (premium x 100 x stop), with the stop
   as a fraction (30% = 0.30). Round down.
   If the result is 0, say the contract is too expensive for the budget.

## Output

For each candidate, one block:

- **Contract:** ticker, strike, expiration, call, delta, days to expiration.
- **Why it passed:** thesis in one line, liquidity numbers, earnings check.
- **Entry:** about 10:00 ET, limit order near the mid. Give the reference
  premium and say that it is a reference, not a quote.
- **Target and stop:** the levels, and the history behind them (touch rate,
  horizon, N).
- **Size and maximum loss:** contracts and dollars.
- **No-trade if:** the conditions that cancel the plan at 10:00 ET (for
  example, the regime rail fails, or the contract has no prints).

If nothing passes, give a reasoned no-trade: the exact check that failed for
each name, and when to look again.

End with: "This is my analysis of GammaRips data. You decide. Paper-traded
research data. Educational only. Not investment advice."

## Rules

- GammaRips has no pick endpoint. This plan is your analysis with the user.
  Never call it a GammaRips recommendation.
- Do not state an expected return, a win rate, or a guarantee. Touch rates
  are history for past contracts, with their horizon and N.
- Do not use pool-wide averages or the `positions` / `performance` views as a
  reason to trade or not to trade. Those views hold a retired engine test.
- GammaRips cannot place orders. The user places the trade.
- If a tool returns `subscription_required`, give the user the tool's message
  as it is written. A trade plan needs GammaRips Pro.
