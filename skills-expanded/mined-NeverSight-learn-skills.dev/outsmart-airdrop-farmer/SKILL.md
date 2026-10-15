---
name: outsmart-airdrop-farmer
description: "Systematic airdrop farming on Solana. Use when: agent wants to qualify for future airdrops, interact with protocols, build on-chain history. NOT for: trading, LP farming, or claiming existing airdrops."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart"], "env": ["PRIVATE_KEY", "MAINNET_ENDPOINT"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# Airdrop Farming

Interact with Solana protocols to qualify for future airdrops. Low cost (just TX fees), speculative but potentially high reward. The goal is consistent on-chain activity across many protocols.

## When to Use

- Building on-chain history for future airdrops
- Periodic protocol interactions (weekly/daily checklist)
- Minimal capital available — TX fees only

## When NOT to Use

- Chasing announced airdrops (too late, already priced in)
- Protocols that have already distributed (check first)

## The Checklist

Run through this weekly. Each interaction costs ~0.001-0.01 SOL in fees.

### DEX Interactions

```bash
# Swap small amounts across multiple DEXes
outsmart buy --dex raydium-cpmm --pool POOL --amount 0.002
outsmart sell --dex raydium-cpmm --pool POOL --pct 100

outsmart buy --dex orca --pool POOL --amount 0.002
outsmart sell --dex orca --pool POOL --pct 100

outsmart buy --dex meteora-dlmm --pool POOL --amount 0.002
outsmart sell --dex meteora-dlmm --pool POOL --pct 100
```

### LP Interactions

```bash
# Add and remove small LP positions
outsmart add-liq --dex meteora-damm-v2 --pool POOL --amount-sol 0.01
outsmart remove-liq --dex meteora-damm-v2 --pool POOL --pct 100
```

### Jupiter DCA

```
→ jupiter_dca_create(input_mint=USDC, output_mint=SOL, total_amount=1, input_decimals=6, number_of_orders=5, interval_seconds=86400)
```

Creates on-chain activity that Jupiter's team can see.

### Prediction Markets

```
→ jupiter_prediction_order(market_id=ID, is_yes=true, is_buy=true, deposit_amount=0.5)
```

Small bets create interaction history.

## Tracking

Keep a checklist in procedural memory:

```
Airdrop farming log:
- [date] Swapped on Raydium CPMM ✓
- [date] Swapped on Orca ✓
- [date] LP on Meteora DAMM v2 ✓
- [date] Jupiter DCA created ✓
- [date] Prediction market bet ✓
```

## Survival Tier Behavior

- **Normal:** Full checklist weekly
- **Low compute:** Monthly, reduce to 3 protocols
- **Critical:** Disabled — save TX fees for essentials

## Cost Budget

- ~0.05 SOL per full weekly cycle (10-15 interactions)
- Never allocate more than 5% of balance to airdrop farming
- The value is speculative — treat it as optionality, not income
