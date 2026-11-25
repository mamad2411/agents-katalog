---
name: cardexscan-swap
description: |
  Use this skill when the user wants to swap via CardexScan/Hydra aggregator,
  get trending tokens, or compare swap rates. Triggers on: "CardexScan swap",
  "Hydra aggregator", "trending tokens", "best swap rate", "compare aggregators",
  "token trades". Alternative to DexHunter with different routing.
version: 1.0.0
---

# CardexScan Swap Aggregator

DEX aggregator with multi-DEX routing, trending tokens, and trade history.

## Scripts

### Estimate Swap
```bash
node scripts/estimate.js --token-in lovelace --token-out-policy <id> --token-out-asset <hex> --amount 10000000
```

### Build Swap Transaction
```bash
node scripts/build.js --address <bech32> --token-in lovelace --token-out-policy <id> --token-out-asset <hex> --amount 10000000
```

### Trending Tokens
```bash
node scripts/trending.js [--timeframe 24h] [--count 20]
```

## Key Concepts

- Token format: `"lovelace"` for ADA, `{policyId, assetName}` for tokens
- Amounts in base units (lovelace for ADA)
- Requires `CARDEXSCAN_API_KEY` env var
- Returns splits across multiple DEXes for best execution
