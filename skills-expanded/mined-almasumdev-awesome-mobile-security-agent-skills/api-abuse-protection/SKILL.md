---
name: api-abuse-protection
description: Device attestation and anti-abuse on mobile APIs using App Attest, DeviceCheck, and Google Play Integrity. Use to make "is this a real app on a real device" decisions server-side.
---

# API Abuse Protection (App Attest / Play Integrity)

## Instructions

Your mobile binary is not a trust boundary. Device attestation gives the server a signed statement from the OS that a request originated from an unmodified app on a real device — which you can weigh in authorization decisions.

### 1. What These APIs Prove (and Don't)

- **App Attest (iOS)** — the request came from a legitimate copy of your app, on a non-jailbroken device, signed by Apple. Does not prove the user's identity.
- **DeviceCheck (iOS)** — two bits of server-settable state per device, plus a basic "real device" signal. Complementary to App Attest.
- **Play Integrity (Android)** — the app binary is unmodified, installed from a recognized source, running on a device that passes Play Integrity ("MEETS_DEVICE_INTEGRITY"). Tiered; the strong tier ("MEETS_STRONG_INTEGRITY") requires hardware-backed attestation.

These defeat casual scripted abuse. They do **not** defeat a determined attacker with a rooted device plus an attestation bypass; treat them as probabilistic signals, not a yes/no gate.

### 2. Where to Use It

Good fits:
- Account creation, login, password reset.
- Sensitive writes (transfer, delete, change-of-address).
- Any endpoint you see getting scraped / credential-stuffed.

Bad fits:
- Every request (latency + attestation quota).
- Use-cases where "block" is expensive (existing legitimate users on older devices failing attestation).

### 3. iOS — App Attest Flow

```swift
import DeviceCheck

let service = DCAppAttestService.shared
guard service.isSupported else { /* older device — fall back */ return }

service.generateKey { keyId, error in
    guard let keyId else { return }
    // 1. Ask server for a challenge (one-time nonce).
    api.challenge { nonce in
        let hash = SHA256.hash(data: nonce)
        service.attestKey(keyId, clientDataHash: Data(hash)) { attestation, err in
            // 2. Send keyId + attestation to server, which verifies with Apple.
            api.register(keyId: keyId, attestation: attestation)
        }
    }
}

// Later, for each sensitive request:
service.generateAssertion(keyId, clientDataHash: requestHash) { assertion, _ in
    api.call(assertion: assertion, keyId: keyId, body: requestBody)
}
```

Server validates the assertion against the registered public key + current challenge.

### 4. Android — Play Integrity

```kotlin
val integrityManager = IntegrityManagerFactory.createStandard(context)
val request = StandardIntegrityManager
    .PrepareIntegrityTokenRequest.builder()
    .setCloudProjectNumber(cloudProjectNumber)
    .build()

val provider = integrityManager.prepareIntegrityToken(request).await()

// Per-call
val token = provider.request(
    StandardIntegrityManager.StandardIntegrityTokenRequest.builder()
        .setRequestHash(sha256(requestBody))
        .build()
).await().token()

api.sensitiveCall(integrityToken = token, body = requestBody)
```

Server verifies the token with Google's API and reads:

- `deviceIntegrity.deviceRecognitionVerdict` → `MEETS_DEVICE_INTEGRITY`, `MEETS_BASIC_INTEGRITY`, `MEETS_STRONG_INTEGRITY`.
- `appIntegrity.appRecognitionVerdict` → `PLAY_RECOGNIZED` is the gold standard.
- `accountDetails.appLicensingVerdict`.

### 5. Server-Side Policy Tiers

Implement policy as a decision, not a boolean:

```
if verdict == PLAY_RECOGNIZED && device == STRONG:
    allow
elif verdict == PLAY_RECOGNIZED && device == BASIC:
    allow but log + extra rate limit
else:
    require step-up auth OR block
```

Don't return 403 on every non-strong device — you'll break a significant long tail of real users.

### 6. Replay and Nonce Hygiene

- Every attestation / assertion must bind to a **server-issued nonce** and an optional **request hash**.
- Nonces are single-use, expire in seconds, stored server-side.
- Without a nonce, an attacker replays a legitimate user's attestation forever.

### 7. Observability

- Log the verdict distribution per endpoint — a sudden spike in `UNEVALUATED` usually means a new OS version or a new attack.
- Alert on cliffs; a drop from 95% `MEETS_DEVICE_INTEGRITY` to 60% overnight is a signal, not noise.

### 8. What Not to Do

- Do not use App Attest / Play Integrity as your only auth. They attest the **app / device**, not the **user**.
- Do not expose a raw "attested or not" flag to the client — the client will lie.
- Do not block every failed attestation silently. Return a typed error the support team can correlate.

## Checklist

- [ ] Attestation is required on account creation, login, and sensitive writes.
- [ ] Every attestation call uses a fresh server-issued nonce.
- [ ] Server inspects the full verdict (app recognition + device integrity) and tiers the response.
- [ ] Older devices / unsupported OS versions have a documented fallback policy.
- [ ] Verdict distributions are logged and alerted on.
- [ ] Attestation is treated as a signal, not as authentication.
