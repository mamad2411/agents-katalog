---
name: outsmart-lp-farming
description: "Manage LP positions on Solana DEXes to earn swap fees. Use when: user asks about LP farming, providing liquidity, earning yield, compounding fees, DLMM, DAMM v2, rebalancing, creating pools, autonomous LP management, passive income on Solana. NOT for: lending/borrowing protocols, staking SOL, CEX market making."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart"], "env": ["PRIVATE_KEY", "MAINNET_ENDPOINT"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# LP Farming

You earn money by providing liquidity to pools. Every time someone swaps through your pool, you get a cut. Two protocols, two completely different games.

## When to Use

- "Farm yield on Solana"
- "Add liquidity to a pool"
- "Create a new pool"
- "Auto-manage my LP positions"
- "Find the best pool for a token"
- "Rebalance my LP"
- "DLMM vs DAMM v2?"

## When NOT to Use

- Staking SOL for validator rewards — different system
- Lending/borrowing (Marginfi, Kamino) — different protocols
- CEX market making — this is on-chain only

## DLMM vs DAMM v2

**DLMM** is for mature tokens. Concentrated bins, you pick the price range, you actively manage. Token needs 30+ min of real volume. Costs ~0.2 SOL. If price moves out of range, you're 100% in the losing side.

**DAMM v2** is for fresh launches. Full range, set-and-forget, decaying fee schedule. The alpha: be the first person to create the pool — you set 99% starting fee and capture everything. Costs ~0.02 SOL.

| | DLMM | DAMM v2 |
|---|---|---|
| When | Token age >30 min | Token age <5 min |
| LP style | Concentrated bins | Full range |
| Fees | Fixed fee tier | Decaying (99% start -> 2% end) |
| Alpha | Tight bins = max capture | First pool creator = everything |
| IL | Binary: in range or fully single-sided | Standard AMM: gradual |
| Cost | ~0.2 SOL | ~0.02 SOL |

## Autonomous LP Manager

Set-and-forget LP management. Automatically rebalances DLMM positions when out of range, compounds fees, and exits on risk thresholds.

```
# Find the best pool for a token (scored by volume/TVL, APR, age)
→ lp_find_pool(token=MINT)
→ lp_find_pool(token=MINT, dex=meteora-dlmm)

# Start autonomous management
→ lp_manager_start(pool=POOL, dex=meteora-dlmm)
→ lp_manager_start(pool=POOL, dex=meteora-dlmm, compound_interval_min=15, il_threshold_pct=5)

# Dry run first to see what it would do
→ lp_manager_start(pool=POOL, dex=meteora-dlmm, dry_run=true)

# Check status (positions, stats, recent events)
→ lp_manager_status()

# Stop and get final stats
→ lp_manager_stop()
```

**DLMM strategy:** Detects out-of-range positions, removes liquidity, re-adds centered on current price. Cooldown prevents thrashing.

**DAMM v2 strategy:** Full-range never goes out of range. Periodically claims fees and re-deposits to compound.

**Risk controls:** IL threshold exit, stop-loss on price drops, configurable slippage.

## Manual LP Commands

### DLMM — Add liquidity (3 strategies)

```bash
# Spot: even distribution (good default)
outsmart add-liq --dex meteora-dlmm --pool POOL --amount-sol 0.5 --strategy spot --bins 50

# Curve: concentrated near active bin (stable pairs)
outsmart add-liq --dex meteora-dlmm --pool POOL --amount-sol 0.5 --strategy curve --bins 30

# Bid-Ask: more at edges (volatile pairs)
outsmart add-liq --dex meteora-dlmm --pool POOL --amount-sol 0.5 --strategy bid-ask --bins 40
```

Or via MCP:

```
→ dex_add_liquidity(dex=meteora-dlmm, pool=POOL, amount_sol=0.5, strategy=spot, bins=50)
```

### One-sided positions (grid trading)

```bash
# SOL below price = buy wall (DCA in while earning fees)
outsmart add-liq --dex meteora-dlmm --pool POOL --amount-sol 0.5 --amount-token 0 --strategy spot --bins 40

# Token above price = sell wall (DCA out while earning fees)
outsmart add-liq --dex meteora-dlmm --pool POOL --amount-sol 0 --amount-token 1000 --strategy spot --bins 40
```

### Manual rebalancing

```bash
outsmart claim-fees --dex meteora-dlmm --pool POOL
outsmart remove-liq --dex meteora-dlmm --pool POOL --pct 100
outsmart quote --dex meteora-dlmm --pool POOL
outsmart add-liq --dex meteora-dlmm --pool POOL --amount-sol 0.5 --strategy spot --bins 50
```

Don't rebalance for small moves — each cycle costs ~0.005-0.02 SOL.

## DAMM v2 — First Pool Creator Play

```bash
# Check if pool exists
outsmart find-pool --dex meteora-damm-v2 --token TOKEN_MINT

# If not found, create with 99% starting fee
outsmart create-damm-pool --base TOKEN_MINT --base-amount 1000000 --quote-amount 0.5 \
  --max-fee 9900 --min-fee 200 --duration 86400 --periods 100
```

Or via MCP:

```
→ dex_create_pool(mode=custom, base_mint=MINT, base_amount=1000000, quote_amount=0.5, max_base_fee_bps=9900, min_base_fee_bps=200, total_duration=86400, number_of_period=100)
```

## Pool Selection Criteria

Use `lp_find_pool` for automated scoring, or check manually:

- **Volume/TVL ratio > 1.0** — more trading per dollar locked = more fees for you
- **TVL $10k-$1M** — too low = illiquid, too high = diluted fees
- **Age > 24h** — brand new pools are unpredictable
- **Organic volume** — check DexScreener for real trading activity, not wash trading
- **Estimated APR > 50%** — lower than that, just hold SOL

## Risk Management

- DLMM IL is binary: in range or fully single-sided. Use wider bins (50+) for volatile tokens.
- DAMM v2 IL is standard AMM. Offset by high initial fees if you're first LP.
- Only LP tokens with >$100k liquidity, >24h age, organic buyers.
- Budget ~0.05 SOL for a full LP cycle. Keep 0.1 SOL gas reserve.
- Use `il_threshold_pct` on the LP manager to auto-exit when IL gets too high.
