---
name: mobile-security-patterns
description: "Security code for Keychain CRUD and biometric-gated items, URLSession certificate pinning, EncryptedSharedPreferences, Keystore-backed biometric auth, Android network security config, and an anti-pattern reference. Use when storing secrets or hardening a mobile app."
---

# Mobile Security Patterns

## iOS: Keychain CRUD

```swift
import Security

struct KeychainService {
    static let service = "com.myapp.credentials"

    // Store credential — fails silently if exists; use update for existing keys
    static func store(key: String, value: String) throws {
        guard let data = value.data(using: .utf8) else { throw KeychainError.encodingFailed }

        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrService: service,
            kSecAttrAccount: key,
            kSecValueData: data,
            // Inaccessible when locked, never syncs to iCloud, tied to this device
            kSecAttrAccessible: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]

        let status = SecItemAdd(query as CFDictionary, nil)

        if status == errSecDuplicateItem {
            // Key exists — update instead
            let updateQuery: [CFString: Any] = [
                kSecClass: kSecClassGenericPassword,
                kSecAttrService: service,
                kSecAttrAccount: key
            ]
            let attributes: [CFString: Any] = [kSecValueData: data]
            let updateStatus = SecItemUpdate(updateQuery as CFDictionary, attributes as CFDictionary)
            guard updateStatus == errSecSuccess else { throw KeychainError.updateFailed(updateStatus) }
        } else {
            guard status == errSecSuccess else { throw KeychainError.saveFailed(status) }
        }
    }

    // Retrieve credential
    static func retrieve(key: String) throws -> String {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrService: service,
            kSecAttrAccount: key,
            kSecReturnData: true,
            kSecMatchLimit: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            throw KeychainError.retrievalFailed(status)
        }

        return value
    }

    // Delete credential
    static func delete(key: String) {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrService: service,
            kSecAttrAccount: key
        ]
        SecItemDelete(query as CFDictionary)
    }
}

enum KeychainError: Error {
    case encodingFailed
    case saveFailed(OSStatus)
    case updateFailed(OSStatus)
    case retrievalFailed(OSStatus)
}
```

### Biometric-Gated Keychain Item
```swift
// Store token that requires Face ID / Touch ID to read
func storeWithBiometric(token: String) throws {
    let access = try SecAccessControlCreateWithFlags(
        nil,
        kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        .biometryCurrentSet,   // Invalidated if new biometric enrolled
        nil
    ).get()

    let query: [CFString: Any] = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrService: "com.myapp.biometric",
        kSecAttrAccount: "auth_token",
        kSecValueData: token.data(using: .utf8)!,
        kSecAttrAccessControl: access,
        kSecUseAuthenticationContext: LAContext()
    ]

    SecItemAdd(query as CFDictionary, nil)
}
```

---

## iOS: Certificate Pinning with URLSession

```swift
// Pin against public key hash (survives certificate rotation)
class PinnedURLSessionDelegate: NSObject, URLSessionDelegate {
    // SHA-256 of SubjectPublicKeyInfo (generate: openssl s_client -connect host:443 | openssl x509 -pubkey | openssl pkey -pubin -outform DER | openssl dgst -sha256 -binary | base64)
    private let pinnedHashes = Set([
        "abc123...primaryHash==",
        "xyz789...backupHash=="   // Always include backup
    ])

    func urlSession(_ session: URLSession,
                    didReceive challenge: URLAuthenticationChallenge,
                    completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Evaluate trust chain
        var error: CFError?
        guard SecTrustEvaluateWithError(serverTrust, &error) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Extract server's leaf certificate SPKI hash
        guard let certificate = SecTrustGetCertificateAtIndex(serverTrust, 0),
              let publicKey = SecCertificateCopyKey(certificate),
              let publicKeyData = SecKeyCopyExternalRepresentation(publicKey, nil) as Data? else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        let keyHash = sha256(publicKeyData).base64EncodedString()

        if pinnedHashes.contains(keyHash) {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }

    private func sha256(_ data: Data) -> Data {
        var hash = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        data.withUnsafeBytes { CC_SHA256($0.baseAddress, CC_LONG(data.count), &hash) }
        return Data(hash)
    }
}
```

---

## Android: EncryptedSharedPreferences

```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

fun createSecurePrefs(context: Context): SharedPreferences {
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    return EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
}

// Usage — identical API to SharedPreferences
val prefs = createSecurePrefs(context)
prefs.edit().putString("auth_token", token).apply()
val token = prefs.getString("auth_token", null)
```

---

## Android: Biometric Authentication with Keystore-Backed Key

```kotlin
class BiometricAuthManager(private val activity: FragmentActivity) {
    private val keyAlias = "biometric_key"

    fun generateKey() {
        val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        val spec = KeyGenParameterSpec.Builder(
            keyAlias,
            KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
        )
            .setBlockModes(KeyProperties.BLOCK_MODE_CBC)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_PKCS7)
            .setUserAuthenticationRequired(true)
            .setInvalidatedByBiometricEnrollment(true)  // Invalidate if new fingerprint added
            .build()

        keyGenerator.init(spec)
        keyGenerator.generateKey()
    }

    fun authenticate(onSuccess: (Cipher) -> Unit, onError: (String) -> Unit) {
        val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val key = keyStore.getKey(keyAlias, null) as SecretKey
        val cipher = Cipher.getInstance("AES/CBC/PKCS7Padding").apply {
            init(Cipher.ENCRYPT_MODE, key)
        }

        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Authenticate")
            .setSubtitle("Use biometric to access your account")
            .setNegativeButtonText("Cancel")
            .build()

        val biometricPrompt = BiometricPrompt(activity, ContextCompat.getMainExecutor(activity),
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    result.cryptoObject?.cipher?.let(onSuccess)
                }
                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                    onError(errString.toString())
                }
            }
        )

        biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
    }
}
```

---

## Android: Network Security Config

```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Block all cleartext traffic app-wide -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <!-- Pin production API -->
    <domain-config>
        <domain includeSubdomains="true">api.myapp.com</domain>
        <pin-set expiration="2027-01-01">
            <!-- Primary: SHA-256 of SubjectPublicKeyInfo DER -->
            <pin digest="SHA-256">primaryPublicKeyHashBase64==</pin>
            <!-- Backup: intermediate CA public key -->
            <pin digest="SHA-256">backupPublicKeyHashBase64==</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

```xml
<!-- AndroidManifest.xml -->
<application
    android:networkSecurityConfig="@xml/network_security_config"
    android:usesCleartextTraffic="false"
    android:allowBackup="false">
```

---

## Security Anti-Patterns Reference

| Anti-Pattern | Risk | Fix |
|---|---|---|
| Token in UserDefaults/SharedPreferences | Readable without auth | Keychain / EncryptedSharedPreferences |
| NSLog/Log.d with auth data | Visible in device logs | Remove or redact in release builds |
| Hardcoded API key in source | Key exposed in IPA/APK | Env var injection or secrets vault |
| ATS disabled globally | MITM possible | Re-enable; whitelist specific domains only |
| allowBackup="true" | Data exposed via adb backup | Set to false or use BackupAgent |
| Certificate pinning disabled in debug | Dev habits disable prod checks | Use separate config, not disabled |
