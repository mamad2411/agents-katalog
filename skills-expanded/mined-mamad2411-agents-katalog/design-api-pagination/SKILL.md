---
name: design-api-pagination
description: Designs paginated list endpoints that stay correct and fast under concurrent writes — cursor/keyset pagination over a stable total ordering with a unique tie-break key (e.g. ORDER BY created_at DESC, id DESC and WHERE (created_at,id) < (?,?)), opaque base64url-encoded cursors that bind sort+filter so they can't be tampered or reused across queries, a sane page_size default (20-50) and hard cap (100), and the {data, next_cursor, has_more} envelope (fetch limit+1 to compute has_more without a COUNT) — instead of OFFSET/LIMIT, which gets O(n) slow on deep pages and skips/duplicates rows when items are inserted or deleted mid-scan; covers REST and GraphQL Relay connections (edges/node/cursor + pageInfo.hasNextPage/endCursor), forward+backward paging, and why total counts are expensive and usually optional.
when_to_use: Building or fixing a list/feed/search endpoint that returns many rows and needs paging, an infinite-scroll or "load more" API, a stable cursor under live inserts/deletes, or migrating a slow OFFSET endpoint to keyset; or implementing a GraphQL Relay connection. Distinct from api-design-review (reviews the whole API surface/REST conventions; this owns the pagination mechanics specifically) and optimize-sql-query (builds the covering composite index that makes the keyset WHERE/ORDER BY fast; this decides the cursor/ordering contract that index must serve).
---

## When to Use

Reach for this skill when an endpoint returns a list that's too big for one response and must page through it correctly:

- "Add pagination to this list/feed/search endpoint" / "support infinite scroll / load-more"
- "Our `?page=500` query takes 8 seconds — deep OFFSET is killing us"
- "Users see duplicate or missing rows while scrolling a live feed" (rows inserted/deleted mid-scan)
- "Design the cursor — should it be opaque? what goes in it?"
- "Implement a GraphQL Relay connection (edges/pageInfo/cursors)"
- "We need stable ordering with a tie-break so pages don't shuffle"
- "Do we have to return a total count?" (usually no — it's the expensive part)

NOT this skill:
- Reviewing the whole REST/HTTP API surface — resource naming, status codes, versioning, error shape → api-design-review (this skill is only the pagination contract within it)
- Defining the serialized field types / GraphQL schema contract in general → rest-graphql-contract (this skill specifies the connection/cursor shape it slots into)
- Building the composite/covering index that makes the keyset `WHERE (a,b) < (?,?)` fast, EXPLAIN-tuning the scan → optimize-sql-query (this skill defines the ordering the index must support)
- Caching list responses / CDN / ETag for pages → caching-strategy
- Rate-limiting how many pages a client can pull → rate-limiting
- Throttling/queuing expensive list jobs → message-queue-jobs
- Designing the underlying table/keys → design-relational-schema (this skill consumes the unique key it needs as a tie-break)

## Steps

1. **Default to keyset (cursor) pagination; reach for OFFSET only for small, static, jump-to-page-N admin tables.** The two models:

   | | Offset/limit | Keyset/cursor |
   |---|---|---|
   | Query | `ORDER BY ... LIMIT 20 OFFSET 980` | `WHERE (sort_key,id) < (?,?) ORDER BY ... LIMIT 20` |
   | Deep-page cost | **O(offset)** — DB scans + discards all skipped rows | **O(1)** w/ index — seeks straight to the cursor |
   | Concurrent insert/delete | **skips or duplicates** rows (offset shifts under you) | stable — anchored to a value, not a position |
   | Jump to page N | yes | no (sequential only) |
   | Total pages | derivable (needs COUNT) | not directly |

   Offset is fine for a 200-row config table behind admin; for any feed, search, timeline, or table that grows or is written concurrently, **keyset is the default**.

2. **Pick a stable total ordering with a unique tie-break — this is the whole game.** The `ORDER BY` columns must be (a) the user-visible sort and (b) **made total** by appending a unique, immutable column (the PK) so no two rows compare equal. A non-unique sort (`ORDER BY created_at` alone) lets rows with the same timestamp straddle a page boundary → duplicates or skips.

   ```sql
   -- newest-first feed, made total by id tie-break
   ORDER BY created_at DESC, id DESC
   ```
   The cursor encodes the **full** sort tuple of the last row returned: `(created_at, id)`. Use row-value comparison so it's one index seek:
   ```sql
   WHERE (created_at, id) < (:last_created_at, :last_id)   -- DESC page
   ORDER BY created_at DESC, id DESC
   LIMIT :page_size + 1;
   ```
   For ASC use `>`. For **mixed** directions (`created_at DESC, name ASC`) row-value syntax doesn't apply — expand the boolean predicate explicitly:
   ```sql
   WHERE created_at < :c
      OR (created_at = :c AND name > :n)
      OR (created_at = :c AND name = :n AND id > :id)
   ```
   Tie-break key must be **unique and never-updated** (PK, not a mutable slug). If the sort column itself is mutable (e.g. `updated_at`), a row can move pages — acceptable for "recently updated" feeds, surprising for "newest"; document it.

3. **Make cursors opaque and self-describing — base64url-encode a small payload, never expose raw offsets/ids.** A cursor is a token the client echoes back verbatim; it is NOT a stable id and clients must not parse it. Encode the sort tuple plus enough to detect misuse:

   ```json
   { "k": [1718409600000, 84213], "d": "desc", "f": "a1b2c3" }
   // k = sort-key tuple of last row, d = direction, f = hash of filter+sort params
   ```
   `base64url(JSON)` → `eyJrIjpb...`. Rules:
   - **Opaque:** document it as "treat as opaque; do not construct or parse." Lets you change the internal format later without breaking clients.
   - **Bind the query shape:** include `f` = a hash (or the canonical filter/sort) the cursor was created under. On the next request, **reject (400) if the client changed `filter`/`sort` but reused the cursor** — a cursor is only valid against the exact query that produced it.
   - **Don't trust it for authz:** re-apply tenant/visibility filters on every page; never assume the cursor proves access. Tamper-resistance optional — sign (HMAC) only if a forged cursor could leak data past a filter; usually re-filtering server-side is enough.
   - **Cross-page consistency:** a cursor's sort tuple is independent of position, so inserts/deletes between pages don't shift it — the core win over offset.

4. **Set a page-size default and a hard cap; fetch `limit + 1` to compute `has_more` cheaply.** Never let the client ask for unbounded rows (DoS / memory blowup).

   | Param | Value |
   |---|---|
   | default `page_size` | 20–50 |
   | hard max | 100 (clamp, don't 400 — `min(requested, 100)`) |
   | `limit + 1` trick | query `page_size + 1`; if you got the extra row, `has_more = true`, drop it from `data`, its predecessor's key is `next_cursor` |

   This avoids a separate `COUNT(*)` just to know if there's a next page. Reject `page_size <= 0`.

5. **Return the `{data, next_cursor, has_more}` envelope; make `next_cursor` null at the end.** Stable, minimal contract:
   ```json
   {
     "data": [ /* page_size items */ ],
     "next_cursor": "eyJrIjpbMTcxODQw...",  // null when has_more=false
     "has_more": true
   }
   ```
   - `next_cursor` is the cursor of the **last returned row** (after dropping the `+1` probe). Client passes it back as `?cursor=...`.
   - When `has_more=false`, `next_cursor=null` and clients stop — don't make them request an empty page to discover the end.
   - **Omit total by default.** A `total_count` forces a full `COUNT(*)` (often as slow as the data scan) and is meaningless under concurrent writes. Offer it only as an opt-in (`?include_total=true`), cache it, or return an estimate (`reltuples` / approximate count).

6. **Support backward paging when the UI needs "previous" — flip comparison + order, then re-reverse.** For bidirectional cursors carry the direction in the token. To page backward from a cursor: flip `<`→`>` (and the `ORDER BY` direction), `LIMIT n+1`, then **reverse the returned slice in memory** so the client still gets ascending-by-display order. Track both `has_next` and `has_prev`. Relay's `pageInfo` (next step) formalizes this with `hasNextPage`/`hasPreviousPage` + `startCursor`/`endCursor`.

7. **For GraphQL, follow the Relay Cursor Connections spec exactly — don't invent a connection shape.** REST and GraphQL share the same keyset engine; only the envelope differs. Relay structure:
   ```graphql
   type PostConnection {
     edges: [PostEdge!]!
     pageInfo: PageInfo!
   }
   type PostEdge { node: Post!  cursor: String! }   # per-row opaque cursor
   type PageInfo {
     hasNextPage: Boolean!  hasPreviousPage: Boolean!
     startCursor: String    endCursor: String
   }
   # query args: first/after (forward), last/before (backward)
   ```
   - `first: 20, after: "<cursor>"` is forward; `last: 20, before: "<cursor>"` is backward. Each `edge.cursor` is the opaque keyset token for that node.
   - `pageInfo.endCursor` ↔ REST `next_cursor`; `hasNextPage` ↔ `has_more`. `totalCount` is a **separate, optional** field — same COUNT cost caveat (step 5).
   - Don't mix `first` with `last`, or `after` with `before`, in one request — reject it.

8. **Hand the ordering to `optimize-sql-query` and make sure a composite index covers it.** Keyset is only O(1) if a B-tree index matches the `ORDER BY` columns **in order and direction**: `CREATE INDEX ON posts (created_at DESC, id DESC)` (plus any equality filter columns as a **leading prefix**: `(tenant_id, created_at DESC, id DESC)` for a per-tenant feed). Without it the DB sorts the whole table per page and you've gained nothing. Verify with `EXPLAIN` that it's an index range scan with no `Sort` node and `Rows Removed by Filter ≈ 0`.

## Common Errors

- **OFFSET for deep pages on a growing table.** `OFFSET 100000` scans and throws away 100k rows; latency grows linearly with page depth. Fix: keyset/cursor (step 1).
- **Non-unique `ORDER BY` (no tie-break).** `ORDER BY created_at` with duplicate timestamps → rows straddle page boundaries, appear twice or vanish. Fix: append the unique PK to make ordering total (step 2).
- **Exposing a raw offset/id/timestamp as the "cursor."** Clients build their own, you can't change the format, and they construct invalid ones. Fix: opaque base64url token, documented as un-parseable (step 3).
- **Cursor not bound to the query.** Client keeps the cursor but switches `sort` or `filter` → garbage page or skipped rows. Fix: encode a filter/sort hash in the cursor and 400 on mismatch (step 3).
- **No page-size cap.** `?page_size=1000000` OOMs the server. Fix: default 20–50, clamp to max 100 (step 4).
- **Separate `COUNT(*)` on every page for `has_more`.** Doubles DB load. Fix: fetch `limit + 1` and check for the extra row (step 4).
- **Mandatory `total_count`.** Forces a full count scan, and it's wrong under concurrent writes anyway. Fix: omit by default; opt-in / cached / estimated (step 5).
- **Sorting on a mutable column without telling anyone.** Ordering by `updated_at` lets a row jump pages mid-scroll → silent dup/skip. Fix: prefer immutable sort (created_at/id); if mutable, document the behavior.
- **Missing/mismatched index.** Keyset query without a composite index matching column order+direction → full sort per page, no speedup. Fix: index the exact `(filter…, sort…, id)` tuple, verify no `Sort` in EXPLAIN (step 8).
- **Row-value comparison with mixed sort directions.** `(a,b) < (?,?)` is wrong when `a` and `b` sort opposite ways. Fix: expand to the explicit OR-chain predicate (step 2).
- **GraphQL inventing its own `{items, nextPage}` instead of Relay connections.** Breaks Relay/Apollo client cache + tooling assumptions. Fix: follow edges/node/cursor + pageInfo (step 7).
- **Off-by-one at the boundary.** Forgetting to drop the `+1` probe row leaks it into `data` and as the cursor. Fix: slice to `page_size`, derive `next_cursor` from the last *kept* row.

## Verify

1. **Deep page is fast:** request the millionth row's page; latency ≈ first page (constant), not linear. `EXPLAIN ANALYZE` shows an index range scan, no `Sort` node, near-zero rows filtered.
2. **Stable under inserts:** start paging, insert/delete rows ahead of and behind the cursor mid-scan; assert no row appears twice and no existing-before-the-cursor row is skipped (the offset failure mode).
3. **Tie-break holds:** seed many rows with identical sort values (same `created_at`); page through and assert every row appears exactly once across page boundaries.
4. **Cursor is opaque + bound:** decode shows no client-meaningful offset; reusing a cursor with a changed `filter`/`sort` returns 400, not a corrupt page.
5. **Page size enforced:** `page_size=1000000` returns ≤100; `page_size=0`/negative is rejected.
6. **End-of-list is clean:** the last page returns `has_more=false` and `next_cursor=null`; clients never need an extra empty request to detect the end.
7. **`has_more` without COUNT:** confirm the query plan fetches `limit+1` and runs no `COUNT(*)` unless `include_total` is explicitly set.
8. **Bidirectional round-trip:** page forward N then backward N lands on the original rows in the original display order (slice was re-reversed correctly).
9. **Relay conformance (GraphQL):** `first/after` and `last/before` work; `pageInfo.hasNextPage`/`endCursor` are correct; mixing `first` with `before` is rejected; `totalCount` is opt-in.

Done = list endpoints use keyset cursors over a unique-tie-break total ordering, cursors are opaque base64url tokens bound to their query, page size is defaulted and hard-capped, `has_more` comes from `limit+1` (no mandatory COUNT), the `{data,next_cursor,has_more}` (or Relay connection) envelope is stable, a composite index backs the ordering, and the consistency/perf tests in checks 1–9 pass under concurrent writes.
