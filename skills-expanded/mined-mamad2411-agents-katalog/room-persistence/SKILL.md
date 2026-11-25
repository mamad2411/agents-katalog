---
name: room-persistence
description: Project-specific Room conventions — KSP-not-kapt, `exportSchema = true` mandate, `@Upsert` over `REPLACE`, no-`fallbackToDestructiveMigration` in release, and the entity-stays-in-`data/` boundary rule. Load whenever writing or reviewing code under `data/local/`.
---

# Room (project delta)

For Room fundamentals — `@Entity`, `@Dao`, `@Query`, `@Insert`/`@Update`/`@Delete`/`@Upsert`, `@TypeConverters`, auto-migrations, `MigrationTestHelper`, in-memory DBs — read the [official Room guide](https://developer.android.com/training/data-storage/room). The canonical `AppDatabase` + `SampleEntity` + `SampleDao` + `PersistenceModule` templates live in `.claude/skills/android-app-skeleton/references/optional-room.md`. Migration mechanics are also covered by the `/add-migration` slash command. This file documents only the project's specific decisions.

## When this applies

Room with KSP. On an existing app:

- **SQLDelight** (`.sq` files) → skip; compile-time-SQL approach is a different model.
- **Realm** (`io.realm.kotlin`) → skip; object-DB semantics differ.
- **Raw SQLite** → don't migrate to Room unless asked; keep the existing access pattern.
- **Room with kapt** → flag the build-time cost when relevant; idioms below still apply.

## Setup mandates

- **KSP only** (`ksp(libs.room.compiler)`). No kapt. The reviewer rejects `kapt(libs.room.compiler)` every time.
- **`exportSchema = true`** is non-negotiable. Without it, auto-migrations don't work and CI has no schema to diff. Wire `room { schemaDirectory("$projectDir/schemas") }` in the module and **commit the `schemas/` directory** — it's the source of truth.
- Dependencies sit on a single `room` version ref in `libs.versions.toml`.

## Entity conventions

- **Column names in `snake_case`, property names in `camelCase`**. Always `@ColumnInfo(name = ...)` explicitly — don't rely on auto-derivation; the implicit mapping makes column-rename migrations harder to read.
- **Every foreign key column gets an `Index`.** Missing indexes show up as silent full-table scans at scale.
- **Timestamps as `Long` (epoch ms).** `kotlinx-datetime` `Instant` round-trips via a TypeConverter on `AppDatabase`.
- **Prefer `String` primary keys** (UUIDs) for domain identity. Auto-increment `Int` is fine for join tables only.

## TypeConverters

Register on the database (`@TypeConverters` on `@Database`), **not per-DAO**. One `AppTypeConverters` class avoids splintering and keeps converter coverage discoverable.

## DAO rules

- **`suspend`** for one-shot reads/writes.
- **`Flow<...>`** for observation. Room handles cancellation + invalidation.
- **`@Upsert` over `@Insert(onConflict = REPLACE)`.** `REPLACE` deletes-then-inserts, which cascades through foreign keys and silently drops child rows. `@Upsert` (SQLite native `UPSERT`) preserves them.
- **No `LiveData` in new DAO method signatures.** `Flow` only.
- **No mixing** `suspend fun foo(): List<T>` and `fun observeFoo(): Flow<List<T>>` for the same query — pick one per use site.

## Repository boundary (project mandate)

**Entities never leave `data/`.** The repository maps `<Feature>Entity → <Feature>` (domain) before exposing anything upward. The reviewer flags any `*Entity` import in `domain/` or `ui/` packages.

## Migrations — prefer auto, then manual

- **Auto-migrations** for schema-only changes (add column, add table, drop column, drop table). Declare with `autoMigrations = [AutoMigration(from = N, to = N+1)]`.
- **Column renames** need an `@AutoMigrationSpec` (`@RenameColumn`) — Room can't infer the rename from the diff.
- **Manual migrations** when data must transform (split columns, backfill, conditional `UPDATE`). Use `Migration(from, to) { db -> db.execSQL(...) }`.
- **Every manual migration ships with a `MigrationTestHelper` test** that loads a golden pre-migration DB from `src/androidTest/assets/databases/`. The `/add-migration` command scaffolds both the migration and the test together — use it.

**Never `fallbackToDestructiveMigration()` in release builds.** Debug-only behind a build flag; the reviewer rejects unconditional calls. Production builds with destructive-fallback enabled silently wipe user data on schema mismatch — the bug report comes in with "lost all my history" and you've already lost the data.

## Hard nos

- **No `allowMainThreadQueries()`** outside tests.
- **No `kapt`** for the Room compiler. KSP only.
- **No dropping `exportSchema`**. Even temporarily.
- **No `LiveData` DAO methods** in new code. `Flow` only.
- **No exposing entities above `data/`.** Map at the repository.
- **No `@Insert(onConflict = REPLACE)`** when `@Upsert` is available — i.e. always, on Room 2.6+.
- **No raw `SupportSQLiteDatabase` access** outside migrations.
- **No `fallbackToDestructiveMigration()`** without a `BuildConfig.DEBUG` guard.
