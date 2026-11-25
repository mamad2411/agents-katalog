---
name: offline-sync
description: Offline-first journaling/CRUD with React Query + Supabase + MMKV. Durable outbox pattern for creates/deletes/edits that survive airplane mode, refetch races, backgrounding, and app restart, then sync on reconnect. Use when adding offline support, or debugging entries that reappear after delete, bookmarks/edits that revert on reconnect, an offline action that spins forever, or a long loader on a no-connection cold start.
---

Build offline support so that any write a user makes without connectivity is
never lost and never visually "undone" by the server. This skill extends
[data-fetching](../data-fetching/SKILL.md) — those online patterns still apply;
this is what changes once an entry must also work offline.

## Stack

- `@tanstack/react-query` — server state + cache (persisted to disk)
- `@react-native-community/netinfo` — real connectivity signal
- `react-native-mmkv` via zustand `persist` — durable offline outboxes
- `supabase-js` — Postgres over HTTP

## The one rule that governs everything

> **Clear durable offline state only when a fresh server *read* confirms it — never on a *write's* success or failure.**

Almost every offline bug (deleted rows reappearing, bookmarks reverting, created
entries vanishing) is a violation of this rule. The reason: React Query refetches
the list in parallel with your sync (on reconnect, focus, foreground). A refetch
whose request was issued *before* your write committed can land *after* it, with
stale data, and overwrite the cache. If you cleared your pending state on the
write's success, there's nothing left to protect the UI and the change is undone.
So pending state is cleared **only** by a read that proves the server agrees.

## 1. Make React Query offline-aware (one-time setup)

Three pieces, or nothing below behaves:

```ts
// queryClient.ts
import { QueryClient, onlineManager } from '@tanstack/react-query'
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister'
import NetInfo from '@react-native-community/netinfo'
import { createMMKV } from 'react-native-mmkv'

// (a) Teach RQ real connectivity. Without this it assumes "online"
//     (navigator.onLine is absent in RN), so an offline read fails and RETRIES
//     with backoff for ~7s — a long spinner with nothing to show. Wired to
//     NetInfo, offline reads *pause* instead and resume on reconnect.
onlineManager.setEventListener((setOnline) =>
  NetInfo.addEventListener((s) => setOnline(s.isConnected === true && s.isInternetReachable !== false)),
)

const CACHE_MAX_AGE = 1000 * 60 * 60 * 24 * 7 // must outlive a realistic offline gap
export const queryClient = new QueryClient({
  defaultOptions: { queries: { gcTime: CACHE_MAX_AGE, retry: 2 } },
})

// (b) Persist the list query to disk so the last-synced data is on screen the
//     instant the app opens — even offline — instead of waiting on a network read.
const mmkv = createMMKV() // MMKV is synchronous, exactly what the sync persister needs
export const persister = createSyncStoragePersister({
  storage: {
    getItem: (k) => mmkv.getString(k) ?? null,
    setItem: (k, v) => mmkv.set(k, v),
    removeItem: (k) => mmkv.remove(k),
  },
  key: 'rq-cache',
})
```

```tsx
// app/_layout.tsx — persist ONLY the list query; leave volatile queries in-memory
<PersistQueryClientProvider
  client={queryClient}
  persistOptions={{
    persister,
    maxAge: CACHE_MAX_AGE,
    dehydrateOptions: { shouldDehydrateQuery: (q) => q.queryKey[0] === 'journal-entries' },
  }}
>
```

**(c) `networkMode: 'always'` on every mutation that handles connectivity itself.**
Any mutation that enqueues to an outbox does its offline work *inside* `mutationFn`.
The default `networkMode: 'online'` **pauses** mutations while offline, so that
code never runs → the button spins forever and nothing saves. `'always'` lets it
run regardless of network state.

## 2. Durable outboxes (persisted zustand + MMKV)

One store per operation. They survive refetch, background/foreground, and restart.

```ts
// pendingDeletions.ts — tombstones for rows deleted offline
const usePendingDeletionsStore = create<{ ids: string[]; add; remove; clear }>()(
  persist((set) => ({
    ids: [],
    add: (id) => set((s) => (s.ids.includes(id) ? {} : { ids: [id, ...s.ids] })),
    remove: (id) => set((s) => ({ ids: s.ids.filter((x) => x !== id) })),
    clear: () => set({ ids: [] }),
  }), { name: 'pending-deletions', storage: createJSONStorage(() => mmkvStorage()) }),
)
```

Create the analogous `pendingJournal` (offline-created entries, each with a
client-assigned **UUID** so the id is stable across the pending→synced
transition) and `pendingBookmarks` (`Record<id, boolean>` desired values). For
field edits use a patch map (`Record<id, Partial<Entry>>`).

## 3. Screens render pending state *over* server data

The list a screen shows is always `outbox applied on top of the cache` — so a
raced refetch can change the cache without changing what the user sees:

```ts
const serverEntries = useJournalEntries().data ?? []
const deletedIds = usePendingDeletionsStore((s) => s.ids)
const bookmarkPatches = usePendingBookmarksStore((s) => s.values)
const pending = usePendingJournalStore((s) => s.entries)

const tombstoned = new Set(deletedIds)
const visibleServer = serverEntries
  .filter((e) => !tombstoned.has(e.id))                                   // hide deleted
  .map((e) => (e.id in bookmarkPatches ? { ...e, is_bookmarked: bookmarkPatches[e.id] } : e)) // apply toggles
const serverIds = new Set(visibleServer.map((e) => e.id))
const unsynced = pending.filter((e) => !serverIds.has(e.id))             // dedupe by id
const entries = [...unsynced, ...visibleServer]                          // newer-pending on top
```

Because the flush syncs **oldest-first**, the still-pending newer entry stays on
top and order never inverts during the transition. Deduping pending vs. server by
the *same* id means a just-synced entry keeps one stable React key — no remount,
no flicker.

## 4. Mutations record the outbox; a flush does the network

```ts
const useDeleteJournalEntry = () =>
  useMutation({
    networkMode: 'always',
    mutationFn: async (id: string) => {
      usePendingDeletionsStore.getState().add(id) // durable tombstone FIRST
      await flushPendingDeletions()               // deletes now if online
    },
    onMutate: (id) => {                            // instant optimistic removal
      queryClient.setQueryData(QUERY_KEY, (old) => (old ?? []).filter((e) => e.id !== id))
    },
    // NO onError revert, NO onSettled invalidate — the tombstone is the source of
    // truth and reconcile clears it. Reverting would re-show a deleted row.
  })
```

Bookmarks/creates follow the same shape: `onMutate` records the durable value
(and mirrors it into the cache for an instant flip), `mutationFn` calls the flush.

## 5. Flushes: write, then invalidate — never clear pending state

```ts
const flushPendingDeletions = async () => {
  if (isDeleteFlushing) return                       // coalesce concurrent triggers
  const { data: { session } } = await supabase.auth.getSession() // local, works offline
  if (!session?.user) return
  if (!outboxBelongsTo(session.user.id)) return      // never sync another account's outbox (§7)

  isDeleteFlushing = true
  let wrote = false
  try {
    for (const id of [...usePendingDeletionsStore.getState().ids].reverse()) { // oldest-first
      try {
        const { error } = await supabase.from('journal_entries').delete().eq('id', id)
        if (error) throw error
        wrote = true
        // ⚠️ do NOT remove the tombstone here
      } catch (err) {
        // NEVER drop the tombstone on a failed write. Offline errors aren't always
        // classified "transient", and a reconnect can 401 for a beat before the
        // token refreshes — dropping here resurrects the row. Stop and retry.
        if (!isTransientNetworkError(err)) console.error('[sync] delete kept queued', err)
        break
      }
    }
  } finally {
    isDeleteFlushing = false
  }
  if (wrote) queryClient.invalidateQueries({ queryKey: QUERY_KEY }) // force the confirming read
}
```

## 6. Reconcile: the only place pending state is cleared (in the read path)

```ts
// inside the list queryFn, after fetching `entries` from the server:
const reconcilePendingState = (entries: Entry[]) => {
  const byId = new Map(entries.map((e) => [e.id, e]))

  // Created entry whose id is now on the server → drop the outbox copy.
  for (const e of usePendingJournalStore.getState().entries) if (byId.has(e.id)) usePendingJournalStore.getState().remove(e.id)

  // Tombstone whose row is gone → delete confirmed.
  for (const id of usePendingDeletionsStore.getState().ids) if (!byId.has(id)) usePendingDeletionsStore.getState().remove(id)

  // Bookmark whose server value already matches (or whose row is gone) → confirmed.
  for (const id of Object.keys(usePendingBookmarksStore.getState().values)) {
    const e = byId.get(id)
    if (!e || e.is_bookmarked === usePendingBookmarksStore.getState().values[id]) usePendingBookmarksStore.getState().remove(id)
  }
}
```

A stale refetch that still shows a deleted row just keeps the tombstone (row
present → not cleared); the row can only be revealed by a read that genuinely
doesn't return it. This is what makes the whole system race-proof.

Trigger the flushes on: mount (cold start with queued work), offline→online
transition (`NetInfo` listener), and app foreground (`AppState` 'active' — the
device may reconnect while backgrounded, which NetInfo won't always report).

## 7. Outbox ownership (don't lose data on token expiry, don't leak across accounts)

Supabase fires `SIGNED_OUT` both on an explicit sign-out **and** when a refresh
token expires. Wiping the outbox on `SIGNED_OUT` silently destroys a user's
unsynced writing after a long absence. Instead:

- Persist an `outboxOwnerId` (the user id that owns the queue).
- On **any** session-bearing auth event (INITIAL_SESSION, SIGNED_IN, TOKEN_REFRESHED):
  if `owner && owner !== currentUser` → clear the outboxes; then stamp the owner.
- On `SIGNED_OUT`: **preserve** the outbox (it's reconciled when a session returns).
- Guard every flush with `outboxBelongsTo(currentUser)` — closes the race where a
  flush fires mid-sign-in and would sync one user's private entries into another's
  account. Works on cold start because the owner is persisted.

## Symptom → cause → fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Long spinner on offline cold start | No cache persistence; RQ retries a failing read ~7s | Persist cache + wire `onlineManager` to NetInfo (§1) |
| Offline action's button spins forever | Mutation paused by offline manager before its enqueue code runs | `networkMode: 'always'` (§1c) |
| Deleted rows reappear after reconnect | Tombstone cleared on delete-success; a raced refetch resurrects them | Clear only in reconcile (§5, §6) |
| Bookmark/edit reverts on reconnect (or won't stick offline) | Same — value cleared on write-success/failure | Same |
| Created entry flashes then vanishes until a re-render | Dequeued on insert-success; a refetch that raced the insert drops it from cache | Keep queued until a read confirms its id (§6) |
| One user sees another's queued entries | Outbox wiped on sign-out / not keyed to an owner | Owner-keyed outbox + flush guard (§7) |
| Crash on navigation / "continue as guest" / sign-in return: "child already has a parent" | A persistent animated **offline/status banner** at the root is reparented by Fabric on the transition | Conditionally mount the banner (render `null` while online) — see the **animations** skill's Fabric gotcha |

## Optional: a network-status banner

A top strip that shows "No connection" (red, persistent) while offline and a
brief green "Back online" on reconnect is a nice reassurance layer over the
outbox. Three things that aren't obvious:

- **Conditionally mount it** — render `null` while online, not an off-screen
  mounted view. A persistent animated view at the root crashes on Fabric during
  navigation/sign-in transitions (see the **animations** skill). This also means
  the enter/exit slide only runs on a real network change.
- **Drive it off a full-state NetInfo subscriber**, not the offline→online *edge*
  subscriber you use to flush the outbox. The banner needs the current state on
  every change (`NetInfo.addEventListener` + an initial `NetInfo.fetch()`), plus
  a `wasOnline` ref so the green "Back online" only fires after a real
  disconnect (not on a normal online cold start).
- **Toasts are separate from the banner.** `burnt` (iOS) and `ToastAndroid`
  (Android) render in native windows *above* all RN views — the banner's
  `zIndex` never covers them, and vice-versa. Don't try to reconcile their
  stacking. And pin any banner label to `numberOfLines={1}`: a short strip clips
  a wrapped second line, so "Back online" can render as just "Back" under large
  font-scaling.

## Shipping it: OTA + backend compatibility

- The client offline layer uses only standard CRUD + device-local stores, so it's
  **backward/forward compatible**: old (un-updated) clients keep working, and a
  new client works against a not-yet-migrated server. Safe to OTA on its own.
- JS-only deps (`*-persist-client`, `*-persister`) **don't change the Expo
  fingerprint**, so the OTA reaches existing builds — verify with
  `expo-updates fingerprint:generate` against the channel's real device runtime
  versions before pushing.
- If you also add **server-side enforcement that reads a lookup table** (e.g. a
  free-tier limit trigger that checks an `entitlements` table), that table starts
  empty in prod → every user looks unentitled → **paying users get blocked**.
  Backfill the table (and wire whatever keeps it current) BEFORE enabling the
  enforcement, and never couple that migration with the client OTA.
