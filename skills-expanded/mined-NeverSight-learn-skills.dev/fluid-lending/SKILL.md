---
name: fluid-lending
description: |
  Use this skill when the user wants to borrow or create lending pools on FluidTokens.
  Triggers on: "FluidTokens", "borrow against NFT", "create lending pool",
  "borrow ADA", "borrow USDM", "collateral lending", "peer-to-pool lending".
  Supports ADA, FLDT, Snek, USDM, USDA, STRIKE, WMTX, HOSKY, wUSDC, wBTC, cAP3X.
version: 1.0.0
---

# FluidTokens Lending

Borrow tokens against collateral or create lending pools on FluidTokens.

## Capabilities

- Borrow any supported token against collateral (server auto-selects best pools)
- Create custom lending pools with configurable terms
- Support for perpetual and fixed-term loans

## Supported Tokens

ADA, FLDT, Snek, USDM, USDA, wUSDC, wBTC, STRIKE, WMTX, cAP3X, HOSKY

## Scripts

### Borrow
```bash
node scripts/borrow.js --address <bech32> --borrow-token ADA --borrow-amount 1000000000 --collateral-policy <policyId> --collateral-asset <assetHex> --collateral-amount 5000
```

### Create Pool
```bash
node scripts/create-pool.js --address <bech32> --lend-token ADA --amount 500000000 --rate 4.65 --markets FLDT --period 168 --perpetual
```

## Key Concepts

- Server auto-selects optimal pools for borrow requests
- Returns array of unsigned CBOR txs — sign in sequence (rootUtxoTx first, then borrowTx)
- Amounts in smallest units (lovelace for ADA)
- `borrowToken` param auto-maps to correct policy ID per network
