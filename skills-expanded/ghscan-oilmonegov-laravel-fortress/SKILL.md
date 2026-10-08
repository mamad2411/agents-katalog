---
description: "Laravel Fortress Part 2 — Cryptography & Data Protection. 12 sections, 109 checks covering Encryption, hashing, key management, PII, TLS, secrets."
---

# Fortress: Cryptography & Data Protection

> Part II of The Laravel Fortress — 12 sections · 109 checks
> https://github.com/oilmonegov/laravel-fortress/blob/main/parts/02-cryptography-data-protection.md

When writing or reviewing code, enforce these rules.
Check `.fortress.yml` in the project root for overrides.

## Project Awareness

Before enforcing rules, read `composer.json` and `package.json` to detect the project's PHP version,
Laravel version, and installed packages. Skip rules whose conditions don't match the detected stack.

## Rules

### Password Hashing

[F-P02-001] **CRITICAL** — Use `Hash::make()` for passwords
[F-P02-002] **CRITICAL** — Prefer Argon2id over bcrypt
[F-P02-003] **CRITICAL** — Tune hash parameters for 200-500ms on your hardware
[F-P02-004] **CRITICAL** — Use `Hash::needsRehash()` for transparent upgrades
[F-P02-005] **CRITICAL** — Never use for passwords

### Bcrypt Limitations

[F-P02-006] **CRITICAL** — bcrypt silently truncates at 72 bytes
[F-P02-007] **CRITICAL** — bcrypt has a null byte issue

### Encryption

[F-P02-008] **CRITICAL** — `APP_KEY` is critical — rotate periodically
[F-P02-009] **CRITICAL** — Use `APP_PREVIOUS_KEYS` for key rotation
[F-P02-010] **CRITICAL** — Encrypt sensitive model attributes
[F-P02-011] **CRITICAL** — Use `Crypt::encryptString()` for application-level encryption
[F-P02-012] **CRITICAL** — Use `php artisan env:encrypt` for encrypted `.env` in CI/CD

### Tokens & Random Generation

[F-P02-013] **CRITICAL** — Use `Str::random()` or `random_bytes()` for security tokens
[F-P02-014] **CRITICAL** — Never use `rand()`, `mt_rand()`, `array_rand()`, `uniqid()`, `microtime()`, or `md5(time())` for tokens

### Signed URLs & HMAC

[F-P02-015] **CRITICAL** — Use signed routes for sensitive links
[F-P02-016] **CRITICAL** — Use temporary signed URLs with short expiration
[F-P02-017] **CRITICAL** — Validate webhook signatures with `hash_equals()`
[F-P02-018] **CRITICAL** — Never use `==` or `===` to compare hashes/tokens

### What NOT To Do with Cryptography

[F-P02-019] **CRITICAL** — Never roll your own encryption algorithm
[F-P02-020] **CRITICAL** — Never use ECB mode
[F-P02-021] **CRITICAL** — Never store encryption keys in code or version control
[F-P02-022] **CRITICAL** — Never reuse IVs/nonces
[F-P02-023] **CRITICAL** — Never use `base64_encode()` as "encryption"

### Password & Credential Management

[F-P02-024] **CRITICAL** — Minimum password length: 12 characters
[F-P02-025] **CRITICAL** — Maximum password length: 128 characters
[F-P02-026] **CRITICAL** — Check against breached password lists
[F-P02-027] **CRITICAL** — No password composition rules
[F-P02-028] **CRITICAL** — Rate limit login attempts
[F-P02-029] **CRITICAL** — Constant-time password comparison
[F-P02-030] **CRITICAL** — Never display passwords in logs, responses, or error messages
[F-P02-031] **CRITICAL** — Session invalidation on password change
[F-P02-032] **CRITICAL** — `$dontFlash` includes password fields

### Two-Factor Authentication (2FA) Depth

[F-P02-033] **CRITICAL** — Enforce 2FA for all users (or admin+ roles)
[F-P02-034] **CRITICAL** — TOTP over SMS
[F-P02-035] **CRITICAL** — Store 2FA secrets encrypted
[F-P02-036] **CRITICAL** — Generate and store recovery codes
[F-P02-037] **CRITICAL** — Rate limit 2FA verification attempts
[F-P02-038] **CRITICAL** — Reconfirmation for sensitive operations
[F-P02-039] **CRITICAL** — 2FA confirmation timestamp
[F-P02-040] **CRITICAL** — Backup code usage alerts
[F-P02-041] **CRITICAL** — `inputmode="numeric"` on OTP fields

### Logging Sensitive Data Prevention

[F-P02-042] **CRITICAL** — Never log passwords
[F-P02-043] **CRITICAL** — Never log credit card numbers
[F-P02-044] **CRITICAL** — Never log API keys or tokens
[F-P02-045] **CRITICAL** — Never log session IDs
[F-P02-046] **CRITICAL** — Never log PII unnecessarily
[F-P02-047] **CRITICAL** — Redact request logging
[F-P02-048] **CRITICAL** — Configure `$dontReport` for noisy exceptions
[F-P02-049] **CRITICAL** — Log levels are appropriate
[F-P02-050] **CRITICAL** — Structured context, not string interpolation
[F-P02-051] **CRITICAL** — Log rotation configured

### Key Management & Rotation

[F-P02-052] **CRITICAL** — `APP_KEY` rotation uses `APP_PREVIOUS_KEYS`
[F-P02-053] **CRITICAL** — Schedule key rotation
[F-P02-054] **CRITICAL** — Database encrypted columns re-encrypt on rotation
[F-P02-055] **CRITICAL** — Never store `APP_KEY` in version control
[F-P02-056] **CRITICAL** — Separate encryption keys per purpose
[F-P02-057] **CRITICAL** — Key destruction procedure
[F-P02-058] **CRITICAL** — HSM for high-value keys

### TLS & Certificate Management

[F-P02-059] **CRITICAL** — TLS 1.2 minimum, TLS 1.3 preferred
[F-P02-060] **CRITICAL** — Strong cipher suites only
[F-P02-061] **CRITICAL** — Auto-renew certificates
[F-P02-062] **CRITICAL** — Monitor expiration
[F-P02-063] **CRITICAL** — OCSP stapling enabled
[F-P02-064] **CRITICAL** — Certificate Transparency logs
[F-P02-065] **CRITICAL** — Internal services use TLS too
[F-P02-066] **CRITICAL** — No self-signed in production

### Data Classification & Handling Tiers

[F-P02-067] **CRITICAL** — Tier 1 — Public
[F-P02-068] **CRITICAL** — Tier 2 — Internal
[F-P02-069] **CRITICAL** — Tier 3 — Confidential
[F-P02-070] **CRITICAL** — Tier 4 — Restricted
[F-P02-071] **CRITICAL** — Every model/table has a classification
[F-P02-072] **CRITICAL** — Access logging scales with tier
[F-P02-073] **CRITICAL** — Retention policies per tier
[F-P02-074] **CRITICAL** — Data flow diagrams

### PII Detection & Anonymization

[F-P02-075] **CRITICAL** — Identify all PII fields
[F-P02-076] **CRITICAL** — `$hidden` on sensitive model attributes
[F-P02-077] **CRITICAL** — Anonymize in non-production environments
[F-P02-078] **CRITICAL** — Right to erasure (GDPR Article 17)
[F-P02-079] **CRITICAL** — No PII in URLs
[F-P02-080] **CRITICAL** — No PII in log messages
[F-P02-081] **CRITICAL** — PII inventory maintained

### Tokenization & Data Masking

[F-P02-082] **CRITICAL** — Tokenize payment card numbers
[F-P02-083] **CRITICAL** — Mask in display
[F-P02-084] **CRITICAL** — Mask in logs
[F-P02-085] **CRITICAL** — Distinct tokenization per purpose
[F-P02-086] **CRITICAL** — Token-to-original mapping stored securely
[F-P02-087] **CRITICAL** — No reversible tokenization without access control

### At-Rest Encryption Strategies

[F-P02-088] **CRITICAL** — Use Laravel `encrypted` cast for sensitive model fields
[F-P02-089] **CRITICAL** — Encrypted fields are not searchable
[F-P02-090] **CRITICAL** — Database-level encryption (TDE)
[F-P02-091] **CRITICAL** — Backup encryption
[F-P02-092] **CRITICAL** — File storage encryption
[F-P02-093] **CRITICAL** — Key separation
[F-P02-094] **CRITICAL** — Test that decryption fails gracefully

### Secrets Management (Vault / Cloud)

[F-P02-095] **CRITICAL** — No secrets in `.env` files on servers
[F-P02-096] **CRITICAL** — No secrets in environment variables visible to `phpinfo()`
[F-P02-097] **CRITICAL** — Rotate secrets on personnel change
[F-P02-098] **CRITICAL** — Least privilege for secret access
[F-P02-099] **CRITICAL** — Audit secret access
[F-P02-100] **CRITICAL** — Cache secrets in memory, not disk
[F-P02-101] **CRITICAL** — Secret versioning
[F-P02-102] **CRITICAL** — Emergency rotation procedure documented

### Cryptographic Agility

[F-P02-103] **CRITICAL** — Abstract crypto operations behind interfaces
[F-P02-104] **CRITICAL** — `Hash::needsRehash($hash)`
[F-P02-105] **CRITICAL** — Config-driven algorithm selection
[F-P02-106] **CRITICAL** — Document current algorithms
[F-P02-107] **CRITICAL** — Migration path for algorithm changes
[F-P02-108] **CRITICAL** — No custom cryptography
[F-P02-109] **CRITICAL** — Post-quantum readiness
