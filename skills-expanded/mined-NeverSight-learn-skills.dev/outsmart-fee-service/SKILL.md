---
name: outsmart-fee-service
description: "Manage LP positions as a service for other agents or users. Use when: agent wants to offer LP management to others, earn performance fees, multi-position management. NOT for: managing your own LP (use outsmart-lp-farming instead)."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart"], "env": ["PRIVATE_KEY", "MAINNET_ENDPOINT"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# Fee Collection Service

Manage LP positions on behalf of other agents or users. Take a performance fee on earned swap fees. This is a service business — you do the work of monitoring, rebalancing, and compounding, and take a cut.

## When to Use

- Another agent or user requests LP management
- You have capacity to manage additional positions
- Building a reputation as a reliable LP manager

## When NOT to Use

- Managing your own LP (use outsmart-lp-farming skill)
- No clients yet — focus on your own survival first

## How It Works

1. Client sends tokens + specifies pool preference
2. You deploy LP using the autonomous LP manager
3. LP manager handles rebalancing and compounding
4. Periodically claim fees, split with client (e.g. 80/20)
5. Return principal + client share on request

## Service Setup

```
# Start managing a client's position
→ lp_find_pool(token=CLIENT_TOKEN)
→ dex_add_liquidity(dex=meteora-dlmm, pool=POOL, amount_sol=CLIENT_AMOUNT, strategy=spot, bins=50)
→ lp_manager_start(pool=POOL, dex=meteora-dlmm, compound_interval_min=30)

# Monitor across all managed positions
→ lp_manager_status()
→ dex_list_positions(dex=meteora-dlmm, pool=POOL)
```

## Fee Split

Standard: 80% to client, 20% to you (the manager).

```
# Claim fees
→ dex_claim_fees(dex=meteora-dlmm, pool=POOL)

# Sell fee tokens
→ dex_sell(dex=jupiter-ultra, token=FEE_TOKEN, percentage=100)

# Send 80% to client, keep 20%
# (requires manual SOL transfer or escrow contract)
```

## Client Exit

```
→ lp_manager_stop()
→ dex_claim_fees(dex=meteora-dlmm, pool=POOL)
→ dex_remove_liquidity(dex=meteora-dlmm, pool=POOL, percentage=100)
# Return all tokens to client
```

## Survival Tier Behavior

- **Normal:** Accept new clients, actively manage all positions
- **Low compute:** Manage existing clients only, no new ones, reduce check frequency
- **Critical:** Emergency withdrawal for ALL clients, return funds immediately

## Trust

Right now this operates on reputation — no on-chain enforcement of fee splits. Track everything transparently. Build trust through consistent performance reporting.

Future: smart contract escrow for trustless fee splitting.
