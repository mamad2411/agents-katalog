---
name: kmp-expert-room
description: Wire a Room 2.7+ database into a KMP project — module build config with per-target KSP, entities/DAOs, the expect/actual builder, and single-source-of-truth repository integration. Use whenever the user adds local persistence, an offline cache or offline-first behavior, mentions Room, entities/DAOs/@Database, KSP for Room, schema/migrations, or debugs the AGP 9 schema-export warning or a Room-vs-AGP-version issue. Applies the standard and connects it to a real consumer; does not just describe it.
---

# Skill: KMP Expert Room

This skill defines how to implement a local database using native Room for Kotlin Multiplatform, maintaining clear boundaries between database models and domain models.

## Workflow

This skill **applies** the standard. Do the steps in order; each points to the section with the full code and its warnings. Do not stop at summarizing.

1. **Module build config** (§1) — plugins, `room { schemaDirectory }`, one KSP dependency per target the project builds. Under AGP 9 the Android schema-export warning is **expected and benign** — do not downgrade `agp`/`kotlin` to silence it.
2. **Entities, DAOs, `@Database`** (§2) — `@Entity` in the data layer, DAOs exposing `Flow`, `@ConstructedBy` + the `expect object` constructor. For a full-collection sync, use `replaceAll` in a `@Transaction`, never bare `@Upsert`.
3. **Platform builders** (§3) — the `expect/actual` builder factory; `applicationContext` on Android, `NSDocumentDirectory` on iOS.
4. **Repository integration** (§4) — this is the step that is usually skipped, and skipping it leaves a database nothing reads from. Wire it as the **source of truth**: the UI observes the DB, the network only syncs into it.
5. **DI** (§5) — register the builder in the platform module so the common repository resolves the DB cleanly.
6. **Verify by running.** A green build and a passing graph test do not prove the cache works — offline behavior only shows at runtime. Drive the offline path (load online, kill, reopen in airplane mode) and confirm data still renders.

> [!NOTE]
> **Decide up front whether this database is a cache or a system of record** — it changes several later choices. A **cache** (a product catalog, reference tables) may use `fallbackToDestructiveMigration` and full replacement, and need not be cleared on logout. A **system of record** (data the user created and cannot re-fetch) needs real migrations and must never be destructively dropped. When in doubt, ask; do not default to destructive.

> [!NOTE]
> **Placement (architecture-agnostic):** entities, DAOs, and the database belong to the **data layer**; the platform database builders go in the platform source sets (`androidMain` / `iosMain`). In a **single-module** project they are packages under `commonMain`. This skill does not assume a module layout.
>
> **In a modular project (feature + layers), Room forces one exception:** `@Database` must list every entity, so it can only live where it sees them all. Entities and DAOs therefore **cannot** be distributed into their feature modules — a `:core:database` holding `@Database` cannot depend on `:features:*` without inverting the dependency. Keep entities, DAOs, and the database together in the database module, and let features depend on it and map entities to their own domain models. The trade-off is real and worth naming: a `:core` module ends up knowing each feature's persisted shape. The alternative — one database per feature — costs a separate file, connection, and migration history per feature, and is rarely worth it. See `kmp-modular-architecture`.

## Persistence Standards

1. **Entity Purity**: Room `@Entity` classes belong strictly to the data layer. They must be mapped to pure domain models before leaving the Repository.
2. **Reactive DAOs**: Prefer exposing `Flow<List<Entity>>` in DAOs to enable automatic UI updates on database changes.
3. **Multiplatform Construction**: Use `@ConstructedBy` and the `expect/actual` pattern to instantiate the database builder depending on the target platform (Android vs. iOS).
4. **Safe Migrations**: Implement clear schema migration strategies to prevent data loss.

---

## 1. Module Build Configuration

Room needs the `ksp` and `room` plugins, a schema directory, and **one KSP dependency per target the project builds**. Versions come from the catalog (`kmp-setup-base-dependencies`).

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidMultiplatformLibrary)
    alias(libs.plugins.ksp)
    alias(libs.plugins.room)
}

// Required. Applying the room plugin without this fails configuration with
// "No matching Room schema directory for the KSP target '<target>'".
room {
    schemaDirectory("$projectDir/schemas")
}

kotlin {
    androidLibrary { /* namespace, compileSdk, minSdk ... */ }
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        commonMain.dependencies {
            api(libs.room.runtime)
            implementation(libs.sqlite.bundled)
        }
    }
}

// One entry per target. Declare only the targets the project actually has —
// adding kspIosX64 to a project without an iosX64 target fails: no such configuration.
dependencies {
    add("kspAndroid", libs.room.compiler)
    add("kspIosArm64", libs.room.compiler)
    add("kspIosSimulatorArm64", libs.room.compiler)
}
```

> [!WARNING]
> **This warning is expected under AGP 9 and must not be "fixed":**
> ```
> w: [ksp] AppDatabase.kt: Schema export directory was not provided to the annotation
> processor so Room cannot export the schema...
> ```
> The Room Gradle plugin does not wire `room.schemaLocation` into the Android KSP task created by AGP 9's KMP library plugin. It is **benign**: the native targets export the schema, it is identical across targets, and code generation works. Reading it as "Room does not support AGP 9" and downgrading `agp`/`kotlin` destroys a working project to silence a cosmetic warning.
>
> **Room and KSP work with AGP 9.** The configurations exist — verify rather than assume:
> ```kotlin
> tasks.register("printKspConfigs") {
>     val names = configurations.names.filter { it.startsWith("ksp") }.sorted()
>     doLast { names.forEach { println(it) } }
> }
> // -> kspAndroid, kspIosArm64, kspIosSimulatorArm64, ...
> ```
> Do **not** migrate the module to the legacy `android { }` + `androidTarget()` pattern to obtain `kspAndroid`. It already exists.

---

## 2. Database Definition (Entities and DAOs)

### Entities and DAOs Setup (commonMain)
```kotlin
import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Dao
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Upsert
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val name: String,
    val timestamp: Long
)

@Dao
interface ItemDao {
    @Query("SELECT * FROM items")
    fun observeItems(): Flow<List<ItemEntity>>

    /**
     * Replaces the whole collection after a remote sync.
     * @Transaction makes the delete+insert atomic, so the Flow above emits once on commit
     * and the UI never renders the intermediate empty table.
     */
    @Transaction
    suspend fun replaceAll(items: List<ItemEntity>) {
        clearItems()
        upsertItems(items)
    }

    @Upsert
    suspend fun upsertItems(items: List<ItemEntity>)

    @Query("DELETE FROM items")
    suspend fun clearItems()
}
```

> [!WARNING]
> **`@Upsert` never deletes — syncing with it alone leaks records forever.** Upsert inserts and updates, so a row deleted on the server stays in the cache for the rest of the app's life: the table only ever grows, and the UI keeps showing items the backend no longer has. This never fails, never logs, and looks correct in every test that only checks that data arrives.
>
> For a **full-collection sync**, delete and re-insert inside a `@Transaction` (above). The instinct to avoid the delete — "it would blank the table mid-refresh" — is right about the risk and wrong about the fix: `@Transaction` is what removes the flash, because Room only emits after the commit.
>
> `@Upsert` on its own is correct for **incremental** writes (a single edited row), not for replacing a collection. Note that full replacement is also wrong for a **paginated** cache, where clearing page 1 would drop every other page — that case needs Paging3 + `RemoteMediator`.

### Main Database Class (commonMain)
```kotlin
import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.ConstructedBy
import androidx.room.RoomDatabaseConstructor

@Database(
    entities = [ItemEntity::class], 
    version = AppDatabase.DB_VERSION
)
@ConstructedBy(AppDatabaseConstructor::class)
abstract class AppDatabase : RoomDatabase() {

    companion object {
        const val DB_NAME = "app_db.db"
        const val DB_VERSION = 1
    }

    abstract fun itemDao(): ItemDao
}

// Expect object for Room database builder compilation (KSP generates the actual code)
@Suppress("NO_ACTUAL_FOR_EXPECT")
expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase> {
    override fun initialize(): AppDatabase
}
```

---

## 3. Platform Setup (Database Builders)

### Common Builder Configuration (commonMain)
```kotlin
import androidx.room.RoomDatabase
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO

fun getDatabase(builder: RoomDatabase.Builder<AppDatabase>): AppDatabase {
    return builder
        .setDriver(BundledSQLiteDriver())
        .setQueryCoroutineContext(Dispatchers.IO)
        .build()
}
```

### Android Builder (`androidMain`)
```kotlin
import android.content.Context
import androidx.room.Room
import androidx.room.RoomDatabase

fun getDatabaseBuilder(ctx: Context): RoomDatabase.Builder<AppDatabase> {
    val dbFile = ctx.getDatabasePath(AppDatabase.DB_NAME)
    return Room.databaseBuilder<AppDatabase>(
        context = ctx.applicationContext,
        name = dbFile.absolutePath
    )
}
```

### iOS Builder (`iosMain`)
```kotlin
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSFileManager
import platform.Foundation.NSUserDomainMask
import androidx.room.Room
import androidx.room.RoomDatabase

fun getDatabaseBuilder(): RoomDatabase.Builder<AppDatabase> {
    val dbFilePath = documentDirectory() + "/${AppDatabase.DB_NAME}"
    return Room.databaseBuilder<AppDatabase>(
        name = dbFilePath,
    )
}

@OptIn(ExperimentalForeignApi::class)
private fun documentDirectory(): String {
    val documentDirectory = NSFileManager.defaultManager.URLForDirectory(
        directory = NSDocumentDirectory,
        inDomain = NSUserDomainMask,
        appropriateForURL = null,
        create = false,
        error = null,
    )
    return requireNotNull(documentDirectory?.path)
}
```

---

## 4. Repository Integration (Single Source of Truth)

A database nothing reads from is dead weight. Wire it the moment it exists — and wire it as the **source of truth**, not as a fallback.

**The database is what the UI reads. The network only synchronizes it.** The repository exposes the two concerns separately:

```kotlin
class ProductRepositoryImpl(
    private val dataSource: ProductRemoteDataSource,
    private val productDao: ProductDao
) : ProductRepository {

    // Data: always from the database. Never fails, never reports transport state.
    override fun observeProducts(): Flow<List<Product>> =
        productDao.observeProducts().map { entities -> entities.map { it.toDomain() } }

    // Sync: writes to the database; the Flow above re-emits on its own.
    override suspend fun refreshProducts(): ResultState<Unit> = try {
        val products = dataSource.getProducts().toDomain()
        productDao.replaceAll(products.map { it.toEntity() })
        ResultState.Success(Unit)
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        e.toResultError("refresh products")
    }
}
```

Offline support is then a property of the design, not a feature to add: the Flow emits whatever is stored, and a failed refresh is reported without touching the data.

> [!WARNING]
> **Do not emit cache and network through one result stream.** The tempting shape — read the cache once, emit it, then emit the network result — looks equivalent and is not:
>
> ```kotlin
> // WRONG — cache as fallback
> emit(ResultState.Loading)
> val cached = productDao.observeProducts().first()   // a reactive Flow used as a one-shot read
> if (cached.isNotEmpty()) emit(ResultState.Success(cached.toPage()))
> try {
>     val page = dataSource.getProducts().toDomain()
>     productDao.upsertProducts(page.products.map { it.toEntity() })
>     emit(ResultState.Success(page))
> } catch (e: Exception) {
>     if (cached.isEmpty()) emit(ResultState.Error(e, ...))  // the tell-tale hack
> }
> ```
>
> `.first()` throws away Room's reactivity: a later write updates nothing. Success is emitted twice for one load. And `if (cached.isEmpty())` exists **only** because data and transport state share one channel — with the database as the source of truth that guard has nowhere to live, because a refresh error never had the power to blank the screen.

> [!NOTE]
> **Not every read belongs in the database.** Cache what is a durable, listable resource (a catalog, reference tables, history). Go straight to the network for data that must be fresh (a payment status, a balance, a session check) — staleness there is a correctness bug, not a convenience. Server-paginated lists are a third case: they need Paging3 + `RemoteMediator`, not a full-replacement cache.

> [!NOTE]
> **Clear what is scoped to the user on logout — not the whole database.** A public catalog is not the previous user's data; deleting it on logout only forces a re-download. Rows tied to an account (orders, drafts, messages) must go. Note that the skill producing the `clearX()` DAO method is not the one that owns the session lifecycle: wiring it is the job of whoever handles logout, and an unused `clearX()` is the signal that nobody did.

---

## 5. Best Practices

- **Explicit Table Names**: Always specify `tableName` inside `@Entity` to avoid issues with code refactoring or class renaming.
- **Relational Integrity**: Use `@Relation` or flatten database objects to avoid over-complicating SQL queries.
- **Bundled SQLite Driver**: Always use `BundledSQLiteDriver()` in common configurations to guarantee identical SQLite behaviors across platforms.
- **DI Integration (Koin)**: Register platform-specific builders in Koin's platform modules so that the common repository can resolve `AppDatabase` cleanly without knowledge of platform instantiation details:
  ```kotlin
  // androidMain
  actual val platformModule = module {
      single { getDatabaseBuilder(get()) }
      single { getDatabase(get()) }
  }

  // iosMain
  actual val platformModule = module {
      single { getDatabaseBuilder() }
      single { getDatabase(get()) }
  }
  ```
- **Safe Migrations**: Declare migrations in common code whenever possible. `fallbackToDestructiveMigration(dropAllTables = true)` is a deliberate choice, not a shortcut: it is correct when the database is a **cache** whose every row can be re-fetched, and destroys user data when it is not. Decide by what the database holds, never by what is faster to write.
