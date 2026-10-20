---
name: checkout-batch-flow
description: Implement/review one-transaction checkout() batching (feed → commit → buyRelics → applyRelics → monthly action) with deterministic validation, canonical ordering, and exact payment reconciliation (refund extra).
---

# Checkout Batch Flow (1 Tx, Canonical Order)

## When to use
- Editing `checkout(CheckoutParams)` in contracts or the UI that builds the cart.
- Touching pricing, fees, stock, slots, or monthly action constraints.

## Goal (Definition of Done)
- ✅ Batch execution matches “manual” sequence semantics.
- ✅ Deterministic ordering and revert reasons.
- ✅ Payment reconciliation: `msg.value >= totalCost`, refund extra.

## Canonical execution order (must not change)
1) `payFeedCost(dayId)` if `includeFeed`
2) `commitDaily(dayId, commitHash)` if present
3) `buyRelics(scope=id/dayId/monthId, batch)`
4) `applyRelics(scope, batch)`
5) `setMonthlyBet/adjust` if `includeMonthlyAction` (enforce 1 action/day)

## Validation rules
- Validate `dayId` always; validate `monthId` iff monthly action is included.
- All arrays must have consistent lengths (ids/qty, ids/targets).
- Enforce phase gates:
  - feed/commit/reveal/draw/claim constraints remain valid even in batch.
- Stock rules:
  - No reservation. If stock changed since UI quote, tx may revert.
- Slot rules:
  - Slot compatibility checks must run before applying.

## Payment reconciliation
- Compute `totalCost` = feedCost (optional) + sum(relicCosts + fees).
- Require `msg.value >= totalCost`.
- Refund `msg.value - totalCost` to sender (safe pattern).
- Emit events as if actions were executed individually.

## Deterministic errors (frontend mapping)
Standardize revert selectors/messages:
- `INVALID_PHASE`, `INVALID_DAY`, `INVALID_MONTH`
- `INSUFFICIENT_PAYMENT`, `INSUFFICIENT_STOCK`, `INSUFFICIENT_SLOTS`
- `INVALID_ARRAY_LENGTH`, `INVALID_TARGET`, `MONTHLY_RATE_LIMIT`

## Testing checklist
- Equivalence: manual sequence vs checkout() produces same state/events.
- Insufficient payment reverts.
- Stock change reverts (no reservation).
- Slot incompatibility reverts deterministically.
- Refund correctness.
