---
name: android-room-database
description: |
  Room database patterns for Android - database module boundaries, entities, DAOs, transactions, relations, migrations, converters, and offline-first persistence. Use this skill whenever adding Room entities or DAOs, changing schemas, writing queries, creating migrations, or deciding where shared database code should live. Trigger on phrases like "Room", "DAO", "entity", "migration", "type converter", "transaction", "query", "database module", or "offline-first persistence".
---

# Android Room Database

## Core Principles

- Room is the local persistence layer, not the domain model layer.
- Entities are data-layer types only; never expose them to presentation.
- DAOs should be focused and query-driven.
- Prefer Room as the single source of truth when offline-first behavior is required.
- Keep schema ownership explicit — shared DB code belongs in a core database module when multiple features use it.

---

## Recommended Module Ownership

Use a dedicated `:core:database` module when the app has a shared Room database used by multiple features:

```text
:core:database              -> RoomDatabase, entities, DAOs, migrations, converters
:core:data                  -> shared repository/data-source utilities
:feature:<name>:data        -> mappers and feature-specific data sources using DAOs
```

If only one feature uses Room and the schema is small, it can stay in that feature's `data` module until reuse justifies extraction.

See the **android-module-structure** skill for extraction rules.

---

## Entities

Entities model how data is stored locally, not how it is shown or used in domain logic:

```kotlin
@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey val id: String,
    val title: String,
    val body: String,
    val updatedAtEpochMillis: Long
)
```

Guidelines:
- keep entities flat and storage-oriented
- prefer primitive columns over nested object graphs
- store foreign keys explicitly
- use clear table names
- avoid putting computed UI formatting logic in entities

---

## DAO Design

DAOs express persistence operations and queries:

```kotlin
@Dao
interface NoteDao {
    @Query("SELECT * FROM notes ORDER BY updatedAtEpochMillis DESC")
    fun observeNotes(): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE id = :id LIMIT 1")
    suspend fun getNoteById(id: String): NoteEntity?

    @Upsert
    suspend fun upsertNotes(notes: List<NoteEntity>)

    @Query("DELETE FROM notes WHERE id = :id")
    suspend fun deleteById(id: String)
}
```

Guidelines:
- return `Flow` for observable queries
- return `suspend` for one-shot reads/writes
- keep SQL explicit and readable
- prefer `@Upsert` over custom replace logic when supported
- do not expose DAO types outside the data layer

---

## Mapping

Always map between entity and domain model in the data layer:

```kotlin
fun NoteEntity.toNote(): Note = Note(
    id = id,
    title = title,
    body = body,
    updatedAt = Instant.fromEpochMilliseconds(updatedAtEpochMillis)
)

fun Note.toNoteEntity(): NoteEntity = NoteEntity(
    id = id,
    title = title,
    body = body,
    updatedAtEpochMillis = updatedAt.toEpochMilliseconds()
)
```

Entities never cross into `domain` or `presentation`.

---

## Transactions

Use transactions when multiple DB operations must succeed or fail together:

```kotlin
@Dao
interface NoteSyncDao {
    @Transaction
    suspend fun replaceAll(notes: List<NoteEntity>) {
        deleteAll()
        upsertNotes(notes)
    }

    @Query("DELETE FROM notes")
    suspend fun deleteAll()

    @Upsert
    suspend fun upsertNotes(notes: List<NoteEntity>)
}
```

Use `@Transaction` for:
- replace-all sync flows
- parent/child inserts that must stay consistent
- multi-step writes that must be atomic

---

## Relations

Use Room relation models for storage joins, then map them to domain models:

```kotlin
data class NoteWithTagsEntity(
    @Embedded val note: NoteEntity,
    @Relation(
        parentColumn = "id",
        entityColumn = "noteId"
    )
    val tags: List<TagEntity>
)
```

Do not expose relation wrappers directly to the UI.

---

## Type Converters

Use converters for stable value objects that cannot be stored as primitives directly:

```kotlin
class InstantTypeConverter {
    @TypeConverter
    fun fromEpochMillis(value: Long?): Instant? = value?.let(Instant::fromEpochMilliseconds)

    @TypeConverter
    fun toEpochMillis(value: Instant?): Long? = value?.toEpochMilliseconds()
}
```

Prefer explicit primitive columns when possible. Do not serialize large structured objects into a single text column unless there is a strong reason.

---

## Database Definition

```kotlin
@Database(
    entities = [NoteEntity::class, TagEntity::class],
    version = 3,
    exportSchema = true,
    autoMigrations = [
        AutoMigration(from = 1, to = 2)
    ]
)
@TypeConverters(InstantTypeConverter::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
    abstract fun tagDao(): TagDao
}
```

Guidelines:
- set `exportSchema = true`
- prefer auto-migrations when possible
- add manual migrations when schema changes are too complex
- keep version bumps intentional and reviewed

---

## Migrations

Use auto-migrations first, manual migrations when needed:

```kotlin
val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE notes ADD COLUMN isPinned INTEGER NOT NULL DEFAULT 0")
    }
}
```

Every non-trivial migration should be tested.

Migration rules:
- never drop user data casually
- provide sensible defaults for new non-null columns
- backfill data if the app depends on it
- keep old-to-new paths maintainable

---

## Offline-First Pattern

Recommended flow:
1. fetch remote DTOs
2. map DTOs to entities
3. write entities to Room
4. expose DAO `Flow`
5. map entities to domain models in repository/data source

```kotlin
fun observeNotes(): Flow<List<Note>> {
    return noteDao.observeNotes().map { entities -> entities.map { it.toNote() } }
}
```

The `ViewModel` should observe Room-backed flows, not network responses directly. See the **android-data-layer** skill.

---

## Testing

What to test:
- DAO queries with realistic seed data
- migrations between released schema versions
- transaction behavior when multiple writes happen together
- repository mapping from entity to domain

Keep migration tests for every shipped version jump that still matters.

---

## Checklist: Adding Room Persistence

- [ ] Decide whether schema belongs in `feature:data` or `:core:database`
- [ ] Add entity classes and DAOs in the data/database layer
- [ ] Write entity/domain mappers in the data layer
- [ ] Use `Flow` for observable queries and `suspend` for one-shot work
- [ ] Add auto-migration or manual migration for schema changes
- [ ] Test DAO queries and non-trivial migrations