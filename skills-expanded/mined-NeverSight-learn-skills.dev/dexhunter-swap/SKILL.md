---
name: dexhunter-swap
description: |
  Use this skill when the user wants the best swap rate across all Cardano DEXes,
  or wants to use DexHunter aggregator. Triggers on: "best price for",
  "swap aggregator", "dexhunter swap", "route across DEXes", "best rate",
  "compare DEX prices", "smart order routing". Aggregates Minswap, WingRiders,
  SundaeSwap, SaturnSwap, and more. Use dexhunter-swap-operator to execute.
version: 1.0.0
---

# DexHunter Swap Aggregator

Find the best swap rate across all Cardano DEXes via DexHunter's smart routing.

## Capabilities

- Estimate swaps with multi-DEX routing and price impact
- Build optimized swap transactions
- Search and discover Cardano tokens
- Get price data across DEXes

## Flow

1. **Search token** — find the token ID by ticker or name
2. **Estimate swap** — see routing, price impact, and expected output across DEXes
3. **Confirm with user** — show route breakdown and fees
4. **Build transaction** — get unsigned CBOR hex
5. **Hand off to operator** — for signing and submission

## Scripts

### Search Tokens

```bash
node scripts/search-tokens.js --query MNT
```

### Estimate Swap

```bash
node scripts/estimate-swap.js --token-in "" --token-out <policyId+assetHex> --amount <lovelace>
```

Note: DexHunter uses **base units** (lovelace for ADA), unlike SaturnSwap.

### Build Swap

```bash
node scripts/build-swap.js --address <bech32> --token-in "" --token-out <id> --amount <lovelace> [--slippage 1]
```

## Key Concepts

- Token IDs: `""` for ADA, `policyId + assetNameHex` for tokens
- Amounts are in **smallest units** (lovelace for ADA, base units for tokens)
- Routing shows which DEXes are used and what percentage goes to each
- `price_impact` indicates market impact — warn if >2%
- Requires `DEXHUNTER_API_KEY` environment variable

## Safety Rules

- Always show the estimate before building
- Warn on price impact >2%
- Show which DEXes are being routed through
- Compare with SaturnSwap direct if the pair exists there
