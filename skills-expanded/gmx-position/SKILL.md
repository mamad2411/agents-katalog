---
name: gmx-position
description: "Use when reviewing a GMX perpetual position or order through SDK v2, including market capacity, fees, keeper execution and request-id reconciliation."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# GMX position

Return a market/position risk view or reconcile one GMX order. An API relay acknowledgement, onchain order creation and keeper execution are separate stages.

## Read current market and account state

Collect chain, public account, market, side, collateral token, intended size and order type. Discover the precise market symbol/address through current `GmxApiSdk` reads in [recipes](references/reads.md). Keep spot-only markets, long/short collateral and market-token identities distinct. Use SDK v2 for new integration; SDK v1 is maintenance-only, not the preferred new implementation.

Read prices, market configuration, available trading capacity, current positions and orders. Confirm data age and JIT-aware capacity for the requested side/size. Measure collateral and margin with protocol math, retaining raw USD/token units. Include position fees, borrowing, signed funding, price impact, execution/keeper gas and any relay charges separately. A displayed leverage limit does not guarantee current capacity.

## Bound the unsigned plan

For a proposed change show size delta, collateral delta, acceptable price, execution fee, trigger/limit conditions and expected remaining exposure. Identify whether this is increase, reduce or collateral-only, and whether collateral/output swaps occur. SDK prepare/sign/submit stages are not all reads; stop at reviewed preparation for research. Resolve current order/relay schema and contract deployments before any authorized handoff; never copy example private keys.

## Track original identity

Preserve API `requestId` and the reviewed idempotency key, then any order key and transaction hashes. Query status for that original request. Relay accepted is not keeper filled; an order can remain pending, cancel or fail. Reconcile final order events, actual position size/collateral and fees. A stop order is contingent execution, not a guaranteed loss cap.

On timeout, rate limits or ambiguous acknowledgement inspect the original request and onchain order before resubmitting. Do not generate a fresh idempotency key to bypass uncertainty. Report partial fills or missing position evidence explicitly.

## Worked result

Synthetic request to reduce a $10,000 long by $4,000 is accepted by relay, but the position still reads $10,000 and keeper status is pending. Report pending reduction and unchanged observed exposure. Only after execution events and a $6,000 remaining size agree can the reduction be called verified.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
