---
name: curve-liquidity
description: "Use when planning a Curve pool deposit or withdrawal, comparing single-coin and balanced exits, or reconciling LP-token and gauge custody."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.7.1"
---

# Curve liquidity

Return the pool's exact coin vector, the user's redeemable claim and an unsigned deposit or exit comparison. A pool ticker does not identify its factory, wrapped assets or gauge.

## Establish the claim

Collect chain, pool address or SDK pool ID, public owner, action, amount and requested output token. Resolve the factory family and current pool metadata through the official Curve SDK. Record LP token, gauge, underlying/wrapped coin addresses and decimals in their returned order. Verify chain and bytecode through the configured read-only RPC.

Read wallet LP balance and gauge balance separately. A zero wallet LP balance is not a zero position when a gauge or wrapper holds the claim. Identify who can unstake; do not infer an EOA owns assets held by an ALM. Read allowances only for a proposed action.

## Quote the action

Use the read methods in [read recipes](references/reads.md), passing decimal strings or the SDK's raw BigInt variants. For a deposit compare the exact ordered amount vector with expected LP output. For an exit quote proportional withdrawal and, if supported, the exact single-coin alternative at the same observation time. Wrapped and underlying methods can produce different assets; keep their vectors separate.

Normalize each returned amount with its own decimals, then compare inventory value, imbalance cost, provider fees and native gas. A smaller token count is not a worse dollar result without a price source. The SDK's transaction slippage argument uses percentage points; translate the user's basis-point limit explicitly rather than passing a fraction accidentally.

## Prepare and reconcile

Return the selected method, ordered inputs, minimum LP or coin output, spender, recipient, gas budget and quote age. Methods named `deposit`, `withdraw`, `stake` or `unstake` may send through a configured signer; research uses expected/balance methods only. If execution is separately authorized, unstaking, removal and claiming each need their own receipt and state reread. Rewards are separate from redeemed principal.

Stop construction when the pool family, wrapper ownership or quoted output asset is unresolved. On stale RPC, partial factory discovery, paused pools or changed coin order, report a bounded gap and refresh rather than substituting a different pool. After an ambiguous send, inspect the original hash before considering another action.

## Worked result

Synthetic owner claim: 100 LP in wallet and 400 LP in a gauge. Quote all 500 LP: balanced exit returns 252 USDC plus 248 USDT; single-coin exit returns 497 USDC before gas. The correct result is a 500-LP total claim, an unstaking prerequisite for 400 LP, and two output alternatives. It is not a 100-LP position or a guaranteed 500-USDC redemption. Report the 3-USDC single-coin shortfall only under an explicitly supplied one-dollar mark for both stablecoins.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
