---
name: balancer-liquidity
description: "Use when adding to or exiting a Balancer V2 or V3 pool, reviewing BPT minima, Permit2, boosted assets or hook-dependent liquidity."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.7.1"
---

# Balancer liquidity

Produce a generation-specific liquidity plan with queried BPT or token limits. Balancer V2, V3 and CoW AMM pools can share SDK tooling while using different contracts and liquidity mechanics.

## Identify the pool and inventory

Collect chain, pool address/ID, owner, deposit or exit intent, amount vector and accepted slippage. Read the exact pool generation, token order, decimals, pool type and vault/router identities. For boosted pools identify the underlying and wrapped claim; for hooks record the actual hook and supported query behavior. Verify current deployment code, paused/recovery state and the user's BPT custody, including gauges or external wrappers.

Use current `@balancer/sdk` pool data and onchain queries as described in [reads](references/reads.md). Keep one block/time context for the comparison. API metadata does not prove the pool is currently operable.

## Query before construction

For deposits choose the documented liquidity kind: unbalanced, proportional or single-token, as supported by that pool. Query exact amounts and sender/recipient context, not an arbitrary address. Record returned BPT and price impact. For exits use the corresponding removal query and preserve which tokens are actually returned.

Derive minimum BPT or minimum token outputs from the user's limit with the SDK's `Slippage` utility. `Slippage.fromPercentage('1')` means one percent. For a query of 100 BPT and 1% limit, the floor is 99 BPT, before any different gas currency. Do not subtract fees already incorporated in the query twice.

## Inspect the unsigned handoff

Return router, calldata, native value, token allowances, permit terms, recipient and calculated minima. Permit2 signing is an authorization action; do not call signing helpers merely to obtain a quote. Check that generation, hook data, token order and all addresses agree with the query. A V2 pool cannot use a V3 vault because the latter is newer.

If hook queries fail, wrapper rates are stale, the selected kind is unsupported or assets are held by another contract, return the specific unresolved dependency. Never approximate missing support with a different pool's ABI. Re-query after approvals or changed balances. A mined liquidity receipt plus BPT/token deltas establishes the result; an SDK call object or a gauge deposit alone does not.

## Worked result

Synthetic deposit quote: 1,000 USDC and 1,000 DAI produce 100 BPT; user accepts 1% slippage and has approved token spending but has not signed Permit2. Return a 99-BPT minimum, the exact two-token order and unsigned permit/call requirements. Status is prepared, awaiting the user's existing wallet boundary. If current pool metadata says V2 but the proposed target is a V3 router, block that handoff and resolve the correct construction path.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
