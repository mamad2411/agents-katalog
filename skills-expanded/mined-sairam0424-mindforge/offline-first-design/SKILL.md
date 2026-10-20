---
name: offline-first-design
version: 1.0.0
min_mindforge_version: 10.4.0
status: stable
triggers: offline-first architecture, conflict resolution sync, sync protocol design, local-first data, CRDT implementation, offline data persistence, background sync, offline queue pattern, network reconnection handling, eventual consistency mobile, offline cache strategy, optimistic offline update
---

# Skill — Offline-First Design & Sync Architecture

## When this skill activates
This skill activates when designing offline-capable mobile or web applications, including conflict resolution strategies, sync protocols, local-first data patterns, or CRDT-based collaborative features.

## Mandatory actions when this skill is active

### Before writing any code
1. Define conflict resolution strategy (last-write-wins, CRDT, operational transformation, or custom merge logic)
2. Choose local storage solution appropriate for data volume and query patterns (SQLite, Realm, WatermelonDB, IndexedDB)
3. Design sync protocol with idempotency, versioning, and resumable transfers for unreliable networks
4. Establish data model with conflict-free properties where possible (append-only logs, tombstone deletions)

### During implementation
- Implement optimistic UI updates with rollback capability — show immediate feedback, reconcile on sync
- Use operation queues with exponential backoff for failed network requests, persist queue to survive app restarts
- Store vector clocks, lamport timestamps, or hybrid logical clocks to track causality across devices
- Implement delta sync to minimize bandwidth — send only changed fields, not entire documents
- Handle edge cases: simultaneous edits on multiple devices, partial sync failures, stale read after write
- Use CRDTs (Automerge, Yjs, or custom implementations) for collaborative editing with automatic conflict resolution
- Implement sync status indicators and manual sync triggers for user transparency

### After implementation
- Test offline scenarios exhaustively: airplane mode, flaky networks, background app termination during sync
- Simulate conflict scenarios with multiple devices editing same data simultaneously
- Verify data integrity after sync — no duplicate records, no lost updates, correct conflict resolution
- Measure sync performance: time to sync after reconnection, battery impact, bandwidth usage

## Self-check before task completion
- [ ] App remains functional offline with clear UI indication of sync status
- [ ] Conflicts are resolved correctly according to business rules, with audit trail if needed
- [ ] Sync protocol is idempotent — replaying operations produces same result
- [ ] Local data persists correctly across app restarts and OS updates
- [ ] Background sync works within platform constraints (iOS background fetch, Android WorkManager)
- [ ] Edge cases handled: clock skew, partial sync, corrupted local data, schema migrations during offline period
