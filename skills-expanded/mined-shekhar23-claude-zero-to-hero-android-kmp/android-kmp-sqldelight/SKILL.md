---
name: android-kmp-sqldelight
description: |
  SQLDelight as the KMP-native database — schema files, generated queries, coroutines extension, platform drivers, migrations. Use as the Room replacement when targeting KMP. Trigger on: "SQLDelight", "KMP database", "multiplatform Room", "shared database", "sqldelight KMP".
---

# KMP SQLDelight

## Dependency setup

```toml
# libs.versions.toml
[versions]
sqldelight = "2.0.2"

[libraries]
sqldelight-android-driver = { module = "app.cash.sqldelight:android-driver", version.ref = "sqldelight" }
sqldelight-native-driver = { module = "app.cash.sqldelight:native-driver", version.ref = "sqldelight" }
sqldelight-coroutines = { module = "app.cash.sqldelight:coroutines-extensions", version.ref = "sqldelight" }

[plugins]
sqldelight = { id = "app.cash.sqldelight", version.ref = "sqldelight" }
```

```kotlin
// core:data build.gradle.kts
sqldelight {
    databases {
        create("AppDatabase") {
            packageName.set("com.example.db")
        }
    }
}
```

## Schema file (`commonMain/sqldelight/`)

```sql
-- Task.sq
CREATE TABLE TaskEntity (
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    due_at INTEGER,
    priority TEXT NOT NULL DEFAULT 'MEDIUM',
    is_completed INTEGER NOT NULL DEFAULT 0
);

selectAll:
SELECT * FROM TaskEntity ORDER BY due_at ASC;

selectById:
SELECT * FROM TaskEntity WHERE id = :id;

upsert:
INSERT OR REPLACE INTO TaskEntity VALUES (?, ?, ?, ?, ?);

delete:
DELETE FROM TaskEntity WHERE id = :id;
```

## Platform driver factory (`expect/actual`)

```kotlin
// commonMain
expect class DriverFactory {
    fun createDriver(): SqlDriver
}

// androidMain
actual class DriverFactory(private val context: Context) {
    actual fun createDriver(): SqlDriver =
        AndroidSqliteDriver(AppDatabase.Schema, context, "app.db")
}

// iosMain
actual class DriverFactory {
    actual fun createDriver(): SqlDriver =
        NativeSqliteDriver(AppDatabase.Schema, "app.db")
}
```

## Database instance (`commonMain`)

```kotlin
fun createDatabase(factory: DriverFactory): AppDatabase =
    AppDatabase(factory.createDriver())
```

## DAO-style wrapper with Flow

```kotlin
// commonMain — core:data
class TaskLocalDataSource(private val db: AppDatabase) {
    fun getTasks(): Flow<List<TaskEntity>> =
        db.taskEntityQueries
            .selectAll()
            .asFlow()
            .mapToList(Dispatchers.IO)

    suspend fun upsert(task: TaskEntity) = withContext(Dispatchers.IO) {
        db.taskEntityQueries.upsert(
            task.id, task.title, task.dueAt, task.priority, if (task.isCompleted) 1L else 0L
        )
    }
}
```

## Checklist

- [ ] `.sq` files in `commonMain/sqldelight/` under the correct package path
- [ ] `DriverFactory` uses `expect`/`actual` per platform
- [ ] All queries emit `Flow` via `.asFlow().mapToList()`
- [ ] Dispatcher is `Dispatchers.IO`, never `Main`
- [ ] Migrations defined in `AppDatabase.Schema` before bumping schema version
