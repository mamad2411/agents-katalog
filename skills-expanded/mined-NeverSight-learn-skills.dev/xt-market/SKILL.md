---
name: xt-market
description: XT market data queries. Use when the user asks about coin prices, spot/futures market data, order book depth, candlesticks, funding rates, gainers/losers leaderboards, or volume leaderboards. Based on the xt-tradekit MCP tools; no API Key required.
---

# XT Market Data Queries

All market data is obtained via the `xt-tradekit` MCP tools; no API Key required.

## Symbol Format

XT trading pairs use lowercase with an underscore: `btc_usdt`, `eth_usdt`. Automatically convert when the user says "BTC", "BTC/USDT", or "BTCUSDT".

## Tool Mapping

| User intent | Tool |
|---------|------|
| Spot price / 24h market data | `xt_spot_ticker` |
| Gainers / losers / turnover leaderboards | `xt_spot_top_movers` (direction: gainers/losers/volume) |
| Spot order book | `xt_spot_depth` |
| Spot candlesticks | `xt_spot_klines` (interval: 1m/5m/15m/30m/1h/4h/1d/1w) |
| Trading pair rules (precision/min order) | `xt_spot_symbol_info` |
| Futures price (incl. mark price/index price) | `xt_futures_ticker` |
| Futures order book | `xt_futures_depth` |
| Futures candlesticks | `xt_futures_klines` |
| Current funding rate | `xt_futures_funding_rate` |
| Historical funding rate | `xt_futures_funding_rate_history` |
| Contract specs (face value per contract/leverage) | `xt_futures_contract_info` |

## Interaction Rules

- When the user names a coin but doesn't say spot or futures: default to spot; if the context is about futures, use futures.
- When the user doesn't give a trading pair, ask once; **do not follow up more than 1 round** — execute as soon as you have it.
- When deeper long/short, liquidation, or sentiment analysis is needed, switch to the `xt-market-analysis` skill.

## Output Guidelines

- **Bold** prices; use 📈 for gains and 📉 for losses.
- The `changePct` field is a decimal (0.0262 = 2.62%); convert it to a percentage when displaying.
- Funding rate is likewise a decimal; display as a percentage (0.0001 = 0.01%).
- Use tables for candlesticks and leaderboards; do not paste raw JSON unless the user asks.
- Timestamps are in milliseconds UTC; convert to a readable format when displaying.

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
