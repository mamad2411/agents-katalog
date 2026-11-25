---
name: polymarket-openclaw-ai-arbitrage-bot
description: AI-enhanced Polymarket CLOB trading bot for BTC 5m/15m arbitrage with OpenClaw decision engine
triggers:
  - "set up polymarket trading bot"
  - "configure openclaw arbitrage strategy"
  - "trade on polymarket btc 5 minute markets"
  - "implement polymarket clob automation"
  - "debug polymarket api credentials"
  - "run polymarket ai trading bot"
  - "configure polymarket arbitrage bot"
  - "troubleshoot polymarket wallet signing"
---

# Polymarket OpenClaw AI Arbitrage Bot

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill enables AI coding agents to work with the OpenClaw Polymarket AI Trading Bot, a TypeScript-based automated trading system for Polymarket CLOB markets focusing on BTC 5-minute and 15-minute Up/Down prediction markets.

## What This Bot Does

The bot automates short-horizon prediction market trading on Polymarket using:

- **Market selection**: Targets BTC/ETH/SOL 5m/15m/60m markets
- **Pricing**: Polls Gamma/CLOB for UP/DOWN outcome token prices
- **Strategies**: Executes `trade_1` or `trade_2` rule-based strategies
- **OpenClaw decision layer**: Optional AI-enhanced decision engine
- **Execution**: Submits market orders via Polymarket v2 CLOB API
- **Risk management**: Cooldowns, retries, position limits, safety locks

**Architecture**: L1 wallet signing → API credential derivation → L2 authenticated CLOB client → market polling → strategy decision → order execution.

## Installation

```bash
# Clone the repository
git clone https://github.com/lorine93s/openclaw-polymarket-ai-arbitrage-trading-bot
cd openclaw-polymarket-ai-arbitrage-trading-bot

# Install dependencies
npm install

# Copy environment template
cp .env.example .env
```

## Environment Configuration

Edit `.env` with your credentials:

```bash
# Required: Polygon wallet private key (never commit this)
POLYMARKET_PRIVATE_KEY=your_private_key_here

# Required: Funder/proxy address that holds trading collateral
POLYMARKET_FUNDER_ADDRESS=0xYourFunderAddress

# Alternative to POLYMARKET_FUNDER_ADDRESS
# PROXY_WALLET_ADDRESS=0xYourProxyAddress

# Optional: Signature type (defaults to proxy-friendly)
# Options: EOA | POLY_PROXY | POLY_GNOSIS_SAFE | POLY_1271
POLYMARKET_SIGNATURE_TYPE=POLY_PROXY
```

**Validation**: The bot validates all required environment variables on startup using Zod schemas. Missing or invalid keys will trigger clear error messages.

## Strategy Configuration (trade.toml)

### Basic Market Setup

```toml
# Strategy selection
strategy = "trade_1"  # or "trade_2"

# Trade size in USD
trade_usd = 10.0

# Error handling
max_retries = 3
entry_buy_cooldown_sec = 30

# Market configuration
[market]
market_coin = "btc"      # btc | eth | sol | xrp
market_period = "5"      # "5" (5min) | "15" (15min) | "60" | "240" | "1440"
```

### Trade Strategy 1 (Time-Based Exits)

```toml
[trade_1]
# Entry conditions
entry_range_min = 0.45
entry_range_max = 0.55
buy_up_ratio_threshold = 1.05
buy_down_ratio_threshold = 1.05

# Exit conditions
exit_after_secs = 120
exit_up_ratio_threshold = 0.95
exit_down_ratio_threshold = 0.95

# Emergency swap
emergency_swap_enabled = true
emergency_swap_ratio_threshold = 1.15
```

### Trade Strategy 2 (Price-Based Exits)

```toml
[trade_2]
# Entry
entry_range_min = 0.40
entry_range_max = 0.60
buy_up_ratio_threshold = 1.08
buy_down_ratio_threshold = 1.08

# Exit targets
exit_up_profit_target = 0.65
exit_down_profit_target = 0.35

# Emergency behavior
emergency_swap_enabled = false
```

### OpenClaw AI Decision Layer

```toml
[openclaw]
enabled = true
mode = "deterministic"  # or "http" for external LLM service

# Signal thresholds
min_edge_bps = 50        # Minimum edge in basis points (0.5%)
max_spread_bps = 200     # Maximum spread tolerance (2%)
lookback_points = 12     # Historical price points to analyze

# Optional: HTTP/LLM integration
# [openclaw.http]
# url = "https://your-openclaw-service.example.com/decide"
# bearer_token = "${OPENCLAW_API_TOKEN}"
# timeout_ms = 2500
```

## Running the Bot

```bash
# Development mode (with hot reload)
npm run dev

# Production build
npm run build
npm start

# Type checking
npm run typecheck

# Linting
npm run lint
```

## Core API and Code Patterns

### Market Slug Generation

```typescript
import { formatSlug } from './config/slug';

// Generate Polymarket market slug
const slug = formatSlug('btc', '5');
// Returns: "will-btc-close-higher-in-the-next-5-minutes"

const ethSlug = formatSlug('eth', '15');
// Returns: "will-eth-close-higher-in-the-next-15-minutes"
```

### CLOB Client Initialization

```typescript
import { initClobClient } from './services/clob';

// Initialize L1 client (for API key derivation)
const clobClient = await initClobClient();

// Derive or create API credentials
await clobClient.createOrDeriveAPIKey();

// Initialize L2 authenticated client
const l2Client = await initClobClient({ signatureType: 'POLY_PROXY', feeRecipient: 'YOUR_ADDRESS' });
```

### Market Data Fetching

```typescript
import { getMarketBySlug } from './services/gamma';

const marketData = await getMarketBySlug(slug);
if (!marketData) {
  throw new Error(`Market not found: ${slug}`);
}

console.log('Market ID:', marketData.id);
console.log('End time:', marketData.end_date_iso);
console.log('Tokens:', marketData.tokens);
// tokens[0] = { token_id, outcome: "Up" | "Down", price }
```

### Price Polling

```typescript
import { updatePrices } from './trade/prices';
import { Trade } from './trade/trade';

const trade = new Trade(
  l2Client,
  config,
  marketData.tokens[0].token_id,  // upTokenId
  marketData.tokens[1].token_id,  // downTokenId
  marketData.end_date_iso
);

// Poll prices and update trade state
await updatePrices(trade, clobClient);

// Access current prices
console.log('UP price:', trade.upPrice);
console.log('DOWN price:', trade.downPrice);
console.log('Spread:', trade.upPrice + trade.downPrice);
```

### Order Execution

```typescript
import { createAndPostMarketOrder } from './trade/trade';

// Buy UP token
await createAndPostMarketOrder(
  trade,
  'BUY',
  trade.upTokenId,
  trade.upPrice,
  10.0  // USD amount
);

// Sell position
if (trade.hasBought) {
  await createAndPostMarketOrder(
    trade,
    'SELL',
    trade.boughtTokenId,
    trade.boughtSide === 'Up' ? trade.upPrice : trade.downPrice,
    trade.boughtTokens  // Sell all tokens
  );
}
```

### Strategy Decision Logic

```typescript
import { make_trading_decision } from './trade/decision';

// Execute strategy decision
await make_trading_decision(trade);

// The function internally:
// 1. Checks if in position (hasBought)
// 2. Evaluates exit conditions (time/price based)
// 3. Checks entry conditions if no position
// 4. Optionally consults OpenClaw decision engine
// 5. Executes buy/sell orders with retry logic
```

### OpenClaw Decision Integration

```typescript
import { openclawDecision } from './trade/openclaw';

const decision = await openclawDecision(trade, config);

console.log('Action:', decision.action);  // BUY_UP | BUY_DOWN | CLOSE_POSITION | HOLD
console.log('Reason:', decision.reason);
console.log('Confidence:', decision.confidence);

// decision.action values:
// - 'BUY_UP': Signal to buy UP token
// - 'BUY_DOWN': Signal to buy DOWN token
// - 'CLOSE_POSITION': Signal to exit current position
// - 'HOLD': No action recommended
```

### Error Handling and Retries

```typescript
import { retryWithPolicy } from './utils/retry';
import { formatTradingError } from './utils/tradingErrorMessage';

try {
  await retryWithPolicy(
    async () => {
      return await clobClient.createOrder(orderArgs);
    },
    3,  // maxRetries
    'createOrder'
  );
} catch (err) {
  const friendlyMessage = formatTradingError(err);
  console.error('Order failed:', friendlyMessage);
  
  // Cooldown before retry
  if (shouldCooldown(err)) {
    await new Promise(r => setTimeout(r, config.entry_buy_cooldown_sec * 1000));
  }
}
```

## Common Patterns

### Running Multiple Market Windows

To trade both 5-minute and 15-minute markets simultaneously, run two separate processes:

**Terminal 1 - 5 minute config (trade-5m.toml)**:
```toml
[market]
market_coin = "btc"
market_period = "5"
```

```bash
npm run dev -- --config=trade-5m.toml
```

**Terminal 2 - 15 minute config (trade-15m.toml)**:
```toml
[market]
market_coin = "btc"
market_period = "15"
```

```bash
npm run dev -- --config=trade-15m.toml
```

### Balance Monitoring

```typescript
// Check USDC balance before trading
const balance = await l2Client.getBalance();
console.log('Available USDC:', balance);

if (balance < config.trade_usd) {
  throw new Error(`Insufficient balance: ${balance} < ${config.trade_usd}`);
}
```

### Position Tracking

```typescript
// Trade state tracking
class Trade {
  hasBought: boolean = false;
  boughtSide: 'Up' | 'Down' | null = null;
  boughtPrice: number = 0;
  boughtTokens: number = 0;
  boughtTokenId: string = '';
  boughtTime: number = 0;
  
  resetPosition() {
    this.hasBought = false;
    this.boughtSide = null;
    this.boughtPrice = 0;
    this.boughtTokens = 0;
    this.boughtTokenId = '';
    this.boughtTime = 0;
  }
}
```

### Safe Shutdown

```typescript
// Graceful shutdown handler
process.on('SIGINT', async () => {
  console.log('\n⚠️ Shutdown signal received');
  
  if (trade.hasBought) {
    console.log('🔒 Warning: Position still open!');
    console.log(`   Side: ${trade.boughtSide}`);
    console.log(`   Tokens: ${trade.boughtTokens}`);
    console.log('   Consider manual exit before shutdown');
  }
  
  process.exit(0);
});
```

## Troubleshooting

### "Private key must be a valid byteslike value"

**Cause**: Invalid or missing `POLYMARKET_PRIVATE_KEY` in `.env`.

**Solution**:
```bash
# Ensure private key is 64 hex characters (no 0x prefix in .env)
POLYMARKET_PRIVATE_KEY=abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

### API Credential Errors

**Symptom**: 401/403 errors from CLOB API.

**Solution**:
```typescript
// Re-derive API credentials
const clobClient = await initClobClient();
await clobClient.createOrDeriveAPIKey();

// Verify funder address matches
console.log('Funder:', process.env.POLYMARKET_FUNDER_ADDRESS);
```

### Order Placement Failures

**Common causes**:
1. Insufficient balance
2. Market expired/not active
3. Price moved (stale quote)
4. Network latency

**Debug approach**:
```typescript
// Add detailed logging
console.log('Attempting order:', {
  side: 'BUY',
  tokenId: trade.upTokenId,
  price: trade.upPrice,
  amount: config.trade_usd,
  balance: await l2Client.getBalance()
});

// Check market status
const market = await getMarketBySlug(slug);
console.log('Market active:', new Date(market.end_date_iso) > new Date());
```

### OpenClaw Decision Issues

**Symptom**: `HOLD` action when expecting trades.

**Solution**:
```toml
# Relax thresholds in trade.toml
[openclaw]
min_edge_bps = 25     # Lower from 50
max_spread_bps = 300  # Increase from 200
lookback_points = 6   # Reduce data requirements
```

### Cooldown Loops

**Symptom**: Bot stuck in cooldown after failed buys.

**Solution**:
```toml
# Reduce cooldown period for testing
entry_buy_cooldown_sec = 10  # Down from 30

# Or check for persistent errors
# - Wallet signing issues
# - Invalid funder address
# - Credential problems
```

### Market Not Found

**Symptom**: `Market not found: will-btc-close-higher-in-the-next-5-minutes`

**Solution**:
```typescript
// Verify market exists on Polymarket
// Check if period is active (markets may not exist outside trading hours)
// Try alternative period:
[market]
market_period = "15"  # Switch from "5" if 5m market unavailable
```

### Memory Leaks / High CPU

**Symptom**: Bot slows down over time.

**Solution**:
```typescript
// Limit lookback buffer size
const MAX_LOOKBACK = 100;
if (priceHistory.length > MAX_LOOKBACK) {
  priceHistory = priceHistory.slice(-MAX_LOOKBACK);
}

// Add polling delays
await new Promise(r => setTimeout(r, 2000));  // 2s between polls
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `src/index.ts` | Entry point, market loop, CLOB auth |
| `src/config/toml.ts` | Config schema and validation |
| `src/config/env.ts` | Environment variable loading |
| `src/config/slug.ts` | Market slug generation |
| `src/services/clob.ts` | CLOB client initialization |
| `src/services/gamma.ts` | Gamma API market data |
| `src/trade/trade.ts` | Trade class, order execution |
| `src/trade/decision.ts` | Strategy decision logic |
| `src/trade/prices.ts` | Price polling and updates |
| `src/trade/openclaw.ts` | OpenClaw AI decision engine |
| `src/utils/retry.ts` | Retry policy for transient errors |
| `src/utils/tradingErrorMessage.ts` | Human-readable error formatting |

## Safety Reminders

- **Start with small `trade_usd`** (5-10 USD) for testing
- **Paper trade first** by setting very restrictive entry thresholds
- **Monitor positions** — 5m/15m markets move fast
- **Execution risk exists** — partial fills, slippage, API latency
- **Not financial advice** — this is experimental automation software
- **Comply with local regulations** — prediction markets may be restricted in your jurisdiction
