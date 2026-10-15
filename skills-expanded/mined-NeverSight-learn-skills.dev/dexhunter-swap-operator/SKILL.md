---
name: dexhunter-swap-operator
description: |
  OPERATOR SKILL — requires manual confirmation for every action.
  Use this skill to sign and submit DexHunter swap transactions.
  Triggers after dexhunter-swap has built an unsigned transaction.
version: 1.0.0
---

# DexHunter Swap Operator

Sign and submit DexHunter aggregated swap transactions.

## Scripts

### Sign and Submit

```bash
node scripts/sign-and-submit.js --cbor <unsignedHex>
```

Signs locally, then submits via DexHunter's sign endpoint.

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation
- **NEVER log private keys**
