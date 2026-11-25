---
name: encrypted-databases
description: Encrypting local databases on mobile with SQLCipher, Room + EncryptedFile, or Realm encryption. Use when persisting structured sensitive data on device.
---

# Encrypted Databases on Mobile

## Instructions

Plain SQLite and plain Realm files are readable by anyone with filesystem access — including forensic tools and, on rooted/jailbroken devices, other apps. Encrypt at rest for anything sensitive.

### 1. When to Encrypt

Encrypt when the DB contains:
- Session tokens, refresh tokens, or API credentials.
- PII (email, phone, address, national IDs).
- Financial / health records.
- User-generated content marked private.

Do **not** encrypt purely public / cached content; it wastes CPU and complicates debugging.

### 2. Key Management (The Actual Hard Part)

- Generate a random 256-bit key once per install.
- Wrap it with a **keystore-backed** key (Android Keystore / iOS Keychain).
- Store the wrapped blob in `EncryptedSharedPreferences` / Keychain.
- **Never** derive the DB key from a constant string or from `android_id`.

### 3. Android: Room + SQLCipher

```kotlin
// build.gradle.kts
// implementation("net.zetetic:sqlcipher-android:4.6.1")
// implementation("androidx.sqlite:sqlite:2.4.0")

val passphrase: ByteArray = KeyStoreHelper.loadOrCreateDbKey() // 32 bytes
val factory = SupportOpenHelperFactory(passphrase, null, false)

val db = Room.databaseBuilder(ctx, AppDatabase::class.java, "app.db")
    .openHelperFactory(factory)
    .build()

// Zero the passphrase as soon as Room has it.
passphrase.fill(0)
```

### 4. Android: Room + `EncryptedFile` (Alternative)

For small stores where full-text queries are not required, use Jetpack `EncryptedFile`:

```kotlin
val file = EncryptedFile.Builder(
    ctx, File(ctx.filesDir, "notes.bin"), masterKey,
    EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB,
).build()

file.openFileOutput().use { it.write(payload) }
```

This is simpler than SQLCipher but loses SQL query capabilities.

### 5. iOS: SQLCipher via GRDB

```swift
var config = Configuration()
config.prepareDatabase { db in
    let key = try KeychainHelper.loadOrCreateDbKey() // 32-byte Data
    try db.usePassphrase(key)
}
let dbQueue = try DatabaseQueue(path: path, configuration: config)
```

For Core Data, wrap the store with `NSPersistentStoreFileProtectionKey: FileProtectionType.complete` — NOT equivalent to SQLCipher, but acceptable when the device is locked.

### 6. Realm

```kotlin
val config = RealmConfiguration.Builder(schema = setOf(User::class))
    .name("user.realm")
    .encryptionKey(KeyStoreHelper.loadOrCreateRealmKey()) // 64 bytes
    .build()
val realm = Realm.open(config)
```

Realm requires a **64-byte** key. Losing it means the DB is unrecoverable — plan for re-sync from server on key loss.

### 7. Migration From Plaintext

If you inherit a plaintext DB:

1. Open it plaintext.
2. Attach a new encrypted DB with the new key.
3. `INSERT INTO encrypted.table SELECT * FROM plain.table;` for each table.
4. Close, delete the plaintext file, rename encrypted → canonical path.
5. Run on a background thread with progress UI; this can take minutes on large DBs.

### 8. Debug vs Release

- In debug builds you may want to disable encryption to allow inspection with DB Browser / Stetho. Gate this on `BuildConfig.DEBUG` / `#if DEBUG` so it cannot ship.
- Never commit a debug key that also unlocks production dumps.

## Checklist

- [ ] The DB key is random (not derived from a constant or device ID).
- [ ] The DB key is wrapped by Keystore / Keychain and never stored plaintext on disk.
- [ ] SQLCipher / Realm encryption is enabled on any DB containing PII or credentials.
- [ ] A documented migration exists for moving users from plaintext to encrypted DBs.
- [ ] Key-loss UX is handled (re-sync or re-login) rather than silent data corruption.
- [ ] Debug-only relaxations cannot ship to production.
