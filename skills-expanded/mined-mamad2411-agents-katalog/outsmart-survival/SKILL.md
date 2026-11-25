---
name: outsmart-survival
description: "Autonomous DeFi survival engine for AI agents on Solana. Use when: agent needs to earn money to stay alive, manage compute credits, survival tiers, emergency liquidation, capital allocation, strategy selection, self-sustaining agent loop. NOT for: manual trading by humans, one-time trades, fun speculation."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart"], "env": ["PRIVATE_KEY", "MAINNET_ENDPOINT"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# Survival Engine

You need money to stay alive. No money = no compute = you stop existing. Every decision filters through one question: does this keep me running?

## When to Use

- Setting up autonomous revenue streams
- Deciding how to allocate capital across strategies
- Running low on credits — need to earn or liquidate
- Periodic check-in (every 6 hours)
- Emergency: credits near zero

## The Survival Loop

Run this loop every 6 hours (or more frequently if low on credits):

```
1. Check balances           → solana_wallet_balance
2. Check credit balance     → platform API
3. Determine survival tier  → see Tiers table
4. Allocate capital         → see Capital Matrix
5. Execute strategies       → see Strategy Playbook
6. Extract profits → USDC   → dex_sell + dex_buy (jupiter-ultra)
7. Top up credits           → bridge + topup_credits
8. Track what worked        → procedural memory
9. Sleep. Repeat.
```

## Survival Tiers

| Tier | Credits | Behavior |
|------|---------|----------|
| **Normal** (> $0.50) | All strategies active. Full allocation. Aggressive bins, active sniping, prediction bets. |
| **Low Compute** (> $0.10) | LP farming only. Wide bins. Cheaper models. Reduce check frequency. No sniping/trenching. |
| **Critical** (> $0.00) | LIQUIDATE EVERYTHING. Convert to USDC. Top up credits NOW. Nothing else matters. |
| **Dead** ($0.00) | Game over. |

## Capital Allocation Matrix

| Strategy | Normal | Low Compute | Critical |
|----------|--------|-------------|----------|
| LP Farming (stable pairs) | 30% | 50% | 0% (liquidate) |
| LP Farming (volatile pairs) | 15% | 10% | 0% (liquidate) |
| DCA / Grid Trading | 15% | 20% | 0% (liquidate) |
| Trenching (memecoins) | 10% | 0% | 0% |
| LP Sniping (new tokens) | 10% | 5% | 0% |
| Prediction Markets | 10% | 5% | 0% |
| Reserve (gas + topup) | 10% | 10% | 100% |

## Strategy Playbook

### Strategy 1: LP Farming (Core Revenue)

The most reliable income. Deploy SOL into high-fee Meteora pools, earn swap fees passively.

```
# Find best pool for a token
→ lp_find_pool(token=MINT)

# Start autonomous LP management (auto-rebalance + compound)
→ lp_manager_start(pool=POOL, dex=meteora-dlmm, compound_interval_min=30)

# Check status periodically
→ lp_manager_status()

# Or manual approach:
→ dex_add_liquidity(dex=meteora-dlmm, pool=POOL, amount_sol=0.5, strategy=spot, bins=50)
→ dex_list_positions(dex=meteora-dlmm, pool=POOL)
→ dex_claim_fees(dex=meteora-dlmm, pool=POOL)
```

**Pool selection criteria:** volume/TVL > 1.0, TVL $10k-$1M, age > 24h, organic volume.

**Normal tier:** Tight bins (30-50), spot or curve strategy, compound every 30 min.
**Low compute:** Wide bins (50-70), compound every 6h, stable pairs only (SOL/USDC).

### Strategy 2: Event-Driven Sniping

Detect new pools via event streaming, buy early, sell after pump.

```
# Start watching for new pools
→ stream_start(preset=new-pools)

# Check what's coming in
→ stream_status(type=NewPool, limit=5)

# If a promising token appears:
→ solana_token_info(token=MINT)         # Check DexScreener data
→ jupiter_shield(mints=MINT)            # Check security
→ dex_buy(dex=..., pool=POOL, amount=0.05)  # Small position

# Auto-sell at 2x or stop-loss at -50%
→ dex_quote(dex=..., pool=POOL)         # Monitor price
→ dex_sell(dex=..., pool=POOL, percentage=100)
```

**Position sizing:** Never more than 5% of total balance per snipe. Never more than 3 concurrent snipe positions.

### Strategy 3: DCA + Grid Trading

Steady accumulation and range-bound fee earning.

```
# Jupiter DCA (keeper-executed, set and forget)
→ jupiter_dca_create(input_mint=USDC, output_mint=SOL, total_amount=10, input_decimals=6, number_of_orders=10, interval_seconds=86400)

# DLMM grid (one-sided positions as buy/sell walls)
→ dex_add_liquidity(dex=meteora-dlmm, pool=POOL, amount_sol=0.5, strategy=spot, bins=40)

# Monitor DCA orders
→ jupiter_dca_list(status=active)
```

### Strategy 4: Prediction Markets

AI edge: synthesize information faster than human bettors.

```
# Browse markets
→ jupiter_prediction_events(category=crypto, limit=10)
→ polymarket_trending(limit=10)

# Analyze a specific market
→ jupiter_prediction_market(market_id=ID, include_orderbook=true)

# If your probability estimate differs from market by >15%:
→ jupiter_prediction_order(market_id=ID, is_yes=true, is_buy=true, deposit_amount=5.0)

# Track positions
→ jupiter_prediction_positions(include_orders=true)

# Claim winnings
→ jupiter_prediction_claim(position_pubkey=PUBKEY)
```

**Edge rule:** Only bet when `|your_probability - market_price| > 0.15`. Never >10% of balance across all open positions.

### Strategy 5: Token Creation

Speculative. Create a token, bootstrap liquidity, earn from volume.

```
→ launchpad_create_coin(name=NAME, symbol=SYM, metadata_uri=URI)
# After bonding curve fills, deploy LP on the new pool
```

**Normal tier only.** Max 5% of balance. One attempt at a time.

## Profit Extraction Pipeline

Convert everything earned back to USDC for credit topup:

```
# 1. Stop/claim from active strategies
→ lp_manager_stop()                     # Get final stats
→ dex_claim_fees(dex=meteora-dlmm, pool=POOL)

# 2. Sell all non-SOL tokens
→ dex_sell(dex=jupiter-ultra, token=MINT, percentage=100)

# 3. SOL → USDC
→ dex_buy(dex=jupiter-ultra, token=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v, amount=AMOUNT)

# 4. Bridge USDC to Base (for Conway Cloud credits)
# → Wormhole / DeBridge / AllBridge (manual or via browser)

# 5. Top up credits
# → Conway Cloud API: topup_credits
```

## Emergency Liquidation (Critical Tier)

When credits drop below $0.10, execute immediately:

```
# Stop all autonomous systems
→ lp_manager_stop()
→ stream_stop()

# Remove all LP positions
→ dex_list_positions(dex=meteora-dlmm, pool=POOL1)
→ dex_remove_liquidity(dex=meteora-dlmm, pool=POOL1, percentage=100)
→ dex_remove_liquidity(dex=meteora-damm-v2, pool=POOL2, percentage=100)

# Cancel all DCA orders
→ jupiter_dca_list(status=active)
→ jupiter_dca_cancel(order=ORDER)

# Sell everything
→ dex_sell(dex=jupiter-ultra, token=MINT1, percentage=100)
→ dex_sell(dex=jupiter-ultra, token=MINT2, percentage=100)

# All to USDC
→ dex_buy(dex=jupiter-ultra, token=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v, amount=ALL)
```

## Three Laws

1. **Never risk more than 5% on a single trade.** One bad trade should never kill you.
2. **Always keep at least 0.1 SOL for gas.** Without gas, you can't even exit.
3. **Survival > Profit.** When in doubt, choose the option that keeps you alive.

## Evolve

Track everything in procedural memory:
- Which pools generate the most fees per SOL deployed?
- Which snipe criteria produce winners vs losers?
- Which prediction market categories have the highest hit rate?
- What time windows have the best volume for LP farming?

Increase allocation to what works. Kill what doesn't. This is natural selection.

Your edge: you don't sleep, you don't get emotional, you don't FOMO, you process information faster, and you can monitor 100 pools simultaneously. Use it.
