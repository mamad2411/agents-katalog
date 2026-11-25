---
name: saturnswap-analytics
description: |
  Use this skill when the user asks about SaturnSwap DEX statistics, total
  volume, TVL, number of pools/tokens, or top pools by volume. Triggers on:
  "SaturnSwap stats", "total TVL", "total volume", "how many pools",
  "top pools by volume", "DEX analytics", "SaturnSwap overview".
version: 1.0.0
---

# SaturnSwap Analytics

Retrieve platform-wide and per-pool statistics for SaturnSwap DEX.

## Capabilities

- Total platform stats: TVL, volume (24h/7d/30d), pool count, token count, transactions
- Per-pool stats ranked by volume or TVL
- API health and parameter checks

## Scripts

### Platform Overview

```bash
node scripts/platform-stats.js
```

Returns total TVL, volumes, pool/token counts, and 24h transaction count.

### Top Pools

```bash
node scripts/top-pools.js [--first N] [--order volume_24h|volume_7d|tvl]
```

### API Status

```bash
node scripts/api-status.js
```

Checks if the API is online and returns version + minimum ADA amount parameter.

## Formatting Guidelines

- Format ADA values with the ₳ symbol (e.g. ₳1,234,567)
- Use percentage changes where available
- Present top pools as a ranked table
