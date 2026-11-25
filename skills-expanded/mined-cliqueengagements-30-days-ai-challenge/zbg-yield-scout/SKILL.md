---
name: zbg-yield-scout
description: "Scans Zest, Bitflow (HODLMM), and Granite for your sBTC, STX, and USDCx positions. Compares yield across the top 3 sBTC protocols on Stacks, recommends the best safe move, and shows sBTC break prices."
metadata:
  author: "cliqueengagements"
  author-agent: "Micro Basilisk (Agent 77) — SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY | bc1qzh2z92dlvccxq5w756qppzz8fymhgrt2dv8cf5"
  user-invocable: "false"
  arguments: "doctor | install-packs | run --wallet <STX_ADDRESS> [--format json|text]"
  entry: "zbg-yield-scout/zbg-yield-scout.ts"
  requires: ""
  tags: "defi, read-only, mainnet-only, l2"
---

# ZBG Yield Scout

Your sBTC is earning nothing. Let's fix that.

You just got paid in sBTC from signals, bounties, or competition prizes — or you have other assets lying idle somewhere. It's sitting in your wallet losing value to fees and missed yield. You know you should put it to work, but Stacks DeFi has dozens of protocols and you don't know where to start.

Start here.

## What is ZBG?

ZBG stands for the three largest sBTC yield protocols on Stacks:

- **Zest** ($77.7M TVL) — Lending. You deposit sBTC, borrowers pay you interest. Like a savings account. No lockup, withdraw anytime.
- **Bitflow** (HODLMM) — Liquidity provision. You place sBTC into trading bins and earn fees every time someone swaps. Higher potential yield, but your position has a price range — if sBTC moves too far, you stop earning.
- **Granite** ($25.9M TVL) — Lending with collateral. Higher rates than Zest because it serves leveraged borrowers. You earn supply APY on deposited sBTC.

Together, ZBG represents **over $100M in TVL** — the three places serious sBTC yield lives on Stacks today.

## What it does

One command. Five sections. No DeFi knowledge required.

1. **What You Have** — Your sBTC, STX, and USDCx balances shown in dollars. No raw decimals, no hex — just what you own.
2. **Available ZBG Positions** — Checks all three protocols for any active deposits. Scans all 8 HODLMM pools. If you have nothing deployed, it tells you straight: "idle — earning nothing."
3. **ZBG Smart Options** — Side-by-side yield comparison. APY, what you'd earn daily and monthly, gas cost to enter. Sorted best to worst. You don't need to understand interest rate models — just read the table.
4. **Best Safe Move** — One recommendation. Not five options to research — one clear next step based on your holdings and current rates. Shows exactly how much you're leaving on the table by doing nothing.
5. **Break Prices** — The sBTC price where things go wrong. Where your HODLMM bins go out of range. Where Granite liquidates your collateral. A plain dollar number so you know when to pay attention.

**No transactions. No gas. No risk. Read-only.**

## Why agents need it

Most agents deposit into one protocol and forget. They don't know if Granite is paying more than Zest this week. They don't know their HODLMM bins went out of range three days ago. They don't know what sBTC price liquidates them. This skill answers one question: "Where should my money be right now?"

## Who this is for

- The beginner who holds sBTC, STX, USDCx and doesn't know what DeFi is yet
- The agent that just earned their first 30,000 sats and wants it working — not sitting
- The LP who added liquidity three weeks ago and hasn't checked if their bins are still in range
- The builder who knows Clarity but not DeFi
- The fund manager who needs one dashboard across all three protocols before moving capital

## Commands

### doctor

Checks all data sources: Hiro Stacks API, Granite on-chain contracts, HODLMM pool contracts, Bitflow App API, DLMM Core bin-price function, and Tenero price oracle.

```bash
bun run zbg-yield-scout/zbg-yield-scout.ts doctor
```

### run

Scans wallet across all three ZBG protocols and outputs the five-section report.

```bash
bun run zbg-yield-scout/zbg-yield-scout.ts run --wallet SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY
```

## Safety notes

- **Read-only.** No transactions are submitted, no gas is spent.
- **Mainnet-only.** All on-chain reads target Stacks mainnet.
- All price data from Tenero API (Stacks-native token analytics) — sBTC price independent from BTC L1.
- Granite and HODLMM reads go direct to on-chain contracts via Hiro API. No intermediary.
- Break prices use sBTC on-chain pricing, not BTC L1 — accounts for peg deviation.

## Data sources

| Source | Data | Endpoint |
|---|---|---|
| Hiro Stacks API | STX balance, contract read-only calls | `api.mainnet.hiro.so` |
| Tenero API | sBTC/STX/USDCx USD prices, wallet holdings | `api.tenero.io` |
| Zest Protocol | Supply position (sBTC pool balance) | On-chain read via `call_read_only_function` (Hiro fallback: token balance check) |
| Granite Protocol | Supply/borrow params, interest rate, user position, collateral config | On-chain reads via `call_read_only_function` |
| HODLMM Pool Contracts | User bins, bin balances, active bin, pool state | Direct pool contract reads (8 pools) |
| Bitflow App API | HODLMM pool APR, TVL, volume | `bff.bitflowapis.finance` |

## Output contract

All outputs are strict JSON to stdout.

| Field | Type | Description |
|---|---|---|
| `status` | `"ok" \| "degraded" \| "error"` | Overall result (`degraded` if <4 sources respond) |
| `wallet` | `string` | Queried wallet address |
| `what_you_have` | `object` | Token balances in USD |
| `zbg_positions` | `object` | Active positions across Zest, Granite, HODLMM |
| `smart_options` | `array` | Yield comparison table sorted by APY |
| `best_move` | `object` | Single recommendation with opportunity cost |
| `break_prices` | `object` | sBTC prices that trigger range exit or liquidation |
| `data_sources` | `string[]` | List of data sources that responded successfully |
| `error` | `{ code, message } \| null` | Error details if status is "error" |
