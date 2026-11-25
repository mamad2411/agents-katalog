---
name: secure-storage
description: Secrets, JWT access/refresh rotation, certificate pinning, biometric gating for Flutter apps. MANDATORY TRIGGERS - "secure storage", "JWT", "token", "refresh token", "keychain", "keystore", "biometric", "certificate pinning", "TLS pin", "secret".
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Skill: secure-storage

## When to use

Storing or reading tokens, secrets, or PII. Configuring Dio with
auth or pinning. Adding biometric gating.

## Storage

- `flutter_secure_storage` only for tokens & secrets:
  ```dart
  const FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
    iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
  );
  ```
- Never put tokens in `shared_preferences`, files, or logs.
- Wipe secure storage on logout / token revocation.

## JWT lifecycle

- Access token: short-lived (<= 15 min), in memory + secure storage.
- Refresh token: long-lived, rotates on every use, single-use.
- 401 handling: `AuthInterceptor` enqueues retries, performs one
  refresh, replays queued requests. Implement with a `Completer`
  (single-flight).
- On refresh failure: clear storage, emit `AuthSessionExpired` effect,
  navigate to login.

## Certificate pinning

- Production builds pin against the API certificate **and** a backup
  pin. Implement via `http_certificate_pinning` or custom adapter.
- Pin rotation plan: ship new pin in build N before retiring old in
  build N+1. Track in `docs/memory/security.md`.

## Biometric

- Use `local_auth`. Gate access to "remember me" / quick-unlock only.
- Always fall back to password; never block sign-in solely on
  biometrics.

## Forbidden

- `badCertificateCallback: (_, __, ___) => true`
- Logging tokens, even at `debug`.
- Storing PII in plain-text caches.

## Output checklist

- [ ] Token paths covered by `secure_storage` reads/writes
- [ ] 401 single-flight refresh wired
- [ ] Pin (+ backup pin) configured for prod flavor
- [ ] Logout wipes everything sensitive

## See also

- `threat-modeling`
