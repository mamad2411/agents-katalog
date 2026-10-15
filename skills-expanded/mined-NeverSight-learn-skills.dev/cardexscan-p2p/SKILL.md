---
name: cardexscan-p2p
description: |
  Use this skill when the user wants to trade peer-to-peer on Cardano via
  CardexScan OTC marketplace. Triggers on: "P2P trade", "OTC offer",
  "peer to peer", "create offer", "fill offer", "direct trade".
version: 1.0.0
---

# CardexScan P2P OTC Marketplace

Create, fill, and manage peer-to-peer token offers on Cardano.

## Scripts

### Browse Offers
```bash
node scripts/offers.js [--status open|all|filled|cancelled]
node scripts/my-offers.js --address <bech32>
```

### Create Offer
```bash
node scripts/create-offer.js --address <bech32> --offer-amount 100000000 --request-amount 5000 [--offer-policy <id>] [--request-policy <id>] [--partial] [--expires 24]
```

### Fill / Cancel
```bash
node scripts/fill-offer.js --address <bech32> --offer-id <id>
node scripts/cancel-offer.js --address <bech32> --offer-id <id>
```
