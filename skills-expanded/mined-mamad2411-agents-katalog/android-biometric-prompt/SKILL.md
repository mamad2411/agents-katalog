---
name: android-biometric-prompt
description: >
  Android BiometricPrompt integration for owned apps: authenticators, crypto-based
  binding (BiometricPrompt + Cipher/Keystore), negative buttons, fallback, and common
  pitfalls (UI-only checks, weak authenticators, key invalidation). Use when adding
  fingerprint/face unlock to secure features — not for bypassing biometrics on third-party apps.
---

# Android BiometricPrompt

## Scope And Authorization

- **In scope:** Apps you develop or are authorized to security-review.
- **Out of scope:** Bypassing biometrics on apps you do not own; producing malware lockscreen bypasses.
- Test on real devices; emulator biometric support varies.
- Pair with `code-quality-standards` and `android-credential-manager` when using modern credential APIs.

## When To Use

- Gate app secrets or actions behind biometric authentication.
- Binding keys in Android Keystore to user presence / biometric auth.
- Migrating from deprecated FingerprintManager APIs.
- Reviewing whether “biometric” is **cryptographic** or cosmetic.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Credential Manager / passkeys | `android-credential-manager` |
| Play Integrity / SafetyNet | `android-safetynet-play-integrity` |
| General pentest tricks | `android-pentesting-tricks` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Meaning |
| --- | --- |
| BiometricPrompt | System UI for biometric (and optional device credential) |
| Authenticators | BIOMETRIC_STRONG / WEAK, DEVICE_CREDENTIAL |
| CryptoObject | Cipher/Mac/Signature tied to Keystore key requiring auth |
| Negative button | Cancel / use password path |
| Key invalidation | New biometric enrollment may invalidate keys if configured |
| UI-only anti-pattern | `onAuthenticationSucceeded` without unlocking a key |

## Workflow

### 1. Confirm threat model and success criteria

1. Record what is protected (session re-auth, decrypt local tokens, approve payment).
2. Success: sensitive key ops require successful biometric (or allowed device credential); no silent success path; lockout handled.
3. Decide if device credential fallback is allowed.

### 2. Choose authenticator strength

```kotlin
val authenticators = BiometricManager.Authenticators.BIOMETRIC_STRONG
// or BIOMETRIC_STRONG or DEVICE_CREDENTIAL when policy allows PIN/pattern fallback
val can = BiometricManager.from(context)
    .canAuthenticate(authenticators)
```

| Strength | Use |
| --- | --- |
| BIOMETRIC_STRONG | Prefer for crypto-bound secrets Class 3 |
| BIOMETRIC_WEAK | Convenience; not for high-value crypto without review |
| DEVICE_CREDENTIAL | PIN/pattern/password fallback |

### 3. Prefer crypto-bound biometric

```kotlin
// Sketch: Keystore AES key with setUserAuthenticationRequired(true)
val keyGen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
val spec = KeyGenParameterSpec.Builder(
    "app_bio_key",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setInvalidatedByBiometricEnrollment(true)
    .build()
keyGen.init(spec)
keyGen.generateKey()

// Init Cipher and pass BiometricPrompt.CryptoObject(cipher)
```

1. Decrypt tokens only after `onAuthenticationSucceeded` **with** CryptoObject unlocking the cipher.
2. Do not store master secrets in SharedPreferences gated only by a boolean “bio ok.”

### 4. Wire BiometricPrompt UI

```kotlin
val prompt = BiometricPrompt(activity, executor, callback)
val info = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Confirm it is you")
    .setSubtitle("Unlock secure storage")
    .setAllowedAuthenticators(authenticators)
    // setNegativeButtonText required when device credential not allowed
    .build()
prompt.authenticate(info, BiometricPrompt.CryptoObject(cipher))
```

1. Handle error codes: lockout, no hardware, none enrolled, user cancel.
2. Offer app password path if product requires, with rate limits.

### 5. Review pitfalls

| Pitfall | Fix |
| --- | --- |
| UI-only biometric | Bind Keystore keys |
| Accepting WEAK for payments | Raise authenticator / step-up server-side |
| Ignoring enrollment change | `setInvalidatedByBiometricEnrollment(true)` + re-provision |
| Auth on wrong thread | Use main executor patterns per docs |
| Logging biometric data | Never log raw biometric material (you should not receive it) |

### 6. Verify

```bash
adb shell dumpsys package your.package.name | rg -i biometric
# Manual: enroll bio, decrypt flow, remove bio, confirm fail + re-enroll path
# Manual: background app mid-prompt; ensure no partial unlock
```

1. Instrumented tests limited; prefer device QA checklist.
2. Security review: static check for `FingerprintManager` legacy and for success callbacks without crypto.

### 7. Hand off

1. Document authenticator policy and key invalidation behavior.
2. Server still authorizes high-risk actions (biometric is local step-up).
3. Align copy with UX for lockout and fallback.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Binding | Keystore + CryptoObject | `if (bioSuccess) showBalance()` |
| Strength | STRONG for secrets | WEAK for anything high value |
| Fallback | Explicit product policy | Silent skip if no biometric |
| Invalidation | Re-enroll re-wrap secrets | Keys work for attacker-added biometrics when not intended |

## Output Checklist

- [ ] Protected assets and authenticator policy documented
- [ ] Crypto-bound keys for sensitive data
- [ ] PromptInfo configured (negative button / device credential)
- [ ] Error/lockout/fallback handled
- [ ] Enrollment invalidation behavior tested
- [ ] No UI-only biometric gate for secrets
- [ ] QA on physical devices
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only; no third-party biometric bypass work.
- Treat biometric as local UX + key unlock, not server identity alone.
- Prefer STRONG + Keystore for secrets.
- Never store or log biometric templates (OS-managed).
- Coordinate with Credential Manager when migrating to passkeys.
