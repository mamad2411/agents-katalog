---
name: biometric-auth
description: Biometric authentication on mobile using BiometricPrompt and LAContext, with keys cryptographically gated by user biometry. Use when adding unlock, re-auth, or step-up auth flows.
---

# Biometric Authentication on Mobile

## Instructions

Biometric auth on mobile is only meaningful when it is **bound to a cryptographic operation**. A biometric prompt that merely returns `true` can be bypassed by a patched binary.

### 1. Threat Model

Biometrics protect against:
- Casual device sharing.
- Lost / stolen devices where the PIN is strong.
- Local attackers without the user's finger/face.

Biometrics do **not** protect against:
- A compromised app process (same binary asking for biometry).
- A coerced user.
- Fingerprint false accepts on cheap sensors (rare but non-zero).

### 2. Android: BiometricPrompt (Class 3 / Strong)

```kotlin
// Require Class 3 (Strong) biometrics so a CryptoObject is usable.
val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Authenticate")
    .setSubtitle("Sign in to Example")
    .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG)
    .setNegativeButtonText("Cancel")
    .build()

val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply {
    init(Cipher.ENCRYPT_MODE, keyStore.getKey("token_key", null) as SecretKey)
}

BiometricPrompt(activity, mainExecutor, object : BiometricPrompt.AuthenticationCallback() {
    override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
        val c = result.cryptoObject?.cipher ?: return
        val ciphertext = c.doFinal(tokenBytes) // only succeeds post-biometry
        store(ciphertext, c.iv)
    }
}).authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
```

The key must be generated with `setUserAuthenticationRequired(true)` and `KeyProperties.AUTH_BIOMETRIC_STRONG`.

### 3. iOS: LAContext + Secure Enclave

```swift
let context = LAContext()
context.localizedReason = "Sign in to Example"

var error: NSError?
guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
    throw BioError.unavailable(error)
}

// Key generated with .biometryCurrentSet (see keystore-keychain skill).
let privateKey: SecKey = try loadAuthKey()

// Signing operation transparently triggers the biometric prompt.
let signature = try SecKeyCreateSignature(
    privateKey, .ecdsaSignatureMessageX962SHA256,
    payload as CFData, nil
) as Data? ?? { throw BioError.sign }()
```

Prefer `.deviceOwnerAuthenticationWithBiometrics` only. Using `.deviceOwnerAuthentication` (which falls back to PIN) changes your threat model — PIN is typically much weaker than Face/Touch ID.

### 4. Invalidation on Enrollment Changes

Always set:

- Android: `setInvalidatedByBiometricEnrollment(true)`.
- iOS: `.biometryCurrentSet` (not `.biometryAny`).

This guarantees that adding a new fingerprint/face invalidates your key, forcing a re-auth.

Handle the resulting exception (`KeyPermanentlyInvalidatedException` / `errSecItemNotFound`) by walking the user through re-enrollment rather than crashing.

### 5. What Biometric Unlock Should Actually Do

A correct biometric unlock flow:

1. On first login, derive / receive a secret (e.g., the refresh token).
2. Encrypt it with a biometric-gated key and store the ciphertext.
3. On next launch, attempt to decrypt → this triggers the biometric prompt.
4. Use the plaintext to resume the session.

A **wrong** flow: `if (fingerprintOk) showHomeScreen()` — easily bypassable.

### 6. React Native / Flutter

- React Native: `react-native-keychain` with `accessControl: BIOMETRY_CURRENT_SET` combined with `storage: KEYCHAIN` (iOS) / `AES_GCM` (Android) provides the same cryptographic gating.
- Flutter: `local_auth` is **only** a boolean check — pair it with `flutter_secure_storage` using `KeychainAccessibility.first_unlock_this_device` and an `iOptions`/`aOptions` entry that requires authentication.

### 7. UX

- Offer a PIN / password fallback for users who can't or won't enroll biometry.
- Never silently fall back from biometry → PIN without telling the user.
- Rate-limit repeated failures on your side; the OS already does basic lockout but your server-side session should also detect anomalies.

## Checklist

- [ ] Biometric auth gates a cryptographic operation (decrypt or sign), not a boolean.
- [ ] Key uses `BIOMETRIC_STRONG` / `.biometryCurrentSet`.
- [ ] Key is invalidated on new biometric enrollment and UI handles re-enrollment.
- [ ] No `.deviceOwnerAuthentication` (PIN fallback) unless the threat model allows it.
- [ ] Fallback to PIN / password is offered and clearly signposted.
- [ ] Failure paths do not leak whether the user exists or not.
