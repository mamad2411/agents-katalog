---
name: binance-trading
description: >-
  Trades on Binance via the binance npm package. Supports spot, USD-M futures,
  COIN-M futures, and portfolio margin. Use when the user asks to buy, sell,
  place orders, check balance, manage positions, transfer funds, or trade on
  Binance. For market data only (prices, orderbook) load modules/market.md.
  Requires Node.js and npm install binance.
license: MIT
metadata:
  version: "1.0.0"
  author: "binance-agent-skills"
  homepage: "https://github.com/JJ-Cro/binance-agent-skills"
---

# Binance Trading Skill

Trade on Binance using the `binance` npm package. Supports spot, USD-M futures, COIN-M futures, and portfolio margin.

**Version:** 1.0.0 | **Architecture:** Modular (on-demand loading)

## Prerequisites

```bash
npm install binance
```

## Language Default

- Use **TypeScript by default** for all code examples and generated scripts.
- Use JavaScript only if the user explicitly asks for JavaScript.

---

## WebSocket-First Rule (Gap Prevention)

When a workflow needs both a snapshot fetch (REST) and streaming updates (WebSocket), always connect WebSocket first to reduce missing in-between data.

Required order:

1. Create and connect `WebsocketClient`, register handlers, subscribe to stream(s)
2. Confirm stream is live (open/subscribed/first event)
3. Fetch REST snapshot/backfill
4. Reconcile by event time/update IDs and then process live updates

Never do "REST first, WebSocket later" for live-tracking flows where gaps matter.

## Auto Update (optional, at session start)

At session start, check for updates:

1. `LOCAL_VERSION = "1.0.0"` (from metadata above)
2. `curl -sf https://raw.githubusercontent.com/JJ-Cro/binance-agent-skills/main/VERSION`
3. If remote > LOCAL: download MANIFEST, fetch listed files, notify user
4. If fetch fails: continue silently

---

## Credential Setup

### Environment Variables

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_secret_key"
```

**Security rules:**
- Never show full API key or secret in output. Show key as `first5...last4`, secret as `***...last5`
- In code examples, use `process.env.BINANCE_API_KEY` / `process.env.BINANCE_API_SECRET` or placeholders
- Recommend Read + Trade permissions only; never Withdraw for AI use
- Use a sub-account with limited balance when possible

### Testnet vs Mainnet

| Mode | Option | Funds |
|------|--------|-------|
| **Mainnet** (default) | `testnet: false` or omit | Real funds |
| **Testnet** | `testnet: true` | Simulated |

Pass `testnet: true` when user says "testnet", "demo", "test", "practice". Default to mainnet.

**Display:** Append `[MAINNET]` or `[TESTNET]` to responses involving API calls.

---

## Module Router

Load modules on-demand. When user request matches a category, fetch the module once per session.

| User Intent | Module | File |
|-------------|--------|------|
| price, ticker, kline, orderbook, depth, funding, market data | **market** | `modules/market.md` |
| buy, sell, spot, limit order, market order, cancel spot | **spot** | `modules/spot.md` |
| long, short, futures, perp, leverage, position, TP/SL | **futures** | `modules/futures.md` |
| balance, wallet, transfer, deposit, fee | **account** | `modules/account.md` |

**Load rule:** Fetch from
`https://raw.githubusercontent.com/JJ-Cro/binance-agent-skills/main/modules/<module>.md`

---

## Client Selection

| Product | Client | Import |
|---------|--------|--------|
| Spot, Margin | `MainClient` | `import { MainClient } from 'binance'` |
| USD-M Futures | `USDMClient` | `import { USDMClient } from 'binance'` |
| COIN-M Futures | `CoinMClient` | `import { CoinMClient } from 'binance'` |
| Portfolio Margin | `PortfolioClient` | `import { PortfolioClient } from 'binance'` |

---

## API Reference

For exact method signatures and parameters, read `node_modules/binance/llms.txt` when needed. The SDK ships this file for AI consumption.

If a user asks for behavior not explicitly covered by this skill/modules, consult `node_modules/binance/llms.txt` before answering or executing.

For edge cases (precision, errors, contract size conversion), see [references/edge-cases.md](references/edge-cases.md).

---

## Write Operation Confirmation

For mainnet write operations (place order, cancel, transfer), confirm parameters with the user before executing. For testnet, execution can proceed without extra confirmation.

---

## Workflow Checklist

Before placing orders:

```
- [ ] Credentials set (BINANCE_API_KEY, BINANCE_API_SECRET)
- [ ] Correct client selected (MainClient spot, USDMClient futures, etc.)
- [ ] Testnet vs mainnet confirmed
- [ ] quantity in correct unit (base for spot, contracts for futures)
- [ ] Mainnet: user confirmed params before execute
```

---

## Quick Examples

```typescript
// Spot market buy
import { MainClient } from 'binance';
const client = new MainClient({ api_key: key, api_secret: secret });
await client.submitNewOrder({ symbol: 'BTCUSDT', side: 'BUY', type: 'MARKET', quantity: 0.01 });

// USD-M futures short
import { USDMClient } from 'binance';
const client = new USDMClient({ api_key: key, api_secret: secret });
await client.submitNewOrder({ symbol: 'BTCUSDT', side: 'SELL', type: 'MARKET', quantity: 0.001 });
```

For full workflows, load the relevant module.
