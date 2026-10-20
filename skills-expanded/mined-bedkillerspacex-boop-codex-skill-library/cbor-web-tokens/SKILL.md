---
name: cbor-web-tokens
description: >
  CBOR Web Tokens (CWT, RFC 8392) for owned systems: claims set, COSE signing/encryption,
  key management, validation rules, and comparison to JWT. Use when CWT, COSE_Sign1,
  RFC 8392, constrained-device tokens, or CBOR tokens instead of JWT — not for forging
  tokens against third parties.
---

# Cbor Web Tokens

## Scope And Authorization

- **In scope:** Token formats and verifiers you design or assess under authorization.
- **Out of scope:** Forging tokens to attack third-party APIs; abusing leaked signing keys.
- Treat signing keys as high-value secrets.
- Pair with `api-auth-and-jwt-abuse` concepts (claims discipline) and `code-quality-standards`.

## When To Use

- Choosing CWT over JWT for constrained IoT/bandwidth environments.
- Implementing or reviewing COSE-signed (`COSE_Sign1`) or MACed CWTs.
- Mapping JWT-like claims (`iss`, `sub`, `exp`, `aud`) into CBOR claim keys.
- Interop with OAuth/ACE profiles that use CWT.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| JWT/JWS/JWE specifically | JWT skills / `api-auth-and-jwt-abuse` |
| Generic OAuth flows | oauth skills |
| Cap’n Proto RPC | `capnproto-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| CWT | CBOR map of claims, secured by COSE |
| Claim keys | Integer labels (RFC 8392) e.g. 1=iss, 2=sub, 3=aud, 4=exp, 5=nbf, 6=iat, 7=cti |
| COSE | Sign/MAC/Encrypt envelopes (RFC 9052 family) |
| cti | Token ID akin to jti |
| Confirmation | `cnf` claim for proof-of-possession patterns |

## Workflow

### 1. Confirm scope and success criteria

1. Devices/services, crypto capability (sign vs MAC), key distribution model.
2. Success: issue+verify path; mandatory claim checks; alg allowlist; key rotation tested.
3. Threat model: stolen token vs stolen key vs alg confusion.

### 2. Define claim profile

| Claim | Integer | Rule |
| --- | --- | --- |
| iss | 1 | Allowlist issuers |
| sub | 2 | Subject format documented |
| aud | 3 | Exact audience check |
| exp | 4 | Required; reject expired |
| nbf | 5 | If present, enforce |
| iat | 6 | Clock skew window |
| cti | 7 | Unique; optional replay cache |

1. Private claims: use unregistered integers from agreed range or text keys carefully for interop.
2. Prefer small binary subjects over verbose strings on IoT.

### 3. Choose COSE protection

| Mode | Use |
| --- | --- |
| COSE_Sign1 | Asymmetric (device verify with pubkeys) |
| COSE_Mac0 | Shared HMAC when both ends have secret |
| Encrypted COSE | Confidentiality of claims in transit/storage |

```text
# Validation order (conceptual)
1. Parse CBOR → COSE structure
2. Check protected headers alg ∈ allowlist (never trust "none")
3. Verify signature/MAC with correct key (kid)
4. Decode CWT claims map
5. Enforce exp/nbf/iss/aud/cti policy
6. Authorize business action
```

1. **Alg allowlist** — refuse unexpected algorithms (JWT-style pitfalls apply).
2. `kid` required when multiple keys; support rotation overlap.
3. Reject unknown critical headers if using crit patterns.

### 4. Implement issuer and verifier

```python
# Pseudocode — use maintained COSE/CWT libraries for your language
def issue_cwt(claims: dict, key) -> bytes:
    assert "exp" in claims
    cwt_map = to_cbor_claim_map(claims)
    return cose_sign1(cwt_map, key, alg="ES256")

def verify_cwt(token: bytes, keys_by_kid, aud, iss) -> dict:
    body = cose_verify(token, keys_by_kid, allowed_algs={"ES256", "EdDSA"})
    claims = parse_cwt(body)
    check_iss_aud_exp(claims, iss=iss, aud=aud, skew_s=60)
    return claims
```

1. Pin library versions; prefer well-reviewed COSE stacks.
2. Constant-time compare for MACs where applicable.
3. Do not implement custom “encrypted JWT-like CBOR” without COSE.

### 5. Key management

1. Store private keys in HSM/KMS/secure element when possible.
2. Distribute verification keys via signed JWKS-like catalog or device provision.
3. Rotate: introduce new kid → dual-verify → retire old.
4. Separate keys per environment and token class (access vs refresh analogs).

### 6. Verify security properties

| Test | Expected |
| --- | --- |
| Tamper one claim byte | Verify fail |
| Wrong aud | Reject |
| Expired exp | Reject |
| alg not allowlisted | Reject |
| Unknown kid | Reject |
| Replay cti (if tracked) | Reject second use |

```bash
# Unit tests with fixed keys vectors in repo (no production keys)
cargo test cwt_ 2>/dev/null || pytest tests/test_cwt.py -q
```

### 7. Hand off

1. Document claim profile and COSE algs as a versioned spec.
2. Interop test vectors between languages if polyglot.
3. Monitoring: verify fail rates; never log full tokens.
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Alg | Explicit allowlist | Trust header blindly |
| exp | Required + skew | Tokens forever |
| Keys | KMS + kid rotation | One static HMAC in firmware worldwide |
| Claims | Integer labels per RFC | Random undocument maps |
| Compare | CWT when size/IoT needs | CWT only for novelty while stack is JWT |
| Logs | cti hash only | Full token in plaintext logs |

## Output Checklist

- [ ] Claim profile documented with integer keys
- [ ] COSE mode and algs chosen
- [ ] Issue/verify libraries integrated
- [ ] iss/aud/exp checks mandatory
- [ ] Key management + rotation defined
- [ ] Negative crypto tests pass
- [ ] Replay policy decided (cti)
- [ ] Spec + test vectors published internally
- [ ] `code-quality-standards` applied

## Rules

- Same discipline as JWT: verify signature first, then claims; allowlist algorithms.
- Protect signing keys; minimize token lifetime.
- Authorized systems only — no token forgery against third parties.
- Prefer standard COSE/CWT libraries over homemade crypto.
- JWT-specific attack catalogs still inform claim validation mindset.
