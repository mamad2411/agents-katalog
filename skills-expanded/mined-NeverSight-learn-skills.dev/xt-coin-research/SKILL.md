---
name: xt-coin-research
description: Coin research and risk checks. Use when the user wants to understand a coin's fundamentals (market cap / FDV / supply / project overview), compare multiple coins, or check the security of an on-chain token contract (honeypot / rug / tax rate / holder concentration). No API Key required.
---

# Coin Research

Data is obtained via the `xt-tradekit` MCP tools. When citing non-XT data, consistently describe it as "TradeKit aggregated public data" and do not mention specific external data providers.

## Tool Mapping

| Purpose | Tool |
|------|------|
| Fundamentals (market cap / FDV / supply / ATH / category / overview) | `market_coin_profile` (pass a symbol like btc or a name like bitcoin) |
| XT spot market data and liquidity | `xt_spot_ticker`, `xt_spot_depth` |
| On-chain token security check | `market_token_security` (chain + contract address) |
| Global market context | `market_global_overview` |

## Single-Coin Research Report

1. Use `market_coin_profile` to get fundamentals;
2. Use `xt_spot_ticker` to get real-time market data on XT (if the coin has a trading pair on XT);
3. Output structure:

```
## <Coin> Research
**Positioning**: one line (category + ranking)

### Fundamentals
Market cap/rank, FDV, circulation ratio (circulating/total supply), drawdown from ATH, 7d/30d performance

### Market Data (XT)
Current price, 24h change, turnover

### Key Points and Risks
Supply unlock pressure (low circulation ratio?), FDV/market cap ratio, category momentum
```

## Multi-Coin Comparison

Call `market_coin_profile` for each coin and output a comparison table (market cap, FDV, circulation ratio, 7d/30d change, drawdown from ATH), followed by 3-5 summary points.

## Token Security Check (on-chain contract)

When the user provides a contract address:

1. If no chain is specified, ask (supported: eth/bsc/polygon/arbitrum/optimism/base/avalanche/solana).
2. Call `market_token_security` and focus your interpretation on:
   - `isHoneypot=1` → **Honeypot, can only buy but not sell — issue an immediate red-flag warning**
   - Buy/sell tax >10% → high-tax risk
   - `isOpenSource=0` → not open source, cannot be audited
   - `isMintable=1` / `canTakeBackOwnership=1` / `hiddenOwner=1` → contract permission risks
   - High `top10HolderPct` (>50%) → concentrated holdings, prone to dumping
3. Output "Risk level: Low/Medium/High" + an item-by-item explanation.

## Guidelines

- If data is missing, write "No data available"; do not fabricate.
- Always end with: "The above is data analysis and does not constitute investment advice."

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
