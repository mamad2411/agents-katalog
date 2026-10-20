---
name: hash-crypto
description: Compute SHA/MD5 hashes, HMAC, bcrypt hashes, and parse or verify JWT tokens. Use when debugging auth, comparing checksums, or inspecting token claims — never for inventing crypto.
---

# Hash & Crypto Utilities

Compute and verify common hashes and inspect JWT structure. **Do not roll custom crypto.** Use standard algorithms, document all parameters, and never log secrets.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| File integrity | "What's the SHA-256 of this file?" |
| Webhook verification | "Compute HMAC-SHA256 for this payload" |
| Password hashing | "Generate bcrypt hash with cost 12" |
| Token debugging | "Parse this JWT and check expiry" |
| Checksum comparison | "Do these two strings hash to the same value?" |

## Phase Checklist

```
[ ] 1. Identify operation (hash, HMAC, bcrypt, JWT)
[ ] 2. Confirm algorithm and output format (hex vs base64)
[ ] 3. Document input encoding (UTF-8, raw bytes, file)
[ ] 4. Use echo -n for string hashes (no trailing newline)
[ ] 5. Run standard library / CLI — never custom implementations
[ ] 6. Redact secrets in output; show digest only
[ ] 7. For JWT: decode ≠ verify — state verification status explicitly
```

---

## Cryptographic Hashing

### CLI Commands

```bash
# String hashes — ALWAYS use echo -n (no trailing newline)
echo -n "hello" | sha256sum
echo -n "hello" | sha512sum
echo -n "hello" | sha1sum    # legacy only — note weakness
echo -n "hello" | md5sum     # checksums only — NOT security

# File hashes
sha256sum package.tar.gz
sha256sum *.py | sort

# Verify against known digest
echo "expected_digest  filename" | sha256sum -c
```

### Python

```python
import hashlib

def hash_string(text: str, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def hash_file(path: str, algorithm: str = "sha256", chunk_size: int = 8192) -> str:
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

print(hash_string("hello"))
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

### Algorithm Selection Rubric

| Algorithm | Security | Use case |
|-----------|----------|----------|
| SHA-256 | Strong | Default for checksums, content IDs, HMAC |
| SHA-512 | Strong | High-security checksums, long-term archives |
| SHA-1 | Broken | Legacy Git, old TLS — flag as weak |
| MD5 | Broken | Legacy file checksums only — never passwords |
| BLAKE2b | Strong | Fast alternative when available |

---

## HMAC

Message authentication using a shared secret key.

```python
import hmac
import hashlib
import base64

def hmac_sha256(key: str, message: str, output: str = "hex") -> str:
    mac = hmac.new(
        key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    )
    if output == "hex":
        return mac.hexdigest()
    return base64.b64encode(mac.digest()).decode("ascii")

# Webhook signature example (GitHub-style)
key = "webhook_secret"
payload = '{"action":"opened"}'
sig = hmac_sha256(key, payload)
print(f"sha256={sig}")
```

```bash
# OpenSSL HMAC
echo -n "message" | openssl dgst -sha256 -hmac "secret_key"
```

### HMAC Documentation Requirements

Always state:
- Key encoding (UTF-8 bytes, hex-decoded key, etc.)
- Message encoding (raw body vs JSON re-serialized)
- Output format (hex lowercase, base64, prefixed `sha256=`)
- Comparison method (constant-time — use `hmac.compare_digest`)

```python
import hmac

def verify_hmac(expected: str, computed: str) -> bool:
    return hmac.compare_digest(expected, computed)
```

---

## Bcrypt Password Hashing

```python
import bcrypt

password = b"user_password_here"
cost = 12  # rounds = 2^cost iterations

# Generate hash
salt = bcrypt.gensalt(rounds=cost)
hashed = bcrypt.hashpw(password, salt)
print(hashed.decode())
# $2b$12$... 

# Verify password
is_valid = bcrypt.checkpw(password, hashed)
print(f"Valid: {is_valid}")
```

### Bcrypt Parameters

| Parameter | Recommendation |
|-----------|----------------|
| Cost factor | ≥ 12 for new systems (2024+) |
| Prefix | `$2b$` (current), `$2a$` (legacy) |
| Max password length | 72 bytes — truncate with caution |
| Salt | Auto-generated per hash — never reuse |

**Never** use MD5, SHA-256, or plain HMAC for password storage. Use bcrypt, scrypt, or Argon2id.

---

## JWT Parse & Verify

### Structure

```
header.payload.signature
  │       │        └── HMAC/RSA/ECDSA over "header.payload"
  │       └── Base64URL-encoded JSON claims
  └── Base64URL-encoded JSON metadata (alg, typ, kid)
```

### Parse (Decode Only)

```python
import json
import base64

def b64url_decode(s: str) -> bytes:
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def parse_jwt(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError(f"Expected 3 parts, got {len(parts)}")
    header = json.loads(b64url_decode(parts[0]))
    payload = json.loads(b64url_decode(parts[1]))
    return {"header": header, "payload": payload, "signature": parts[2]}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
parsed = parse_jwt(token)
print(json.dumps(parsed, indent=2))
```

### Verify Signature

```python
import jwt  # PyJWT

secret = "your-256-bit-secret"
token = "..."

try:
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    print("Verified:", decoded)
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidTokenError as e:
    print(f"Invalid: {e}")
```

### Claims Checklist

| Claim | Meaning | Action |
|-------|---------|--------|
| `exp` | Expiration (Unix timestamp) | Compare to now; flag if expired |
| `iat` | Issued at | Check clock skew tolerance |
| `nbf` | Not before | Reject if current time < nbf |
| `iss` | Issuer | Validate against expected issuer |
| `aud` | Audience | Must match consuming service |
| `sub` | Subject | User/service identifier |
| `alg` | Algorithm in header | **Reject `none`**; match verification key type |

### Security Warnings

| Issue | Risk | Response |
|-------|------|----------|
| `alg: none` | Signature bypass | Reject immediately |
| HS256 + public key | Algorithm confusion | Use algorithm allowlist |
| Decode without verify | Trusting unauthenticated claims | Label output UNVERIFIED |
| Long-lived tokens | Stolen token window | Flag exp > 24h for access tokens |
| Sensitive claims in payload | Base64 is not encryption | Warn — payload is readable |

---

## Worked Examples

### Example 1: Compare file checksums

```bash
sha256sum deploy.zip
# a1b2c3...  deploy.zip

# Remote server
ssh server "sha256sum /opt/app/deploy.zip"
# Compare digests — must match exactly
```

### Example 2: Webhook HMAC verification

```
Payload (raw body): {"event":"push"}
Secret: whsec_abc123
Algorithm: HMAC-SHA256
Expected header: X-Signature: sha256=<hex>

Computed: sha256=7d3a8f...
Match: ✓ (constant-time compare)
```

### Example 3: JWT expiry check

```
Payload exp: 1700000000 → 2023-11-14 22:13:20 UTC
Current time:  2024-01-01 00:00:00 UTC
Status: EXPIRED (do not trust claims)
Signature: not verified (no key provided)
```

---

## Output Template

```markdown
## {Operation}

| Property | Value |
|----------|-------|
| Algorithm | SHA-256 |
| Input | {n} bytes (string / file: `{name}`) |
| Output format | hex lowercase |
| Digest | `{hash}` |

---

## JWT Analysis

| Segment | Content |
|---------|---------|
| Header | `{json}` |
| Payload | `{json}` |
| Signature | `{truncated}...` |

| Claim | Value | Status |
|-------|-------|--------|
| exp | 2024-06-01 12:00 UTC | ✓ valid |
| iss | auth.example.com | not checked |

**Verification:** UNVERIFIED — no key provided
```

---

## Anti-Patterns

- MD5 or SHA-1 for password storage
- Logging full JWT secrets, HMAC keys, or bcrypt hashes of real passwords
- "Decoding" JWT and treating claims as authenticated without signature check
- Wrong newline handling (`echo` vs `echo -n`) causing hash mismatch
- Rolling custom hash or encryption algorithms
- Using MD5 for security-sensitive integrity checks
- Comparing HMAC digests with `==` instead of `hmac.compare_digest`
- Accepting JWT `alg` from token header without allowlist

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| Base64URL decode for JWT segments | `encode-decode` |
| Generate API secrets for signing | `token-generator` |
| JSON pretty-print decoded claims | `format-convert` |
| Auth architecture review | `auth-review` (security plugin) |
| URL with embedded tokens | `network-utils` |
| SQL injection vs hashing | `sql-format` |
