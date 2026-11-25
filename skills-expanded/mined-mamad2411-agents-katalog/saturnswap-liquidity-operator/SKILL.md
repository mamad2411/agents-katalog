---
name: saturnswap-liquidity-operator
description: |
  OPERATOR SKILL — requires manual confirmation for every action.
  Use this skill to sign and submit liquidity transactions (add or withdraw).
  Triggers after saturnswap-liquidity has created an unsigned transaction.
  "sign liquidity tx", "submit liquidity", "execute add liquidity", "confirm withdraw".
version: 1.0.0
---

# SaturnSwap Liquidity Operator

Sign and submit liquidity transactions. OPERATOR skill — every action
requires explicit user confirmation.

## Prerequisites

- An unsigned transaction (transactionId + hexTransaction) from the guidance skill
- A wallet signing key (PAYMENT_SKEY_HEX or PAYMENT_SKEY_CBOR)

## Scripts

### Sign and Submit Liquidity Transaction

```bash
node scripts/sign-and-submit.js --address <bech32> --txid <transactionId> --hex <unsignedHex>
```

Note: Liquidity transactions use `submitLiquidityTransaction` (not `submitOrderTransaction`).

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation
- **NEVER log private keys**
- Verify transaction ID matches user-approved operation
- Report final on-chain transaction ID for verification
