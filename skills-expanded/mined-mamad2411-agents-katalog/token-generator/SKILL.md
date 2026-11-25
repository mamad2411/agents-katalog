---
name: token-generator
description: Generate UUIDs, ULIDs, secure random tokens, OTP patterns, and analyze password strength. Use when scaffolding IDs, API keys, test fixtures, or reviewing password policy.
---

# Token Generator

Generate identifiers and secrets with correct entropy and format. **Cryptographically secure** for anything authentication-related. Never use `random` module for secrets.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Database IDs | "Generate 5 UUID v7 values" |
| API keys | "Create a 256-bit URL-safe token" |
| Test fixtures | "Generate 10 deterministic test IDs" |
| OTP codes | "Generate 6-digit numeric OTP" |
| Password review | "Analyze strength of this password policy" |
| Sortable IDs | "ULID or UUID v7 for indexed column" |

## Phase Checklist

```
[ ] 1. Identify token type (UUID, ULID, hex, urlsafe, OTP)
[ ] 2. Confirm entropy requirements (min 128 bits for API keys)
[ ] 3. Use secrets module — never random module for secrets
[ ] 4. Document format (hyphens, uppercase, charset)
[ ] 5. Label test/deterministic tokens as non-production
[ ] 6. Warn: show once, do not commit to git
[ ] 7. For password analysis: never store or log the password
```

---

## UUID Generation

### Versions

| Version | Method | Use case |
|---------|--------|----------|
| v4 | Random 122 bits | Default general-purpose IDs |
| v7 | Unix ms timestamp + random | Time-sortable, DB index friendly |
| v1 | MAC + timestamp | **Avoid** — MAC leak in old implementations |
| v5 | SHA-1 namespace hash | Deterministic from name + namespace |

### Python

```python
import uuid

# v4 — random (default)
u4 = uuid.uuid4()
print(f"v4: {u4}")

# v7 — time-sortable (Python 3.12+)
u7 = uuid.uuid7()
print(f"v7: {u7}")

# v5 — deterministic
namespace = uuid.NAMESPACE_DNS
u5 = uuid.uuid5(namespace, "example.com")
print(f"v5: {u5}")

# Output formats
uid = uuid.uuid4()
print(uid)                          # lowercase hyphenated (standard)
print(str(uid).upper())             # uppercase
print(uid.hex)                      # no hyphens: 32 hex chars
print(f"{uid.hex[:8]}-{uid.hex[8:]}")  # custom grouping
```

```bash
# CLI (if uuidgen available)
uuidgen                    # random UUID v4
uuidgen -r                 # explicit random
uuidgen -t                   # time-based v1 (avoid for public IDs)
```

### UUID Selection Rubric

| Requirement | Recommendation |
|-------------|----------------|
| General unique ID | UUID v4 |
| DB primary key with time ordering | UUID v7 or ULID |
| Reproducible ID from input | UUID v5 with fixed namespace |
| Public-facing opaque ID | UUID v4 (no MAC leakage) |

---

## ULID

Lexicographically sortable, 128-bit identifier. Crockford Base32, 26 characters.

```
 01ARZ3NDEKTSV4RRFFQ69G5FAV
 |----------||------------|
 timestamp     randomness
  48 bits        80 bits
```

### Python (ulid-py)

```bash
pip install ulid-py -q
```

```python
import ulid

u = ulid.new()
print(f"ULID: {u}")
print(f"Timestamp ms: {u.timestamp()}")
print(f"Sortable: yes")

# Generate batch
for _ in range(3):
    print(ulid.new())
```

### ULID vs UUID v7

| Feature | ULID | UUID v7 |
|---------|------|---------|
| Sortable | Yes | Yes |
| Length | 26 chars (Base32) | 36 chars (hex + hyphens) |
| Stdlib | No (needs package) | Python 3.12+ |
| Case sensitivity | Crockford (no I/L/O/U) | Hex lowercase |

If `ulid-py` unavailable, recommend UUID v7 as stdlib alternative.

---

## Secure Random Tokens

```python
import secrets
import string

# Hex token (64 chars = 256 bits)
api_key_hex = secrets.token_hex(32)
print(f"hex: {api_key_hex}")

# URL-safe token (no padding, ~256 bits)
api_key_url = secrets.token_urlsafe(32)
print(f"urlsafe: {api_key_url}")

# Alphanumeric token (custom length)
def alphanumeric_token(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

print(f"alnum: {alphanumeric_token(32)}")

# Numeric OTP (6 digits)
def numeric_otp(digits: int = 6) -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(digits))

print(f"OTP: {numeric_otp(6)}")

# Bytes (raw)
raw_bytes = secrets.token_bytes(32)
print(f"bytes: {len(raw_bytes)} bytes, hex={raw_bytes.hex()}")
```

### Token Type Reference

| Type | Command | Entropy | Use |
|------|---------|---------|-----|
| Hex string | `token_hex(32)` | 256 bits | API keys, secrets |
| URL-safe | `token_urlsafe(32)` | ~256 bits | Query params, cookies |
| Raw bytes | `token_bytes(32)` | 256 bits | Encryption keys |
| Numeric OTP | 6× `randbelow(10)` | ~20 bits | 2FA codes (short-lived) |
| Alphanumeric | `choice` × n | n×log2(62) | Invite codes |

**Minimum entropy:** API keys ≥ 128 bits (16 bytes). Prefer 256 bits (32 bytes) for long-lived secrets.

---

## Password Strength Analysis

Analyze without storing the password — compute metrics in memory, discard immediately.

```python
import math
import re
import string

def analyze_password(password: str) -> dict:
    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^\w\s]", password))

    charset = 0
    if has_lower: charset += 26
    if has_upper: charset += 26
    if has_digit: charset += 10
    if has_symbol: charset += 32

    entropy = length * math.log2(charset) if charset else 0

    # Pattern penalties
    penalties = []
    if re.search(r"(.)\1{2,}", password):
        penalties.append("repeated characters")
    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde)", password.lower()):
        penalties.append("sequential pattern")
    if re.search(r"^(password|qwerty|admin|letmein)", password.lower()):
        penalties.append("common prefix")
    if length < 8:
        penalties.append("too short (<8)")
    elif length < 12:
        penalties.append("minimum acceptable (8-11)")

    classes = sum([has_lower, has_upper, has_digit, has_symbol])
    score = "weak"
    if length >= 16 and classes >= 3 and not penalties:
        score = "strong"
    elif length >= 12 and classes >= 3:
        score = "good"
    elif length >= 8 and classes >= 2:
        score = "fair"

    return {
        "length": length,
        "character_classes": classes,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "estimated_entropy_bits": round(entropy, 1),
        "penalties": penalties,
        "score": score,
    }

# Analyze without printing the actual password
result = analyze_password("user_provided_password")
print(result)
```

### Strength Rubric

| Score | Criteria |
|-------|----------|
| Weak | <8 chars, or common pattern, or 1 class |
| Fair | 8-11 chars, 2+ classes |
| Good | 12-15 chars, 3+ classes, no patterns |
| Strong | 16+ chars, 4 classes, no patterns |
| Excellent | 20+ char passphrase (4+ random words) |

### Passphrase Recommendation

```python
# Example word list approach (use diceware or similar in production)
import secrets
words = ["correct", "horse", "battery", "staple"]  # illustrative
passphrase = "-".join(secrets.choice(words) for _ in range(4))
print(f"Passphrase pattern: 4 random words, ~44+ bits entropy")
```

Recommend passphrases (4+ random words, 20+ chars) over complex short passwords.

---

## Test Fixtures (Non-Production)

```python
import uuid
import random

# Deterministic IDs for reproducible tests ONLY
def test_uuid(seed: int, n: int = 5) -> list[str]:
    rng = random.Random(seed)
    return [str(uuid.UUID(int=rng.getrandbits(128))) for _ in range(n)]

print("TEST ONLY:", test_uuid(42))
```

**Label clearly:** `⚠ TEST FIXTURE — not cryptographically secure`

For production IDs in tests that need uniqueness but not security, document the distinction.

---

## Batch Generation

```python
import uuid

def batch_uuids(count: int, version: int = 4) -> list[str]:
    gen = uuid.uuid4 if version == 4 else uuid.uuid7
    return [str(gen()) for _ in range(count)]

for uid in batch_uuids(5, version=7):
    print(uid)
```

---

## Worked Examples

### Example 1: API key for .env

```
Type:     URL-safe token
Command:  secrets.token_urlsafe(32)
Output:   xK7mN2pQ... (43 chars, ~256 bits)
⚠ Add to .env — do not commit
⚠ Show once — user must copy now
```

### Example 2: Database migration to UUID v7

```
Current:  SERIAL integer PK
Target:   UUID v7 for time-ordered inserts
Benefit:  Reduced B-tree page splits vs random v4
Command:  uuid.uuid7() per row
```

### Example 3: Password policy review

```
Policy: min 8 chars, 1 upper, 1 digit
Analysis: Meets minimum but entropy ~40 bits
Risk: Dictionary attacks, no symbol requirement
Recommend: min 12 chars OR passphrase, add breach check
```

---

## Output Template

```markdown
## Generated {type}

| Property | Value |
|----------|-------|
| Value | `{token}` |
| Format | UUID v7 lowercase hyphenated |
| Entropy | ~122 bits (random portion) |
| Environment | PRODUCTION / TEST FIXTURE |

⚠ **Show once — copy now**
⚠ **Do not commit to git** — add to `.env` or secrets manager

### Batch ({n} tokens)
1. `{token_1}`
2. `{token_2}`
...
```

---

## Anti-Patterns

- UUID v1 for public IDs (MAC leak in old implementations — prefer v4/v7)
- Short API keys (<128 bit entropy)
- Generating "memorable" passwords by reducing charset
- Reusing example tokens from docs in production
- Using `random.randint` or `random.choice` for secrets
- Committing generated tokens to version control
- Storing analyzed passwords in logs or output

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| Store secrets safely | `secrets-audit` (security plugin) |
| JWT signed with generated secret | `hash-crypto` |
| HMAC key generation | `hash-crypto` |
| URL-safe encoding of tokens | `encode-decode` |
| MAC address generation | `network-utils` |
| QR code encoding of OTP setup URI | `qr-generator` |
