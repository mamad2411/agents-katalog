---
name: offline-first-design
description: >
  Extends agent's knowledge of offline-first architecture for Java desktop apps.
  Use when the app must work without network, syncing to a server when available.
  Local SQLite is the source of truth; remote is a mirror.
compatibility: Java 21+
metadata:
  domain: architecture
  level: advanced
  stack: [java-21, sqlite, ebean-15, slf4j]
  version: "1.0.0"
---

# Offline-First Design

Local database is the system of record. Remote sync is asynchronous and best-effort.

## Core Principles

1. **Local-first reads** — All queries hit SQLite. Never block on network.
2. **Write locally, sync later** — Mutations write to local DB; a background sync pushes to server.
3. **Conflict resolution** — Last-write-wins with vector clocks or server-authoritative timestamps.
4. **Sync queue** — Pending operations stored in an `outbox` table; replayed on connectivity.

## Architecture

```
UI → Service → LocalRepository (SQLite/Ebean)
              ↕
         SyncService (background thread)
              ↕
         RemoteClient (HTTP/REST)
              ↕
         Outbox table (pending ops)
```

## Rules

- Every syncable entity has `localId`, `remoteId`, `updatedAt`, `syncStatus` columns.
- Sync runs on virtual threads (`Thread.ofVirtual()`) — never blocks UI.
- On conflict, prefer server timestamp; log the divergence.
- Outbox pattern: write to outbox in same transaction as entity mutation.
- Exponential backoff on sync failure; cap retries.

## See also

- service-repository-pattern — service/repo layer for local DB
- event-driven-ui — notify UI of sync state changes
