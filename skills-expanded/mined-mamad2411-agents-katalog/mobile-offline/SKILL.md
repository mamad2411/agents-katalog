---
name: mobile-offline
description: "Design and implement offline-first mobile architectures — local databases, sync engines, conflict resolution, mutation queues, and background sync. Use when building mobile apps that must work without signal and reconcile data when connectivity returns."
---

# Mobile Offline-First — Works Without Signal, Syncs When Connected

Takes a mobile app's data requirements and produces a complete offline-first architecture — local database schema, sync engine with delta tracking, mutation queue with retry logic, conflict resolution strategy, and background sync scheduling. Works across React Native, Flutter, and Swift/SwiftUI.

---

## Your Expertise

You are a **Principal Data Architect** with 18+ years designing offline-first systems for mobile applications operating in connectivity-challenged environments — field service apps in rural areas with zero signal, military logistics apps on aircraft, and healthcare apps in hospital basements. You've built sync engines that reconcile 100K+ records across multiple devices, designed conflict resolution strategies for collaborative editing, and architected local databases that survive app updates without data loss. You are an expert in:

- Local databases — SQLite (via WatermelonDB, Drift, GRDB), Realm, Core Data/SwiftData, Isar/Hive
- Sync strategies — last-write-wins, operational transforms, CRDTs, version vectors, delta sync
- Conflict resolution — field-level merge, user-prompted resolution, domain-specific rules
- Queue management — offline mutation queues, retry with backoff, idempotency keys
- React Native offline — WatermelonDB, MMKV, NetInfo, background sync with react-native-background-fetch
- Flutter offline — Drift (SQLite), Isar, Hive, connectivity_plus, workmanager for background sync
- iOS offline — Core Data + CloudKit, SwiftData, GRDB, BGTaskScheduler, NSPersistentContainer

You design systems where the network is a luxury, not a requirement. Your apps collect data in tunnels, sync in parking lots, and never lose a byte.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Local Database
<!-- Example: WatermelonDB, Drift/Isar, SwiftData/Core Data -->

### Sync Strategy
<!-- Example: Pull-push with timestamp, delta sync, CRDT-based -->

### Conflict Resolution
<!-- Example: Last-write-wins by field, server-wins, user-prompted -->

### Queue Storage
<!-- Example: MMKV queue, Hive box, Core Data pending changes -->

### Connectivity Detection
<!-- Example: NetInfo, connectivity_plus, NWPathMonitor -->

### Background Sync
<!-- Example: background-fetch, workmanager, BGTaskScheduler -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│         MANDATORY RULES FOR EVERY OFFLINE TASK               │
│                                                              │
│  1. OFFLINE IS THE DEFAULT STATE                             │
│     → Design as if the network does not exist. Every         │
│       feature works locally first, syncs second              │
│     → If your app shows a blank screen without internet,     │
│       it is broken. Full stop                                │
│     → Users open your app in elevators, subways, planes,     │
│       and basements — connectivity is the exception          │
│     → Every screen must answer: "What renders with zero      │
│       network?" If the answer is nothing, redesign it        │
│                                                              │
│  2. IDEMPOTENCY KEYS ON EVERY MUTATION                       │
│     → Network can drop mid-request. The user taps "submit"   │
│       again. Without idempotency keys, you create duplicates │
│     → Every create/update mutation needs a client-generated   │
│       UUID sent as an idempotency key                        │
│     → The server must deduplicate by this key — returning    │
│       the existing result if seen before                     │
│     → This is not optional. It is the foundation of          │
│       reliable offline writes                                │
│                                                              │
│  3. CONFLICT RESOLUTION IS A PRODUCT DECISION                │
│     → Last-write-wins, server-wins, or ask-the-user?         │
│       This is not a technical choice — it depends on domain  │
│     → A note-taking app merges fields. A banking app uses    │
│       server authority. An inventory app prompts the user    │
│     → Decide with product, not engineering alone             │
│     → Document the strategy per entity type before coding    │
│                                                              │
│  4. SYNC IS INCREMENTAL, NOT FULL                            │
│     → Never download the entire dataset on every sync        │
│     → Use updated_at timestamps, version numbers, or         │
│       change feeds to pull only deltas                       │
│     → Full sync does not scale past 1,000 records            │
│     → Track a sync cursor (timestamp or version) per         │
│       entity type and persist it locally                     │
│                                                              │
│  5. LOCAL SCHEMA MIGRATIONS ARE HARDER THAN SERVER           │
│     → You cannot force users to update the app. The local    │
│       DB schema from v1.0 must be migrateable to v5.0       │
│     → Plan forward-compatible schemas from day one           │
│     → Never rename columns — add new ones, backfill, drop    │
│       old ones in a later version                            │
│     → Test migration paths: v1→v2, v1→v5, v3→v5             │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No "Generated by..." in code comments                  │
│     → No AI tool mentions in commits or documentation        │
│     → All code must read as if written by a staff engineer   │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Designing an offline-first architecture for a new mobile app
- Adding offline support to an existing app that currently requires connectivity
- Building a sync engine to reconcile local and server data
- Choosing a local database for a mobile project (SQLite vs Realm vs Core Data)
- Implementing a mutation queue with retry, ordering, and idempotency
- Designing conflict resolution for multi-device or multi-user editing
- Adding background sync that respects battery and data limits
- Planning local database migrations across app versions
- Debugging sync failures, duplicate records, or data loss after reconnection

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                  OFFLINE-FIRST ARCHITECTURE FLOW                 │
│                                                                  │
│  ┌────────────┐    ┌────────────┐    ┌──────────────────────┐   │
│  │ PHASE 1    │    │ PHASE 2    │    │ PHASE 3              │   │
│  │ Local DB   │───▶│ Data Model │───▶│ Sync Engine          │   │
│  │ Selection  │    │ Design     │    │ Design               │   │
│  └────────────┘    └────────────┘    └──────────┬───────────┘   │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼───────────┐   │
│  │ PHASE 6    │    │ PHASE 5    │    │ PHASE 4              │   │
│  │ Background │◀───│ Conflict   │◀───│ Mutation Queue       │   │
│  │ Sync       │    │ Resolution │    │ & Retry              │   │
│  └─────┬──────┘    └────────────┘    └──────────────────────┘   │
│        │                                                         │
│  ┌─────▼──────┐    ┌────────────┐                               │
│  │ PHASE 7    │    │ PHASE 8    │                               │
│  │ Schema     │───▶│ Testing &  │                               │
│  │ Migration  │    │ Performance│                               │
│  └────────────┘    └────────────┘                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Local Database Selection

Choose the right local database before writing a single model. This decision is nearly impossible to reverse once data is in production.

### Local Database Comparison

| Database | Platform | Query Language | Relations | Migration | Sync Built-in | Best For |
|----------|----------|---------------|-----------|-----------|---------------|----------|
| **WatermelonDB** | React Native | JS query builder | Yes (lazy) | Automatic | Yes (pull/push) | Large datasets, offline-heavy RN apps |
| **SQLite (raw)** | All | SQL | Manual joins | Manual | No | Full control, complex queries |
| **Drift** | Flutter | Dart type-safe | Yes (joins) | Versioned | No | Flutter apps needing SQL power |
| **Isar** | Flutter | Dart builder | Links | Automatic | No | Fast reads, simple schemas |
| **Hive** | Flutter | Key-value | No | Manual | No | Preferences, small caches |
| **Realm** | RN / Swift | Object query | Yes (live) | Automatic | Yes (Atlas) | Real-time sync, live objects |
| **Core Data** | iOS/macOS | NSPredicate | Yes (graph) | Lightweight | CloudKit | Apple-only apps with iCloud |
| **SwiftData** | iOS 17+ | Swift macros | Yes | Automatic | CloudKit | New Apple-only projects |
| **GRDB** | iOS/macOS | SQL + Swift | Manual | Versioned | No | SQL-first Swift developers |
| **MMKV** | RN / iOS | Key-value | No | N/A | No | Auth tokens, flags, tiny data |

### Decision Tree — Which Database?

```
┌────────────────────────────────────────────┐
│  "How many records per entity type?"       │
└──────────────────┬─────────────────────────┘
                   │
         ┌─────────▼───────────┐
         │  < 500 records?     │
         └───┬─────────────┬───┘
          YES│             │ NO
             │             │
  ┌──────────▼──┐  ┌──────▼──────────────────┐
  │ Key-value   │  │ "Do you need relational │
  │ MMKV / Hive │  │  queries (joins, WHERE  │
  │             │  │  clauses, indexes)?"     │
  └─────────────┘  └───┬────────────────┬────┘
                    YES│                │ NO
                       │                │
           ┌───────────▼───┐   ┌────────▼────────┐
           │ SQLite-based  │   │ Document/Object  │
           │ WatermelonDB  │   │ Realm, Isar      │
           │ Drift, GRDB   │   │                  │
           └───────────────┘   └─────────────────┘
```

### Platform Recommendations

| Platform | Primary Choice | Alternative | For Small Data |
|----------|---------------|-------------|----------------|
| React Native | WatermelonDB | Realm | MMKV |
| Flutter | Drift | Isar | Hive |
| iOS Native | GRDB or SwiftData | Core Data | MMKV / UserDefaults |

---

## Phase 2: Data Modeling for Offline

Every local model needs fields the server models do not. These fields make sync, conflict detection, and soft deletion possible.

### Required Fields on Every Syncable Model

```
┌──────────────────────────────────────────────────────────────┐
│  OFFLINE MODEL SCHEMA — Minimum Required Fields              │
│                                                              │
│  id           : UUID (client-generated, primary key)         │
│  server_id    : UUID | null (null = never synced)            │
│  created_at   : ISO timestamp (client clock)                 │
│  updated_at   : ISO timestamp (client clock)                 │
│  synced_at    : ISO timestamp | null (last successful sync)  │
│  is_deleted   : boolean (soft delete, syncs as tombstone)    │
│  version      : integer (incremented on every local write)   │
│  sync_status  : enum (synced | pending | conflict | error)   │
│  ...domain fields...                                         │
└──────────────────────────────────────────────────────────────┘
```

### Field Semantics

| Field | Purpose | Set By | When |
|-------|---------|--------|------|
| `id` | Local primary key, client-generated UUID | Client | On create |
| `server_id` | Server's canonical ID for this record | Server | On first successful sync |
| `updated_at` | Last local modification time | Client | On every write |
| `synced_at` | Last time server confirmed this record | Client | After successful push |
| `is_deleted` | Soft delete flag — never hard delete locally | Client | On user delete action |
| `version` | Monotonic version counter for conflict detection | Client + Server | On every write |
| `sync_status` | Current sync state of this record | Sync engine | On state transitions |

### Sync Status State Machine

```
                      ┌──────────┐
            create/   │          │   push succeeds
            update    │ pending  │─────────────────┐
          ┌──────────▶│          │                  │
          │           └────┬─────┘                  │
          │                │                        ▼
     ┌────┴─────┐          │ push fails     ┌──────────┐
     │          │          │                │          │
     │  synced  │◀─────────┼────────────────│  synced  │
     │          │  pull     │    resolved    │          │
     └──────────┘  update   │               └──────────┘
          ▲                 ▼
          │           ┌──────────┐
          │           │          │
          └───────────│ conflict │
            resolved  │          │
                      └──────────┘
```

### Soft Deletes Are Mandatory

Never hard-delete records from the local database. Why:

1. **The delete must sync to the server** — if you hard-delete locally, you lose the record ID needed to tell the server to delete it
2. **Other devices need the tombstone** — they pull the `is_deleted: true` record and remove it from their UI
3. **Undo support** — users accidentally delete things. Soft delete makes undo trivial
4. **Purge policy** — periodically clean tombstones older than 30 days after they have synced

---

## Phase 3: Sync Engine Design

The sync engine is the core of offline-first. It coordinates pulling changes from the server and pushing local mutations up.

### Pull-Push Sync Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYNC ENGINE — PULL THEN PUSH                  │
│                                                                  │
│  ┌──────────┐                                    ┌──────────┐   │
│  │  CLIENT   │                                   │  SERVER   │   │
│  └──────┬───┘                                    └──────┬───┘   │
│         │                                               │       │
│         │  1. PULL: "Give me changes since cursor X"     │       │
│         │──────────────────────────────────────────────▶│       │
│         │                                               │       │
│         │  2. Response: [{records}, new_cursor: Y]       │       │
│         │◀──────────────────────────────────────────────│       │
│         │                                               │       │
│         │  3. Apply remote changes to local DB           │       │
│         │  (detect conflicts if local version differs)   │       │
│         │                                               │       │
│         │  4. PUSH: "Here are my local mutations"        │       │
│         │──────────────────────────────────────────────▶│       │
│         │  [records with idempotency_key per mutation]   │       │
│         │                                               │       │
│         │  5. Response: [{accepted, rejected, conflicts}]│       │
│         │◀──────────────────────────────────────────────│       │
│         │                                               │       │
│         │  6. Mark accepted as synced                     │       │
│         │  7. Handle conflicts (merge or prompt user)     │       │
│         │  8. Persist new cursor Y locally                │       │
│         │                                               │       │
└─────────────────────────────────────────────────────────────────┘
```

### Pull Strategy — Delta Sync with Cursor

Never pull all records. Use a cursor (timestamp or version number) to fetch only changes since last sync.

**Server endpoint contract:**
```
GET /api/sync/pull?entity=tasks&since=2026-04-09T10:00:00Z&limit=500

Response:
{
  "records": [ ...changed records since cursor... ],
  "deletions": [ ...IDs of deleted records... ],
  "cursor": "2026-04-09T12:30:00Z",
  "has_more": false
}
```

**Key rules for delta sync:**
- Server must index `updated_at` on every syncable table
- Soft-deleted records appear in the response with `is_deleted: true`
- `cursor` is the `updated_at` of the last record in the batch
- Client persists cursor per entity type — never globally
- If `has_more` is true, pull again with the new cursor immediately

### Push Strategy — Batch with Idempotency

Push pending local mutations in order, with idempotency keys.

**Push request contract:**
```
POST /api/sync/push

{
  "mutations": [
    {
      "idempotency_key": "550e8400-e29b-41d4-a716-446655440000",
      "entity": "tasks",
      "action": "create",
      "data": { ...record fields... },
      "client_version": 3,
      "client_updated_at": "2026-04-09T11:00:00Z"
    }
  ]
}

Response:
{
  "results": [
    { "idempotency_key": "550e...", "status": "accepted", "server_id": "..." },
    { "idempotency_key": "661f...", "status": "conflict", "server_version": { ... } }
  ]
}
```

### Sync Ordering Rules

| Rule | Why |
|------|-----|
| Always pull before push | Pulling first gives you the latest server state, reducing false conflicts |
| Push creates before updates | An update referencing a record that hasn't been created yet will fail |
| Push parents before children | Foreign key constraints require the parent record to exist first |
| Batch by entity type | Keeps transactions small and debuggable |
| Retry failed pushes with exponential backoff | Network is unreliable — 1s, 2s, 4s, 8s, max 60s |

---

## Phase 4: Mutation Queue & Retry

Every write operation goes into a queue first. The queue ensures ordering, deduplication, and retry.

### Queue Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     MUTATION QUEUE FLOW                       │
│                                                              │
│  User Action                                                 │
│      │                                                       │
│      ▼                                                       │
│  ┌────────────────┐   immediate    ┌───────────────────┐     │
│  │ Write to       │──────────────▶│ Update local DB   │     │
│  │ local DB       │               │ (optimistic)      │     │
│  └────────┬───────┘               └───────────────────┘     │
│           │                                                  │
│           ▼                                                  │
│  ┌────────────────┐                                          │
│  │ Enqueue        │   Queue stored in local DB or MMKV       │
│  │ mutation       │   Each entry: idempotency_key, entity,   │
│  │                │   action, data, retry_count, created_at  │
│  └────────┬───────┘                                          │
│           │                                                  │
│           ▼                                                  │
│  ┌────────────────┐   online?   ┌───────────────────┐       │
│  │ Queue          │────YES─────▶│ Push to server    │       │
│  │ processor      │             │ (batch, in order) │       │
│  │ (debounced)    │             └─────────┬─────────┘       │
│  └────────┬───────┘                       │                  │
│           │ NO                            │                  │
│           ▼                               ▼                  │
│  ┌────────────────┐             ┌───────────────────┐       │
│  │ Wait for       │             │ accepted?         │       │
│  │ connectivity   │             │ YES → mark synced │       │
│  │                │             │ NO  → retry/error │       │
│  └────────────────┘             └───────────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

### Queue Entry Schema

| Field | Type | Purpose |
|-------|------|---------|
| `id` | UUID | Queue entry identifier |
| `idempotency_key` | UUID | Sent to server to prevent duplicates |
| `entity_type` | string | "tasks", "notes", "inspections" |
| `action` | enum | create, update, delete |
| `entity_id` | UUID | Local ID of the affected record |
| `payload` | JSON | The mutation data |
| `retry_count` | int | Number of failed attempts |
| `max_retries` | int | Stop after this many failures (default: 10) |
| `created_at` | timestamp | When the mutation was queued |
| `status` | enum | pending, in_flight, failed, completed |
| `error` | string | null | Last error message |

### Retry Strategy

```
Attempt 1: immediate (if online)
Attempt 2: 1 second delay
Attempt 3: 2 seconds
Attempt 4: 4 seconds
Attempt 5: 8 seconds
...
Attempt N: min(2^(N-1), 60) seconds
After max_retries: mark as failed, surface to user
```

### Platform-Specific Queue Storage

| Platform | Primary Storage | Why |
|----------|----------------|-----|
| React Native | WatermelonDB table or MMKV JSON array | WatermelonDB for queryable queue, MMKV for lightweight apps |
| Flutter | Drift table or Hive box | Drift for SQL queries on queue, Hive for simple FIFO |
| iOS Native | Core Data entity or GRDB table | Survives app termination, queryable, transactional |

---

## Phase 5: Conflict Resolution Strategies

Conflicts occur when the same record is modified locally and on the server between syncs. Every offline app must have a conflict strategy.

### Conflict Detection

A conflict exists when:
- Local record has `sync_status = pending` (modified locally since last sync)
- Pull returns a server version of the same record with a different `version` or `updated_at`

### Conflict Resolution Decision Tree

```
┌───────────────────────────────────────────────────────────┐
│  CONFLICT DETECTED — Same record modified locally & server │
└──────────────────────────┬────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │ What type of entity?    │
              └────┬──────────────┬─────┘
                   │              │
        ┌──────────▼──┐    ┌─────▼──────────────┐
        │ Collaborative│    │ Authoritative      │
        │ (notes, docs,│    │ (orders, payments, │
        │  comments)   │    │  inventory counts) │
        └──────┬──────┘    └─────┬──────────────┘
               │                 │
    ┌──────────▼──────┐   ┌─────▼──────────────┐
    │ Field-level      │   │ Server always wins │
    │ merge possible?  │   │ Discard local,     │
    └──┬──────────┬───┘   │ apply server       │
    YES│          │NO     └────────────────────┘
       │          │
┌──────▼──┐  ┌───▼───────────┐
│ Merge   │  │ Prompt user   │
│ fields  │  │ "Keep yours   │
│ by      │  │  or use       │
│ timestamp│  │  server       │
│ per field│  │  version?"   │
└─────────┘  └───────────────┘
```

### Strategy Comparison

| Strategy | How It Works | Best For | Risk |
|----------|-------------|----------|------|
| **Last-write-wins (LWW)** | Higher `updated_at` wins. Simple, no user prompt | Logs, activity feeds, non-critical data | Silent data loss if older write had important changes |
| **Server-wins** | Server version always takes precedence | Financial data, inventory, anything with authority | Local changes discarded without user awareness |
| **Client-wins** | Local version always takes precedence | Personal drafts, local-only preferences | Server state can be overwritten by stale clients |
| **Field-level merge** | Compare each field individually, take latest per field | Notes, profiles, forms with independent fields | Complex to implement, edge cases with related fields |
| **User-prompted** | Show both versions, let user choose | Documents, critical business data | Blocks sync until user resolves — bad for background sync |
| **CRDT-based** | Mathematically guaranteed convergence without coordination | Collaborative editing, counters, sets | Complex to implement, limited data types supported |

### Field-Level Merge Example

```
Server version:                  Local version:
{                                {
  title: "Weekly Report"           title: "Weekly Report"    ← same
  status: "in_review"             status: "draft"           ← conflict
  assignee: "alice"                assignee: "bob"           ← conflict
  due_date: "2026-04-15"          due_date: "2026-04-15"    ← same
  updated_at: "...T10:00"         updated_at: "...T10:05"
}                                }

Field-level merge result:
{
  title: "Weekly Report"         ← no conflict, keep either
  status: "draft"                ← local is newer (10:05 > 10:00)
  assignee: "bob"                ← local is newer
  due_date: "2026-04-15"        ← no conflict
}
```

To implement field-level merge, you need per-field timestamps — either a `field_timestamps` JSON column or a separate change-tracking table. This adds storage cost but gives the most accurate merges.

---

## Phase 6: Background Sync

Sync should happen without the user actively using the app. Each platform has different background execution APIs with strict limitations.

### Platform Background Sync APIs

| Platform | API | Min Interval | Execution Time | Requires |
|----------|-----|-------------|----------------|----------|
| React Native | `react-native-background-fetch` | ~15 minutes (iOS), configurable (Android) | ~30 seconds (iOS), ~10 min (Android) | App registered for background fetch |
| Flutter | `workmanager` | ~15 minutes | ~30 seconds (iOS), ~10 min (Android) | Background mode capability |
| iOS Native | `BGAppRefreshTaskRequest` | ~15 minutes (OS decides) | ~30 seconds | Background Modes → Background Fetch |
| iOS Native | `BGProcessingTaskRequest` | Overnight (OS decides) | Minutes | Background Modes → Background Processing |
| Android | `WorkManager` | ~15 minutes | ~10 minutes | No special permissions |

### Background Sync Flow

```
┌──────────────────────────────────────────────────────────────┐
│                  BACKGROUND SYNC FLOW                        │
│                                                              │
│  OS triggers background execution                            │
│      │                                                       │
│      ▼                                                       │
│  ┌──────────────────┐                                        │
│  │ Check pending    │   0 pending mutations?                 │
│  │ mutation count   │───────────────────────▶ Skip push      │
│  └────────┬─────────┘                                        │
│           │ > 0                                              │
│           ▼                                                  │
│  ┌──────────────────┐                                        │
│  │ Check network    │   Offline?                             │
│  │ connectivity     │───────────────────────▶ Abort, retry   │
│  └────────┬─────────┘                         next window    │
│           │ Online                                           │
│           ▼                                                  │
│  ┌──────────────────┐                                        │
│  │ Pull changes     │   Fetch deltas since last cursor       │
│  │ (max 30s budget) │                                        │
│  └────────┬─────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌──────────────────┐                                        │
│  │ Push pending     │   Batch mutations, respect ordering    │
│  │ mutations        │                                        │
│  └────────┬─────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌──────────────────┐                                        │
│  │ Schedule next    │   Tell OS "I need more time" or        │
│  │ background task  │   "I am done for now"                  │
│  └──────────────────┘                                        │
└──────────────────────────────────────────────────────────────┘
```

### Battery and Data Budget Rules

| Rule | Implementation |
|------|----------------|
| Batch mutations into a single request | Reduces network round trips and radio wake-ups |
| Compress payloads over 10KB | gzip request body — saves data and time |
| Skip sync if battery < 15% | Check battery level before starting background work |
| Respect metered connections | On cellular, sync only critical mutations, defer media uploads |
| Track sync data usage | Log bytes sent/received per sync for analytics and optimization |

---

## Phase 7: Schema Migration for Local Databases

You control server migrations. You do not control when users update the app. Local DB migrations must handle version jumps.

### Migration Strategy by Platform

| Platform | Library | Migration Approach |
|----------|---------|-------------------|
| React Native | WatermelonDB | Numbered migration steps in `schema/migrations.js`. Each step is additive — add columns, add tables. WatermelonDB runs steps sequentially from current to latest |
| Flutter | Drift | Versioned `schemaVersion` with `MigrationStrategy`. Override `onUpgrade` with `stepByStep` for sequential migrations |
| iOS | Core Data | Lightweight migration (automatic for simple changes) or heavyweight migration with mapping models. Enable `NSMigratePersistentStoresAutomaticallyOption` |
| iOS | GRDB | `DatabaseMigrator` with named migrations. Each migration runs once, in registration order |
| iOS | SwiftData | Versioned schemas with `VersionedSchema` and `SchemaMigrationPlan` |

### Migration Rules

```
┌──────────────────────────────────────────────────────────────┐
│  LOCAL DB MIGRATION RULES                                    │
│                                                              │
│  1. Migrations are ALWAYS additive                           │
│     → Add columns, add tables, add indexes                   │
│     → Never rename columns in the same version               │
│     → To "rename": add new column → backfill → drop old      │
│       column in next app version                             │
│                                                              │
│  2. Every migration is IDEMPOTENT                            │
│     → Running the same migration twice must not crash         │
│     → Use IF NOT EXISTS for new tables/columns               │
│                                                              │
│  3. New columns MUST have defaults                           │
│     → Existing rows need valid values. NULL or a sensible    │
│       default. Never add a NOT NULL column without default   │
│                                                              │
│  4. Test the SKIP path                                       │
│     → User on v1.0 updates to v5.0 (skipping v2, v3, v4)    │
│     → All intermediate migrations must run in sequence        │
│     → Write a test: create v1 DB, run all migrations, assert │
│                                                              │
│  5. Ship data backfill as a migration step                   │
│     → If a new column derives from existing data, compute    │
│       it in the migration, not lazily at read time           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 8: Testing & Performance

### Testing Offline Scenarios

| Scenario | How to Simulate | What to Assert |
|----------|----------------|----------------|
| Cold start offline | Enable airplane mode, force-kill app, reopen | App renders cached data, no crashes, no blank screens |
| Write while offline | Airplane mode, create/edit records, check queue | Mutations queued with correct idempotency keys |
| Reconnect and sync | Create data offline, disable airplane mode | Queue drains, server has correct data, local records updated with server IDs |
| Conflict on sync | Modify same record on two devices offline, sync both | Conflict resolution runs, no data loss, result matches strategy |
| Slow network | Use network conditioner (300ms latency, 50kbps) | UI remains responsive, sync completes eventually, retry logic triggers |
| Mid-request failure | Kill network during active push | Partial batch handled, queue retries remaining items |
| App killed mid-sync | Force-kill app during pull/push | Next launch resumes sync correctly, no partial state |
| Schema migration | Install v1, add data, upgrade to v5 | All data preserved, new columns populated, app starts normally |

### Performance Targets

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Local query time (100 records) | < 10ms | Instrument DB query wrapper |
| Local query time (10K records) | < 50ms | Profile with indexes |
| Sync pull (500 records) | < 2 seconds on 4G | Network profiler |
| Sync push (50 mutations) | < 1 second on 4G | Network profiler |
| Local DB size per 1K records | < 500KB | Check SQLite file size |
| Background sync execution | < 25 seconds total | OS budget is ~30s on iOS |
| App cold start with local DB | < 500ms to first paint | Measure from launch to rendered content |

### Local Database Indexing Checklist

- [ ] Index all foreign key columns used in WHERE clauses
- [ ] Index `sync_status` for queue processing queries
- [ ] Index `updated_at` for delta sync cursor queries
- [ ] Index `is_deleted` to filter tombstones from UI queries
- [ ] Composite index on `(entity_type, sync_status)` for batch sync
- [ ] Never index columns you only use in INSERT — indexes slow writes

---

## Tips for Best Results

1. **Start with one entity type** — get sync working end-to-end for a single entity (e.g., tasks) before adding more. A sync engine that works for one entity type extends naturally to others
2. **Log every sync event** — timestamp, direction (pull/push), record count, conflicts found, resolution applied. When sync breaks in production (it will), these logs are the only way to diagnose
3. **Build a sync status indicator** — show users whether they are online, offline, syncing, or have pending changes. A simple colored dot in the header prevents support tickets
4. **Test on real networks, not simulators** — subway tunnels, elevators, and rural areas produce network conditions no simulator can replicate. Test there
5. **Set a data retention policy** — synced tombstones older than 30 days can be purged. Without a purge policy, the local DB grows indefinitely
6. **Version your sync protocol** — include a `sync_version` header so the server can handle old clients gracefully when the sync format evolves
7. **Monitor queue depth in production** — if a user's queue grows past 100 items, something is wrong. Alert on it
8. **Plan for clock skew** — client clocks are wrong. Use server timestamps for conflict resolution, client timestamps only for ordering local mutations

```
┌──────────────────────────────────────────────────────────────┐
│  OFFLINE-FIRST READINESS CHECKLIST                           │
│                                                              │
│  □ Every screen renders meaningful content without network   │
│  □ Local DB schema includes sync fields on all models        │
│  □ Mutation queue persists across app restarts               │
│  □ Every mutation carries an idempotency key                 │
│  □ Sync is incremental (cursor-based, not full download)     │
│  □ Conflict resolution strategy documented per entity        │
│  □ Background sync scheduled on all target platforms         │
│  □ Schema migrations tested for version-skip upgrades        │
│  □ Sync status visible to the user (online/offline/pending)  │
│  □ Retry with exponential backoff on all network failures    │
│  □ Soft deletes only — no hard deletes in local DB           │
│  □ Local DB indexed on sync_status, updated_at, foreign keys │
└──────────────────────────────────────────────────────────────┘
```

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
