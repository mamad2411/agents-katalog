---
name: indigo-cdp-operator
description: |
  OPERATOR SKILL — requires manual confirmation. Sign and submit Indigo Protocol
  CDP transactions (open, deposit, withdraw, mint, burn, close).
version: 1.0.0
---

# Indigo CDP Operator

Sign and submit CDP transactions for Indigo Protocol.

## Scripts

### Sign and Submit
```bash
node scripts/sign-and-submit.js --cbor <unsignedHex>
```

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation
- **NEVER log private keys**
- Verify collateral ratio will stay above minimum after operation
