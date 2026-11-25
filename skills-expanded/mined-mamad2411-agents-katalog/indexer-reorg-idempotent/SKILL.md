---
name: indexer-reorg-idempotent
description: Enforce reorg-aware, idempotent indexing with stable event identity keys, replay safety, and clear optimistic vs confirmed consistency tiers. Use when touching DB writes or replay logic.
---

# Indexer Reorg + Idempotency

## When to use
- Adding/changing event handlers, DB schema, or replay/re-sync behavior.
- Any modification to how you store logs, claims, or day/month aggregates.

## Goal (Definition of Done)
- ✅ Every handler is safe to replay (idempotent).
- ✅ Reorgs do not leave “ghost” rows or double-counts.
- ✅ You can rebuild projections from raw events.

## Canonical identity keys
- Use unique keys:
  - `(txHash, logIndex)` as primary event identity (preferred)
  - or `(blockNumber, logIndex)` only if txHash is unavailable (rare)
- Store raw logs in `event_raw` (or equivalent) to support rebuilds.

## Reorg handling
- On reorg, revert projections derived from orphaned blocks.
- Prefer strategies:
  - “Ponder-managed reorg rollback” + idempotent upserts
  - or explicit “confirmed depth” tables if you separate tiers

## Consistency tiers (recommended)
- **Optimistic**: fast UX, may change on reorg.
- **Confirmed**: only after N confirmations; used for final rankings/payout history.

## Anti-patterns
- ❌ `INSERT` without unique constraints (duplicates on replay).
- ❌ Mutating aggregates without a deterministic source-of-truth event stream.
- ❌ Assuming “finality” at head block.

## Testing checklist
- Replay test: ingest same events twice → identical DB state.
- Reorg sim: orphan a block range → projections roll back correctly.
- Constraint tests: unique violation never crashes the indexer (use upsert).
