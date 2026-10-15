---
name: polymarket-openclaw-ai-trading-bot
description: AI-enhanced Polymarket CLOB trading bot for BTC 5m/15m prediction markets with arbitrage strategies and risk management
triggers:
  - "set up polymarket trading bot"
  - "configure openclaw ai trading"
  - "trade polymarket btc 5 minute markets"
  - "implement polymarket clob arbitrage"
  - "run polymarket automated trading"
  - "configure polymarket trading strategies"
  - "debug polymarket trading bot"
  - "set up polymarket wallet authentication"
---

# Polymarket OpenClaw AI Trading Bot

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

An OpenClaw-enhanced Polymarket AI trading bot designed for BTC 5m/15m Up/Down prediction markets on the Polymarket CLOB. This TypeScript/Node.js system automates short-horizon prediction market trading using deterministic rule-based logic with optional HTTP/LLM OpenClaw decision engine for signal experimentation. Includes strict risk management gates (cooldowns, retries, safety locks), continuous market polling, and structured decision flow.

**Key capabilities:**
- Trades Polymarket BTC 5-minute and 15-minute Up/Down markets
- CLOB-based market orders with Gamma API integration
- Two built-in strategies (`trade_1`, `trade_2`) with configurable thresholds
- Optional OpenClaw AI decision layer (deterministic or HTTP mode)
- L1 wallet signing with L2 authenticated CLOB client
- Automatic retry logic for transient errors
- Entry cooldown and position management

## Installation

### Prerequisites

- Node.js ≥ 20.6
- Polygon wallet with Polymarket-compatible setup
- Small USDC balance for trading experiments

### Setup

```bash
git clone https://github.com/Predictly-MCP-Labs/polymarket-openclaw-ai-btc-arbitrage-trading-bot
cd polymarket-openclaw-ai-btc-arbitrage-trading-bot
npm install
```

### Environment Configuration

Create `.env` file from template:

```bash
cp .env.example .env
```

Required environment variables:

```bash
# Wallet configuration
POLYMARKET_PRIVATE_KEY=your_private_key_here
POLYMARKET_FUNDER_ADDRESS=your_funder_address_here

# Optional: signature type (defaults to proxy-friendly)
# Options: EOA, POLY_PROXY, POLY_GNOSIS_SAFE, POLY_1271
POLYMARKET_SIGNATURE_TYPE=POLY_PROXY

# Alternative to POLYMARKET_FUNDER_ADDRESS
PROXY_WALLET_ADDRESS=your_proxy_address_here
```

**Never commit `.env` to version control.**

## Configuration

### trade.toml Structure

The `trade.toml` file controls all trading behavior:

```toml
# Strategy selection: trade_1 or trade_2
strategy = "trade_1"

# Trading parameters
trade_usd = 1.0  # USD per trade
max_retries = 3  # Retry attempts for transient errors
entry_buy_cooldown_sec = 30  # Cooldown after failed entry

# Market selection
[market]
market_coin = "btc"  # Options: btc, eth, sol, xrp
market_period = "5"  # Options: 5, 15, 60, 240, 1440 (minutes)

# OpenClaw AI decision layer (optional)
[openclaw]
enabled = false  # Set true to enable
mode = "deterministic"  # Options: deterministic, http
min_edge_bps = 50  # Minimum edge in basis points
max_spread_bps = 200  # Maximum spread in basis points
lookback_points = 12  # Historical data points for decisions

# Optional HTTP/LLM integration
# [openclaw.http]
# url = "https://your-openclaw-service.example.com/decide"
# bearer_token = "your_bearer_token"
# timeout_ms = 2500

# Trade_1 strategy parameters
[trade_1]
sell_hold_sec = 120
sell_profit_target = 0.15
sell_stop_loss = -0.10
buy_last_sec = 30
range_up_min = 0.45
range_up_max = 0.55
range_down_min = 0.45
range_down_max = 0.55

# Trade_2 strategy parameters
[trade_2]
sell_hold_sec = 180
sell_profit_target = 0.20
sell_stop_loss = -0.08
emergency_swap_ratio = 0.85
range_up_min = 0.40
range_up_max = 0.60
range_down_min = 0.40
range_down_max = 0.60
```

## Running the Bot

### Development Mode

```bash
npm run dev
```

### Production Mode

```bash
npm run build
npm start
```

### Key Startup Sequence

1. Banner displays configuration
2. Environment validation (private key, funder address)
3. CLOB L1 authentication → API key derivation/creation
4. CLOB L2 client initialization
5. Market slug resolution (e.g., `btc-5m-up-down`)
6. Continuous market polling begins

## Code Examples

### Basic Trade Execution Flow

```typescript
import { ClobClient } from '@polymarket/clob-client';
import { loadConfig } from './config/toml';
import { Trade } from './trade/trade';

// Initialize CLOB client with wallet
const clobClient = new ClobClient(
  process.env.CLOB_HOST,
  process.env.CHAIN_ID,
  wallet,
  process.env.POLYMARKET_SIGNATURE_TYPE
);

// Load trading configuration
const config = loadConfig();

// Create trade instance
const trade = new Trade(clobClient, config);

// Main trading loop
async function runTradingLoop() {
  while (true) {
    // Fetch current market prices
    const upPrice = await fetchPrice(marketId, 'UP');
    const downPrice = await fetchPrice(marketId, 'DOWN');
    
    // Update prices and make decision
    trade.updatePrices(upPrice, downPrice, timeToExpiry);
    
    await sleep(config.poll_interval_ms);
  }
}
```

### Custom Strategy Implementation

```typescript
// src/trade/decision.ts
export async function make_trading_decision(
  trade: Trade,
  upPrice: number,
  downPrice: number,
  timeToExpiry: number
): Promise<void> {
  const { strategy } = trade.config;
  
  if (strategy === 'trade_1') {
    return trade_1_decision(trade, upPrice, downPrice, timeToExpiry);
  } else if (strategy === 'trade_2') {
    return trade_2_decision(trade, upPrice, downPrice, timeToExpiry);
  }
}

async function trade_1_decision(
  trade: Trade,
  upPrice: number,
  downPrice: number,
  timeToExpiry: number
): Promise<void> {
  const cfg = trade.config.trade_1;
  
  // Entry logic: check if in buy range
  if (!trade.hasBought) {
    const inUpRange = upPrice >= cfg.range_up_min && upPrice <= cfg.range_up_max;
    const inDownRange = downPrice >= cfg.range_down_min && downPrice <= cfg.range_down_max;
    
    if (inUpRange) {
      await trade.buyUp();
    } else if (inDownRange) {
      await trade.buyDown();
    }
    return;
  }
  
  // Exit logic: time, profit, or stop-loss
  const holdTime = (Date.now() - trade.buyTimestamp) / 1000;
  const profitPct = trade.calculateProfitPct();
  
  if (
    holdTime >= cfg.sell_hold_sec ||
    profitPct >= cfg.sell_profit_target ||
    profitPct <= cfg.sell_stop_loss ||
    timeToExpiry <= cfg.buy_last_sec
  ) {
    await trade.sell();
  }
}
```

### Market Order Execution

```typescript
// src/trade/trade.ts
async buyUp(): Promise<void> {
  if (this.hasBought || this.isInCooldown()) {
    return;
  }
  
  try {
    const order = await this.createAndPostMarketOrder(
      this.upTokenId,
      'BUY',
      this.config.trade_usd
    );
    
    this.hasBought = true;
    this.side = 'UP';
    this.buyTimestamp = Date.now();
    this.boughtPrice = this.upPrice;
    
    log.success(`✅ Bought UP @ ${this.upPrice.toFixed(4)}`);
  } catch (error) {
    this.lastFailedBuyTime = Date.now();
    log.error(`Buy failed: ${getFriendlyTradingError(error)}`);
  }
}

async createAndPostMarketOrder(
  tokenId: string,
  side: 'BUY' | 'SELL',
  amountUSD: number
): Promise<any> {
  const order = {
    tokenID: tokenId,
    price: side === 'BUY' ? 0.99 : 0.01, // Market order limits
    size: amountUSD.toString(),
    side,
    feeRateBps: '0',
    nonce: Date.now(),
    expiration: Math.floor(Date.now() / 1000) + 300,
  };
  
  return await retryWithPolicy(
    () => this.clobClient.postOrder(order),
    this.config.max_retries
  );
}
```

### OpenClaw Decision Integration

```typescript
// src/trade/openclaw/deterministic.ts
export function makeDeterministicDecision(
  upPrice: number,
  downPrice: number,
  timeToExpiry: number,
  lookbackWindow: Array<{ up: number; down: number; timestamp: number }>,
  config: OpenClawConfig,
  positionState: { hasBought: boolean; side?: 'UP' | 'DOWN' }
): OpenClawDecision {
  // Calculate spread
  const spread = Math.abs(upPrice - downPrice);
  const spreadBps = spread * 10000;
  
  if (spreadBps > config.max_spread_bps) {
    return { action: 'HOLD', reason: `Spread too wide: ${spreadBps.toFixed(0)}bps` };
  }
  
  // Calculate edge
  const upEdge = (0.5 - upPrice) * 10000;
  const downEdge = (0.5 - downPrice) * 10000;
  
  // Entry signals
  if (!positionState.hasBought) {
    if (upEdge > config.min_edge_bps) {
      return { action: 'BUY_UP', reason: `UP edge ${upEdge.toFixed(0)}bps` };
    }
    if (downEdge > config.min_edge_bps) {
      return { action: 'BUY_DOWN', reason: `DOWN edge ${downEdge.toFixed(0)}bps` };
    }
    return { action: 'HOLD', reason: 'No edge found' };
  }
  
  // Exit signals
  if (timeToExpiry < 60) {
    return { action: 'CLOSE_POSITION', reason: 'Near expiry' };
  }
  
  return { action: 'HOLD', reason: 'Monitoring position' };
}
```

### Market Slug Generation

```typescript
// src/config/slug.ts
export function buildSlug(coin: string, period: string): string {
  const coinMap: Record<string, string> = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'sol': 'solana',
    'xrp': 'ripple',
  };
  
  const periodMap: Record<string, string> = {
    '5': '5-minute',
    '15': '15-minute',
    '60': '1-hour',
    '240': '4-hour',
    '1440': '1-day',
  };
  
  const coinName = coinMap[coin.toLowerCase()] || coin;
  const periodName = periodMap[period] || `${period}-minute`;
  
  return `${coinName}-${periodName}-up-down`;
}

// Usage
const slug = buildSlug('btc', '5'); // "bitcoin-5-minute-up-down"
```

### Error Handling with Retry Logic

```typescript
// src/utils/retry.ts
export async function retryWithPolicy<T>(
  fn: () => Promise<T>,
  maxRetries: number,
  delayMs: number = 1000
): Promise<T> {
  let lastError: any;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;
      
      // Only retry transient errors
      if (isTransientError(error) && attempt < maxRetries) {
        await sleep(delayMs * Math.pow(2, attempt)); // Exponential backoff
        continue;
      }
      
      throw error;
    }
  }
  
  throw lastError;
}

function isTransientError(error: any): boolean {
  const transientCodes = [429, 500, 502, 503, 504];
  const transientMessages = ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND'];
  
  return (
    transientCodes.includes(error.status) ||
    transientMessages.some(msg => error.message?.includes(msg))
  );
}
```

## Common Patterns

### Running Multiple Time Windows

Run separate processes for 5m and 15m markets:

```bash
# Terminal 1 - 5 minute markets
cp trade.toml trade-5m.toml
# Edit trade-5m.toml: market_period = "5"
npm run build
CONFIG_PATH=./trade-5m.toml npm start

# Terminal 2 - 15 minute markets
cp trade.toml trade-15m.toml
# Edit trade-15m.toml: market_period = "15"
CONFIG_PATH=./trade-15m.toml npm start
```

### Monitoring Position State

```typescript
// Add to main loop for logging
function logPositionState(trade: Trade) {
  if (trade.hasBought) {
    const holdTime = (Date.now() - trade.buyTimestamp) / 1000;
    const profitPct = trade.calculateProfitPct();
    
    console.log(`📊 Position: ${trade.side} | Hold: ${holdTime.toFixed(0)}s | P&L: ${(profitPct * 100).toFixed(2)}%`);
  } else {
    console.log(`💤 No position | Watching market`);
  }
}
```

### Safe Shutdown Handler

```typescript
// src/index.ts
let isShuttingDown = false;

process.on('SIGINT', async () => {
  if (isShuttingDown) return;
  isShuttingDown = true;
  
  log.warn('🛑 Shutdown signal received');
  
  // Close any open positions
  if (trade.hasBought) {
    log.info('Closing open position...');
    await trade.sell();
  }
  
  log.info('Shutdown complete');
  process.exit(0);
});
```

## Troubleshooting

### Authentication Issues

**Error:** `Invalid private key` or `byteslike value`

```typescript
// Validate environment
import { validateEnv } from './config/validateEnv';

try {
  validateEnv();
} catch (error) {
  console.error('Environment validation failed:', error.message);
  process.exit(1);
}
```

Ensure:
- Private key is valid hex (with or without `0x` prefix)
- Funder address is valid Polygon address
- Wallet has been initialized with Polymarket

### Market Not Found

**Error:** `Market slug not found`

- Verify `market_coin` and `market_period` in `trade.toml`
- Check if market exists on Polymarket for current time
- 5m/15m markets may not be available 24/7

```bash
# Test slug generation
node -e "console.log(require('./dist/config/slug').buildSlug('btc', '5'))"
```

### Order Failures

**Error:** `Insufficient balance` or `Order rejected`

- Check USDC balance: must exceed `trade_usd`
- Verify funder address has deposited funds
- Reduce `trade_usd` for testing
- Check if in cooldown period after failed buy

```typescript
// Check balance before trading
const balance = await clobClient.getBalance();
console.log(`Available balance: ${balance.usdc} USDC`);

if (parseFloat(balance.usdc) < config.trade_usd) {
  throw new Error('Insufficient balance for trade');
}
```

### Retry Exhaustion

**Error:** `Max retries exceeded`

- Increase `max_retries` in `trade.toml` for flaky networks
- Check API rate limits (429 errors)
- Verify CLOB host is reachable
- Review `entry_buy_cooldown_sec` to avoid tight loops

### Price Polling Issues

**Error:** `Failed to fetch prices`

```typescript
// Add timeout to price fetching
const fetchWithTimeout = async (marketId: string, timeout: number = 5000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(`https://gamma-api.polymarket.com/markets/${marketId}`, {
      signal: controller.signal
    });
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
};
```

## Best Practices

1. **Start Small:** Begin with `trade_usd = 1.0` or less
2. **Test Paper Mode:** Verify logic before live funds (add `dry_run` flag to config)
3. **Monitor Logs:** Watch for cooldown triggers, failed orders, and position state
4. **Risk Management:** Set conservative `sell_stop_loss` values
5. **Network Reliability:** Run on stable connection; consider VPS for uptime
6. **OpenClaw Experimentation:** Leave `openclaw.enabled = false` until comfortable with base strategies
7. **Multiple Markets:** Run separate processes rather than single multi-market binary
8. **Backup Keys:** Store private keys securely; never commit to git

## Architecture Reference

**Key Modules:**

- `src/index.ts` - Entry point, CLOB auth, main loop
- `src/services/clob.ts` - CLOB client configuration
- `src/services/gamma.ts` - Polymarket Gamma API integration
- `src/config/toml.ts` - Configuration loading and validation
- `src/trade/decision.ts` - Strategy branching (trade_1/trade_2)
- `src/trade/trade.ts` - Order execution and position management
- `src/trade/openclaw/` - OpenClaw AI decision layer
- `src/utils/retry.ts` - Retry policy for transient errors
- `src/utils/tradingErrorMessage.ts` - Human-friendly error messages

This bot is designed for **experimental and educational use** with prediction markets. Always understand the risks of automated trading and start with minimal capital.
