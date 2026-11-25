---
name: build-offline-first-sync
description: Designs offline-first client data layers — a local store (SQLite/Room/Core Data/WatermelonDB), a durable outbound mutation queue with idempotency keys, optimistic local writes, cursor-based delta pull, conflict resolution (last-writer-wins/vector clocks/CRDT), tombstone deletes, and reconnect reconciliation.
when_to_use: When an app must read/write while offline and reconcile with a server — choosing the local store, queuing offline mutations, pulling deltas since a cursor, resolving write conflicts. Distinct from manage-client-server-state (online cache/TanStack Query) and message-queue-jobs (server-side worker queues).
---

## When to Use

Reach for this when the client is the **source of truth while offline** and must converge with a server later, not just cache responses:

- "App has to work in airplane mode and sync when it reconnects"
- "Pick a local store — SQLite vs Room vs Core Data vs WatermelonDB"
- "Queue writes made offline and replay them in order without dupes"
- "Two devices edited the same row offline — who wins?"
- "Pull only what changed since last sync instead of refetching everything"
- "Deletes keep coming back after sync" (missing tombstones)
- "Optimistic edit, then roll back if the server rejects it"

NOT this skill:
- Online data fetching / cache invalidation with a live connection (TanStack/React Query, hydration, refetch) → manage-client-server-state
- The **server-side** worker that processes the sync queue (consumers, DLQ, exactly-once on the backend) → message-queue-jobs
- The shape of the sync API itself (REST vs GraphQL, pagination params, error envelopes) → rest-graphql-contract
- Changing the **server** schema the deltas come from (DDL locks, rollback) → db-migration-safety
- Identifying who the syncing user is / token refresh on reconnect → auth-jwt-session

## Steps

1. **Pick the local store by platform + reactivity need — don't reach for raw SQLite by reflex.**

   | Store | Best when | Reactive queries | Migrations |
   |---|---|---|---|
   | **SQLite** (SQLDelight/Drift/expo-sqlite) | Cross-platform, you want real SQL + full control | Manual (triggers/`PRAGMA data_version`) or lib-provided | Hand-written `user_version` steps |
   | Room (Android) | Native Android, Kotlin/Flow | `Flow`/`LiveData` built-in | `Migration` objects, `fallbackToDestructive` = data loss, avoid |
   | Core Data / SwiftData (Apple) | Native iOS, object graph + iCloud | `@FetchRequest`/`NSFetchedResultsController` | Lightweight (auto) vs mapping model |
   | **WatermelonDB** (RN) | React Native, large datasets, lazy reads | Observables out of the box | `schemaMigrations` versioned |
   | Realm/MongoDB Atlas Device Sync | You want sync *built in* and accept the lock-in | Live objects | Schema-versioned |

   Default: **SQLite via a typed wrapper** (SQLDelight/Drift) for cross-platform; **WatermelonDB** for React Native with thousands of rows; native (Room/Core Data) only if single-platform. Avoid building your own sync on Realm Device Sync unless you adopt their whole model.

2. **Add sync bookkeeping columns to every syncable table.** The on-device schema is the server schema **plus** local metadata:

   ```sql
   CREATE TABLE task (
     id            TEXT PRIMARY KEY,        -- client-generated UUIDv7 (sortable), NOT server autoincrement
     title         TEXT NOT NULL,
     updated_at    INTEGER NOT NULL,        -- server-assigned ms epoch on last sync (the LWW clock)
     version       INTEGER NOT NULL DEFAULT 0, -- server row version for optimistic concurrency
     deleted_at    INTEGER,                 -- tombstone; NULL = live
     sync_status   TEXT NOT NULL DEFAULT 'synced'  -- synced | pending | conflict
   );
   ```
   Generate IDs **on the client** (UUIDv7/ULID) so offline-created rows have a stable PK and FKs link before they ever reach the server — never depend on a server autoincrement id you don't have yet.

3. **Reads are local-first and reactive — the UI never awaits the network.** Every screen queries the local store and observes it (`Flow`, WatermelonDB observables, `NSFetchedResultsController`, or a SQLite change-notify). Filter out tombstones (`WHERE deleted_at IS NULL`) in the read layer, not the UI. Network sync mutates the local store; the reactive query repaints. Surface freshness from a `last_synced_at` you store per-collection, not per-render guesses.

4. **Writes go optimistic + into a durable outbox in one transaction.** Apply the change to the domain table **and** append an op to `outbox` atomically, so a crash can't lose one without the other:

   ```sql
   CREATE TABLE outbox (
     op_id        TEXT PRIMARY KEY,    -- idempotency key, client UUID, sent as Idempotency-Key header
     entity       TEXT NOT NULL,
     entity_id    TEXT NOT NULL,
     op           TEXT NOT NULL,       -- insert | update | delete
     payload      TEXT NOT NULL,       -- JSON of changed fields (delta, not whole row)
     base_version INTEGER NOT NULL,    -- server version the edit was based on (0 for an offline insert; for conflict detection)
     created_at   INTEGER NOT NULL,
     attempts     INTEGER NOT NULL DEFAULT 0
   );
   ```
   Set the row's `sync_status='pending'`. **Coalesce** repeated edits to the same `entity_id` before send (collapse 5 title edits into the latest) so the queue doesn't replay every keystroke. A delete is an op with `op='delete'` that sets `deleted_at` locally — never `DELETE FROM` until the server confirms the tombstone.

5. **Sync engine = push-then-pull, both idempotent, with bounded backoff.** Run on connectivity-gain and on an interval:
   1. **Push:** drain `outbox` oldest-first, `Idempotency-Key: {op_id}`. On `2xx`, apply the server's returned `{version, updated_at}` to the row, set `synced`, delete the op. On `409 Conflict`, go to step 6. On `5xx`/timeout, leave the op, bump `attempts`, retry with exponential backoff + jitter (`min(2^attempts * base, 60s)`).
   2. **Pull:** `GET /sync?since={cursor}&limit=500`, where `cursor` is the **server-issued** opaque cursor (or `updated_at` high-watermark) from the last successful pull. Apply each changed/deleted row, then persist the new `cursor` **only after** the whole page is committed. Page until `has_more=false`. Pull **after** push so the server already reflects your writes and you don't fight your own optimistic state.

   Never pull before push, never advance the cursor mid-page, and order by `(updated_at, id)` server-side so pagination is stable under concurrent writes.

6. **Resolve conflicts deterministically — pick a strategy per entity, don't mix silently.**

   | Strategy | Use when | Mechanism | Cost |
   |---|---|---|---|
   | **Last-Writer-Wins** | Independent scalar fields, low contention (default) | Compare `updated_at`; higher wins | trivial, can lose a field |
   | Version / optimistic concurrency | Need to *detect* and merge, not silently drop | Server rejects with `409` if `base_version` ≠ current; client re-reads + replays | a round-trip per conflict |
   | Vector clocks | Multi-device causal ordering matters | Per-replica counters; detect concurrent vs causal | bookkeeping per row |
   | **CRDT** (Yjs/Automerge) | Collaborative text/lists, must merge without loss | Mergeable types converge automatically | larger payloads, library |

   Default **field-level LWW** for most records; escalate to **CRDT only** for collaborative documents/lists. On `409`, the server returns the current row + version: re-base the pending op onto it (re-apply the user's delta to the latest server state), bump `base_version`, re-queue. If a field truly diverges, mark `sync_status='conflict'` and surface it — never drop a user's write without a trace.

7. **Reconnect & reconciliation.** Detect connectivity transitions (`NWPathMonitor` / `ConnectivityManager` / `@react-native-community/netinfo`) — treat reachability as "maybe", confirm with the first real request, don't trust the radio flag alone. On reconnect: push outbox → pull deltas → clear stale `pending` that the server now confirms. Cap `attempts`; an op that exceeds the cap (e.g. permanent `400`/`422`) moves to a **client-side dead-letter / `conflict`** state and is surfaced to the user — it must not block the rest of the queue (head-of-line blocking).

8. **Integrity: make partial sync recoverable.** Persist the cursor only after a page fully commits, so a crash mid-pull re-fetches that page (idempotent apply makes re-fetch safe). Dedupe on apply by `(id)` + `version` — ignore an incoming row whose `version` ≤ local. Negotiate schema with a `schema_version` in the sync request; on mismatch the server returns `426 Upgrade Required` and the client forces an app update rather than corrupting data. Run local migrations (`user_version` / `schemaMigrations`) **before** the first sync after an app upgrade.

## Common Errors

- **Server-autoincrement PKs for offline-created rows.** You can't link FKs or reference the row until the server replies. Generate UUIDv7/ULID on the client; keep that id forever.
- **Hard-deleting locally instead of tombstoning.** The next pull from another device re-creates the row (it never saw the delete). Set `deleted_at`, sync the tombstone, GC tombstones only after all clients have pulled past them.
- **Advancing the sync cursor before the page is committed.** A crash mid-apply skips rows permanently — silent data loss. Commit the page, *then* persist the cursor.
- **No idempotency key on push.** A retried op after a timeout (where the server actually succeeded) double-applies — duplicate rows / double charges. `Idempotency-Key: {op_id}`, server dedupes.
- **Replaying every keystroke from the outbox.** 200 ops to sync one note. Coalesce ops per `entity_id` before push.
- **Pull before push.** The server hasn't seen your local edits yet, so the delta overwrites your optimistic state and the UI flickers back. Always push first.
- **Trusting the OS "connected" flag.** Captive portals and dead Wi-Fi report "connected". Confirm with an actual lightweight request before draining the queue.
- **Unbounded retries on a permanent `4xx`.** A `422` op retries forever and head-of-line-blocks every later op. Cap attempts; dead-letter the poison op; keep draining the rest.
- **Last-Writer-Wins on a whole row.** One device edits `title`, another edits `due_date`; whole-row LWW silently drops one field. Do **field-level** LWW or merge.
- **Ignoring clock skew in LWW.** Client clocks lie. Use the **server-assigned** `updated_at` as the LWW clock, not the device clock.
- **Migrating local schema after the first sync.** Incoming rows don't fit the old schema → crash or silent drop. Migrate on app start, before sync runs.

## Verify

1. **Airplane-mode write survives restart:** Go offline, create + edit + delete records, force-quit and relaunch → all local changes still present, `outbox` intact, `sync_status='pending'`.
2. **Reconnect drains correctly:** Re-enable network → outbox empties, every op acked, rows flip to `synced`, server reflects every offline change exactly once (no dupes — proves idempotency keys work).
3. **Delta pull is incremental:** Trigger a remote change, sync → only the changed rows transfer (inspect request: `since={cursor}` with a non-empty cursor, response page << full table). A second sync with no remote changes transfers zero rows.
4. **Conflict resolves deterministically:** Two clients edit the same row offline, both reconnect → result matches the documented strategy (field-level LWW = each field = latest server `updated_at`; CRDT = both edits merged), and no write vanishes silently — divergence shows as `conflict`.
5. **Tombstone delete stays deleted:** Delete on device A, sync; device B syncs → row disappears on B and does **not** resurrect on A's next pull.
6. **Flaky network / mid-sync kill:** Throttle to 2G + 30% packet loss (Network Link Conditioner / Charles), kill the app mid-pull → relaunch re-fetches the uncommitted page, converges, no duplicate or missing rows; cursor never advanced past uncommitted data.
7. **Poison op doesn't block the queue:** Inject an op the server rejects with `422` → it dead-letters after the attempt cap and surfaces to the user; every other queued op still syncs.
8. **Schema-version mismatch is safe:** Point an old client at a newer server → `426`/upgrade path, not a corrupt write or crash.

Done = a record created **offline** survives an app restart, syncs **exactly once** on reconnect, incremental pull transfers only deltas since the cursor, concurrent edits resolve per the documented strategy with **no silent data loss**, deletes stay deleted, and a mid-sync kill under a flaky network converges with no duplicate or missing rows.
