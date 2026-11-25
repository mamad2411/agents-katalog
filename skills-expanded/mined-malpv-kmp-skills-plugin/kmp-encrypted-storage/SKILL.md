---
name: kmp-encrypted-storage
description: Wire encrypted key-value storage into a KMP project — a domain-specific SecureStorage contract, its multiplatform-settings implementation, and the hardware-backed engines (EncryptedSharedPreferences / Keychain) via DI. Use whenever the user stores tokens, credentials, or sensitive flags, mentions secure/encrypted storage, Keychain, EncryptedSharedPreferences, multiplatform-settings, or needs the TokenStorage that the Ktor auth layer depends on. Applies the standard and composes with the auth layer; does not just describe it.
---

# Skill: KMP Encrypted Storage

This skill provides the official architectural standard to implement native key-value encrypted storage in Kotlin Multiplatform (KMP) projects, protecting session data such as refresh tokens, device identifiers, or sensitive flags.

It utilizes the **multiplatform-settings** library as a common abstraction and delegates storage physical operations to native hardware-protected mechanisms on each platform (`EncryptedSharedPreferences` on Android and `Keychain` on iOS).

> [!NOTE]
> **Placement (architecture-agnostic):** the `SecureStorage` contract and its implementation belong to the **data layer**; the platform encryption engines go in the platform source sets (`androidMain` / `iosMain`). In a **modular** project (feature + layers) map these to the corresponding modules — see `kmp-modular-architecture`. In a **single-module** project they are packages under `commonMain`. This skill does not assume a module layout.

## Workflow

This skill **applies** the standard. Do the steps in order; each points to the section with the full code and its warnings. Do not stop at summarizing.

1. **Contract** (§1) — a domain-specific interface (`SessionSecureStorage`), not a generic key-value map. Model exactly the keys the app stores.
2. **Implementation** (§2) — back the contract with `multiplatform-settings`.
3. **Platform engines** (§3) — `EncryptedSharedPreferences` on Android, `Keychain` on iOS via `expect/actual`. **No plaintext fallback**: if hardware-backed init fails, fail closed, never degrade to unencrypted.
4. **DI** (§4) — one module that `includes` the platform module and binds the contract.
5. **Compose with the consumer.** If this stores auth tokens, it is the implementation behind `kmp-expert-ktor`'s `TokenStorage` — expose both access and refresh, and let an adapter bridge the two. Wire the lifecycle: whoever owns logout must call `clearAll()`; a `clearAll()` nothing calls is the sign the session lifecycle was left unwired.

> [!WARNING]
> **Jetpack Security (`EncryptedSharedPreferences`, `MasterKey`) is deprecated as of `androidx.security:security-crypto` 1.1.0.** It still functions and remains the most common approach for hardware-backed key-value storage in KMP, but it receives no further maintenance and a security audit may flag it. There is no drop-in successor — the manual path is Android Keystore + Tink. Surface this to the user rather than letting a compiler deprecation warning be how they find out; the choice to accept it or build on Keystore directly is theirs.

---

## 1. Define the Storage Contract (commonMain)

To adhere to SOLID principles and decouple infrastructure from business logic, a clean interface contract is defined in the data layer.

```kotlin
package com.yourproject.data.local.secure

interface SessionSecureStorage {
    fun saveRefreshToken(value: String)
    fun getRefreshToken(): String?
    fun clearRefreshToken()
    fun clearAll()
}
```

> [!TIP]
> **Design Standard:**
> Model explicit, domain-specific contracts (`SessionSecureStorage`, `UserSecureStorage`) instead of exposing a generic key-value `HashMap` interface that allows storing arbitrary keys from anywhere in the codebase. This helps prevent unstructured storage access.

---

## 2. Multiplatform Settings Implementation (commonMain)

```kotlin
package com.yourproject.data.local.secure

import com.russhwolf.settings.Settings

private const val KEY_REFRESH_TOKEN = "secure_session_refresh_token"

class SessionSecureStorageImpl(
    private val settings: Settings
) : SessionSecureStorage {

    override fun saveRefreshToken(value: String) {
        settings.putString(KEY_REFRESH_TOKEN, value)
    }

    override fun getRefreshToken(): String? {
        return settings.getStringOrNull(KEY_REFRESH_TOKEN)
    }

    override fun clearRefreshToken() {
        settings.remove(KEY_REFRESH_TOKEN)
    }

    override fun clearAll() {
        clearRefreshToken()
    }
}
```

---

## 3. Platform-Specific Encryption Engine Setup

It is strictly prohibited to use fallback plain text storage (e.g., standard `SharedPreferences` or default `NSUserDefaults`) for sensitive credentials.

### Android Engine (`androidMain` - EncryptedSharedPreferences)
Uses Android's `EncryptedSharedPreferences` backed by a 256-bit AES cryptographic key managed inside the Android Keystore (`MasterKey`).
```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import com.russhwolf.settings.Settings
import com.russhwolf.settings.SharedPreferencesSettings
import org.koin.dsl.module

actual val platformModule = module {
    single<Settings> {
        val context: android.content.Context = get()

        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()

        val encryptedPrefs = EncryptedSharedPreferences.create(
            context,
            "encrypted_shared_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )

        SharedPreferencesSettings(encryptedPrefs)
    }
}
```

### iOS Engine (`iosMain` - Keychain)
Uses native `KeychainSettings` to persist credentials inside the protected Apple Keychain system.
```kotlin
import com.russhwolf.settings.ExperimentalSettingsImplementation
import com.russhwolf.settings.KeychainSettings
import com.russhwolf.settings.Settings
import org.koin.dsl.module

actual val platformModule = module {
    @OptIn(ExperimentalSettingsImplementation::class)
    single<Settings> {
        KeychainSettings(service = "com.yourproject.secure_storage")
    }
}
```

---

## 4. DI Registration (Koin)

The platform engine (`Settings`) lives in an `expect/actual platformModule`; the shared module pulls it in with `includes` so a single `secureStorageModule` fully wires the contract regardless of platform.

```kotlin
// commonMain — platformModule provides the encrypted Settings per platform (section 3)
expect val platformModule: Module

val secureStorageModule = module {
    includes(platformModule)
    // Bind the contract to the implementation injecting the platform Settings instance
    single<SessionSecureStorage> { SessionSecureStorageImpl(get()) }
}
```

> [!NOTE]
> **Composition with `kmp-expert-ktor`:** the Ktor `Auth` plugin persists tokens through a `TokenStorage` interface. Implement that interface with an adapter that delegates to `SessionSecureStorage` (this skill) — the ktor module never depends on `multiplatform-settings` directly, only on its own `TokenStorage` abstraction. Note that Ktor's `loadTokens` needs **both** access and refresh tokens, so model the contract with both (`saveAccessToken`/`saveRefreshToken`) rather than refresh-only. See the composition note in `kmp-expert-ktor`.

---

## Security and Usage Guidelines

- **Do Not Store Large Blobs:** Key-value storage engines are optimized for short, high-sensitivity strings. Do not use them to cache large network response payloads, serialized images, or complete relational databases.
- **Strict Session Lifecycle:** Invoke `clearAll()` immediately upon critical events: user logout, session expiration, or a `401 Unauthorized` API network error.
- **No Unencrypted Fallbacks:** If native hardware-backed encryption initialization fails (e.g., due to Android Keystore corruption), the app must fail safely by terminating the user session, rather than falling back to unencrypted storage.
