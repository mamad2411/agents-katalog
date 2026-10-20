---
name: datastore-preferences
description: Project-specific DataStore conventions — repository wrapping mandate, IOException catch on the read path, Preferences-vs-Proto heuristic, Tink-not-ESP alignment, and the multi-process gotcha. Load whenever adding a new setting or on-device preference.
---

# DataStore (project delta)

For Jetpack DataStore fundamentals — the `preferencesDataStore by` delegate, `dataStore(fileName = ..., serializer = ...)` for Proto, `Preferences` key types, `SharedPreferencesMigration`, basic read/write — read the [official DataStore guide](https://developer.android.com/topic/libraries/architecture/datastore). The canonical `AppPreferences` + `DataStoreModule` templates live in `.claude/skills/android-app-skeleton/references/optional-datastore.md`. This file documents only the project's specific decisions.

## When this applies

Jetpack DataStore (Preferences or Proto). On an existing app:

- **SharedPreferences-only** → don't push a DataStore migration unless asked. The migration helper exists, but the SharedPreferences code may be working fine.
- **MMKV / Tink-encrypted stores** → skip; not drop-in equivalents, and migrating off them has security implications.

## Preferences vs Proto — project heuristic

- **Preferences DataStore**: a handful of independent toggles and scalars.
- **Proto DataStore**: a single message as the whole store. Use when values are related (onboarding state, feature config, filters), or when type-safety across keys matters.

**If you would write more than ~10 keys in a Preferences store, switch to Proto.** That's the threshold where the implicit cost of mistyping a key name dominates the implicit cost of writing a serializer.

For Proto, use `kotlinx.serialization` rather than protobuf when the project already pulls in `kotlinx-serialization-json` (every scaffolded project does). The `Serializer<T>` must:
- Provide a `defaultValue` for first-run reads.
- Throw `CorruptionException` (not the underlying `SerializationException`) on bad input — DataStore relies on this to trigger its corruption handler.

## Repository wrapping (project mandate)

**Presentation never touches `DataStore` directly.** Every setting goes through a feature- or domain-level repository that exposes typed `Flow<T>` reads and `suspend fun` writes.

The non-obvious rule on the read path:

```kotlin
override val theme: Flow<AppTheme> = store.data
    .catch { e -> if (e is IOException) emit(emptyPreferences()) else throw e }
    .map { /* … */ }
    .distinctUntilChanged()
```

**Always `catch { IOException → emit(emptyPreferences()) }`** on the read path. `IOException` is an expected failure mode for first-run reads or a corrupted store; swallowing it propagates the failure into the flow and leaves the UI on a spinning Loading state forever. The reviewer flags any `DataStore.data` consumer in a repository that doesn't carry this guard.

## Keys

- Group in a private `object Keys` inside the repository.
- Key string in `snake_case` matching the Kotlin property name.
- **Never leak raw keys** (or `DataStore<Preferences>` itself) through the repository surface. The repository is the type boundary.

## SharedPreferences migration

`SharedPreferencesMigration` does the one-shot copy. Project policy: **ship the migration for exactly one release, then remove it** (and delete the legacy `SharedPreferences` XML) in the next release. Keeping the migration around indefinitely means every cold start re-runs the read on a file you've deleted in 99% of installs.

## Multi-process — read this before it bites

**DataStore is not multi-process safe.** If you have a widget, a `:remote` process, or a background service in a separate process:

- Funnel all reads/writes through a single process (bind to it via a `ContentProvider` facade), **or**
- Use `androidx.datastore:datastore-core-multiprocess` (available since 1.1).

If you go multi-process, pin the artifact to the existing `datastore` version ref in `libs.versions.toml`:

```toml
datastore-multiprocess = { module = "androidx.datastore:datastore-core-multiprocess", version.ref = "datastore" }
```

**Don't pin a separate version** — drift between single-process and multi-process variants causes silent serializer mismatches that look like data corruption.

Opening the same file from two processes with the **single-process** API corrupts silently. The reviewer flags any `preferencesDataStore by` delegate combined with manifest `<service android:process=":...">` or `<provider android:process=":...">`.

## Hard nos

- **No `runBlocking { store.data.first() }`** on the main thread.
- **No writes from a `@Composable`** — go through the repository + ViewModel.
- **No exposing `DataStore<Preferences>` to UI layers.** Repository surface only.
- **No storing secrets here.** Use **Tink (Keystore-backed)** — see `android-security` → "Secrets at rest". `EncryptedSharedPreferences` is deprecated (`androidx.security:security-crypto` was withdrawn); don't add it to new code. This alignment is enforced in `android-security` and `android-security-reviewer` — they recommend the same.
- **No raw key strings** in a repository's public API.
