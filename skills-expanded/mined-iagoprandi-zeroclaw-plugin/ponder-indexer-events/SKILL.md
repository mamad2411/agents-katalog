---
name: ponder-indexer-events
description: Maintain Ponder event coverage + Postgres projections for the game. Use when adding/modifying on-chain events, handler logic, schema migrations, or API alignment.
---

# Ponder Indexer Events (Coverage + Projections)

## When to use
- Contracts changed events/fields.
- You add new game mechanics requiring new projections or endpoints.

## Goal (Definition of Done)
- ✅ ABI is synced with the contracts build artifacts.
- ✅ All required events are handled and projected consistently.
- ✅ DB schema supports queries needed by the UI/API.

## Required event coverage (minimum set)
- Turn lifecycle: `DayOpened`, `DailyShopOpened`, `MonthlyCycleOpened`, `MonthlyStockEOD`
- Participation: `FeedPaid`, `DailyCommitted`, `DailyRevealed`, `MonthlyBetSet`
- Shop: `ShopDailyItem`, `ShopMonthlyItem`, `RelicBought`, `RelicApplied`, `SoldoutReached`
- Draw: `DrawRequested`, `DrawResult`
- Payout: `Claimed`, `PotRollover`, `UnclaimedPrizeMoved`
- Resources: `ResourcesEarned`, `ResourcesRedeemed`

## Projection integrity
- Use idempotent keys `(txHash, logIndex)` for every event row.
- Upsert player/day/month entities:
  - Create if missing, update if exists.
- Keep derived fields consistent (e.g., day phase/status, remaining stock, last_active_day).

## API alignment
- API responses must be explainable by DB schema + events.
- Prefer “read models” (views/materialized views) for leaderboard queries.

## Change workflow
1) Update contracts → regenerate ABI
2) Add/update Ponder handlers
3) Add DB migration (dbmate)
4) Update API types (Kysely typings)
5) Tests + replay sanity

## Testing checklist
- Handler unit test for each new/changed event.
- Replay test for duplicates.
- Reorg sanity test where feasible.
- Snapshot test for API response shape.
