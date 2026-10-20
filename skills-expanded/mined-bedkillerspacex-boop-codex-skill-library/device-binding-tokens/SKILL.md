---
name: device-binding-tokens
description: >
  Bind session or refresh tokens to a device or client instance: device identifiers,
  public-key proof-of-possession (DPoP-style), mTLS token binding, sender-constrained
  access tokens, rotation with reuse detection, and step-up on new device. Use when
  device-bound refresh tokens, token binding, DPoP, certificate-bound access tokens,
  refresh token reuse detection, or reducing stolen-token replay on owned IdP/apps —
  not for covert tracking fingerprints alone (see device-fingerprint-ethics).
---

# Device Binding Tokens

## Scope And Authorization

- **In scope:** Identity and session systems you own; authorized security design reviews.
- **Out of scope:** Covert device tracking without lawful basis; bypassing users’ security on third-party IdPs.
- Prefer privacy-preserving device keys over invasive fingerprinting when the goal is anti-theft of tokens.
- Redact refresh tokens, device keys, and customer IDs in logs and tickets.
- Pair with `api-auth-and-jwt-abuse`, `account-takeover-methodology`, `device-fingerprint-ethics`, and `code-quality-standards`.

## When To Use

- Stolen refresh tokens from XSS/logs/DB dumps are replayable from any machine.
- Designing mobile/desktop clients with per-install keypairs.
- Implementing OAuth sender-constrained tokens (DPoP, mTLS bound access tokens).
- Adding refresh rotation + reuse detection tied to a device session record.
- Hardening high-risk actions to require the original bound device or step-up MFA.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| JWT alg/iss/aud validation basics | `api-auth-and-jwt-abuse` |
| Privacy/ethics of fingerprinting | `device-fingerprint-ethics` |
| Full ATO multi-vector | `account-takeover-methodology` |
| WebAuthn / passkeys primary auth | WebAuthn/passkey skills |
| Session fixation | `session-fixation-management` |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Mechanism | Binds token to | Notes |
| --- | --- | --- |
| Server-side device session | Opaque `device_id` + refresh handle | Simple; needs secure device id storage |
| Public-key PoP | Client holds private key; proves each use | Stronger against pure bearer theft |
| DPoP (OAuth) | Proof JWT per request | Sender-constrained access tokens |
| mTLS / cert-bound tokens | Client certificate | Excellent for confidential/service clients |
| Refresh rotation + reuse detect | Token family | Detects replay; revoke family on reuse |
| Fingerprint soft bind | Browser signals | Weak; privacy-sensitive; secondary signal only |

**Goal:** A bearer token alone should be insufficient when an attacker lacks the device key or session binding secret.

## Workflow

### 1. Confirm scope and success criteria

1. Clients: SPA, native mobile, desktop, confidential server—binding differs by threat model.
2. Success: refresh stolen from network logs cannot mint new access tokens without device proof; reuse triggers global revoke.
3. UX: new device login path (MFA) defined; account recovery without bricking users.

### 2. Inventory current token model

1. Access token lifetime, refresh lifetime, rotation yes/no, storage (cookie, localStorage, Keychain).
2. Whether tokens are pure bearer at API gateway.
3. Existing device/session tables and logout-all behavior.

```bash
rg -n "refresh_token|RotateRefresh|DPoP|token_binding|device_id|reuse" --type-add 'web:*.{ts,js,go,py}' -t web .
```

### 3. Choose binding strength

| Client type | Recommended approach |
| --- | --- |
| Native mobile / desktop | App-attested or install keypair in secure enclave/keychain; refresh requires signed challenge |
| Confidential backend | mTLS or client secret + sender constraints as applicable |
| First-party browser | httpOnly secure cookie session + server device record; consider DPoP where supported; avoid localStorage refresh |
| Third-party API | DPoP or mTLS per OAuth profile you implement |

1. Do not rely solely on spoofable JS fingerprints as the only bind.
2. Prefer platform secure storage for private keys.

### 4. Design data model

```text
DeviceSession:
  id, user_id, public_key_or_secret_hash, user_agent_hash?,
  created_at, last_seen, revoked_at, refresh_family_id,
  amr/mfa_level
RefreshToken:
  hash, device_session_id, parent_hash, expires_at, used_at
```

1. Store **hashes** of refresh tokens, not raw tokens.
2. On refresh: verify device proof → rotate token → invalidate old.
3. On reuse of old refresh: revoke **entire family** + device session; alert user.

### 5. Implement proof-of-possession (illustrative)

```text
# High-level DPoP-style flow
1. Client generates key pair (device install)
2. Token request includes DPoP proof binding htm/htu/jti
3. AS issues access token with cnf.jkt thumbprint
4. RS verifies DPoP proof matches cnf on each call
```

```text
# Simpler first-party refresh bind
1. At login, create device_session + store client_secret in secure storage
2. Refresh endpoint requires device_session_id + HMAC(device_secret, refresh_nonce)
3. Rotate refresh; fail closed on bad MAC
```

1. Use constant-time compare; short nonces; anti-replay `jti` cache where relevant.
2. Clock skew bounds for proof JWTs.

### 6. Step-up and recovery

1. New device: full auth + MFA; do not silently accept refresh from unknown device.
2. User-facing device list: revoke individual devices.
3. Lost device: password/MFA recovery revokes all device sessions.
4. Avoid permanent lockout: support break-glass with strong identity proof.

### 7. Verify and observe

```bash
# Authorized test plan
# 1) Capture refresh (lab) → replay without device key → expect 401
# 2) Legitimate refresh → new token works; old refresh fails
# 3) Reuse old refresh → family revoked
# 4) Logout device → tokens dead
```

1. Metrics: refresh failures, reuse detections, devices per user, proof validation errors.
2. Alerts on reuse detection spikes (possible theft).
3. Apply `code-quality-standards` to crypto/session code; threat-model reviews required.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Storage | Keychain / httpOnly cookie | Refresh in localStorage |
| Theft | PoP or rotation+reuse revoke | Long-lived pure bearer refresh |
| Fingerprint | Optional risk signal | Sole binding factor |
| Reuse | Revoke family + notify | Ignore reuse |
| Logs | Token hashes only | Raw refresh in log aggregator |
| Recovery | Device list + revoke all | No way to drop stolen device |

## Output Checklist

- [ ] Client types and threat model documented
- [ ] Binding mechanism chosen (PoP / mTLS / server device secret)
- [ ] Refresh rotation + reuse detection specified
- [ ] Secure storage for device secrets/keys
- [ ] Step-up and recovery UX defined
- [ ] Negative tests: stolen bearer alone fails
- [ ] Metrics/alerts for reuse and proof failures
- [ ] Privacy review vs fingerprinting skill
- [ ] Gateway/RS validates constraints for access tokens
- [ ] `code-quality-standards` applied

## Rules

- Bearer-only long-lived refresh tokens are high risk—bind or constrain them.
- Fingerprinting is not a substitute for cryptographic binding.
- Fail closed on proof validation errors for sensitive APIs.
- Authorized systems only; minimize personal data in device records.
- Focus on token–device binding; ethics of tracking are a neighbor skill.
