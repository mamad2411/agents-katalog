---
name: saturnswap-limit-orders-operator
description: |
  OPERATOR SKILL — requires manual confirmation for every action.
  Use this skill to sign and submit limit order or cancel order transactions.
  Triggers after saturnswap-limit-orders has created an unsigned transaction.
  "sign limit order", "submit order", "execute the cancel", "confirm order".
version: 1.0.0
---

# SaturnSwap Limit Orders Operator

Sign and submit limit order and cancel transactions. OPERATOR skill — every
action requires explicit user confirmation.

## Prerequisites

- An unsigned transaction (transactionId + hexTransaction) from the guidance skill
- A wallet signing key (PAYMENT_SKEY_HEX or PAYMENT_SKEY_CBOR)

## Scripts

### Sign and Submit Order

```bash
node scripts/sign-and-submit.js --address <bech32> --txid <transactionId> --hex <unsignedHex>
```

Uses the same sign-and-submit pattern as market swap operator.

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation
- **NEVER log private keys**
- Verify transaction ID matches user-approved operation
- Report final on-chain transaction ID for verification
