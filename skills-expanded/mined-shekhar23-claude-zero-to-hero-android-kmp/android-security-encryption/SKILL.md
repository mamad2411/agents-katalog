---
name: android-security-encryption
description: |
  Android security and encryption patterns - encrypted local storage, biometrics, keystore usage, secret boundaries, secure backups, and handling sensitive user data. Use this skill whenever storing sensitive local data, protecting secrets, adding biometric unlock, or deciding whether data needs encryption at rest. Trigger on phrases like "encryption", "Keystore", "biometric", "secure storage", "encrypted preferences", "sensitive data", or "protect local data".
---

# Android Security and Encryption

## Core Principles

- Encrypt sensitive local data only when the threat model justifies it.
- Keep secrets out of source control and out of logs.
- Minimize what is stored locally in the first place.
- Prefer platform-backed security primitives over custom crypto.
- Security decisions should be explicit and documented, not accidental.

---

## What Usually Needs Protection

Typical sensitive data:
- auth/session secrets
- refresh tokens
- locally cached private user data when risk is meaningful
- API credentials used only for local dev tooling, not production runtime
- cryptographic keys and encrypted file metadata

Usually not worth heavy encryption by itself:
- theme settings
- sort order
- onboarding flags
- non-sensitive feature toggles

See the **android-datastore-preferences** and **android-auth-security** skills for adjacent storage guidance.

---

## Use Platform Security First

Prefer:
- Android Keystore for key management
- platform biometric/device credential prompts for local unlock
- vetted libraries/APIs for encrypted storage

Avoid:
- inventing custom encryption schemes
- hardcoding keys in app code
- storing raw secrets unencrypted in SharedPreferences or plain files

---

## Keystore Boundary

The Keystore should manage keys, not your whole app architecture.

Good pattern:
- generate/store a key alias in Keystore
- use it to wrap or protect local sensitive values
- keep higher-level repositories unaware of crypto details when possible

Bad pattern:
- sprinkling crypto calls through screens and ViewModels

---

## Repository Boundary

Wrap secure storage behind abstractions:

```kotlin
interface SecureStorage {
    suspend fun putString(key: String, value: String)
    suspend fun getString(key: String): String?
    suspend fun remove(key: String)
}
```

Higher layers should depend on a secure storage abstraction, not directly on cipher setup or Keystore APIs.

---

## Biometrics

Use biometrics as a local convenience gate, not as a replacement for server-side auth.

Good uses:
- unlock locally cached session
- re-enter sensitive area
- confirm sensitive local action

Bad uses:
- silently replaying stored passwords
- treating biometric success as app-wide backend authorization

Biometric flows should fail gracefully when:
- hardware is unavailable
- biometrics are not enrolled
- the user cancels
- the device falls back to PIN/password

---

## Encryption at Rest

Ask before encrypting everything:
- what data is truly sensitive?
- what attack are we mitigating?
- what is the UX cost?
- what keys are used and where are they stored?

Encrypt only the data that needs it. Broad indiscriminate encryption adds complexity and can hurt reliability without improving actual security much.

---

## Logging and Analytics Redaction

Never log:
- plaintext secrets
- decrypted payloads
- tokens
- encryption keys or aliases tied to secrets
- biometric prompt results beyond minimal safe state

Telemetry must remain redaction-safe. See the **android-analytics-logging** skill.

---

## Backups and Export

Consider whether sensitive data should be:
- excluded from backups
- cleared on logout
- invalidated on account switch
- re-derived after reinstall instead of restored blindly

Security-sensitive local state often should not survive all restore flows unchanged.

---

## Failure Handling

Design for failure states:
- secure storage unavailable
- key invalidated after device security change
- biometric prompt cancelled
- encrypted payload corrupted
- migration from old storage failed

These should produce safe fallback behavior, not silent data loss when avoidable.

---

## Testing Guidance

Test:
- repository behavior when secure reads/writes succeed or fail
- logout/account switch clearing sensitive state
- fallback behavior when biometrics or keys are unavailable
- migration from old insecure storage if supported

Keep crypto implementation details isolated so most tests can use fakes.

---

## Checklist: Adding Secure Local Storage

- [ ] Confirm the data truly needs encryption or secure gating
- [ ] Use platform-backed key management instead of custom crypto
- [ ] Hide crypto details behind a storage abstraction
- [ ] Clear sensitive state on logout or account switch
- [ ] Redact secrets from logs, analytics, and crash reports
- [ ] Handle unavailable, invalidated, or corrupted secure state safely