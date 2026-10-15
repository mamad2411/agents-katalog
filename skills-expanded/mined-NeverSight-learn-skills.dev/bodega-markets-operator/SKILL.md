---
name: bodega-markets-operator
description: |
  OPERATOR SKILL — requires manual confirmation. Sign and submit Bodega
  prediction market transactions (buy, sell, cancel, claim).
version: 1.0.0
---

# Bodega Markets Operator

Sign and submit prediction market transactions.

## Scripts

### Sign and Submit

```bash
node scripts/sign-and-submit.js --cbor <unsignedHex>
```

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation
- **NEVER log private keys**
