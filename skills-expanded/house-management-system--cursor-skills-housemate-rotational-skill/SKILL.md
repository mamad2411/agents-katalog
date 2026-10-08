---
name: housemate-rotational
description: >-
  Implements HouseMate rotational expense types and queue algorithm per PRD
  epic 6 and section 5.1. Use for rotational CRUD, next-in-queue, and
  ROTATIONAL expenses without ExpenseSplits.
---

# Rotational Agent (Phase 2)

## Ownership

`backend/src/modules/rotational/` only.

## Requirements

- FR-6.1–6.6: Types CRUD, queue display, override warning
- FR-6.7: **No ExpenseSplits** for ROTATIONAL
- PRD 5.1: counts from latest snapshot `rotational_counts` + expenses after `snapshot.created_at`

## Algorithm

1. Load latest BalanceSnapshot for house
2. Merge rotational_counts with post-snapshot Expenses per type
3. Filter by respectsAbsence + active absence at query time
4. Min count → tiebreaker oldest expense date → joined_at for count=0

## API

GET rotational-types returns `{ ...type, nextMember, counts }`.

POST expense with mismatch → 409 with `allowOverride: true` body flag.

## Do not

- Implement split calculator or templates
- Create snapshots
