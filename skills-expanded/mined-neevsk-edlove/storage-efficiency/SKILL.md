---
name: storage-efficiency
description: Consolidated cross-stack storage efficiency and data-schema optimization guidance across Postgres, ZenStack, Drizzle, PowerSync, and SQLite.
---

# Storage Efficiency & Data-Schema Optimization

## Purpose
A consolidated cross-stack doctrine skill for the Polymath platform that codifies storage-efficiency and data-schema optimization guidance across the full stack: **Supabase Postgres ↔ ZenStack `.zmodel` ↔ Drizzle `AppSchema` ↔ PowerSync ↔ SQLite (SQLCipher/WASQLite) ↔ MMKV ↔ SecureStore**. Fills the confirmed gap where fragments live scattered inside `powersync`, `mmkv-guidance`, `zenstack-*`, and `supabase` with no unified home.

## Scope
This skill complements (does not replace) existing skills:
- `powersync` / `powersync-expert` — sync mechanics, `compact`, EXPLAIN
- `mmkv-guidance` — KV size/trim/compareBeforeSet
- `zenstack-*` — schema modeling, `@@index`, pagination `skip/take`
- `supabase` / `supabase-expert` — migrations, RLS
- `drizzle` — schema organization, constraints
- `expo-rn-expert` — RN performance, FlashList, sacred pins

## Doctrines (one-liner each)

### 1. Single SSOT Reconciliation Rule
> **Postgres columns ⇄ ZenStack .zmodel columns ⇄ Drizzle AppSchema columns** must match exactly for the 4 PowerSync-replicated tables (`bonds`, `school_memberships`, `classrooms`, `classroom_students`). Any drift is a bug — not a feature. For the 12 non-synced tables, annotate `local_only` explicitly; never let PowerSync queue CRUD for them.

### 2. Normalization vs. Denormalization
> **Normalize** structural relations (FKs, enums, typed JSON). **Denormalize** only frequency-cross-query counters (`member_count`, `nodes.view_count`, `endorsement_count`) via triggers or recomputation jobs; never store derived counters in the same table as the source row without a trigger.

### 3. Query Performance Boundary
> Use `EXPLAIN QUERY PLAN` as the yardstick: `SEARCH TABLE ... USING INDEX` is good; `SCAN TABLE` without covering index is a performance anti-pattern. Prefer compound `@@index` / Drizzle composite indexes on `(classroomId, date)` / `(studentId, status)` patterns. Raw Drizzle tables (no JSON wrapper) keep SQLite page-count low.

### 4. Retention & Pruning
> Define TTL per table (`ai_messages.retention_days = 90`, `mood_logs` ≥ 90d old, `group_messages` ≥ 60d old, `community_posts` ≥ 180d old). Run a **cache-eviction job** on app foreground (backed by `expo-background-task`) that (a) deletes rows beyond TTL, (b) runs `VACUUM` to reclaim SQLCipher file size. Safe defaults; dry-run/report mode first.

### 5. Compaction
> After prune, always `VACUUM` the SQLite file (SQLCipher or WASQLite). On server side, leverage PowerSync `compact` + Postgres `autovacuum` + `pg_repack` for tables that have grown beyond the high-water mark.

### 6. MMKV Hygiene
> Use `byteSize()` to surface per-account storage; `trim()` on a cadence to clear unused keys; `compareBeforeSet` to skip disk writes when value unchanged; `recoveryStrategy` (4.3.2+) for resilient falls-back. Never store structured relational data in MMKV — use SQLite; MMKV is fast KV only for preferences, draft state, feature-flag cache, localSeq counters.

### 7. Low-Device Boundary Conditions (from `local-first-architecture-principles.md`)
> Design inside the boundary conditions: a low-RAM/low-storage phone sets veto power on what upper layers can achieve. Cache eviction + VACUUM + TTL are not "nice-to-haves" — they are first-class boundary conditions, the way a building is designed inside gravity, not around it.

## Cross-Links
- **powersync** → `references/powersync-debug.md` (EXPLAIN + raw-tables), `references/powersync-cli.md` (`compact`)
- **mmkv-guidance** → `byteSize`, `trim`, `compareBeforeSet`, `recoveryStrategy`
- **zenstack-querying** → pagination `skip/take`, `@@index` / `@@unique` / `@@id`
- **zenstack-schema-modeling** → `@@index([a,b])` / `@@map` / FK/relation shape
- **supabase** → migration SSOT, RLS, column-types
- **drizzle** → `sqliteTable`, compound indexes via `(...).on(...)`
- **expo-rn-expert** → sacred pins (don't downgrade), `FlashList` for rendering, `expo-background-task` for scheduler

## Verification Discipline (AGENTS.md anti-slop)
- `check-types` / `lint` / `test` on touched packages (`core`, `schema`, `database`, `gurudevi-mobile`)
- `pnpm run stack-map:bootstrap` after any workspace-package or dependency change; review `stack-map-annotations.yaml`; then `pnpm run stack-map`
- `pnpm run check:anti-slop` — aislop + fallow gates must exit 0
- No restating comments; no dead abstractions; no duplicate utilities; no defensive noise; no happy-path-only code; no weakened tests or quality gates