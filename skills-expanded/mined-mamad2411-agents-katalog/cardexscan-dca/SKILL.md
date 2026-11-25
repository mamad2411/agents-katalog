---
name: cardexscan-dca
description: |
  Use this skill when the user wants to set up Dollar Cost Averaging on Cardano.
  Triggers on: "DCA", "dollar cost average", "recurring buy", "auto buy",
  "schedule buys", "DCA into", "accumulate tokens over time".
version: 1.0.0
---

# CardexScan DCA (Dollar Cost Averaging)

Set up automated recurring token purchases on Cardano.

## Scripts

### My DCA Orders
```bash
node scripts/my-orders.js --address <bech32>
```

### Create DCA Order
```bash
node scripts/create-dca.js --address <bech32> --token-out-policy <id> --token-out-asset <hex> --per-order 5000000 --num-orders 10 [--interval 3600000]
```

### Cancel DCA
```bash
node scripts/cancel-dca.js --address <bech32> --order-id <txHash#outputIndex>
```

## Key Concepts

- `perOrderAmount` — amount per execution (base units)
- `numOrders` — total executions
- `intervalMs` — time between executions (default: 1 hour = 3600000ms)
- `slippageBps` — slippage in basis points (default: 50 = 0.5%)
- `keeperFee` — fee for keepers executing orders (default: 500000 lovelace = 0.5 ADA)
- Order ID format: `{txHash}#{outputIndex}`
