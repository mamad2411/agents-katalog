---
name: prediction-market-arbitrage
description: Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi. Use when you need to match equivalent markets, compare prices, and verify whether a spread looks actionable.
license: MIT
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries curl, python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills
  tags: market,prediction
  platforms: agentskills.io,agentskill.sh,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# Prediction Market Arbitrage ⚖️

Find and analyze arbitrage opportunities across prediction markets such as Polymarket and Kalshi.

This skill helps agents:

- find matching markets across platforms
- compare current prices
- inspect orderbook depth and liquidity
- judge whether an apparent spread may be actionable

Powered by AIsa with a single `AISA_API_KEY`.

## Use when

- You want to find the Kalshi or Polymarket equivalent of a market on another platform.
- You want to compare implied probabilities across platforms for the same event.
- You want to check whether a price gap is large enough to investigate as a possible arbitrage.
- You want to verify liquidity before treating a spread as actionable.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other harnesses that implement the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` from [aisa.one](https://aisa.one).

## Quick start

```bash
export AISA_API_KEY="your-key"
```

## Example requests

### Detect price discrepancies

```text
"Find the current price difference for the US election market between Polymarket and Kalshi."
```

### Match cross-platform markets

```text
"Find the Kalshi equivalent for this Polymarket sports event."
```

### Track arbitrage spreads

```text
"Monitor the price spread for the upcoming NBA game across all supported prediction markets."
```

### Analyze orderbook depth

```text
"Check the orderbook depth on both platforms to see if the arbitrage opportunity is actionable."
```

## How to look up IDs

Most endpoints require an ID from the `/markets` or `/matching-markets` responses. Query markets first, then pass the relevant ID into downstream endpoints.

1. **Polymarket `token_id`**: Query `/polymarket/markets`, find `side_a.id` or `side_b.id` in the response, then use that value in the market price and orderbook endpoints.
2. **Kalshi `market_ticker`**: Query `/kalshi/markets`, find `market_ticker` in the response, then use that value in the market price and orderbook endpoints.

## Core capabilities

### 1. Find matching markets

The first step in arbitrage analysis is finding the same event on multiple platforms.

#### Match by event ticker or slug

```bash
# Find equivalent markets across platforms using a Polymarket slug
curl -X GET "https://api.aisa.one/apis/v1/matching-markets/sports?polymarket_market_slug={polymarket_market_slug}" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Or find equivalent markets using a Kalshi event ticker
curl -X GET "https://api.aisa.one/apis/v1/matching-markets/sports?kalshi_event_ticker={kalshi_event_ticker}" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### Match sports by date

```bash
# Find all matching sports markets across platforms for a specific date
curl -X GET "https://api.aisa.one/apis/v1/matching-markets/sports/{sport}?date={date}" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 2. Compare prices

Once matching markets are found, fetch the current prices on both platforms to calculate the spread.

#### Get Polymarket price

```bash
# token_id comes from side_a.id or side_b.id in /polymarket/markets response
curl -X GET "https://api.aisa.one/apis/v1/polymarket/market-price/{token_id}" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### Get Kalshi price

```bash
# market_ticker comes from /kalshi/markets response
curl -X GET "https://api.aisa.one/apis/v1/kalshi/market-price/{market_ticker}" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 3. Verify liquidity

A price discrepancy is only actionable if there is enough liquidity to execute the trades.

#### Polymarket orderbook

```bash
# token_id comes from side_a.id or side_b.id in /polymarket/markets response
curl -X GET "https://api.aisa.one/apis/v1/polymarket/orderbooks?token_id={token_id}" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### Kalshi orderbook

```bash
# ticker is the same value as market_ticker from /kalshi/markets response
curl -X GET "https://api.aisa.one/apis/v1/kalshi/orderbooks?ticker={ticker}" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## API endpoints reference

### Cross-platform endpoints

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `/matching-markets/sports` | Find matching sports markets | `polymarket_market_slug` or `kalshi_event_ticker` |
| `/matching-markets/sports/<sport>` | Find sports markets by date | `sport`, `date` |

### Price and liquidity endpoints

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `/polymarket/market-price/<token_id>` | Get Polymarket price | `token_id`, `at_time` |
| `/kalshi/market-price/<market_ticker>` | Get Kalshi price | `market_ticker`, `at_time` |
| `/polymarket/orderbooks` | Get Polymarket orderbook | `token_id`, `start_time`, `end_time` |
| `/kalshi/orderbooks` | Get Kalshi orderbook | `ticker`, `start_time`, `end_time` |

## Important note about cURL placeholders

The `{...}` values in the cURL examples are product-level placeholders and must be replaced before execution.

Execution constraint:
- Before running `curl`, the agent or runner must verify that every `{...}` placeholder has been replaced with a concrete value.
- If any placeholder such as `{token_id}`, `{market_ticker}`, `{sport}`, or `{date}` is still present in the final command, do not execute the command. Fail fast and surface a missing-parameter error instead.

This constraint is required because a literal brace placeholder may be interpreted by `curl` as URL globbing syntax rather than as plain text.

## Understanding arbitrage and odds

- **Prices as probabilities**: Prices are usually shown as decimals. For example, `0.65` means a 65% implied probability.
- **Arbitrage opportunity**: An opportunity exists when the combined price of all mutually exclusive outcomes across different platforms is less than `1.0`. For example, if "Yes" is trading at `0.40` on Polymarket and "No" is trading at `0.55` on Kalshi, buying both guarantees a payout of `1.00` for a total cost of `0.95`, before fees and slippage.
- **Liquidity check**: Always check the `/orderbooks` endpoints. A price difference might exist, but if the orderbook lacks depth, executing the trade may eliminate the profit.

## Pricing

| API | Cost |
|-----|------|
| Prediction market read query | $0.01 |

## Get started

1. Sign up at [aisa.one](https://aisa.one)
2. Get your API key
3. Add credits (pay-as-you-go)
4. Set the environment variable: `export AISA_API_KEY="your-key"`

## Full API reference

See [API Reference](https://aisa.one/docs/api-reference/) for complete endpoint documentation.
