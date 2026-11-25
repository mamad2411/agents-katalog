---
name: indigo-cdp
description: |
  Use this skill when the user wants to manage Collateralized Debt Positions on
  Indigo Protocol. Triggers on: "open a CDP", "mint iUSD", "mint iBTC",
  "synthetic assets", "Indigo Protocol", "collateral ratio", "CDP health",
  "burn iAssets", "deposit collateral", "withdraw collateral", "close CDP".
  Use indigo-cdp-operator to execute transactions.
version: 1.0.0
---

# Indigo Protocol CDP Management

Manage Collateralized Debt Positions to mint synthetic assets (iUSD, iBTC, iETH, iSOL).

## Capabilities

- Open CDPs with ADA collateral to mint iAssets
- Deposit/withdraw collateral to adjust collateral ratio
- Mint more iAssets or burn to reduce debt
- Close CDPs (return all collateral, burn all debt)
- Analyze CDP health and liquidation risk

## Synthetic Assets (iAssets)

| Asset | Decimals | Description |
|---|---|---|
| iUSD | 6 | Synthetic US Dollar |
| iBTC | 8 | Synthetic Bitcoin |
| iETH | 18 | Synthetic Ethereum |
| iSOL | 9 | Synthetic Solana |

## Scripts

### View CDPs
```bash
node scripts/my-cdps.js --owner <bech32>
node scripts/cdp-health.js --tx-hash <hash> --output-index <idx>
```

### Open CDP
```bash
node scripts/open-cdp.js --address <bech32> --asset iUSD --collateral 5000000000
```
Collateral in lovelace (5000000000 = 5000 ADA).

### Manage CDP
```bash
node scripts/manage-cdp.js --address <bech32> --action deposit|withdraw|mint|burn|close --tx-hash <hash> --output-index <idx> [--amount <lovelace>]
```

### Asset Prices
```bash
node scripts/prices.js
```

## Key Concepts

- **Collateral Ratio** = (Collateral ADA x ADA Price) / (Minted iAssets x iAsset Price) x 100%
- Minimum ratio typically 150% — below this, CDP is liquidatable
- **Healthy**: >150% of min ratio | **Warning**: 100-150% | **Danger**: <100%
- All amounts in smallest units (lovelace for ADA, base units for iAssets)

## Safety Rules

- Always show collateral ratio before and after any operation
- Warn if ratio would drop below 200% (buffer above 150% min)
- Show liquidation price when opening or adjusting
- Require confirmation before mint, withdraw, or close operations
