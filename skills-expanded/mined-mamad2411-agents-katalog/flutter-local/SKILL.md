---
name: flutter-local
description: On-device storage standards for Flutter — choosing the store by data class (secure storage, SharedPreferences, encrypted database, cache directory), database encryption with a keystore-generated key, backup exclusion, stores exposed as providers rather than singletons, TTL plus size-capped user-scoped caches, staleness on read, and schema versioning with migrations tested from the oldest installed version. Load when writing or reviewing token stores, cache stores, preferences, or the local database.
user-invocable: false
stack: storage/flutter-local
paths:
  - "**/core/storage/*.dart"
  - "**/core/cache/*.dart"
  - "**/*_store.dart"
  - "**/app_database.dart"
---

Full standards in [flutter-local.md](flutter-local.md). Always-on summary:

**Scope:** the physical stores. Cache *policy* (cacheFirst/networkFirst, the caching decorator, `Cached<T>`) is `api-style/dio`; what sign-out clears and when is `auth/flutter-session`.

**Pick the store by data class — this is the first decision, and it is not reversible cheaply:**

| Data | Store |
|---|---|
| Tokens, refresh tokens, PINs, encryption keys | `FlutterSecureStorage` |
| Non-personal UI preferences (theme, last tab, onboarding seen) | `SharedPreferences` — assume world-readable |
| Personal or business records, cached API rows | Encrypted database (drift + SQLCipher) |
| Large binaries (images, video, PDFs) | `getApplicationCacheDirectory()`, never the sole copy |

**Secure storage:** `IOSOptions(accessibility: KeychainAccessibility.first_unlock_this_device)` and `AndroidOptions(encryptedSharedPreferences: true)`. Never a token, key, or personal field in `SharedPreferences`.

**Encryption:** the database key is 32 bytes from `Random.secure()`, generated once on first open, written to secure storage, and applied with `PRAGMA key`. Never a compiled-in constant, `String.fromEnvironment`, a bundled asset, or a value derived from a device identifier.

**Backup exclusion is part of encryption:** `android:allowBackup="false"` plus empty `dataExtractionRules`, and `first_unlock_this_device` (not `…_this_device`'s cloud-syncing siblings). An unencrypted cloud backup undoes on-device encryption.

**Stores are providers, never singletons.** `X.instance` cannot be overridden in a test and hides lazy init that silently no-ops (`_box?.put(...)` when `_box` is null). Every store is constructed in a provider, its dependencies arrive by `ref.watch`, it is closed in `ref.onDispose`, and tests substitute it with `overrideWith` / `overrideWithValue` — that override is the whole reason for the indirection.

**Every cache entry carries `expiresAt`, a `userId`, and the store carries a `maxEntries` cap with an `evict()` pass** run on open and after writes. TTL alone bounds age, not size. A row that fails to decode deletes itself and returns null rather than throwing forever.

**Reads return staleness, not a lie.** The store returns the entry with `fetchedAt`/`isStale` so the dio decorator and the UI can both act on it; it never silently returns expired data as fresh, and never `null` when the caller could have used the stale copy.

**Schema is versioned from release one.** `schemaVersion` is bumped on every shape change; the drift `MigrationStrategy`'s `onUpgrade` is written as sequential `if (from < N)` steps, never `if (from == previous)`; and the migration test runs from the oldest version still installed — users skip releases, so a path exercised only from `v-1` is untested for most of them. Never `deleteDatabase` as a migration.

**Related:** `api-style/dio`, `auth/flutter-session`, `state/riverpod`, `language/dart-models`, `testing/flutter-test`.
