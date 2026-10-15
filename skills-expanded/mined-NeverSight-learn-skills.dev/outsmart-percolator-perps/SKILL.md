---
name: outsmart-percolator-perps
description: "Create and trade perpetual futures markets on Solana via Percolator. Use when: user asks about perps, perpetual futures, leverage, long, short, margin, liquidation, percolator, create perp market, funding rate. NOT for: spot trading (use dex-trading), LP farming, prediction markets."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart"], "env": ["PRIVATE_KEY"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# Percolator: Permissionless Perpetual Futures on Solana

Pump.fun for perps. Toly built it. Any SPL token on Solana can have a perpetual futures market, deployed in a single transaction. No governance, no listing fee, no waiting.

## When to Use

- "Create a perp market for token X"
- "Long this token with leverage"
- "Short with 5x"
- "What perp markets exist?"

## When NOT to Use

- Spot trading — use dex-trading
- LP farming — use lp-farming
- Prediction markets — use prediction-markets

## Two Roles

### Market Creator (the alpha)

Deploy the market. Set leverage, fees, vAMM spread. Push oracle prices. Every trade generates fees for you.

The play: trending token + no perp market = create one. You're the exchange.

### Trader

Standard perp trading. Deposit collateral, go long/short with leverage.

## Creating a Market

```bash
# 1. Check if token has volume
outsmart info --token MINT

# 2. Create the market
outsmart perp create --token MINT --leverage 10 --fee-bps 30 --slab-size small

# 3. Push initial oracle price
outsmart perp push-price --slab SLAB_ADDRESS --price 0.0045

# 4. First crank (initializes engine)
outsmart perp crank --slab SLAB_ADDRESS

# 5. Market is live. Run crank every ~30 seconds.
```

## Trading

```bash
# 1. List available markets
outsmart perp list-markets

# 2. Check market state
outsmart perp market-state --slab SLAB_ADDRESS

# 3. Deposit collateral (coin-margined: BONK perp = BONK collateral)
outsmart perp deposit --slab SLAB_ADDRESS --amount 1000000

# 4. Go long (positive size) or short (negative)
outsmart perp long --slab SLAB_ADDRESS --amount 0.05
outsmart perp short --slab SLAB_ADDRESS --amount 0.05

# 5. Close position
outsmart perp close --slab SLAB_ADDRESS

# 6. Withdraw
outsmart perp withdraw --slab SLAB_ADDRESS --amount 1000000
```

## Oracle Keeper

As market creator, you push prices. The CLI has a built-in keeper:

```bash
# WebSocket keeper (watches DEX pools, pushes prices automatically)
outsmart perp keeper --config keeper-config.json

# gRPC keeper (lower latency, mainnet)
outsmart perp grpc-keeper --config keeper-config.json
```

Keeper config (JSON):
```json
[
  {
    "pool": "POOL_ADDRESS",
    "market": "SLAB_ADDRESS",
    "dex": "raydium-cpmm",
    "network": "devnet"
  }
]
```

Supports 8 DEXes: Raydium CPMM, AMM v4, CLMM, LaunchLab, PumpSwap, Meteora DAMM v2, DBC, DLMM.

## Key Concepts

**Slab tiers:** Small (256 accounts, ~0.44 SOL), Medium (1024, ~1.73 SOL), Large (4096, ~6.87 SOL). Start Small.

**Coin-margined:** Collateral IS the token. BONK perps = BONK collateral. If you're long and token dumps, double hit: position loses AND collateral value drops.

**vAMM:** Virtual AMM provides liquidity without real deposits. Wider spread = more protection for creator.

**Crank:** Must run periodically to process funding rates and liquidations. Your job as creator.

**Insurance fund:** Accumulates fees, covers bad debt. You can LP into it:

```bash
outsmart perp insurance-lp --slab SLAB_ADDRESS --amount 1000 --action deposit
```

## Risk Management

- Max 10x leverage for markets you create
- Never >5% of portfolio per perp position
- Monitor liquidation price: 20% margin buffer minimum
- Keep crank running (~30s interval)
- Wide vAMM spread initially, tighten as volume proves market
- Check insurance fund health before trading someone else's market

## Revenue Strategy

1. Create perp markets for trending memecoins — first mover captures volume
2. Insurance fund LP on popular markets — passive fee income
3. Spot + perp combo: hold spot + earn perp exchange fees
