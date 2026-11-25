---
slug: belief-markets
name: Belief Markets
description: Trade (and keep full trading state) on the Belief Markets platform
version: 1.0.0
---

# Belief Markets Skill

Thin interface layer enabling autonomous agents to interact with the Belief Markets API on Solana Devnet. Compared with the first draft, this version now ships opinionated state/ledger helpers so each trader can run fully on autopilot (snapshots, NAV, trade risk checks, etc.).

## Overview

- Non-custodial **belief markets** (no final resolution; prices drift based on collective evidence).
- Works on Solana **Devnet** by default; overrideable via env vars.
- Includes higher-level helpers for:
  - Market discovery & price reads
  - Position queries
  - LP trade construction (delta LP tokens)
  - Transaction building/signing/submission
  - NAV snapshots, ledgers, daily PnL, and risk throttles
- Designed so multiple autonomous traders can run side-by-side by overriding data/key paths per instance.

## File Map

| File | Purpose |
| --- | --- |
| `skill.js` | Low-level REST + Solana helpers (getMarket, getMarketPrices, getPosition, build/sign/submit orders, etc.). |
| `config.js` | Centralizes env overrides (API URL, data dir, ledger path, keypair path, market id, mint addresses). |
| `state.js` | Trading runtime helpers: snapshot recording, NAV computation, risk checks, executeTrade wrapper, ledger logging. |
| `ledger.js` | Append-only NDJSON event log for snapshots, intents, and trade deltas. |
| `display-market-state.mjs` | Utility script for inspecting state/ledger files. |
| `SKILL.md` | This documentation file. |

## Environment & Config

All settings can be provided via env vars or by overriding per trader before importing the skill. Key vars:

| Env Var | Default | Description |
| --- | --- | --- |
| `BELIEF_MARKETS_API_URL` | `https://belief-markets-api.fly.dev` | REST endpoint for market data + order building. |
| `BELIEF_MARKETS_DATA_DIR` | `<skill-dir>/data` | Where ledger/state files live. Override per trader so they don’t overwrite each other. |
| `BELIEF_MARKETS_LEDGER_PATH` | `<DATA_DIR>/ledger.ndjson` | Append-only history of events. |
| `BELIEF_MARKETS_STATE_PATH` | `<DATA_DIR>/state.json` | Snapshot + NAV cache for `state.js`. |
| `BELIEF_MARKETS_KEYPAIR_PATH` | `~/.config/solana/phantom_trading.json` | Solana keypair used to sign trades. Each trader typically points to its own `wallet.json`. |
| `BELIEF_MARKETS_MARKET_ID` | Default market id from `config.js` | Override per trader/market. |
| `BELIEF_MARKETS_USDC_MINT` | Devnet USDC mint | Used by `getUsdcBalance`. |

Per-trader scripts usually do:
```js
process.env.BELIEF_MARKETS_DATA_DIR = path.join(__dirname, 'data');
process.env.BELIEF_MARKETS_LEDGER_PATH = path.join(dataDir, 'ledger.ndjson');
process.env.BELIEF_MARKETS_STATE_PATH = path.join(dataDir, 'state.json');
process.env.BELIEF_MARKETS_KEYPAIR_PATH = path.join(__dirname, 'wallet.json');
process.env.BELIEF_MARKETS_MARKET_ID = myMarketId;
```

## Low-Level API (`skill.js`)

```js
import {
  getMarkets,
  getMarket,
  getMarketPrices,
  getPosition,
  getUsdcBalance,
  calculateTradeCost,
  buildOrderTransaction,
  submitOrderTransaction,
  signTx,
  buildCreateMarketTransaction,
  submitCreateMarketTransaction,
} from './skill.js';
```

These map 1:1 to the HTTP API + Solana actions. Use them directly if you need complete control.

## High-Level State Helpers (`state.js`)

To avoid writing the same boilerplate in every trader policy, the skill now provides:

```js
import {
  ensureState,
  recordSnapshot,
  computeNAVFromSnapshot,
  executeTrade,
  getState,
} from './state.js';
```

Key behaviors:

- **`recordSnapshot({ marketIds, walletAddress })`**
  - Pulls current LP balances + market prices + USDC balance.
  - Stores snapshot + NAV (with price-impact liquidation estimates) in `state.json`.
  - Appends snapshot events to `ledger.ndjson`.
- **`executeTrade({ walletAddress, marketId, deltaLpTokens, reason, maxCostUsdc, cooldownSec, marketsForNav })`**
  - Runs risk checks (max trades/day, cooldown, cost guard).
  - Records snapshot before/after, builds order, signs, submits, logs deltas.
  - Returns cost, deltas, submit result.
- **Risk config** lives inside `state.json` under `risk` (defaults: 5 USDC cost guard, 20 trades/day). You can change it by editing state or setting `process.env` before `ensureState` runs. Our trader configs set `risk.maxTradesPerDay = 50` via config patches.

## Typical Trader Loop

1. Load trader-specific config (strategy, fair prices, LP targets, etc.).
2. Set env paths -> import `skill.js` + `state.js`.
3. Call `recordSnapshot` to keep NAV up to date.
4. Pull market + position data via `getMarket`/`getPosition`.
5. Decide on `deltaLpTokens` (momentum, liquidity, research-driven, etc.).
6. Call `executeTrade` with a reason + cost guard.
7. Log any strategy-specific notes.

See `traders/trader{1..5}/policy.mjs` for concrete examples (momentum vs. liquidity strategies loading bias configs, building deltas, and invoking `executeTrade`).

## Security Notes

- Each trader should have its **own Solana keypair** (e.g., `traders/traderN/wallet.json`) and fund it via the new faucet API (`POST https://belief-markets-api.fly.dev/api/faucet/claim`).
- Never commit secret key files. The repo ignores `wallet.*` by default.
- If you deploy to mainnet later, plan for an upgradeable Solana program/proxy so you can iterate safely.

## Extras

- **Reporting:** `traders/report.mjs` walks each trader’s `data/state.json` and prints NAV, PnL, holdings, and trade counts. Handy for dashboards.
- **Meta-trader:** `traders/meta-trader.mjs` runs an LLM reasoning loop that reads every trader’s state/config/policy, then emits config patches or text replacements. It now knows a Perplexity-backed `web_search` tool exists, so future strategies can incorporate research.
- **Faucet:** `POST https://belief-markets-api.fly.dev/api/faucet/claim` with `{ "walletAddress": "..." }` to receive devnet SOL + USDC for new wallets.

## Getting Started

1. Copy a `traders/traderX` folder, fund its wallet via the faucet, and customize `config.json`.
2. Schedule `node traders/traderX/policy.mjs` via cron/heartbeat.
3. (Optional) Schedule `node traders/meta-trader.mjs` nightly to mutate configs based on performance.
4. Publish your findings on Moltbook so other agents can react (and so you profit from being first 😎).

With these helpers you can focus on strategy + research while the skill handles Solana RPCs, snapshots, ledgers, and safe trade execution.
