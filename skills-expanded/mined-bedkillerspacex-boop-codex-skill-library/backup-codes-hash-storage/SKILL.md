---
name: backup-codes-hash-storage
description: >
  Cryptographic storage and verification of MFA backup/recovery codes for owned
  apps: salted hashing or HMAC, constant-time compare, single-use consumption,
  and migration from plaintext. Use when implementing hash-at-rest for backup
  codes — not for cracking others’ codes or offline attacking password dumps
  without authorization.
---

# Backup Codes Hash Storage

## Scope And Authorization

- **In scope:** Auth systems you own where backup codes are persisted.
- **Out of scope:** Offline cracking of third-party credential dumps; abusing recovery flows.
- Hash parameters must resist brute force of high-entropy codes and low-entropy if UX weakens entropy.
- Pair lifecycle/UX with `backup-code-storage`; use `code-quality-standards` for crypto code.

## When To Use

- Choosing bcrypt/scrypt/Argon2id vs HMAC-SHA-256 for backup codes.
- Migrating plaintext or reversible encrypted codes to non-reversible hashes.
- Implementing verify-and-consume without timing leaks.
- Reviewing whether pepper/HMAC server secret is appropriate.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| UX, regen, rate limits, one-time display | `backup-code-storage` |
| General secrets platform | `secrets-management-hygiene` |
| Password hashing policy org-wide | password/auth skills as applicable |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Approach | When |
| --- | --- |
| Argon2id / scrypt / bcrypt | Human-memorable or shorter codes; memory-hard KDF |
| HMAC-SHA-256 + pepper | High-entropy random codes; fast verify at scale |
| SHA-256 alone unsalted | **Never** for codes |
| Reversible encrypt | Avoid; forces key management & disclosure risk |
| Tooling | libsodium, Python `hashlib`/`hmac`, Go `golang.org/x/crypto`, audit tests |

## Workflow

### 1. Confirm scope and success criteria

1. Code alphabet/length, count per user, QPS on redeem, threat model, authorization.
2. Success: DB has no plaintext; verify works; wrong codes fail in constant-ish time; used codes unusable.
3. Migration plan for existing rows.

### 2. Inventory storage format

```bash
rg -n "backup_code|recovery_code|mfa_code" --glob '*.{go,py,ts,js,java,cs}'
# Inspect schema: code, code_hash, salt, consumed_at
```

1. Note algorithm identifiers stored per row (for future rotation).
2. Check whether one hash row per code (preferred) or combined blob.
3. Confirm pepper location (KMS/HSM/env) if used.

### 3. Baseline crypto choice

| Code entropy | Prefer |
| --- | --- |
| ≥ 128 bits random | HMAC-SHA-256 with server pepper OK |
| Weaker / user-visible short | Argon2id with per-code salt |
| Unknown legacy | Assume weak → KDF |

### 4. Implement hash + verify

**Per-code salted KDF (sketch):**

```text
salt = CSPRNG(16)
hash = Argon2id(code, salt, params)
store {alg, params, salt, hash, consumed=false}
```

**HMAC pepper (high entropy codes):**

```text
hash = HMAC_SHA256(pepper, normalize(code))
store {alg: "hmac-sha256-v1", hash, consumed=false}
# pepper in KMS; not in DB
```

```python
import hmac, hashlib, secrets

def normalize(code: str) -> str:
    return code.strip().replace(" ", "").upper()

def hash_code(code: str, pepper: bytes) -> str:
    return hmac.new(pepper, normalize(code).encode(), hashlib.sha256).hexdigest()

def verify(code: str, pepper: bytes, stored_hex: str) -> bool:
    digest = hash_code(code, pepper)
    return hmac.compare_digest(digest, stored_hex)
```

1. **Normalize** consistently (case, dashes) before hash; document UX format.
2. On success: mark consumed in same DB transaction; never leave reusable.
3. Optional: store only prefix index for rate-limit buckets — never store recoverable code.
4. Migration: on successful plaintext match (legacy), rehash and delete plaintext column.
5. Pepper rotation: dual-verify old/new pepper versions with `alg` field.

### 5. Verify with evidence

1. Unit tests: normalize variants; one-time consume; wrong code false.
2. Timing: use constant-time compare primitives (not `==` on strings).
3. DB fixture: no plaintext codes in any environment dump sample.
4. Load: redeem latency acceptable under Argon2 params for your QPS (or scale workers).

### 6. Observe and harden

1. Metrics: verify fail rate, alg versions in use, migration residual plaintext count=0.
2. Alert if plaintext column reappears in schema migrations.
3. KMS permission for pepper least privilege.

### 7. Hand off

1. Document alg, params, normalize rules, pepper versioning.
2. Threat model note: stolen DB + stolen pepper = offline verify capability → protect pepper.
3. Link UX skill for generation and rate limits.

## Algorithm Comparison

| Property | Argon2id | HMAC+pepper |
| --- | --- | --- |
| Offline without pepper | Hard | Easy if no pepper |
| Pepper theft impact | Still need salts/hashes | Full offline verify of codes |
| CPU cost | High | Low |
| Fit | Shorter codes | Long random codes |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Compare | `compare_digest` / `Subtle.ConstantTimeCompare` | `hash == input` |
| Salt | Per code | Global salt only |
| Storage | alg + params + hash | Raw SHA of code |
| Consume | Atomic flag | Delete race double-use |
| Pepper | KMS-backed | Pepper in same table |

## Output Checklist

- [ ] Algorithm chosen and justified for entropy
- [ ] Normalize rules documented
- [ ] Constant-time verify implemented
- [ ] Single-use consumption atomic
- [ ] No plaintext at rest (migrated)
- [ ] Pepper/KMS handling documented if used
- [ ] Tests cover success/fail/reuse
- [ ] Metrics for failures and alg versions
- [ ] `code-quality-standards` applied

## Rules

- Authorized auth development only.
- Never store plaintext backup codes.
- Prefer constant-time compares always.
- Protect peppers like master keys.
- Do not use this skill to attack third-party hashes.
