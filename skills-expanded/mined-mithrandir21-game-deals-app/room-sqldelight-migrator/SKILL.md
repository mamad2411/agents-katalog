---
name: room-sqldelight-migrator
description: Author and validate database migrations for Room or SQLDelight on Android/KMP — schema changes, schema export verification, paging integration, and query optimization. Use whenever the user mentions "database migration", "Room migration", "SQLDelight migration", "schema version", "schema mismatch on upgrade", "ALTER TABLE", or wants to add/change columns/tables. Also use for query performance investigation (slow queries, indexes, N+1) on the data layer.
---

# Room & SQLDelight Migrator

Database migrations are unforgiving: they run on user data in production, and a bad one corrupts everything. This skill enforces the discipline that keeps that from happening.

## When to use

Triggers: "migrate the database", "add a column", "change schema", "schema version bump", "Room migration", "SQLDelight migration", "schema mismatch on startup", "slow query", "missing index".

For initial database design, use the `network-layer-architect` complement or a fresh design discussion. This skill is for changes to a shipping database.

## Process

### Phase 1: Confirm the change is necessary

Most migrations are needed. Some aren't:

- Adding a column with a default value? Necessary.
- Renaming a column for clarity? Can it wait or happen via a view?
- Restructuring tables for a new feature? Often yes, but consider whether a new table alongside is safer than altering the existing one.

Migrations are forever — every user who installed the old schema must travel through every migration to reach the latest. The fewer, the better.

### Phase 2: Bump the version and write the migration

**Room**

```kotlin
@Database(
    entities = [User::class, Post::class],
    version = 7,                       // bumped from 6
    exportSchema = true,                // MUST be true
)
abstract class AppDatabase : RoomDatabase()
```

In `build.gradle.kts` for the module:

```kotlin
ksp { arg("room.schemaLocation", "$projectDir/schemas") }
```

The exported JSON in `schemas/AppDatabase/7.json` is your source of truth — commit it.

Write the migration:

```kotlin
val MIGRATION_6_7 = object : Migration(6, 7) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE user ADD COLUMN email TEXT NOT NULL DEFAULT ''")
    }
}

Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .addMigrations(MIGRATION_6_7)
    .build()
```

For complex migrations Room can't auto-handle (column type changes, table restructure), do it manually inside the `Migration`:

```kotlin
db.execSQL("""
    CREATE TABLE user_new (
        id INTEGER PRIMARY KEY NOT NULL,
        email TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
""")
db.execSQL("INSERT INTO user_new (id, email, created_at) SELECT id, '', timestamp FROM user")
db.execSQL("DROP TABLE user")
db.execSQL("ALTER TABLE user_new RENAME TO user")
```

**SQLDelight**

Migration files in `src/.../sqldelight/migrations/`:

```sql
-- 6.sqm
ALTER TABLE user ADD COLUMN email TEXT NOT NULL DEFAULT '';
```

(Name is `<oldVersion>.sqm`, runs to bring oldVersion → oldVersion+1.)

SQLDelight verifies schema on build; if your migration doesn't produce the new schema from the old one, the build fails. That's a feature.

### Phase 3: Test the migration

This is not optional. Migrations that aren't tested fail in production.

**Room**: `MigrationTestHelper`

```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {
    @get:Rule val helper = MigrationTestHelper(
        InstrumentationRegistry.getInstrumentation(),
        AppDatabase::class.java
    )

    @Test fun migrate6To7() {
        helper.createDatabase("test.db", 6).use { db ->
            db.execSQL("INSERT INTO user (id) VALUES (1)")
        }
        helper.runMigrationsAndValidate("test.db", 7, true, MIGRATION_6_7).use { db ->
            val c = db.query("SELECT email FROM user WHERE id = 1")
            assertTrue(c.moveToFirst())
            assertEquals("", c.getString(0))
        }
    }
}
```

**SQLDelight**: schema verification is automatic at build. Add a runtime test that opens an old-schema test DB and applies migrations, then queries the new schema.

For both: also test the **happy path** by opening at the new version directly (`fallbackToDestructiveMigration` should never be on for production builds; verify it isn't).

### Phase 4: Watch for the traps

- **`NOT NULL` without `DEFAULT`** on existing tables → migration crashes on rows that exist.
- **Renaming a primary key column** → almost always requires the table-rebuild dance.
- **Adding a foreign key with `ON DELETE CASCADE`** to an existing table → SQLite doesn't support adding constraints via `ALTER`; rebuild the table.
- **Changing column type** → rebuild the table.
- **Forgetting to bump the version** → app crashes on the next user upgrade with "database is corrupted" (it isn't, the schema just changed underneath).
- **Editing an already-shipped migration** → travelers from older versions go through different migration paths than your tests assume. Don't edit shipped migrations; add a new one.

### Phase 5: Verify in production-like conditions

- Install the previous app version, generate some data, upgrade to the new version. Confirm no data loss and no crash.
- For wide changes, ship behind a feature flag or canary release.
- Have a fallback strategy. `fallbackToDestructiveMigrationOnDowngrade()` is reasonable for downgrades during development; never for upgrades on production.

### Phase 6: Query optimization (if that's the actual problem)

If the request is "the database is slow", not "I need to migrate":

- Capture the slow query. Room: turn on query logging. SQLDelight: use `transaction { }` for batching.
- `EXPLAIN QUERY PLAN <query>` shows whether it's using indexes.
- Add indexes for columns used in `WHERE` and `ORDER BY`:
  ```kotlin
  @Entity(indices = [Index("user_id"), Index(value = ["created_at"], orders = [Index.Order.DESC])])
  ```
- N+1 problems: replace `forEach { dao.getById(it) }` with a single `IN (...)` query.
- Large result sets: paginate (Paging 3) instead of loading everything.

## Output

For a migration:

1. **Schema diff** — what changed.
2. **Migration code** — the SQL/code.
3. **Test** — the migration test that proves the data survives.
4. **Validation steps** — how to verify locally before merging.

For a perf investigation:

1. **Query** in question.
2. **Query plan** before and after.
3. **Index added** or query rewrite.
4. **Measured improvement**.

## Common pitfalls

- **`fallbackToDestructiveMigration` in production code.** Wipes user data silently on schema mismatch. Acceptable in tests, never in production.
- **No migration test.** You won't notice the failure until it's in users' hands.
- **Editing a shipped migration.** Breaks travelers from older versions. Add a new migration instead.
- **Schemas not committed to version control.** Without them, you can't review schema changes or generate auto-migrations.
- **Adding indexes blindly.** Indexes cost writes. Only add for queries that actually need them.
