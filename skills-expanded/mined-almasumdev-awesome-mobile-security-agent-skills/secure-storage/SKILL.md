---
name: secure-storage
description: Cross-platform secure storage on mobile. Covers Android EncryptedSharedPreferences / Tink, iOS Keychain, flutter_secure_storage, and react-native-keychain. Use when persisting tokens, credentials, or PII on device.
---

# Secure Storage on Mobile

## Instructions

Follow these guidelines to persist sensitive values without leaking them to disk, backups, or co-resident apps.

### 1. What Belongs Where

| Data | Android | iOS |
| ---- | ------- | --- |
| Opaque tokens (refresh, session) | Keystore-wrapped blob or `EncryptedSharedPreferences` | Keychain (`kSecClassGenericPassword`) |
| Symmetric / asymmetric keys | Android Keystore | Keychain (`kSecClassKey`) / Secure Enclave |
| Structured data (blobs, JSON) | `EncryptedFile` or SQLCipher | File with `NSFileProtectionComplete` or SQLCipher |
| User preferences that are **not** sensitive | `SharedPreferences` / DataStore | `NSUserDefaults` |

Never place tokens or PII in `SharedPreferences`, `NSUserDefaults`, or a plain SQLite file.

### 2. Android: EncryptedSharedPreferences (Tink-backed)

```kotlin
// build.gradle.kts: androidx.security:security-crypto:1.1.0-alpha06
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .setUserAuthenticationRequired(false) // set true + timeout for biometric gating
    .build()

val prefs = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
)
prefs.edit().putString("refresh_token", token).apply()
```

For new code prefer **Tink** directly (`AeadConfig`, `KeysetHandle`) so you control the keyset lifecycle — `EncryptedSharedPreferences` is in `alpha` indefinitely.

### 3. iOS: Keychain

```swift
let query: [String: Any] = [
    kSecClass as String:       kSecClassGenericPassword,
    kSecAttrService as String: "com.example.app.auth",
    kSecAttrAccount as String: "refresh_token",
    kSecValueData as String:   Data(token.utf8),
    kSecAttrAccessible as String:
        kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
]
SecItemDelete(query as CFDictionary)
let status = SecItemAdd(query as CFDictionary, nil)
guard status == errSecSuccess else { throw KeychainError.store(status) }
```

Always use a `*ThisDeviceOnly` accessibility class so items don't sync via iCloud Keychain.

### 4. Flutter: `flutter_secure_storage`

```dart
const storage = FlutterSecureStorage(
  aOptions: AndroidOptions(encryptedSharedPreferences: true),
  iOptions: IOSOptions(
    accessibility: KeychainAccessibility.first_unlock_this_device,
  ),
);
await storage.write(key: 'refresh_token', value: token);
```

On Android < 23 the plugin falls back to `RSA + AES` in `SharedPreferences` — document this in the threat model or raise `minSdk` to 23.

### 5. React Native: `react-native-keychain`

```ts
import * as Keychain from 'react-native-keychain';

await Keychain.setGenericPassword('user', token, {
  service: 'com.example.app.auth',
  accessible: Keychain.ACCESSIBLE.AFTER_FIRST_UNLOCK_THIS_DEVICE_ONLY,
  accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_CURRENT_SET, // optional
  storage: Keychain.STORAGE_TYPE.AES_GCM, // Android 23+
});
```

Avoid `AsyncStorage` for secrets — it is plain JSON on disk.

### 6. Backups, Exports, and Logs

- Android: set `android:allowBackup="false"` or provide an explicit `backup_rules.xml` that excludes secure stores.
- iOS: set `NSFileProtectionComplete` on anything sensitive written to the filesystem; mark files with `isExcludedFromBackupKey = true` where appropriate.
- Never log token values. Log only token IDs / hashes for debugging.

### 7. Migration & Wipe

- On logout, explicitly delete every entry you wrote — do not rely on app uninstall.
- On key rotation (OS upgrade invalidating keystore entries), surface a re-auth flow rather than crashing.

## Checklist

- [ ] No tokens or PII written to `SharedPreferences` / `NSUserDefaults` / `AsyncStorage`.
- [ ] Keys use `*ThisDeviceOnly` accessibility on iOS.
- [ ] Android uses `EncryptedSharedPreferences` or Tink, backed by Keystore.
- [ ] `allowBackup="false"` or an explicit backup exclusion rule is set.
- [ ] Logout path deletes every secure entry.
- [ ] No secret values appear in logs, crash reports, or analytics.
