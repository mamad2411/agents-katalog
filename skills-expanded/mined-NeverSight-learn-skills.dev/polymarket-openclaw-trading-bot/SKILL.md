---
name: polymarket-openclaw-trading-bot
description: Build and operate AI-powered trading bots for Polymarket prediction markets with CLOB arbitrage on BTC 5m/15m windows
triggers:
  - how do I set up a Polymarket trading bot
  - create a bot to trade BTC 5 minute markets on Polymarket
  - configure OpenClaw AI decision engine for Polymarket
  - implement Polymarket CLOB arbitrage strategy
  - debug Polymarket trading bot order execution
  - set up wallet authentication for Polymarket bot
  - run a TypeScript prediction market trading bot
  - configure trade strategies for Polymarket short-duration markets
---

# Polymarket OpenClaw Trading Bot

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

A TypeScript/Node.js trading bot for Polymarket prediction markets using the CLOB (Central Limit Order Book) API. Specializes in short-duration BTC markets (5m/15m windows) with rule-based strategies, optional OpenClaw AI decision layer, strict risk management, and real-time market polling.

## What This Bot Does

- **Market Selection**: Automatically constructs Polymarket market slugs from coin + period (e.g., BTC + 5m)
- **Price Polling**: Fetches real-time UP/DOWN outcome token prices from Gamma/CLOB API
- **Strategy Execution**: Runs configurable `trade_1` or `trade_2` strategies with entry/exit rules
- **OpenClaw AI Layer**: Optional deterministic decision engine for signal experimentation
- **Order Management**: Submits market orders via CLOB v2 with retry logic and cooldowns
- **Authentication**: L1 wallet signing to derive API credentials, L2 authenticated trading client
- **Risk Controls**: Cooldowns, position limits, emergency swaps, balance validation

## Installation

```bash
git clone https://github.com/Predictly-MCP-Labs/polymarket-openclaw-ai-btc-arbitrage-trading-bot.git
cd polymarket-openclaw-ai-btc-arbitrage-trading-bot
npm install
```

**Prerequisites:**
- Node.js ≥ 20.6
- Polygon wallet with private key
- USDC balance on Polygon for trading
- Polymarket account with funder/proxy address

## Environment Configuration

Create `.env` file (never commit this):

```bash
# Required wallet credentials
POLYMARKET_PRIVATE_KEY=0x...  # Your wallet private key
POLYMARKET_FUNDER_ADDRESS=0x...  # Funder/deposit proxy address

# Optional signature type (defaults to proxy-friendly)
POLYMARKET_SIGNATURE_TYPE=POLY_PROXY  # EOA | POLY_PROXY | POLY_GNOSIS_SAFE | POLY_1271
```

**Environment Variable Reference:**
- `POLYMARKET_PRIVATE_KEY`: Wallet private key for signing CLOB operations (required)
- `POLYMARKET_FUNDER_ADDRESS`: Address holding trading collateral (required)
- `PROXY_WALLET_ADDRESS`: Alternate alias for funder address
- `POLYMARKET_SIGNATURE_TYPE`: Signature method for your account type

## Strategy Configuration (trade.toml)

The bot uses TOML for strategy configuration:

```toml
# Core strategy settings
strategy = "trade_1"  # or "trade_2"
trade_usd = 10.0      # Notional per buy in USD
max_retries = 3       # Retries for transient errors
entry_buy_cooldown_sec = 30  # Pause after failed entry

# Market selection
[market]
market_coin = "btc"    # btc | eth | sol | xrp
market_period = "5"    # 5 | 15 | 60 | 240 | 1440 (minutes)

# trade_1 strategy: time/price exits
[trade_1]
buy_range_start_pct = 40  # Enter when price is 40-60%
buy_range_end_pct = 60
exit_time_pct = 80        # Exit at 80% of window elapsed
exit_price_min_pct = 55   # Only exit if price >= 55%
emergency_swap_enabled = false

# trade_2 strategy: ratio-based
[trade_2]
entry_ratio_min = 1.05
entry_ratio_max = 1.25
exit_ratio_threshold = 0.95
exit_time_emergency_pct = 90
emergency_swap_enabled = true

# Optional OpenClaw AI decision layer
[openclaw]
enabled = false       # Set true to activate
mode = "deterministic"  # deterministic | http
min_edge_bps = 50     # Minimum edge in basis points
max_spread_bps = 200  # Maximum allowed spread
lookback_points = 12  # Price history window

# Optional HTTP/LLM integration
# [openclaw.http]
# url = "https://your-openclaw-service.example.com/decide"
# bearer_token = "optional_token"
# timeout_ms = 2500
```

## Running the Bot

```bash
# Development mode with hot reload
npm run dev

# Production build and run
npm run build
npm start
```

## Key Code Patterns

### Initialize CLOB Client and Authenticate

```typescript
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers";

// Create wallet from private key
const wallet = new Wallet(process.env.POLYMARKET_PRIVATE_KEY!);

// Initialize CLOB client
const clobClient = new ClobClient(
  "https://clob.polymarket.com",  // host
  137,  // Polygon chain ID
  wallet,
  {
    funderAddress: process.env.POLYMARKET_FUNDER_ADDRESS,
    signatureType: parseInt(process.env.POLYMARKET_SIGNATURE_TYPE || "1")
  }
);

// Derive or create API credentials
const apiCreds = await clobClient.deriveApiKey();
console.log("API Key:", apiCreds.apiKey);
```

### Fetch Market Data

```typescript
import { getMarket } from "./services/gamma";

// Build market slug from config
const coin = config.market.market_coin;  // "btc"
const period = config.market.market_period;  // "5"
const slug = `will-btc-close-higher-in-${period}-minutes`;

// Fetch market metadata
const market = await getMarket(slug);
console.log("Market ID:", market.id);
console.log("Condition ID:", market.condition_id);
console.log("Tokens:", market.tokens);  // [UP token, DOWN token]
```

### Poll Prices and Execute Strategy

```typescript
import { Trade } from "./trade/trade";

// Create trade instance
const trade = new Trade(
  clobClient,
  config.trade_usd,
  config.max_retries,
  config.entry_buy_cooldown_sec
);

// Update prices (fetches from CLOB)
await trade.updatePrices(
  market.tokens[0].token_id,  // UP token
  market.tokens[1].token_id   // DOWN token
);

// Make trading decision based on strategy
import { make_trading_decision } from "./trade/decision";

const decision = await make_trading_decision(
  trade,
  config.strategy,
  config.trade_1,
  config.trade_2,
  market.end_date_iso
);

console.log("Decision:", decision);
```

### Place Market Order

```typescript
// Buy UP token
const buyResult = await trade.buy(
  market.tokens[0].token_id,  // UP token ID
  "UP"
);

if (buyResult.success) {
  console.log("Buy successful:", buyResult.orderId);
} else {
  console.error("Buy failed:", buyResult.error);
}

// Sell position
const sellResult = await trade.sell("UP");
if (sellResult.success) {
  console.log("Sell successful:", sellResult.orderId);
}
```

### Strategy Decision Logic (trade_1)

```typescript
import { TradeAction } from "./trade/decision";

function evaluateTrade1Strategy(
  trade: Trade,
  config: Trade1Config,
  endTimeIso: string
): TradeAction {
  const now = Date.now();
  const endTime = new Date(endTimeIso).getTime();
  const timeElapsedPct = ((now - (endTime - 5 * 60 * 1000)) / (5 * 60 * 1000)) * 100;

  const upPrice = trade.upPrice;
  const downPrice = trade.downPrice;

  // Entry logic: price in range, not already holding
  if (!trade.hasBought) {
    const priceInRange = 
      upPrice >= config.buy_range_start_pct &&
      upPrice <= config.buy_range_end_pct;

    if (priceInRange) {
      return { action: "BUY_UP", reason: "Price in entry range" };
    }
    return { action: "HOLD", reason: "Waiting for entry conditions" };
  }

  // Exit logic: time threshold or price target
  const shouldExitTime = timeElapsedPct >= config.exit_time_pct;
  const shouldExitPrice = upPrice >= config.exit_price_min_pct;

  if (shouldExitTime && shouldExitPrice) {
    return { action: "CLOSE_POSITION", reason: "Time and price exit met" };
  }

  return { action: "HOLD", reason: "Holding position" };
}
```

### OpenClaw Decision Integration

```typescript
import { getOpenClawDecision } from "./trade/openclaw";

if (config.openclaw.enabled) {
  const openclawDecision = await getOpenClawDecision(
    trade,
    {
      upPrice: trade.upPrice,
      downPrice: trade.downPrice,
      timeToExpiry: (new Date(market.end_date_iso).getTime() - Date.now()) / 1000,
      hasBought: trade.hasBought,
      positionSide: trade.positionSide
    },
    config.openclaw
  );

  console.log("OpenClaw signal:", openclawDecision.action);
  console.log("Reason:", openclawDecision.reason);
}
```

### Error Handling with Retry Logic

```typescript
import { retryOnTransient } from "./utils/retry";

async function placeOrderWithRetry(
  clobClient: ClobClient,
  tokenId: string,
  side: "BUY" | "SELL",
  size: number,
  maxRetries: number
) {
  return retryOnTransient(
    async () => {
      const order = await clobClient.createMarketOrder({
        tokenID: tokenId,
        side,
        amount: size.toString()
      });

      const result = await clobClient.postOrder(order);
      return result;
    },
    maxRetries,
    (error) => {
      // Check if error is transient (network, 5xx, 429)
      const isTransient = 
        error.message.includes("ECONNRESET") ||
        error.message.includes("429") ||
        error.message.includes("5xx");
      return isTransient;
    }
  );
}
```

## Common Trading Workflows

### Setup and Run for BTC 5-Minute Markets

1. Configure `.env` with wallet credentials
2. Edit `trade.toml`:
   ```toml
   [market]
   market_coin = "btc"
   market_period = "5"
   
   strategy = "trade_1"
   trade_usd = 5.0
   ```
3. Run: `npm run dev`
4. Monitor logs for entry/exit signals

### Switch to 15-Minute Markets

Change only the period in `trade.toml`:
```toml
[market]
market_period = "15"
```

### Enable OpenClaw AI Decision Layer

```toml
[openclaw]
enabled = true
mode = "deterministic"
min_edge_bps = 50
max_spread_bps = 200
lookback_points = 12
```

### Run Multiple Strategies Simultaneously

Run separate processes with different configs:

```bash
# Terminal 1: 5-minute BTC
cp trade.toml trade-5m.toml
# Edit trade-5m.toml: market_period = "5"
CONFIG_PATH=trade-5m.toml npm run dev

# Terminal 2: 15-minute BTC
cp trade.toml trade-15m.toml
# Edit trade-15m.toml: market_period = "15"
CONFIG_PATH=trade-15m.toml npm run dev
```

## Module Reference

| Module | Path | Purpose |
|--------|------|---------|
| Entry point | `src/index.ts` | Bootstrap, auth, market loop |
| CLOB service | `src/services/clob.ts` | Wallet, signer, client setup |
| Gamma API | `src/services/gamma.ts` | Market metadata by slug |
| Config | `src/config/toml.ts` | TOML parsing and validation |
| Env validation | `src/config/validateEnv.ts` | Zod schema for env vars |
| Slug builder | `src/config/slug.ts` | Coin + period → market slug |
| Decision engine | `src/trade/decision.ts` | Strategy routing (trade_1/trade_2) |
| Price polling | `src/trade/prices.ts` | Quote fetching and display |
| Trade execution | `src/trade/trade.ts` | Buy/sell, cooldowns, balances |
| OpenClaw | `src/trade/openclaw.ts` | AI decision layer |
| Retry logic | `src/utils/retry.ts` | Transient error handling |
| Error messages | `src/utils/tradingErrorMessage.ts` | Human-friendly errors |

## Troubleshooting

### "Invalid BytesLike" Error

**Cause**: Malformed `POLYMARKET_PRIVATE_KEY`

**Fix**: Ensure private key starts with `0x` and is 64 hex characters:
```bash
POLYMARKET_PRIVATE_KEY=0xabcdef1234567890...
```

### Orders Not Filling

**Possible causes:**
- Insufficient USDC balance on funder address
- Market moved before order posted
- Spread too wide (`max_spread_bps` exceeded)

**Debug:**
```typescript
const balance = await clobClient.getBalance();
console.log("USDC balance:", balance.usdc);

console.log("Current spread:", Math.abs(trade.upPrice - trade.downPrice));
```

### Entry Cooldown Blocking Trades

**Expected behavior**: After a failed buy, bot waits `entry_buy_cooldown_sec` before retrying

**Adjust**: Lower cooldown in `trade.toml`:
```toml
entry_buy_cooldown_sec = 10  # Instead of 30
```

### OpenClaw Not Triggering

**Check**:
1. `[openclaw].enabled = true` in `trade.toml`
2. Mode is `"deterministic"` or `"http"` with valid endpoint
3. Logs show "OpenClaw signal:" messages

**Debug**:
```typescript
console.log("OpenClaw config:", config.openclaw);
console.log("Edge BPS:", calculatedEdge);
```

### API Authentication Failures

**Symptoms**: "401 Unauthorized" or "Invalid signature"

**Fix**:
1. Verify `POLYMARKET_SIGNATURE_TYPE` matches your account:
   - `EOA` for standard wallets
   - `POLY_PROXY` for Polymarket proxy accounts
2. Regenerate API credentials:
   ```typescript
   const newCreds = await clobClient.createApiKey();
   ```

### Market Not Found

**Error**: `Market slug not found`

**Cause**: Coin/period combination doesn't match active Polymarket markets

**Fix**: Verify active markets at polymarket.com and adjust:
```toml
[market]
market_coin = "btc"  # Check available coins
market_period = "5"  # Check available periods
```

## Advanced Patterns

### Custom Decision Logic

Extend decision engine with custom strategy:

```typescript
// src/trade/customStrategy.ts
export function customDecision(
  trade: Trade,
  customConfig: any
): TradeAction {
  // Your custom logic
  const momentum = calculateMomentum(trade.priceHistory);
  
  if (momentum > customConfig.momentum_threshold) {
    return { action: "BUY_UP", reason: "Strong upward momentum" };
  }
  
  return { action: "HOLD", reason: "Waiting for momentum" };
}

// Register in decision.ts
import { customDecision } from "./customStrategy";

if (config.strategy === "custom") {
  return customDecision(trade, config.custom);
}
```

### Monitor Multiple Markets

```typescript
const markets = [
  { coin: "btc", period: "5" },
  { coin: "eth", period: "5" },
  { coin: "btc", period: "15" }
];

for (const market of markets) {
  const slug = buildSlug(market.coin, market.period);
  const marketData = await getMarket(slug);
  
  // Run parallel trading loops
  runMarketLoop(marketData, config);
}
```

### Backtesting Strategy

```typescript
import { Trade } from "./trade/trade";

async function backtestStrategy(
  historicalData: PricePoint[],
  config: TomlConfig
) {
  const results = [];
  
  for (const dataPoint of historicalData) {
    const trade = new Trade(mockClient, config.trade_usd, 1, 0);
    trade.upPrice = dataPoint.upPrice;
    trade.downPrice = dataPoint.downPrice;
    
    const decision = await make_trading_decision(
      trade,
      config.strategy,
      config.trade_1,
      config.trade_2,
      dataPoint.endTime
    );
    
    results.push({ time: dataPoint.time, decision });
  }
  
  return results;
}
```

## Safety and Compliance

- **Start small**: Use low `trade_usd` values initially
- **Paper trading**: Test strategies without real orders first
- **Risk limits**: Respect `max_retries` and cooldowns
- **Market risk**: 5m/15m windows move fast; fills may not match signals
- **Regulatory**: Ensure compliance with local prediction market regulations
- **API limits**: CLOB has rate limits; bot includes retry backoff

## Key Search Terms

Polymarket trading bot, Polymarket CLOB API, Polymarket arbitrage bot, BTC 5 minute Polymarket, BTC 15 minute Polymarket, TypeScript prediction market bot, Polymarket API credentials, OpenClaw AI trading, Polymarket wallet setup, CLOB order execution
