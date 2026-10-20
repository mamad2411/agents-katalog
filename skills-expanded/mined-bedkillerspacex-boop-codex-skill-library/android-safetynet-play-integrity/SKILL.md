---
name: android-safetynet-play-integrity
description: >
  Migrate and operate Play Integrity API (successor to SafetyNet Attestation) for owned
  Android apps: request integrity tokens, server-side decrypt/verify, verdict handling
  (MEETS_DEVICE_INTEGRITY, app integrity, account), and anti-abuse design. Use for
  attestation on sensitive actions — not for bypassing Integrity on third-party apps.
---

# Play Integrity (SafetyNet Migration)

## Scope And Authorization

- **In scope:** Apps and backends you own; Google Cloud project linked to Play.
- **Out of scope:** Bypassing Play Integrity for cheating/fraud on others’ apps; distributing spoof tools.
- Server must verify tokens — never trust client boolean alone.
- Pair with `code-quality-standards` and account abuse controls.

## When To Use

- Replacing SafetyNet Attestation API with **Play Integrity API**.
- Gating high-risk actions (login step-up, payments, coupon claim) with device/app integrity.
- Debugging verdict mismatches on emulators/rooted lab devices.
- Designing graceful degradation when Integrity unavailable.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Biometric local unlock | `android-biometric-prompt` |
| General pentest | `android-pentesting-tricks` |
| Root detection-only DIY | Prefer Integrity + server policy |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Integrity token | Device requests; server verifies via Google API |
| Nonce/requestHash | Bind token to transaction |
| App integrity | Package name + cert match Play |
| Device integrity | MEETS_DEVICE_INTEGRITY / basic / strong tiers (labels evolve) |
| Account licensing | Optional Play licensing signals |
| Classic SafetyNet | Legacy; plan full removal |

## Workflow

### 1. Confirm threats and success criteria

1. Record abuse cases Integrity should raise cost for (bots, modified APKs, emulators).
2. Success: server rejects invalid/replayed tokens; nonce bound; false-positive plan for rare devices; SafetyNet code removed.
3. Link Play Console ↔ Cloud project per Google docs.

### 2. Client: request token

```kotlin
// Sketch — use latest Play Integrity library APIs
val nonce = serverIssuedNonce() // base64, high entropy
val integrityManager = IntegrityManagerFactory.create(context)
val request = IntegrityTokenRequest.builder().setNonce(nonce).build()
integrityManager.requestIntegrityToken(request)
    .addOnSuccessListener { resp -> sendToBackend(resp.token()) }
```

1. Nonce from server, single-use, short TTL.
2. Call close to the sensitive action, not once per week only.

### 3. Server: verify

```bash
# Call Google Play Integrity decode/verify API with service account
# Validate: packageName, certDigest, nonce/requestHash, timestamp, verdicts
```

| Check | Fail closed? |
| --- | --- |
| Signature/Google verify error | Yes |
| Nonce mismatch / reuse | Yes |
| Package/cert mismatch | Yes |
| Device integrity insufficient | Policy-dependent |
| Clock skew large | Yes |

### 4. Policy matrix (example)

| Action | Required verdict |
| --- | --- |
| Read public content | None |
| Login from new device | Basic device + app integrity |
| Redeem high-value coupon | Stricter device integrity + rate limits |
| Lab/debug builds | Alternate attestation or allowlist builds |

1. Combine with account risk scores — Integrity is not CAPTCHA alone.
2. Log reason codes without logging full tokens.

### 5. Migrate off SafetyNet

```bash
rg -n "SafetyNet|Attestation" -S .
# Remove dependencies; replace with Play Integrity library
```

1. Dual-run period: accept both only with clear deprecation date.
2. Update runbooks and customer support macros (“device doesn’t meet integrity”).

### 6. Verify

```bash
# Lab: stock device success; modified APK failure; emulator per policy
adb logcat | rg -i integrity
# Server unit tests: forged token rejected; replay rejected
```

### 7. Hand off

1. Document Cloud project, service account, key rotation.
2. Metrics: failure rates by verdict; watch for outages.
3. Break-glass for Integrity API downtime (limited, ticketed).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Trust | Server verify | `if (client.integrityOk)` |
| Nonce | Server one-time | Static string in APK |
| UX | Explain + support path | Hard block with no recovery |
| Scope | Sensitive actions | Every public GET |

## Output Checklist

- [ ] Play/Cloud linkage done
- [ ] Client token request with server nonce
- [ ] Server verify + replay protection
- [ ] Policy matrix documented
- [ ] SafetyNet removed or dated dual-run
- [ ] Lab verdict tests recorded
- [ ] Metrics/alerts for API errors
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only; no bypass tooling for third parties.
- Always verify on server with nonce binding.
- Integrity raises attacker cost — combine with other controls.
- Protect Google service account keys.
- Respect user privacy in logging.
