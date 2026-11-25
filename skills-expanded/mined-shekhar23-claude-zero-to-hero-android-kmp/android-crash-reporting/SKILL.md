---
name: android-crash-reporting
description: |
  Crash reporting and ANR detection for Android - Firebase Crashlytics setup, non-fatal exception boundaries, custom keys and log lines, user identity rules, ANR detection, ViewModel crash boundaries, and debug vs release configuration. Use this skill whenever adding crash reporting, recording non-fatal errors, adding diagnostic context to crashes, setting up Crashlytics, or tuning crash triage workflows. Trigger on phrases like "crash reporting", "Crashlytics", "Firebase Crashlytics", "non-fatal", "ANR", "crash boundary", "recordException", "crash log", "custom key", "crash triage".
---

# Android Crash Reporting

## Overview

Crash reporting surfaces real-world failures that never appear in tests. This skill covers the full setup from Gradle to triage, with strict rules on what context to attach and how to keep PII out of crash reports.

Stack: **Firebase Crashlytics** (primary), Strict Mode for ANR/violation detection.

Related skills: `android-analytics-logging`, `android-error-handling`.

---

## Gradle Setup

```kotlin
// build.gradle.kts (:app)
plugins {
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
}

dependencies {
    implementation(platform(libs.firebase.bom))
    implementation(libs.firebase.crashlytics)
}
```

---

## Enable / Disable by Build Type

Never send debug crashes to Crashlytics — it pollutes production data.

```kotlin
// build.gradle.kts (:app)
buildTypes {
    debug {
        manifestPlaceholders["crashlyticsEnabled"] = false
    }
    release {
        manifestPlaceholders["crashlyticsEnabled"] = true
    }
}
```

```xml
<!-- AndroidManifest.xml -->
<meta-data
    android:name="firebase_crashlytics_collection_enabled"
    android:value="${crashlyticsEnabled}" />
```

Or programmatically in `Application.onCreate()`:

```kotlin
FirebaseCrashlytics.getInstance()
    .setCrashlyticsCollectionEnabled(!BuildConfig.DEBUG)
```

---

## CrashReporter Interface (Domain Layer)

Wrap Crashlytics behind an interface so presentation/domain never import Firebase directly.

```kotlin
// domain layer
interface CrashReporter {
    fun recordException(throwable: Throwable)
    fun log(message: String)
    fun setKey(key: String, value: String)
    fun setUserId(anonymousId: String) // NEVER real name/email
}

// data layer
class CrashlyticsReporter : CrashReporter {
    private val c get() = FirebaseCrashlytics.getInstance()
    override fun recordException(t: Throwable) = c.recordException(t)
    override fun log(message: String) = c.log(message)
    override fun setKey(key: String, value: String) = c.setCustomKey(key, value)
    override fun setUserId(anonymousId: String) = c.setUserId(anonymousId)
}
```

Koin binding:
```kotlin
single<CrashReporter> { CrashlyticsReporter() }
```

---

## Non-Fatal Boundaries in ViewModels

Record exceptions at recovery boundaries — not deep inside business logic.

```kotlin
class NotesViewModel(
    private val repository: NoteRepository,
    private val crashReporter: CrashReporter,
) : ViewModel() {

    fun loadNotes() {
        viewModelScope.launch {
            when (val result = repository.getNotes()) {
                is Result.Success -> { /* update state */ }
                is Result.Error -> {
                    crashReporter.log("loadNotes failed: ${result.error}")
                    crashReporter.recordException(RuntimeException("loadNotes: ${result.error}"))
                    // update error UI state — do not rethrow
                }
            }
        }
    }
}
```

---

## Custom Keys for Crash Context

Set keys immediately before the risky operation. Keys are overwritten each call — the last value before the crash is what Crashlytics shows.

```kotlin
fun syncNotes() {
    viewModelScope.launch {
        crashReporter.setKey("sync_trigger", "manual")
        crashReporter.setKey("note_count", noteCount.toString())
        crashReporter.log("Starting note sync")

        when (val result = repository.sync()) {
            is Result.Error -> crashReporter.recordException(RuntimeException("sync: ${result.error}"))
            is Result.Success -> crashReporter.log("Sync complete")
        }
    }
}
```

**Safe to attach:** feature name, screen name, anonymized entity IDs (hashed), operation type, non-sensitive counts.

**Never attach:** email, name, phone, auth tokens, passwords, raw user content.

---

## ANR Detection with StrictMode

Enable in debug builds only to catch main-thread violations before they reach users.

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(
                StrictMode.ThreadPolicy.Builder()
                    .detectAll()
                    .penaltyLog()
                    .penaltyDeath()
                    .build()
            )
            StrictMode.setVmPolicy(
                StrictMode.VmPolicy.Builder()
                    .detectAll()
                    .penaltyLog()
                    .build()
            )
        }
    }
}
```

---

## ViewModel Crash Boundary

Uncaught exceptions in `viewModelScope` crash the app. Use a `CoroutineExceptionHandler` to record them.

```kotlin
class BaseViewModel(private val crashReporter: CrashReporter) : ViewModel() {

    protected fun safeLaunch(block: suspend CoroutineScope.() -> Unit): Job =
        viewModelScope.launch(
            CoroutineExceptionHandler { _, throwable ->
                crashReporter.log("Unhandled ViewModel exception: ${throwable.message}")
                crashReporter.recordException(throwable)
            }
        ) { block() }
}
```

---

## Release Checklist

- [ ] Crashlytics disabled in debug, enabled in release
- [ ] No PII in `setUserId` — hashed/anonymous IDs only
- [ ] Mapping file upload configured (Crashlytics Gradle plugin handles this automatically)
- [ ] StrictMode zero violations in debug before merging to main
- [ ] Main thread never blocked > 200ms
- [ ] Non-fatal alert thresholds configured in Firebase console

---

## Anti-Patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| `recordException` in every catch block | Floods dashboard, hides real issues | Record only at top-level boundaries |
| `setUserId(email)` | PII violation | Use a hashed or server-assigned anonymous ID |
| Crashlytics enabled in debug | Pollutes production dashboard | Guard with `BuildConfig.DEBUG` |
| Logging full request/response bodies | May contain tokens or PII | Log only operation name and error code |
| Ignoring non-fatal volume | High-rate non-fatals degrade UX as much as crashes | Set up Firebase alerts on non-fatal rate |
