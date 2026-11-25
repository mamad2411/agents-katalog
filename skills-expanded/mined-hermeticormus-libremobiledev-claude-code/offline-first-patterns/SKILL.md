---
name: offline-first-patterns
description: "Offline-first code: Room with a sync queue and WorkManager worker, Core Data with background sync, Drift with a sync queue, a conflict resolution decision matrix, and a Flutter network monitor. Use when building local-first storage and sync."
---

# Offline First Patterns

## Android: Room with Sync Queue

```kotlin
// Entity with sync metadata
@Entity(tableName = "tasks")
data class TaskEntity(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val title: String,
    val completed: Boolean = false,
    val updatedAt: Long = System.currentTimeMillis(),
    val syncStatus: SyncStatus = SyncStatus.PENDING   // PENDING, SYNCED, FAILED
)

enum class SyncStatus { PENDING, SYNCED, FAILED }

@Dao
interface TaskDao {
    @Query("SELECT * FROM tasks ORDER BY updatedAt DESC")
    fun observeAll(): Flow<List<TaskEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(task: TaskEntity)

    @Query("SELECT * FROM tasks WHERE syncStatus != 'SYNCED'")
    suspend fun getPending(): List<TaskEntity>

    @Query("UPDATE tasks SET syncStatus = :status WHERE id = :id")
    suspend fun updateSyncStatus(id: String, status: SyncStatus)
}
```

### Repository: Write Local First

```kotlin
class TaskRepository(
    private val dao: TaskDao,
    private val api: TaskApi,
    private val workManager: WorkManager
) {
    // Write to DB immediately; schedule sync
    suspend fun createTask(title: String): TaskEntity {
        val task = TaskEntity(title = title)
        dao.upsert(task)
        scheduleSyncWork()
        return task
    }

    fun observeTasks(): Flow<List<Task>> =
        dao.observeAll().map { entities -> entities.map { it.toDomain() } }

    private fun scheduleSyncWork() {
        val request = OneTimeWorkRequestBuilder<SyncWorker>()
            .setConstraints(
                Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build()
            )
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 15, TimeUnit.SECONDS)
            .build()

        workManager.enqueueUniqueWork("task_sync", ExistingWorkPolicy.KEEP, request)
    }
}
```

### WorkManager Sync Worker

```kotlin
class SyncWorker(
    context: Context,
    params: WorkerParameters,
    private val dao: TaskDao,
    private val api: TaskApi
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val pending = dao.getPending()

        for (task in pending) {
            try {
                val serverTask = api.upsertTask(task.toApiModel())
                // Server wins on conflict: update local with server response
                dao.upsert(task.copy(
                    updatedAt = serverTask.updatedAt,
                    syncStatus = SyncStatus.SYNCED
                ))
            } catch (e: HttpException) {
                if (e.code() == 409) {
                    // Conflict: fetch server version and resolve
                    val serverVersion = api.getTask(task.id)
                    resolveConflict(task, serverVersion)
                } else {
                    dao.updateSyncStatus(task.id, SyncStatus.FAILED)
                }
            } catch (e: IOException) {
                // Network error — retry (WorkManager handles backoff)
                return Result.retry()
            }
        }

        return Result.success()
    }

    // Last-Write-Wins conflict resolution
    private suspend fun resolveConflict(local: TaskEntity, server: ApiTask) {
        val resolved = if (local.updatedAt > server.updatedAt) {
            local.copy(syncStatus = SyncStatus.SYNCED)
        } else {
            server.toEntity().copy(syncStatus = SyncStatus.SYNCED)
        }
        dao.upsert(resolved)
    }
}
```

---

## iOS: Core Data with Background Sync

```swift
class TaskRepository: ObservableObject {
    private let container: NSPersistentContainer
    private var viewContext: NSManagedObjectContext { container.viewContext }

    init() {
        container = NSPersistentContainer(name: "TaskModel")
        container.loadPersistentStores { _, error in
            if let error { fatalError("Core Data failed: \(error)") }
        }
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        container.viewContext.automaticallyMergesChangesFromParent = true
    }

    // Write on background context — never block main thread
    func createTask(title: String) async throws {
        let context = container.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

        try await context.perform {
            let task = TaskMO(context: context)
            task.id = UUID().uuidString
            task.title = title
            task.updatedAt = Date()
            task.syncStatus = "pending"
            try context.save()
        }

        await scheduleBGSync()
    }

    // Reactive fetch for SwiftUI
    func tasksFetchRequest() -> NSFetchRequest<TaskMO> {
        let request = TaskMO.fetchRequest()
        request.sortDescriptors = [NSSortDescriptor(key: "updatedAt", ascending: false)]
        return request
    }

    private func scheduleBGSync() async {
        let request = BGProcessingTaskRequest(identifier: "com.myapp.sync")
        request.requiresNetworkConnectivity = true
        request.requiresExternalPower = false
        try? BGTaskScheduler.shared.submit(request)
    }
}
```

---

## Flutter: Drift with Sync Queue

```dart
// drift table definition
class Tasks extends Table {
  TextColumn get id => text().withDefault(const CustomExpression('(randomblob(16)'))();
  TextColumn get title => text()();
  BoolColumn get completed => boolean().withDefault(const Constant(false))();
  IntColumn get updatedAt => integer()();
  TextColumn get syncStatus => text().withDefault(const Constant('pending'))();
}

// DAO methods
Future<void> upsertTask(TasksCompanion task) =>
    into(tasks).insertOnConflictUpdate(task);

Stream<List<Task>> watchAllTasks() =>
    select(tasks).watch().map((rows) => rows.map((r) => r.toDomain()).toList());

Future<List<Task>> getPendingTasks() =>
    (select(tasks)..where((t) => t.syncStatus.isNotValue('synced'))).get()
      .then((rows) => rows.map((r) => r.toDomain()).toList());
```

### Repository Layer (Dart)
```dart
class TaskRepository {
  final AppDatabase _db;
  final TaskApi _api;

  TaskRepository(this._db, this._api);

  Stream<List<Task>> watchTasks() => _db.watchAllTasks();

  Future<void> addTask(String title) async {
    final task = TasksCompanion.insert(
      id: Value(const Uuid().v4()),
      title: title,
      updatedAt: Value(DateTime.now().millisecondsSinceEpoch),
    );
    await _db.upsertTask(task);
    _triggerSync();
  }

  Future<void> syncPending() async {
    final pending = await _db.getPendingTasks();
    for (final task in pending) {
      try {
        final serverTask = await _api.upsertTask(task);
        await _db.upsertTask(task.toCompanion().copyWith(
          updatedAt: Value(serverTask.updatedAt),
          syncStatus: const Value('synced'),
        ));
      } on SocketException {
        break; // No network — try again later
      }
    }
  }

  void _triggerSync() {
    // workmanager package for background
    Workmanager().registerOneOffTask('sync_tasks', 'syncTasks');
  }
}
```

---

## Conflict Resolution Decision Matrix

| Strategy | Use When | Risk |
|---|---|---|
| Last Write Wins (LWW) | Single-user, device sync | Concurrent edits from two devices: one lost |
| Server Wins | Server is source of truth | User loses unsynced local changes |
| Client Wins | Local action always valid | Overwrites server changes from other clients |
| Three-way merge | Multi-field objects | Complex; requires base version tracking |
| CRDT | Collaborative / multi-user editing | High implementation complexity |

## Network Monitor (Flutter)

```dart
// connectivity_plus
final connectivity = Connectivity();

connectivity.onConnectivityChanged.listen((result) {
  if (result != ConnectivityResult.none) {
    taskRepository.syncPending();
  }
});
```
