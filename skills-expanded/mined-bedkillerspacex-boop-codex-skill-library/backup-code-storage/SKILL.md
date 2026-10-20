---
name: backup-code-storage
description: >
  Secure storage of MFA/account backup (recovery) codes for owned applications:
  generation UX, one-time display, encrypted or hashed at rest, inventory rate
  limits, and regeneration flows. Use when implementing or reviewing backup code
  features — not for stealing recovery codes or bypassing others’ MFA.
---

# Backup Code Storage (Application Recovery Codes)

## Scope And Authorization

- **In scope:** Applications you own where users receive MFA backup/recovery codes.
- **Out of scope:** Using recovery codes against accounts without authorization; phishing for codes.
- Backup codes are equivalent to passwords — protect like credentials.
- Prefer hash storage skill detail in `backup-codes-hash-storage`; use `code-quality-standards` for implementation.

## When To Use

- Adding “download backup codes” to an auth product.
- Reviewing how recovery codes are stored, shown, and rotated.
- Incident: plaintext recovery codes in DB logs or support tools.
- Designing regeneration (invalidate old set) and rate limits.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Hashing/verification specifics | `backup-codes-hash-storage` |
| Account takeover methodology (authorized testing) | `account-takeover-methodology` |
| Secrets management platform | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concern | Guidance |
| --- | --- |
| Generate | High entropy (e.g. 8–12 codes × 8–10 chars, CSPRNG) |
| Display | Once at creation; force download/copy; then never show full set again |
| Storage | Hash at rest (see companion skill); encrypt if reversible required (avoid) |
| Use | Single-use; constant-time compare; rate limit |
| Regen | Replace entire set; audit event |
| Tooling | Auth service DB, KMS for any encryption keys, audit logs |

## Workflow

### 1. Confirm scope and success criteria

1. Product, MFA methods, compliance needs, authorization to change auth.
2. Success: codes work once; plaintext not retrievable from DB; abuse rate-limited.
3. Support process: no reading user codes from admin panel.

### 2. Inventory current implementation

```bash
# Repo search
rg -n "backup.?code|recovery.?code|mfa.?code" --glob '!node_modules'
# DB schema review: columns storing codes
# Logs: ensure codes not logged
```

1. Determine plaintext vs hashed vs encrypted storage.
2. Check if used codes are deleted or marked consumed.
3. Admin/support APIs that might return codes.

### 3. Baseline threat model

| Threat | Mitigation |
| --- | --- |
| DB dump | Hash codes; no plaintext |
| Support abuse | No code read API; identity-proofed reset instead |
| Brute force | Rate limit + lockout + long codes |
| Phishing | UX education; bind to session carefully |
| Reuse | Single-use + regen invalidates old |

### 4. Implement secure storage lifecycle

1. Generate with CSPRNG; reject low-entropy custom codes.
2. Show once in UI; optional PDF/TXT download over HTTPS only.
3. Persist **hashes** (or HMAC with server secret) — see `backup-codes-hash-storage`.
4. On redeem: rate-limit by account+IP; constant-time compare; mark consumed in same transaction.
5. On regen: wipe previous hashes; emit security event; optionally notify email.
6. Never put codes in analytics, email (except secure delivery product decisions with caution), or CDN logs.

```text
// Pseudocode
codes = [random() for _ in 1..10]
store(user, [hash(c) for c in codes])
return codes to client once
```

### 5. Verify with evidence

1. Unit: redeem succeeds once, second attempt fails.
2. DB inspection: only hashes present.
3. Log review: no code material.
4. Rate limit test: burst redeem attempts blocked.
5. Admin API cannot fetch codes.

### 6. Observe and harden

1. Metrics: redeem success/fail, regen counts, rate-limit hits.
2. Alerts on mass redeem failures (credential stuffing).
3. Periodic review of support tooling access.

### 7. Hand off

1. UX copy for users to store codes offline securely.
2. Runbook for lost MFA without codes (identity verification).
3. Link hashing details skill for crypto parameters.

## UX Checklist

| Step | Requirement |
| --- | --- |
| Create | Explicit user action; acknowledge stored offline |
| Display | One-time; mask in UI after leave page |
| Download | HTTPS; no third-party script scrape |
| Regen | Warn that old codes die |
| Redeem | Clear errors without user enumeration extras |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Storage | Salted hashes / HMAC | Plaintext column |
| Display | Once | “View my codes” anytime from DB |
| Use | Single-use | Reusable codes |
| Support | Identity proof + reset MFA | Agent reads codes aloud |
| Logging | Event only | `printf(code)` |

## Output Checklist

- [ ] Threat model documented
- [ ] Generation entropy adequate
- [ ] One-time display enforced
- [ ] At-rest protection (hash preferred) implemented
- [ ] Single-use + rate limits verified
- [ ] Regen invalidates old set
- [ ] No admin plaintext read path
- [ ] Logs clean of code material
- [ ] `code-quality-standards` applied

## Rules

- Authorized product development/review only.
- Treat backup codes as passwords.
- Prefer non-reversible storage.
- Never exfiltrate user codes.
- Rate-limit and audit all redeem/regen operations.
