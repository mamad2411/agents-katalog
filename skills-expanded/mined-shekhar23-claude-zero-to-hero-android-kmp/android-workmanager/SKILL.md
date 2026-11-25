---
name: android-workmanager
description: |
  WorkManager patterns for Android - background sync, unique work, constraints, retries, periodic jobs, worker injection, and observing work state from the app. Use this skill whenever scheduling deferrable background work, syncing local and remote data, retrying uploads, or running tasks that must survive process death. Trigger on phrases like "WorkManager", "background sync", "periodic work", "retry upload", "constraints", "CoroutineWorker", "enqueueUniqueWork", or "observe work info".
---

# Android WorkManager

## When to Use It

Use WorkManager for work that is:
- deferrable
- guaranteed eventually
- expected to continue across app restarts or process death
- constrained by network, charging, battery, or storage conditions

Do **not** use WorkManager for:
- immediate in-app UI actions
- work that must finish while the screen is visible only
- exact alarms
- long-running foreground media playback

---

## Core Principles

- Workers must be **idempotent** — safe to run more than once.
- Prefer **unique work** so duplicate jobs do not pile up.
- Keep business logic in domain/data classes; the worker only coordinates execution.
- Return `Result.retry()` only for failures that may succeed later.
- Pass IDs and lightweight flags through `Data`, not large payloads.

---

## Worker Structure

Use `CoroutineWorker` for suspending APIs:

```kotlin
class SyncNotesWorker(
    appContext: Context,
    params: WorkerParameters,
    private val noteRepository: NoteRepository
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        return when (noteRepository.sync()) {
            is com.example.core.domain.Result.Success -> Result.success()
            is com.example.core.domain.Result.Error -> Result.retry()
        }
    }
}
```

Map typed domain/data failures to WorkManager results intentionally:
- temporary network failure -> `Result.retry()`
- invalid input or permanent server rejection -> `Result.failure()`
- success -> `Result.success()`

---

## Unique One-Time Work

Prefer `enqueueUniqueWork(...)` for user-triggered syncs:

```kotlin
workManager.enqueueUniqueWork(
    "sync-notes",
    ExistingWorkPolicy.KEEP,
    OneTimeWorkRequestBuilder<SyncNotesWorker>()
        .setConstraints(syncConstraints())
        .build()
)
```

Use:
- `KEEP` when an existing in-flight job should continue
- `REPLACE` when the newest request should win
- `APPEND` only for true chains that must run in sequence

---

## Periodic Work

Use periodic work for recurring sync or cleanup:

```kotlin
workManager.enqueueUniquePeriodicWork(
    "periodic-note-sync",
    ExistingPeriodicWorkPolicy.KEEP,
    PeriodicWorkRequestBuilder<SyncNotesWorker>(12, TimeUnit.HOURS)
        .setConstraints(syncConstraints())
        .build()
)
```

Periodic work is inexact. Do not use it for exact-time requirements.

---

## Constraints

Create reusable constraint builders:

```kotlin
fun syncConstraints(): Constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)
    .setRequiresBatteryNotLow(true)
    .build()
```

Common defaults:
- uploads/sync -> network connected
- expensive maintenance -> charging + idle if appropriate
- local cleanup -> no network needed

Avoid over-constraining work or it may never run.

---

## Retry and Backoff

When retrying, define backoff explicitly:

```kotlin
OneTimeWorkRequestBuilder<SyncNotesWorker>()
    .setBackoffCriteria(
        BackoffPolicy.EXPONENTIAL,
        30,
        TimeUnit.SECONDS
    )
    .build()
```

Use retry only for transient failures like:
- no internet
- 5xx server responses
- temporary rate limits

Do not retry validation failures, missing required IDs, or unsupported states.

---

## Chaining Work

Chain work when steps are strictly sequential:

```kotlin
workManager
    .beginUniqueWork("export-notes", ExistingWorkPolicy.REPLACE, exportRequest)
    .then(uploadRequest)
    .enqueue()
```

Each step should still be independently safe and idempotent.

---

## Input and Output Data

Keep `Data` small and primitive:

```kotlin
val request = OneTimeWorkRequestBuilder<UploadAttachmentWorker>()
    .setInputData(workDataOf("attachmentId" to attachmentId))
    .build()
```

Pass IDs, not serialized objects or file blobs.

---

## Observing Work State

Expose work status to presentation through a repository or small observer abstraction:

```kotlin
fun observeSyncWork(): Flow<WorkInfo?> {
    return workManager.getWorkInfosForUniqueWorkFlow("sync-notes")
        .map { infos -> infos.firstOrNull() }
}
```

The `ViewModel` maps `WorkInfo.State` into UI state like `isSyncing`, `lastSyncFailed`, or `lastSyncAt`.

---

## Dependency Injection

If the app uses Koin, register workers in DI and configure the app-level `WorkManager` factory once. Keep worker constructors thin and inject repositories/use cases instead of service locators.

---

## Checklist: Adding Background Work

- [ ] Confirm the use case really needs WorkManager
- [ ] Make the worker idempotent
- [ ] Keep worker logic orchestration-only
- [ ] Use unique work for duplicate-prone jobs
- [ ] Add only necessary constraints
- [ ] Retry only transient failures
- [ ] Expose work status to the `ViewModel` if the UI needs it