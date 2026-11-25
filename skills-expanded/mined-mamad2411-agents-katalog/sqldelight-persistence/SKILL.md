---
name: sqldelight-persistence
description: SQLDelight patterns for this KMP project — `.sq` schema files, typed queries, platform drivers, migrations with verification, Flow wrappers, coroutines integration. Load whenever working in `shared/src/commonMain/sqldelight/` or the `data/local/` layer.
---

# SQLDelight persistence

## Why SQLDelight

Type-safe SQL that generates Kotlin interfaces from `.sq` files. Compared to Room:
- **Multiplatform**: Android, iOS, desktop, JS — single source of truth.
- **Compile-time checked SQL**, not runtime-only.
- **No KSP/kapt on common**; generation is a Gradle task.

Trade-off: you write SQL. That's the point.

## Gradle

```kotlin
// shared/build.gradle.kts
plugins {
    alias(libs.plugins.sqldelight)
}

sqldelight {
    databases {
        create("AppDatabase") {
            packageName.set("com.example.shared.db")
            schemaOutputDirectory.set(file("src/commonMain/sqldelight/databases"))
            verifyMigrations.set(true)
        }
    }
}

kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(libs.sqldelight.coroutines.extensions)
        }
        androidMain.dependencies {
            implementation(libs.sqldelight.android.driver)
        }
        iosMain.dependencies {
            implementation(libs.sqldelight.native.driver)
        }
    }
}
```

`verifyMigrations = true` makes schema diffs a build-time error when a migration is missing.

## Schema files

`shared/src/commonMain/sqldelight/com/example/shared/db/Order.sq`:

```sql
CREATE TABLE Orders (
    id TEXT NOT NULL PRIMARY KEY,
    customer_id TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE INDEX orders_customer_id ON Orders(customer_id);
CREATE INDEX orders_created_at ON Orders(created_at DESC);

selectById:
SELECT * FROM Orders WHERE id = :id;

selectByCustomer:
SELECT * FROM Orders
WHERE customer_id = :customerId
ORDER BY created_at DESC;

upsert:
INSERT INTO Orders (id, customer_id, total_cents, status, created_at)
VALUES (:id, :customerId, :totalCents, :status, :createdAt)
ON CONFLICT(id) DO UPDATE SET
    customer_id = excluded.customer_id,
    total_cents = excluded.total_cents,
    status = excluded.status,
    created_at = excluded.created_at;

deleteById:
DELETE FROM Orders WHERE id = :id;
```

Generated Kotlin:

```kotlin
public data class Orders(
    public val id: String,
    public val customer_id: String,
    public val total_cents: Long,
    public val status: String,
    public val created_at: Long,
)

public interface OrderQueries : Transacter {
    public fun selectById(id: String): Query<Orders>
    public fun selectByCustomer(customerId: String): Query<Orders>
    public fun upsert(...)
    public fun deleteById(id: String): Unit
}
```

## Platform drivers

Expose via Koin / explicit factory:

```kotlin
// shared/src/androidMain/kotlin/.../DriverFactory.kt
actual class DriverFactory(private val context: Context) {
    actual fun create(): SqlDriver = AndroidSqliteDriver(AppDatabase.Schema, context, "app.db")
}

// shared/src/iosMain/kotlin/.../DriverFactory.kt
actual class DriverFactory {
    actual fun create(): SqlDriver = NativeSqliteDriver(AppDatabase.Schema, "app.db")
}

// shared/src/commonMain/kotlin/.../DriverFactory.kt
expect class DriverFactory {
    fun create(): SqlDriver
}
```

Hook into Koin:

```kotlin
val dbModule = module {
    single { get<DriverFactory>().create() }
    single { AppDatabase(get()) }
    single { get<AppDatabase>().orderQueries }
}
```

## Repository wrapping

Presentation never sees `OrderQueries`. Wrap it:

```kotlin
class OrderRepositoryImpl(
    private val queries: OrderQueries,
    private val dispatcher: CoroutineDispatcher,
) : OrderRepository {
    override fun observeByCustomer(customerId: String): Flow<List<Order>> =
        queries.selectByCustomer(customerId)
            .asFlow()
            .mapToList(dispatcher)
            .map { rows -> rows.map(Orders::toDomain) }

    override suspend fun save(order: Order) = withContext(dispatcher) {
        queries.upsert(
            id = order.id,
            customerId = order.customerId,
            totalCents = order.totalCents,
            status = order.status.name,
            createdAt = order.createdAt.toEpochMilliseconds(),
        )
    }
}
```

- `.asFlow().mapToList(...)` from `sqldelight-coroutines-extensions` emits on each table change.
- Map row types to domain entities at this layer; domain doesn't import `com.example.shared.db`.

## Transactions

Use `transaction { ... }` for multi-statement atomicity:

```kotlin
queries.transaction {
    afterRollback { logger.w("Rolled back") }
    queries.upsert(...)
    queries.deleteById(...)
}
```

Read within a transaction: `transactionWithResult { ... }`.

## Migrations

Bump `schema` version in your database:

```sql
-- shared/src/commonMain/sqldelight/com/example/shared/db/migrations/1.sqm
ALTER TABLE Orders ADD COLUMN currency TEXT NOT NULL DEFAULT 'USD';
```

File name is the _from_ version — `1.sqm` migrates v1 -> v2. SQLDelight runs them in order.

Verification: the Gradle task `verifyMainDatabaseMigration` compares the cumulative schema with the current `.sq` definition. Failing the build on a mismatch is the point.

## Testing

Common tests with the JDBC driver:

```kotlin
class OrderRepositoryTest {
    private lateinit var driver: SqlDriver
    private lateinit var db: AppDatabase

    @BeforeTest fun setup() {
        driver = JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY)
        AppDatabase.Schema.create(driver)
        db = AppDatabase(driver)
    }

    @AfterTest fun teardown() = driver.close()

    @Test fun upsertThenSelect() = runTest {
        val sut = OrderRepositoryImpl(db.orderQueries, StandardTestDispatcher(testScheduler))
        sut.save(Order.sample)
        assertEquals(1, sut.observeByCustomer(Order.sample.customerId).first().size)
    }
}
```

JDBC driver is fine for schema / query shape tests. Platform-specific behaviour (iOS threading) needs an `iosTest`.

## Hard nos

- No raw `sql()` execution in new code. Every query lives in an `.sq` file.
- No emitting SQLDelight types above the repository. Map to domain.
- No `.executeAsList()` inside a `@Composable` / SwiftUI body. Go through Flow -> StateFlow.
- No migrations without `verifyMigrations = true`. Silent schema drift destroys production data.
- No sharing a single `SqlDriver` across threads on iOS without the native driver's thread-safe wrapper. Use `NativeSqliteDriver`, not the JDBC one.
