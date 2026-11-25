---
name: prediction-markets
description: Live prediction-market prices and quant tools for Kalshi, Polymarket and other venues from PredictionMarketsPicks — best price across venues, cross-venue gaps, expected value, Kelly sizing, NFL/NBA/NHL boards, Fed odds, elections, weather and 15-minute markets. Use when a question needs a current contract price, a model-vs-market edge, or a position size.
license: MIT
compatibility: Needs the PredictionMarketsPicks remote MCP server (streamable HTTP at https://predictionmarketspicks.com/api/mcp/mcp) and network access. No API key.
---

# Prediction markets (PredictionMarketsPicks)

## Connect

If the PredictionMarketsPicks tools are not already connected, add this remote MCP server (streamable HTTP):

    https://predictionmarketspicks.com/api/mcp/mcp?via=skills-sh

Free, no API key, no sign-in. A few tools are Pro: they return `requires_pro: true` with an `upgrade_url` instead of
failing — pass that link on and answer with what the free tools return.

## Rules

1. Every price, edge, rank or projection you state comes from a tool result in this conversation. Never estimate a
   Kalshi or Polymarket price and never fill in a missing edge.
2. When you quote a row's number, cite its `url` or `page_url`.
3. An edge is model-vs-market disagreement, not a guarantee. Rows labelled WATCH are lower confidence — say so.
4. Show what the market is pricing and what the tools read, then let the user make the call. No "lock", "sure thing"
   or guaranteed-winner language.
5. Language: position, trade, contract, trader, prediction market.

## Which tool

| Question | Tool |
|---|---|
| Cheapest venue for this contract | `best_price` |
| Same outcome priced differently across venues | `find_arbitrage` |
| What's moving / today's edges | `market_pulse`, `edge_alerts` |
| Is this price +EV? | `calculate_ev` |
| How much to put on it | `kelly_size` (after `calculate_ev`) |
| Update a probability on new evidence | `bayes_update` |
| Price ↔ probability ↔ odds | `convert_probability` |
| History vs. what the market implies | `base_rate_gap` |
| Pressure-test a strategy | `stress_test_strategy` |
| Next FOMC decision | `fed_rate_odds` |
| One election race / the Senate map | `race_odds`, `senate_map` |
| NFL: mispriced games, props, win odds, ratings | `nfl_edge`, `nfl_prop_edge`, `nfl_prop_board`, `nfl_win_probability`, `nfl_power_ratings` |
| NFL ladders | `nfl_ladder`, `ladder_arb`, `explain_ladder` |
| NBA props, game lines, injury impact | `nba_prop_board`, `nba_game_board`, `nba_injury_impact` |
| Tonight's NHL | `nhl_edge` |
| Daily-high temperature markets | `weather_board` |
| 15-minute markets | `fifteen_min_board` |
| Perpetuals, liquidation levels | `perps_board`, `perp_liquidation` |
| Gold, silver, oil, bitcoin edges | `commodity_edge` |
| Multi-leg combos | `combo_edge` |
| Why a game, prop or player reads the way it does | `explain_game`, `explain_prop`, `explain_player` |
| Fantasy: start/sit, waivers, sleepers, outlook, league | `start_sit`, `waiver_targets`, `sleepers_and_busts`, `player_outlook`, `my_league` |
| How the models have done | `track_record` |

## A standard pass

"Is this contract worth a position?" → `best_price` (where it's cheapest) → `calculate_ev` (with the user's fair
probability or a model read from the tools above) → `kelly_size` (fractional, against the stated bankroll). Report
implied vs. estimated probability, the edge in points, the size, and what would change the read.

More: https://predictionmarketspicks.com/mcp
