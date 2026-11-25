---
name: api-pagination-design
description: Picks cursor or offset pagination for a list endpoint, then implements stable ordering, hard limits and next links that never skip or repeat rows.
---

# API pagination design

Choose with evidence, then make paging deterministic.

## Steps

1. Read the endpoint, the table and its indexes. Note the expected size, whether rows are inserted while clients page, and whether users need to jump to page N.
2. Choose. Use cursor (keyset) pagination for feeds, logs and anything large or changing. Use offset only for small, stable lists where a page number is a real feature, and cap the maximum offset.
3. Make the order total. Sort by a column plus a unique tiebreaker, for example `ORDER BY created_at DESC, id DESC`. Without the tiebreaker, equal timestamps cause skipped rows.
4. For keyset, filter with a row comparison: `WHERE (created_at, id) < (:c, :i)`. Fetch `limit + 1` rows to learn whether a next page exists.
5. Encode the cursor as opaque base64 of the sort values. Never let clients build it.
6. Add a composite index that matches the sort and filters. Run `EXPLAIN` and show that it avoids a sort step.
7. Enforce a default and a maximum limit (for example 25 and 100). Reject larger values with a 400.
8. Return `items`, `next` (a URL or null) and, when cheap, no total. Counting millions of rows on every request is a bug.

## Rules

- Never paginate without a deterministic order.
- Never expose raw database ids or timestamps in the cursor contract.
- Tests must insert a row between page 1 and page 2 and assert no duplicates and no gaps.

## Report

The choice and why, the index added, the query plan before and after, and the response shape.
