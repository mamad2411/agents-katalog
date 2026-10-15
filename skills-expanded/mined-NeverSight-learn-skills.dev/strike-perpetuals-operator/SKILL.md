---
name: strike-perpetuals-operator
description: |
  OPERATOR SKILL — requires manual confirmation. Execute Strike Finance v2
  perpetual trades (orders, leverage changes, cancellations).
  Strike v2 uses Ed25519 signed API requests — no CBOR signing needed.
  Auth is handled by the client via STRIKE_API_PUBLIC_KEY/PRIVATE_KEY.
version: 2.0.0
---

# Strike Perpetuals Operator

Execute perpetual trades on Strike Finance v2.

Unlike other operators, Strike v2 doesn't use CBOR transactions.
Orders are placed via authenticated REST API calls signed with Ed25519.

## Scripts

### Place Order (wrapper with confirmation)

```bash
node scripts/confirm-and-place.js --symbol ADA-USD --side buy --type market --size 100
```

### Cancel Order

```bash
node scripts/cancel-order.js --order-id <id> --symbol ADA-USD
```

## Safety Rules

- **NEVER auto-trade** — always require explicit user confirmation
- **NEVER log private keys**
- Show estimated entry/exit price before confirming
- Warn on leverage >10x
