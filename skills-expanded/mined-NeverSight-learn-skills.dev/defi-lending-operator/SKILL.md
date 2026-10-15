---
name: defi-lending-operator
description: |
  OPERATOR SKILL — requires manual confirmation. Sign and submit lending/borrowing
  transactions from Surf Finance or FluidTokens.
version: 1.0.0
---

# DeFi Lending Operator

Sign and submit lending/borrowing transactions.

## Scripts

### Sign and Submit

```bash
node scripts/sign-and-submit.js --cbor <unsignedHex>
```

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation
- **NEVER log private keys**
- Verify the operation matches what user approved (supply vs borrow, amount)
