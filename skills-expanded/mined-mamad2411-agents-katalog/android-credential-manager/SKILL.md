---
name: android-credential-manager
description: >
  Android Credential Manager for owned apps: passwords, passkeys/WebAuthn, Sign in with
  Google flows via Credential Manager APIs, GetCredential/CreatePublicKeyCredential, and
  migration from Smart Lock. Use when implementing modern sign-in UX and passkey support —
  not for phishing credentials from third-party apps.
---

# Android Credential Manager

## Scope And Authorization

- **In scope:** Android applications you own; associated relying-party (RP) server config.
- **Out of scope:** Intercepting or stealing credentials from other apps; fake system UI.
- Coordinate RP ID, Digital Asset Links, and server WebAuthn endpoints carefully.
- Pair with `code-quality-standards` and server auth skills (`api-auth-and-jwt-abuse` for token review).

## When To Use

- Adding **passkeys** or unified credential selector on Android.
- Replacing deprecated Smart Lock for Passwords integrations.
- Combining password + federated + passkey in one GetCredential flow.
- Debugging Digital Asset Links / RP ID mismatches.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| BiometricPrompt crypto binding | `android-biometric-prompt` |
| OAuth deep abuse testing | `api-auth-and-jwt-abuse` / OAuth skills |
| Play Integrity | `android-safetynet-play-integrity` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| API area | Role |
| --- | --- |
| CredentialManager | Jetpack entry for get/create credential |
| GetCredentialRequest | Password, public key (passkey), federated options |
| CreatePublicKeyCredential | Passkey registration |
| Digital Asset Links | Link app ↔ website for passkeys/passwords |
| Server WebAuthn | Attestation/assertion verification |

## Workflow

### 1. Confirm scope and success criteria

1. Record package name, SHA-256 cert fingerprints, website domains, existing auth.
2. Success: users can register/authenticate with passkey; password save/get works when enabled; failed RP validation is loud in logs; server verifies assertions.
3. Decide credential types to support.

### 2. Link app and site (Asset Links)

```json
// https://example.com/.well-known/assetlinks.json
[{
  "relation": ["delegate_permission/common.handle_all_urls",
               "delegate_permission/common.get_login_creds"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.app",
    "sha256_cert_fingerprints": ["AA:BB:..."]
  }
}]
```

```bash
# Verify fingerprint of signing cert
keytool -list -v -keystore release.jks
# Check asset links reachable
curl -sS https://example.com/.well-known/assetlinks.json
```

1. Include **all** signing keys (Play App Signing vs upload key nuances).
2. HTTP must serve correct JSON content-type; no auth walls.

### 3. Client: get credential (sketch)

```kotlin
val request = GetCredentialRequest.Builder()
    .addCredentialOption(
        GetPublicKeyCredentialOption(requestJson = publicKeyRequestJson)
    )
    // .addCredentialOption(GetPasswordOption())
    .build()
val result = credentialManager.getCredential(context, request)
when (val cred = result.credential) {
    is PublicKeyCredential -> sendToServer(cred.authenticationResponseJson)
    is PasswordCredential -> loginWithPassword(cred.id, cred.password)
}
```

### 4. Client: create passkey (sketch)

```kotlin
val createRequest = CreatePublicKeyCredentialRequest(requestJson = registrationJson)
val response = credentialManager.createCredential(context, createRequest)
// Send registration response JSON to server for verification + store credential id
```

1. `requestJson` is WebAuthn options from your server (challenge, rp, user, pubKeyCredParams).
2. Never generate challenges only on-device without server trust.

### 5. Server requirements

| Step | Requirement |
| --- | --- |
| Challenge | High entropy, single-use, short TTL, server-stored |
| RP ID | Matches domain; origin validation |
| Verify | Signature, counter (if used), authenticator data flags |
| Account link | Bind credential id to user; allow multiple passkeys |
| Recovery | Non-passkey recovery path still secure (not weak security questions) |

### 6. Verify end-to-end

```bash
adb logcat | rg -i 'CredentialManager|PublicKeyCredential|assetlink'
# Manual: register passkey, reinstall app, authenticate, revoke passkey server-side
```

1. Test on multiple OEMs; credential providers differ.
2. Confirm phishing resistance: wrong RP app should not get credentials.

### 7. Hand off

1. Document Asset Links owners and Play signing cert process.
2. Metrics: passkey success rate, fallback to password.
3. Runbook: rotate site association when package/signing changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Challenge | Server-issued | Static challenge in APK |
| Asset Links | All certs listed | Only debug keystore fingerprint |
| UX | Credential Manager unified | Custom fake system sheets |
| Server | Full WebAuthn verify | Trust client “success” boolean |
| Recovery | Strong reset flow | SMS only forever with no rate limit |

## Output Checklist

- [ ] Domains, package, cert fingerprints recorded
- [ ] assetlinks.json live and complete
- [ ] Get/Create credential flows implemented
- [ ] Server WebAuthn verify complete
- [ ] Password/federated options decided
- [ ] Device QA across providers
- [ ] Recovery path reviewed
- [ ] `code-quality-standards` applied

## Rules

- Owned apps and RPs only.
- Passkeys require correct server verification — client UI is not authz.
- Protect signing keys; fingerprint mismatches break association.
- Do not phish or spoof Credential Manager UI.
- Coordinate biometric unlock policies with `android-biometric-prompt` when encrypting local data.
