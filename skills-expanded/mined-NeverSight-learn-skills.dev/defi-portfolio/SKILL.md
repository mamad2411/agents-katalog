---
name: defi-portfolio
description: |
  Use this skill for a unified view of a wallet's DeFi positions across all
  Cardano protocols. Triggers on: "show all my positions", "DeFi portfolio",
  "what do I have open", "total exposure", "all my DeFi",
  "positions across protocols", "unified portfolio view".
version: 1.0.0
---

# Unified DeFi Portfolio

View all DeFi positions across Cardano protocols in one place.

## Capabilities

Aggregates positions from:
- **SaturnSwap**: Open orders + liquidity positions
- **Strike Finance**: Leveraged perp positions
- **Bodega Markets**: Prediction market shares
- **Surf Finance**: Lending/borrowing positions (via pool state)

## Scripts

### Full Portfolio

```bash
node scripts/portfolio.js --address <bech32>
```

Queries all protocols in parallel and shows a unified summary.

## Key Concepts

- Each protocol is queried independently — some may fail without affecting others
- Positions are grouped by protocol and type
- Values are shown in ADA where possible
- Environment variables for each protocol must be set for their section to appear
