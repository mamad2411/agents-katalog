---
name: indigo-stability
description: |
  Use this skill when the user wants to manage Indigo stability pool positions.
  Triggers on: "stability pool", "deposit iUSD", "Indigo pool", "liquidation rewards",
  "stability account", "earn from liquidations". Use indigo-cdp-operator to sign.
version: 1.0.0
---

# Indigo Stability Pools

Deposit iAssets into stability pools to earn ADA from liquidations + INDY rewards.

## Scripts

### View Pools
```bash
node scripts/pools.js
node scripts/my-accounts.js --owner <bech32>
```

### Manage Account
```bash
node scripts/manage-sp.js --address <bech32> --action create --asset iUSD --amount 1000000000
node scripts/manage-sp.js --address <bech32> --action adjust --asset iUSD --amount 500000000 --tx-hash <hash> --output-index <idx>
node scripts/manage-sp.js --address <bech32> --action close --tx-hash <hash> --output-index <idx>
```

## Key Concepts

- Deposit iAssets → earn ADA when undercollateralized CDPs are liquidated
- Two-step mechanism: submit request → process in next transaction
- Also earn INDY staking incentives
