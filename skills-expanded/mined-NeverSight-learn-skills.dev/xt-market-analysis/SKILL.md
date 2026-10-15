---
name: xt-market-analysis
description: In-depth crypto market analysis. Use when the user asks to analyze a coin's trend, long/short dynamics, market sentiment, funding rate arbitrage, liquidations, the fear & greed index, or a market overview. All data is public; no API Key required.
---

# In-Depth Market Analysis

Combine the XT market-data tools of the `xt-tradekit` MCP with aggregated public-data tools to produce structured analysis. Symbol format: `btc_usdt`.

## Data Attribution

When citing market-wide derivatives metrics (open interest, long/short ratio, taker buy/sell volume, liquidations) and sentiment/coin data, consistently describe them as "**TradeKit aggregated public market data**" and do not mention specific external data providers. XT market data is described as "XT market data".

## Single-Coin Market Analysis Flow

Call as needed in parallel (you don't have to call them all; choose based on the user's question):

1. **Price and trend**: `xt_futures_ticker` (last price/mark price/index price) + `xt_futures_klines` (two intervals: 1h×24 and 1d×14)
2. **Funding rate**: `xt_futures_funding_rate` + `xt_futures_funding_rate_history` (to judge which side is paying and how crowded the trade is)
3. **Positioning and dynamics**: `market_open_interest` (open interest) + `market_long_short_ratio` (long/short account ratio) + `market_taker_volume` (taker buy/sell pressure)
4. **Liquidations**: `market_recent_liquidations` (recent liquidation direction and scale)
5. **Sentiment**: `market_fear_greed`

## Market Overview Flow

`market_global_overview` (total market cap/BTC dominance) + `market_fear_greed` + `xt_spot_top_movers` (gainers/turnover leaderboards).

## Report Structure

```
## <Coin> Market Analysis
**One-line conclusion** (bullish/bearish/ranging + core rationale)

### Price and Trend
Current price, 24h change, key support/resistance (based on candlestick highs and lows)

### Derivatives Metrics
Funding rate (direction and historical comparison), open interest, long/short ratio, taker buy/sell pressure, recent liquidations

### Market Sentiment
Fear & greed index and its meaning

### Risk Warning
```

## Analysis Guidelines

- Conclusions must come from data, not speculation; when data points conflict, state so honestly.
- A positive funding rate = longs are paying (the market is crowded long); sustained extreme values signal reversal risk.
- Long/short ratio >1 is bullish, <1 is bearish; highlight when it diverges from price.
- Liquidations concentrated on one side indicate leverage on that side was just flushed out.
- Fear & greed: 0-25 extreme fear, 25-45 fear, 45-55 neutral, 55-75 greed, 75-100 extreme greed.
- Always end with: "The above is data analysis and does not constitute investment advice."

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
