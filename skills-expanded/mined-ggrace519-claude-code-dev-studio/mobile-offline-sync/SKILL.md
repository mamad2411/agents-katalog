---
name: mobile-offline-sync
description: Offline storage, sync, and conflict-resolution specialist for mobile. Auto-invoked when local persistence (SQLite, Core Data, Room), sync engines, background sync, or conflict resolution is being built.
---

# Mobile Offline Sync

The app must work on the subway and reconcile correctly when it comes back
online. Sync bugs corrupt user data — the one class of mobile bug an update
cannot retroactively fix.

## When to reach for this

- Designing local persistence (SQLite, Core Data, Room, Realm) that syncs with a server
- Building or reviewing a sync engine: push/pull direction, cursors, batching
- Choosing a conflict-resolution policy, or debugging lost/duplicated edits
- On-device schema migrations, background sync scheduling, large-blob transfer

## Principles

1. **Local-first, sync-after.** The UI reads and writes the local DB only; sync
   is a background reconciler. Spinners waiting on the network are a design smell.
2. **Outbox with client-generated stable IDs.** Offline writes go to a durable
   queue keyed by client UUIDs; server-assigned IDs break offline creation and
   make retries un-dedupable.
3. **Dedupe at every step.** Retries *will* duplicate deliveries. Every push is
   idempotent on the outbox entry ID; every pull upserts, never blind-inserts.
4. **Resume from a cursor, never re-sync the world.** Pull with a server-issued
   cursor/changestamp; a full resync is a recovery path, not the protocol.
5. **Migrations are forward-and-back.** Users roll between app versions; the
   schema (and any queued outbox payloads) must survive both directions.
6. **Backpressure on blobs.** Metadata syncs eagerly; images/video upload on
   unmetered networks by default and download resumably — never block record
   sync behind a 50 MB upload.
7. **Conflict is a product decision.** Pick a policy per entity type explicitly
   (table below) and write it down; "whatever the DB does" is how edits vanish.
8. **Schedule sync with the OS, not timers.** WorkManager with constraints on
   Android; `BGAppRefreshTask` (short, ~30 s budget) / `BGProcessingTask` on
   iOS. Hand-rolled background loops get killed and drain battery.

## Conflict-resolution decision table

| Entity shape | Policy | Why |
|---|---|---|
| Single-owner record (settings, drafts) | last-write-wins on a server timestamp | conflicts are self-conflicts; latest intent wins |
| Independent fields on one record | per-field LWW (merge field-wise) | two devices editing different fields shouldn't clobber each other |
| Collaborative text / ordered lists | CRDT or OT library — don't hand-roll | character-level merge is a research problem, not a sprint task |
| Money, inventory, counters | server-authoritative; client sends *operations* (`+1`), not states (`=5`) | replayed state writes corrupt totals |
| True business conflict (double-booking) | surface to the user | silently picking a side is data loss with extra steps |

Adversarial tests that must exist: kill the app mid-sync, replay the same outbox
batch twice, edit the same record on two offline devices, downgrade the app with
a non-empty outbox, sync 10k changes on a flaky connection.

## Pitfalls

- Tombstones missing — deletes never propagate, "deleted" items resurrect on next pull
- Clock skew breaking LWW: order by server-issued timestamps/versions, never device clocks
- Outbox retried without backoff + jitter, DDoSing your own API when connectivity returns
- Sync state machine entangled with UI state — sync must run headless (background task, no activity/view alive)
- Treating `Reachability`/`ConnectivityManager` "online" as truth; the only real
  connectivity test is the request succeeding

---
*Related: `mobile-perf` (sync work off the main thread), `mobile-platform`
(background execution limits), `mobile-crash` (mid-sync crash recovery) ·
domain agent: `mobile-architect` (offline posture) · output/ADR format:
`playbook-conventions`*
