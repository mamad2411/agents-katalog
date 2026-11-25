---
name: mobile-data
description: "Data on a phone that is often offline: a local database as the source of truth, syncing with the server (pull by cursor, push through a queue with idempotency keys), conflicts, retries and timeouts, caching, secure storage for tokens, local schema migrations, background sync limits, and large downloads. Read before building features that load, store or sync data in a mobile app."
---

# Data on a phone that is often offline

The naive mobile data layer: every screen fetches when it opens and shows a
spinner, nothing works on a train, a failed save is simply lost, a retry
creates a second order, two devices overwrite each other in silence, the
token sits in plain preferences, an update's migration wipes the local
data, and a 2 GB download restarts from zero after every dropped
connection. This skill is the design that survives real networks. Stack
details are in `mobile-ios`, `mobile-android`, `mobile-react-native` and
`mobile-flutter`; the server side of the contract in `backend-api`.

## 1. Decide how offline the app is

| Level | Works offline | Build |
|---|---|---|
| Online with a cache | Recent reads; writes need a connection | HTTP cache or a persisted query cache; clear write errors |
| Offline reads | Everything synced can be browsed; writes fail fast with Retry | A local database filled by sync |
| Offline-first | Read and write everything; sync when possible | Local database as the truth, an outbox, a conflict policy, a server change feed |

- Offline-first for apps used on the move: field work, inspections,
  delivery, notes, travel, logs.
- Some commits need the server at that moment (a payment, a booking against
  stock): keep the user's intent locally and say plainly that it is not
  done until confirmed.

## 2. The local database is what the UI reads

- The UI observes the local database (Room `Flow`, SwiftData `@Query`,
  Drift `watch()`, WatermelonDB observables, Drizzle live queries on
  expo-sqlite). Network responses are written into it; screens update from
  it, never straight from a response.

| Stack | Local store | Sync engines to consider |
|---|---|---|
| Android | Room | PowerSync, Firestore, Couchbase Lite |
| iOS | SwiftData, Core Data, GRDB | CloudKit (private data), PowerSync |
| Flutter | Drift | PowerSync, Firestore |
| React Native | expo-sqlite with Drizzle, op-sqlite, WatermelonDB | PowerSync, WatermelonDB's sync protocol |

- Realm's Atlas Device Sync reached end of life in September 2025: do not
  start on it; plan the move where it is still in use.
- Ids generated on the device (UUID v7, time-ordered, or v4), so records
  created offline have stable ids before the server sees them.
- Ordering comes from the server (a version or its timestamp), never from
  the device clock, which users and time zones change.

## 3. Pull: changes since a cursor

```
GET /sync/orders?cursor=eyJ2IjoxMjM0fQ&limit=500
200 { "changes": [{ "id": "0192…", "version": 1235, "deletedAt": null, "status": "paid" }],
      "cursor": "eyJ2IjoxMjM1fQ", "hasMore": false }
```

- The server stamps each change with an increasing version (a sequence set
  in the same transaction as the write); the cursor is opaque.
- Deletes are tombstones (`deletedAt`), kept for a set window (30 to 90
  days). A client whose cursor is older than the window does a full resync.
- Apply each page and its new cursor in one local transaction, so a crash
  never keeps one without the other. Page until `hasMore` is false.
- Pull on launch and foreground, after a push, when a push notification
  says something changed, and in background work when the OS allows.
- Sync only what the user needs (their records, recent months).

## 4. Push: an outbox with idempotency keys

- Each local write is one transaction: the row changes (marked pending) and
  an outbox row is added: entity, operation, payload, idempotency key,
  attempts, next attempt time, last error.
- One sender drains the outbox in order. The idempotency key is created
  once, when the user acted, and sent on every retry
  (`Idempotency-Key`); the server returns the stored result for a repeat.
- Success applies the server's version to the row and removes the outbox
  entry. Transient failures (offline, timeout, 5xx, 429) back off. Permanent
  ones (validation, 403, an unresolved 409) mark the item failed and show
  it to the user with fix or discard, never retried forever.
- Parents before children: a record created offline that references
  another created offline waits for it.

```ts
export async function drainOutbox(db: Db, api: Api, signal: AbortSignal) {
  for (const item of await db.outbox.due(Date.now())) {
    if (signal.aborted) return;
    try {
      const saved = await api.send(item.op, item.payload, { idempotencyKey: item.key, signal });
      await db.transaction(async (tx) => {
        await tx.records.applyServerVersion(saved);
        await tx.outbox.remove(item.id);
      });
    } catch (e) {
      if (isPermanent(e)) await db.outbox.markFailed(item.id, errorCode(e));
      else await db.outbox.reschedule(item.id, Date.now() + backoffMs(item.attempts));
      if (isOffline(e)) return; // wait for connectivity instead of failing every item
    }
  }
}
```

## 5. Conflicts

| Policy | Use for | Cost |
|---|---|---|
| Server authority: stale versions get `409` | Money, stock, bookings, anything with rules | The user reloads and redoes the change |
| Last write wins, in the server's order | One person's data across their devices, low-stakes fields | Concurrent edits are lost silently |
| Field-level merge against a base version | Profiles, forms, records several people edit | More server logic |
| CRDTs (Yjs, Automerge) | Collaborative text and lists edited offline | Complexity, growing history |

- Every update carries the base `version` it was made from; the server
  compares, applies the policy, and returns the current record on conflict.
- Tell the user when something could not sync: a visible state on the item
  ("Not synced", with Retry and Discard), never a silent drop.

## 6. Network reality

- Timeouts on every request: about 10 seconds to connect, 15 to 30 seconds
  in total for an API call, longer for uploads by size. Defaults are wrong:
  URLSession waits 60 seconds, `fetch` and Dart's `http` never time out.
- Retry only idempotent requests (GET, PUT, DELETE, and POST with an
  idempotency key), with exponential backoff and full jitter, capped:

```ts
const backoffMs = (attempt: number) => Math.random() * Math.min(60_000, 1_000 * 2 ** attempt);
```

- Honour `Retry-After` on `429` and `503`; stop after about 5 attempts in
  the foreground and leave the rest to the outbox.
- Reachability (`NWPathMonitor`, `ConnectivityManager`, NetInfo,
  connectivity_plus) is a hint: a connected network may be a captive
  portal. Always try and handle failure; use it to resume sync and show
  the offline banner.
- Fewer round trips: one sync call with many changes, pages of 50 to 500
  rows, only the fields needed, compressed responses (the platform clients
  decode gzip for you). Cancel requests when their screen leaves.
- On metered or Low Data connections (`isActiveNetworkMetered`,
  `NWPath.isConstrained`), defer large optional downloads.

## 7. Caching

- Images through the platform or library cache (Coil, Nuke, Kingfisher,
  expo-image, cached_network_image), from URLs that change when the content
  does, so caches never go stale.
- HTTP caching: `Cache-Control` and `ETag` with `If-None-Match` turn repeat
  loads into `304`s; OkHttp needs a `Cache` configured to use them.
- TanStack Query in React Native: persist the cache with a `maxAge` (24
  hours) and a `gcTime` at least as long, and resume paused mutations after
  the restore (`onSuccess={() => queryClient.resumePausedMutations()}` on
  `PersistQueryClientProvider`).
- Show cached data at once with its age ("Updated 5 min ago") and refresh
  behind it.

## 8. Secure storage

- Tokens in the Keychain or Keystore-backed storage (expo-secure-store,
  flutter_secure_storage, `mobile-ios`, `mobile-android`); never
  AsyncStorage, UserDefaults, SharedPreferences, plain SQLite, logs or
  crash reports.
- The access token short-lived and in memory; the refresh token in secure
  storage; one refresh in flight at a time.
- Sign-out clears tokens, the user's local data, caches and the outbox
  (warn first when changes are unsynced: "3 changes are not synced yet"),
  and unregisters the push token.
- Sensitive databases encrypted with SQLCipher (op-sqlite, GRDB, Room with a
  SQLCipher factory), the key in the Keychain or Keystore; iOS files with
  complete data protection.

## 9. Local schema migrations

- The schema has a version; migrations run in order from any shipped
  version to the current one. Test upgrading a real database file from
  every version still installed (Room `MigrationTestHelper`, Drift schema
  tests, SwiftData migration plans).
- Adding is cheap; renames and type changes copy through a new table. A
  destructive fallback only for caches that can be downloaded again.

```ts
const row = await db.getFirstAsync<{ user_version: number }>("PRAGMA user_version");
const current = row?.user_version ?? 0;
for (const [version, sql] of MIGRATIONS) { // [[1, "CREATE TABLE ..."], [2, "ALTER TABLE ..."]]
  if (version <= current) continue;
  await db.withTransactionAsync(async () => {
    await db.execAsync(sql);
    await db.execAsync(`PRAGMA user_version = ${version}`);
  });
}
```

- Old app versions stay installed for months: the sync API accepts them, or
  the app checks a minimum supported version at launch and shows "Update
  required".

## 10. Background sync limits

- iOS gives no guaranteed background time: app refresh runs when the system
  chooses, for about 30 seconds; silent pushes are throttled; background
  `URLSession` handles transfers.
- Android: WorkManager with a network constraint, periodic work at most
  every 15 minutes, delayed by Doze and standby buckets.
- expo-background-task and Flutter's workmanager plugin wrap the same
  schedulers, with the same limits.
- So sync on launch, on foreground, after each write and when connectivity
  returns, and show the last sync time instead of promising "always up to
  date".

## 11. Large downloads

- Resumable: HTTP range requests; a background `URLSession` with resume
  data on iOS; WorkManager (long-running, with a notification) or
  DownloadManager on Android.
- Check free space before starting (iOS
  `volumeAvailableCapacityForImportantUsage`, Android
  `StorageManager.getAllocatableBytes`); on Wi-Fi when the user prefers or
  the file is large; progress and Cancel visible.
- Download to a temporary file, verify size or checksum, then move it into
  place. Re-downloadable content goes where the system may purge it
  (Caches on iOS), or is excluded from backup.

## 12. Privacy

Keep on the device only what offline features need, and purge old data on
a schedule (90 days of history, not everything ever). Encrypt what is
sensitive, keep personal data out of logs and crash reports, and clear
everything of the previous user on sign-out.

## Check it

- Airplane mode: cold launch, browse, create, edit, delete. Back online,
  everything syncs once, with no duplicates.
- A bad network: Network Link Conditioner on iOS ("Very Bad Network"),
  `adb emu network speed gsm` and `adb emu network delay gprs` on the
  emulator, or a proxy such as Proxyman or Charles. Timeouts and retries
  behave as designed.
- Kill the app mid-sync (swipe away, `adb shell am kill`), relaunch: no
  lost writes and no doubles.
- Two devices edit the same record: the policy holds and the user is told.
- Install the previous store build, create data, install the new build
  over it: the data is intact.
- Sign out and in as another user: nothing of the first remains.

## Avoid

Screens that read straight from the network; writes lost when offline;
retries without idempotency keys; device clocks deciding conflicts;
silent overwrites; reachability treated as truth; requests without
timeouts; tokens outside secure storage; destructive migrations over user
data; promises of background sync the OS will not keep; downloads that
restart from zero.
