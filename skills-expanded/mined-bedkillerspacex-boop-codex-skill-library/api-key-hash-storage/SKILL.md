---
name: api-key-hash-storage
description: >
  Store API keys hashed at rest for owned API platforms: generate high-entropy keys,
  display once, persist only salted hashes (or HMAC with server secret), keep prefixes
  for lookup, and verify in constant-ish time. Use when implementing partner API keys —
  not for cracking others’ key databases.
---

# API Key Hash Storage

## Scope And Authorization

- **In scope:** API platforms you build/operate.
- **Out of scope:** Offline attacking stolen key DBs you do not own.
- Treat API keys as passwords with automated use — leak impact is high.
- Pair with `api-key-lifecycle` and `code-quality-standards`.

## When To Use

- Designing `api_keys` table storage.
- Migrating from plaintext/encrypted-at-rest-only keys to **hash verification**.
- Implementing lookup by key prefix + hash compare.
- Security review of partner credential stores.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full key lifecycle (rotate/revoke) | `api-key-lifecycle` |
| Gateway validation patterns | `api-gateway-authz-patterns` |
| User password hashing policy | secrets/auth password skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Item | Guidance |
| --- | --- |
| Key entropy | ≥128 bits random (e.g. 32 bytes) |
| Display | Show full key **once** at creation |
| Storage | Hash only (argon2id/bcrypt/scrypt or HMAC-SHA256 with server pepper) |
| Prefix | Public `ak_live_3f2a…` prefix for UX + indexed lookup |
| Scopes | Stored as metadata beside hash |
| Compare | Prefer constant-time compare APIs |

**Password hashers vs HMAC:** slow hashes (argon2) throttle offline attacks if DB stolen; HMAC with pepper in KMS also common for high-QPS key checks — document trade-off.

## Workflow

### 1. Confirm success criteria

1. No plaintext keys in DB/logs; verification path clear; migration plan for existing keys.
2. QPS budget for verify (choose argon2 params or HMAC accordingly).

### 2. Generate and format

```python
import secrets
raw = secrets.token_urlsafe(32)
prefix = raw[:8]
# present: f"ak_live_{raw}" to user once
```

1. Namespace prefixes: `ak_live_`, `ak_test_`.
2. Optional checksum character to detect typos.

### 3. Persist

```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY,
  principal_id UUID NOT NULL,
  prefix VARCHAR(16) NOT NULL,      -- indexed, not secret alone
  key_hash BYTEA NOT NULL,          -- argon2/bcrypt/HMAC output
  scopes TEXT[] NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  last_used_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ
);
CREATE INDEX api_keys_prefix_idx ON api_keys(prefix);
```

```python
# Example argon2 verify path
from argon2 import PasswordHasher
ph = PasswordHasher()
key_hash = ph.hash(full_key)
# verify:
ph.verify(key_hash, presented_key)
```

**HMAC variant (high QPS):**

```python
import hmac, hashlib
digest = hmac.new(PEPPER, full_key.encode(), hashlib.sha256).digest()
# store digest; pepper in KMS/HSM only
```

### 4. Authenticate request

```text
1. Read key from Authorization: Bearer / X-API-Key
2. Extract prefix; SELECT candidates by prefix (+ principal if known)
3. Verify hash/HMAC
4. Check revoked_at, scopes, IP allowlist
5. Update last_used_at asynchronously
```

1. Do not log full keys — log prefix + key id only.
2. Rate-limit failed verifications per IP/prefix.

### 5. Migration from plaintext

1. Dual-write: on successful plaintext match, rehash and clear plaintext column.
2. Deadline to disable plaintext path.
3. Force rotate keys that never logged in if needed.

### 6. Verify

```bash
# Unit tests: wrong key fails; right key passes; revoked fails
# Grep codebase/SQL dumps for ak_live_ full secrets
rg -n "ak_live_[A-Za-z0-9_-]{20,}" .
```

### 7. Hand off

1. Document algorithm params and pepper location.
2. Tie to lifecycle: rotate creates new hash row; old revoke.
3. Incident: DB leak → rotate all keys; pepper rotation procedure.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rest | Hash/HMAC only | Plaintext keys column |
| Logs | Prefix + id | Full `X-API-Key` |
| Lookup | Prefix index | Full table scan bcrypt all rows |
| Entropy | 32+ random bytes | 6-char “keys” |

## Output Checklist

- [ ] Generation entropy sufficient
- [ ] One-time display UX
- [ ] Hash/HMAC + prefix storage implemented
- [ ] Verify path + revoke check
- [ ] Logging redaction verified
- [ ] Migration plan if legacy plaintext
- [ ] Tests for success/fail/revoke
- [ ] Linked to lifecycle skill
- [ ] `code-quality-standards` applied

## Rules

- Never store API keys in recoverable form without explicit crypto design + key escrow policy (prefer non-recoverable hash).
- Pepper/KMS material is crown jewel.
- Pair with rotation and least-scope keys.
- Do not attempt to crack third-party key stores.
- Fail authentication closed on parse errors.
