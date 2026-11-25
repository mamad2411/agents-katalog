---
name: keystore-keychain
description: Using the Android Keystore (StrongBox / TEE) and iOS Keychain / Secure Enclave for hardware-backed keys, including biometric-gated keys. Use when generating or using long-lived cryptographic keys on device.
---

# Android Keystore & iOS Keychain

## Instructions

Prefer hardware-backed keys for any long-lived cryptographic material. The key should never leave the secure element.

### 1. Why Hardware-Backed Keys

- Key material is non-extractable — a rooted / jailbroken device still cannot export the raw bytes from StrongBox or the Secure Enclave.
- OS enforces access policies (user auth, invalidation on biometric enrollment change).
- Compliance frameworks (PCI, FIDO2) increasingly require it.

### 2. Android: Generate a Key

```kotlin
val spec = KeyGenParameterSpec.Builder(
    "auth_key",
    KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY,
)
    .setDigests(KeyProperties.DIGEST_SHA256)
    .setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1"))
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationParameters(
        0, // every use requires auth
        KeyProperties.AUTH_BIOMETRIC_STRONG,
    )
    .setInvalidatedByBiometricEnrollment(true)
    .setIsStrongBoxBacked(true) // fall back if unsupported
    .build()

val kpg = KeyPairGenerator.getInstance(
    KeyProperties.KEY_ALGORITHM_EC, "AndroidKeyStore",
)
kpg.initialize(spec)
kpg.generateKeyPair()
```

Wrap `setIsStrongBoxBacked(true)` in a `try/catch` for `StrongBoxUnavailableException` and retry without StrongBox. Check `KeyInfo.isInsideSecureHardware` to confirm TEE backing.

### 3. iOS: Secure Enclave Key

```swift
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    [.privateKeyUsage, .biometryCurrentSet],
    nil
)!

let attributes: [String: Any] = [
    kSecAttrKeyType as String:       kSecAttrKeyTypeECSECPrimeRandom,
    kSecAttrKeySizeInBits as String: 256,
    kSecAttrTokenID as String:       kSecAttrTokenIDSecureEnclave,
    kSecPrivateKeyAttrs as String: [
        kSecAttrIsPermanent as String:    true,
        kSecAttrApplicationTag as String: "com.example.auth".data(using: .utf8)!,
        kSecAttrAccessControl as String:  access,
    ],
]

var error: Unmanaged<CFError>?
guard let key = SecKeyCreateRandomKey(attributes as CFDictionary, &error) else {
    throw error!.takeRetainedValue()
}
```

Secure Enclave supports only **EC P-256**. For RSA or AES, the key still lives in Keychain but is not in the SE.

### 4. Biometric-Gated Keys (Correctly)

A biometric prompt that only returns a boolean is **not** real gating — a modified app can skip it. The correct pattern:

1. Generate the key with `setUserAuthenticationRequired(true)` (Android) or `.biometryCurrentSet` (iOS).
2. Attempt a cryptographic operation (sign / decrypt).
3. The OS automatically shows the biometric prompt and only releases the key on success.
4. Use the signature / plaintext as proof of authentication.

Android Jetpack example:

```kotlin
val signature = Signature.getInstance("SHA256withECDSA").apply {
    initSign(keyStore.getKey("auth_key", null) as PrivateKey)
}
BiometricPrompt(activity, executor, callback)
    .authenticate(promptInfo, BiometricPrompt.CryptoObject(signature))
```

### 5. Key Invalidation

- Android: `setInvalidatedByBiometricEnrollment(true)` nukes the key when a new fingerprint/face is enrolled.
- iOS: `.biometryCurrentSet` does the same.

Catch `KeyPermanentlyInvalidatedException` (Android) / `errSecInvalidKeychain` and drive the user through re-enrollment.

### 6. Pitfalls

- Do **not** generate software keys (`ProviderException` fallback) silently — explicit error beats silent downgrade.
- Do **not** store the key's passphrase alongside the key.
- Do **not** share a single keystore alias across unrelated purposes; name keys per purpose (`auth_key`, `payload_enc_key`).

## Checklist

- [ ] All long-lived keys live in Keystore / Keychain — never in a file.
- [ ] Key generation falls back from StrongBox only with explicit error handling.
- [ ] Biometric gating uses a `CryptoObject` (Android) or `.biometryCurrentSet` (iOS), not a raw boolean.
- [ ] Keys are invalidated on biometric enrollment changes and the UI handles re-enrollment.
- [ ] Each key has a distinct alias / tag tied to its purpose.
- [ ] No code path silently downgrades to a software-backed key.
