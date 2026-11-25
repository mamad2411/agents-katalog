---
name: android-paging-offline-sync
description: |
  Paging and offline sync patterns for Android - Paging 3, remote mediators, paged UI state, cache-backed loading, and large dataset strategies. Use this skill whenever loading long lists, adding infinite scroll, combining Room with network pagination, or deciding how to sync large datasets efficiently. Trigger on phrases like "paging", "PagingData", "RemoteMediator", "infinite scroll", "paginated list", or "offline sync for lists".
---

# Android Paging and Offline Sync

## Core Principles

- Use paging when datasets are large enough that loading everything at once is wasteful.
- Prefer database-backed paging for offline-first or cache-aware experiences.
- Keep pagination logic in the data layer.
- UI renders paged state; it does not own page bookkeeping.
- Remote and local sources should cooperate through a clear sync strategy.

---

## When Paging Is Worth It

Good fits:
- long feeds
- search results with many items
- media catalogs
- server-driven lists with page/cursor APIs

Bad fits:
- tiny lists that always fit in memory
- static settings screens
- datasets where pagination adds complexity without benefit

---

## Recommended Architecture

For robust paging, prefer:

```text
network API <-> RemoteMediator / paging source <-> Room <-> Pager <-> ViewModel <-> Compose UI
```

This keeps Room as the source of truth while the mediator keeps data fresh.

See the **android-room-database**, **android-data-layer**, and **android-coroutines-flow** skills.

---

## Repository Contract

Expose paging from the repository/data layer, not from UI code:

```kotlin
interface NoteRepository {
    fun observePagedNotes(): Flow<PagingData<Note>>
}
```

Or expose UI-ready models from the `ViewModel` when mapping belongs there:

```kotlin
val notes: Flow<PagingData<NoteUi>> = repository
    .observePagedNotes()
    .map { pagingData -> pagingData.map { it.toNoteUi() } }
```

---

## PagingSource vs RemoteMediator

### `PagingSource`

Use when data comes from one source only, usually network or database.

### `RemoteMediator`

Use when:
- the list should be cached locally
- paging should survive process death/app restarts better
- network and Room should stay synchronized
- offline viewing matters

For many production apps, `RemoteMediator + Room` is the best long-term pattern.

---

## Room as Source of Truth

Recommended flow:
1. request next page/cursor from remote source
2. map DTOs to entities
3. store entities and remote keys in Room
4. UI observes paged Room query

This avoids UI dependence on raw network pages.

---

## Remote Keys

When server paging requires page numbers or cursors, store remote keys explicitly:
- per item when needed
- per query/list when appropriate

Guidelines:
- remote key schema should match the API pagination model
- clear keys when refreshing from scratch
- keep keys in the local database layer, not the `ViewModel`

---

## Refresh and Invalidation

Define refresh behavior intentionally:
- pull-to-refresh should invalidate and re-sync
- changing search/filter input should create a new pager/query scope
- logout/account change should clear user-scoped cached paged data when required

Do not keep stale paging caches across incompatible user/session state.

---

## Compose Integration

In Compose, collect paged data in the Root/UI boundary and render with lazy components:

```kotlin
val items = viewModel.notes.collectAsLazyPagingItems()
```

The screen should handle:
- initial loading
- append loading
- append error
- empty state
- retry actions

Keep page/request logic out of the composable itself.

---

## Error Handling

Paged UIs need clear handling for:
- initial load failure
- next page failure
- empty results
- offline cached data with refresh failure

A good offline-first paged experience may still show cached items while communicating refresh failure separately.

See the **android-error-handling** skill.

---

## Search and Filtering

For search:
- debounce input before creating new paging streams
- cancel old queries when input changes
- avoid mixing results from different queries

For filters/sorts:
- treat them as part of the paging query identity
- reset cached paging streams when query inputs meaningfully change

---

## Performance Guidance

- keep row composables lightweight
- avoid expensive mapping inside every recomposition
- let paging reduce memory pressure by loading incrementally
- use thumbnails, not full-resolution assets, in long lists

See the **android-image-loading-coil** and **android-performance-profiling** skills.

---

## Testing Guidance

Test:
- repository paging contract for expected query behavior
- remote mediator refresh/append logic
- remote key correctness
- UI handling of loading, error, and empty states
- cache clearing on session/query changes

Use fakes where possible and integration tests where mediator/database behavior is non-trivial.

---

## Checklist: Adding Paging

- [ ] Confirm the dataset is large enough to justify paging
- [ ] Keep paging logic in repository/data layer
- [ ] Prefer Room-backed paging for offline-first lists
- [ ] Store and manage remote keys explicitly when needed
- [ ] Handle initial, append, error, and empty states in UI
- [ ] Reset paging caches correctly for refresh, query, or session changes