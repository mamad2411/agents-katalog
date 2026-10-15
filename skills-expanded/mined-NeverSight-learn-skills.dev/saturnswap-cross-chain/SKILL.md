---
name: saturnswap-cross-chain
description: |
  Use this skill when the user wants to swap tokens across different blockchains
  via SaturnSwap's Cosmic Router (UEX). Triggers on: "swap ADA for ETH",
  "cross-chain swap", "bridge ADA to Ethereum", "convert ADA to BTC",
  "send SOL from Cardano", "swap to Solana", "bridge tokens",
  "what chains does SaturnSwap support", "cross-chain quote".
  Supports 119 chains: Cardano, Ethereum, Bitcoin, Solana, BSC, Polygon,
  Arbitrum, Base, Optimism, and 110+ more.
version: 1.0.0
---

# SaturnSwap Cross-Chain Swap (Cosmic Router)

Swap tokens across 119 blockchains via SaturnSwap's UEX aggregator.

## How It Works

Cross-chain swaps use a **deposit-based flow** — different from on-chain DEX swaps:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1. QUOTE     │────▶│ 2. ORDER     │────▶│ 3. DEPOSIT   │────▶│ 4. RECEIVE   │
│ Get rate     │     │ Get deposit  │     │ Send funds   │     │ Tokens arrive│
│ & fees       │     │ address      │     │ to address   │     │ on dest chain│
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Quote** — Check rate, fees, and min/max amounts
2. **Create Order** — Get a unique deposit address and exact amount
3. **Deposit** — Send the exact amount to the deposit address (on source chain)
4. **Receive** — Tokens arrive at destination address on the target chain

## API Endpoints

All endpoints are at `https://saturnswap.io/api/uex/`:

| Endpoint | Method | Description |
|---|---|---|
| `/metadata` | GET | List all supported chains and tokens |
| `/quote` | POST | Get swap quote with rate and fees |
| `/order` | POST | Create swap order, get deposit address |

## Scripts

### List Supported Chains

```bash
node scripts/list-chains.js [--type cardano|evm|solana|other]
```

### Find Token

```bash
node scripts/find-token.js --symbol ETH [--chain ethereum-mainnet]
```

### Get Quote

```bash
node scripts/get-quote.js --from ADA --to ETH --amount 500
node scripts/get-quote.js --from-chain cardano-mainnet --from-token ADA@ADA --to-chain ethereum-mainnet --to-token ETH@ETH --amount 500
```

### Create Order

```bash
node scripts/create-order.js --from ADA --to ETH --amount 500 --destination 0xYourEthAddress
```

## Key Concepts

- **Token IDs** use the format `SYMBOL@CHAIN_SYMBOL` (e.g. `ADA@ADA`, `ETH@ETH`, `SOL@SOL`)
- **Chain IDs** are slugified (e.g. `cardano-mainnet`, `ethereum-mainnet`, `solana-mainnet`)
- Cardano tokens use `cardano:<policyId><assetName>` format for non-ADA tokens
- **Deposit address** is unique per order — send the EXACT `depositAmount`
- Orders that require Cardano signing return `requiresSignature: true` + `unsignedTxCbor`
- Cross-chain swaps typically take 5-30 minutes depending on chain confirmation times
- **Min/max amounts** are enforced — quote returns `minAmountIn` and `maxAmountIn`

## Chain Types

| Type | Examples | Wallet |
|---|---|---|
| `cardano` | Cardano mainnet | CIP-30 (Nami, Eternl) |
| `evm` | Ethereum, Polygon, Arbitrum, Base, Optimism | MetaMask |
| `solana` | Solana mainnet | Phantom |
| `other` | Bitcoin, BSC, DOGE, TRX, etc. | Deposit-only (send to address) |

## Order Status Flow

```
waiting_for_deposit → confirming → swapping → sending → completed
                                                      ↘ expired / refunded / failed
```

## Safety Rules

- **Always show the quote** before creating an order (rate, fees, min/max)
- **Verify destination address** matches the correct chain — wrong chain = lost funds
- **Check min/max amounts** — amounts outside range will fail
- **Warn about fees** — cross-chain fees are shown in `feeAmount`
- **Confirm before order creation** — orders create real deposit addresses
- Display units everywhere — amounts are human-readable, not base units
