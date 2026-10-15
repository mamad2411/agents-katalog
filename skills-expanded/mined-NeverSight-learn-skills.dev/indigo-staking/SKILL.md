---
name: indigo-staking
description: |
  Use this skill when the user wants to stake INDY tokens on Indigo Protocol.
  Triggers on: "stake INDY", "Indigo staking", "INDY rewards", "staking position",
  "governance voting power", "staking APR". Use indigo-cdp-operator to sign.
version: 1.0.0
---

# INDY Token Staking

Stake INDY tokens to earn rewards and gain governance voting power.

## Scripts

### View Staking
```bash
node scripts/staking-info.js
node scripts/my-staking.js --owner <bech32>
```

### Manage Position
```bash
node scripts/manage-staking.js --address <bech32> --action open --amount 1000000000
node scripts/manage-staking.js --address <bech32> --action adjust --tx-hash <hash> --output-index <idx> --amount 2000000000
node scripts/manage-staking.js --address <bech32> --action close --tx-hash <hash> --output-index <idx>
```

## Key Concepts

- INDY: 6 decimals (1000000 = 1 INDY)
- Rewards proportional to stake share of total pool
- Grants governance voting power
