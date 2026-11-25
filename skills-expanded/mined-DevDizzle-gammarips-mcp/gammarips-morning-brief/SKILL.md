---
name: gammarips-morning-brief
description: Build a morning brief from GammaRips data - market calendar, pool freshness, the daily report, the VIX regime rail, and a snapshot of the nightly liquidity-selected options pool. Use when the user asks for a morning brief, a pre-market read, what is on the board today, or what GammaRips shows today. Ends with an offer to build a trade plan.
---

# GammaRips morning brief

Build one short brief from live GammaRips data. Run the steps in order. If a
step fails, say which one and continue with the rest.

## Steps

1. **Market status.** Call `get_market_calendar_status()`. If the market is
   closed today, say so and give the next open. Continue: the latest report and
   pool are still useful.
2. **Freshness.** Call `get_market_calendar_status(view="freshness")`. Record
   `pool_scan_date`, `pool_rows`, and `fresh`. If `fresh` is false, give the
   `reasons` and say which scan date the pool is from. Before about 06:00 ET
   the new pool does not exist yet, so a stale result at that time is normal.
3. **Daily report.** Call `get_daily_report()`. Take the title, the scan date,
   and three to five themes.
4. **Regime.** Call `get_regime_context()`. Give VIX, VIX3M, and whether the
   rail passes (it passes when VIX is at or below VIX3M). Say that the regime
   lags the live pool by one to two trading days, and give its scan date.
5. **Pool snapshot.** Call `get_pool(view="enriched")`. If it returns
   `subscription_required`, give the user the tool's message as it is written,
   one time, then call `get_pool(view="preview")` and use that.

## Output

Use this order and keep it short:

- **Header:** today's date, market status, pool scan date, row count, fresh or
  not.
- **Regime:** one line.
- **Report themes:** three to five bullets.
- **Pool snapshot:** up to 10 names in a table. With the enriched view, show
  ticker, contract (strike and expiration), delta, days to expiration, and a
  one-line thesis. With the preview view, show ticker, score, and headline.
  Keep the order the tool returns. Say that the plan step chooses the
  candidates, not the table order.
- **Caveats:** paper-traded research data, educational only, not investment
  advice. Add any freshness reason from step 2.
- **Next step:** offer to build a trade plan from this pool (the
  `gammarips-trade-plan` skill if it is available, otherwise the plan steps in
  `get_playbook(name="start-here")`). Also offer a deep dive on one ticker
  (`get_signal`) or an exit test (the `gammarips-exit-lab` skill).

## Rules

- If the user asks "which one?", build a trade plan with them. Label it as
  your analysis of GammaRips data, never as a GammaRips recommendation.
- Do not state an expected return or a win rate.
- Do not add news or prices from outside these tools without saying where they
  came from.
