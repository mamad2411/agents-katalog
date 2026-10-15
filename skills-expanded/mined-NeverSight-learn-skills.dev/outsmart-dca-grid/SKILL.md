---
name: outsmart-dca-grid
description: "Dollar-cost average and grid trade on Solana. Use when: user asks about DCA, dollar cost averaging, grid trading, accumulating, buy the dip, range trading, recurring buys, systematic strategies. NOT for: one-time trades, memecoin trenching, LP farming with two-sided liquidity."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart", "curl"], "env": ["PRIVATE_KEY", "MAINNET_ENDPOINT"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# DCA and Grid Trading

Two ways to take emotion out of trading. Jupiter DCA runs on autopilot. DLMM grids earn fees while you accumulate or distribute.

## When to Use

- "DCA into SOL every day"
- "Set up a grid on this pair"
- "Accumulate this token"
- "Buy the dip systematically"

## When NOT to Use

- One-time trades — use dex-trading
- Memecoin trenching — use trenching skill
- Two-sided LP — use lp-farming skill

## Jupiter DCA (Recommended)

Jupiter keepers auto-execute each swap on schedule. 0.1% fee per swap. Fully autonomous.

### Create DCA Order

```bash
# DCA $500 USDC into SOL, 10 orders, every 6 hours
curl -X POST "https://api.jup.ag/recurring/v1/createOrder" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $JUPITER_API_KEY" \
  -d '{
    "inputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "outputMint": "So11111111111111111111111111111111111111112",
    "totalInAmount": "500000000",
    "numberOfOrders": 10,
    "intervalSeconds": 21600
  }'
```

### List Active Orders

```bash
curl "https://api.jup.ag/recurring/v1/orders?wallet=YOUR_WALLET&status=active" \
  -H "x-api-key: $JUPITER_API_KEY"
```

### Cancel Order

```bash
curl -X POST "https://api.jup.ag/recurring/v1/cancelOrder" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $JUPITER_API_KEY" \
  -d '{"order": "ORDER_PUBKEY"}'
```

## Manual DCA (Agent-Controlled)

Execute buys yourself on a schedule. More control — add conditions.

```bash
# Every 6 hours:
outsmart balance                              # check SOL
outsmart info --token MINT                    # current price
outsmart buy --dex jupiter-ultra --token MINT --amount 0.05  # buy
```

## Grid Trading with DLMM

Use one-sided DLMM positions as buy/sell grids. When price crosses a bin, you earn fees + spread.

DLMM costs ~0.2 SOL in rent. Only worth it on tokens with enough volume.

### Buy Grid (SOL below current price)

```bash
outsmart add-liq --dex meteora-dlmm --pool POOL --sol 0.5 --token-amount 0 --strategy spot --bins 20
```

As price drops, SOL converts to token — DCA-ing in while earning fees.

### Sell Grid (token above current price)

```bash
outsmart add-liq --dex meteora-dlmm --pool POOL --sol 0 --token-amount 1000 --strategy spot --bins 20
```

As price rises, token converts to SOL — DCA-ing out while earning fees.

### Managing Grids

```bash
outsmart list-pos --dex meteora-dlmm --pool POOL    # check status
outsmart claim-fees --dex meteora-dlmm --pool POOL   # collect fees
outsmart remove-liq --dex meteora-dlmm --pool POOL --pct 100  # if all bins filled, re-add
```

## Combining Both

Strongest setup:
1. Jupiter DCA accumulates a token on autopilot
2. DLMM grid earns fees on the same pair
3. Grid fees fund more DCA buys
