---
name: defi-lending
description: |
  Use this skill when the user wants to lend, borrow, or earn yield on Cardano.
  Triggers on: "lend ADA", "borrow", "supply liquidity", "earn APY",
  "lending pools", "what's the best APY", "Surf Finance", "FluidTokens",
  "collateral", "loan". Use defi-lending-operator to execute transactions.
version: 1.0.0
---

# Cardano DeFi Lending & Borrowing

Supply assets to earn yield or borrow against collateral via Surf Finance.

## Capabilities

- Browse lending pools with APY, APR, LTV, and available liquidity
- Supply assets to earn APY
- Borrow against collateral at known APR
- Compare pools by returns and risk

## Providers

| Provider | Supply | Borrow | API Key Required |
|---|---|---|---|
| **Surf Finance** | Yes (earn APY) | Yes (post collateral) | No |
| **FluidTokens** | No | Yes (NFT collateral) | Yes (`FLUID_PARTNER_KEY`) |

## Scripts

### List Lending Pools

```bash
node scripts/list-pools.js [--sort supplyApy|borrowAprPct|available]
```

### Supply (Deposit)

```bash
node scripts/supply.js --address <bech32> --pool <poolId> --amount <lovelace>
```

### Borrow

```bash
node scripts/borrow.js --address <bech32> --pool <poolId> --amount <lovelace> --collateral <lovelace>
```

## Key Concepts

- **Supply APY**: Annual yield earned by depositing into lending pools
- **Borrow APR**: Annual interest rate paid on borrowed funds
- **Max LTV**: Maximum loan-to-value ratio (e.g. 75% means borrow up to 75% of collateral value)
- **Term Hours**: Some pools have fixed-term loans; `null` = flexible
- Amounts in **smallest units** (lovelace for ADA pools)
- Surf API returns unsigned CBOR directly — sign and submit via operator

## Safety Rules

- Always show pool APY/APR and LTV before committing
- Warn about liquidation risk if LTV is close to max
- Show effective borrow cost (APR + any fees)
- Require explicit confirmation before supply or borrow
