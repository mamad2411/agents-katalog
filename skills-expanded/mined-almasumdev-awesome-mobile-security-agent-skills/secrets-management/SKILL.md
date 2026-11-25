---
name: secrets-management
description: Handling secrets for mobile clients — why the client should not hold secrets, how to use a config server, and how App Check / Play Integrity replace API keys. Use when adding third-party SDKs or new server endpoints.
---

# Secrets Management for Mobile Clients

## Instructions

The first rule of mobile secrets: **the client cannot keep a secret**. Anything embedded in your APK / IPA is extractable in minutes. Design accordingly.

### 1. What's Actually a Secret

| Value | Can ship in the app? |
| ----- | --- |
| OAuth `client_id` (public client) | Yes |
| OAuth `client_secret` | **No** — do not use confidential clients on mobile |
| Public keys (pinning, verification) | Yes |
| Private signing keys | **No** |
| Firebase / Maps / Analytics API key | Yes, but restrict by bundle ID + SHA |
| Third-party SDK secret (Stripe secret key, Twilio auth token) | **No, never** |
| Symmetric encryption key for local data | Generate on device, wrap with Keystore |

If the vendor says "use this secret from the mobile SDK", they mean the publishable key. Their secret key belongs on your server.

### 2. Restrict, Don't Hide

"Public" API keys (Firebase, Google Maps) can still be abused. Restrict at the provider:

- **Google Cloud keys** → restrict to `packageName + SHA-256 signing certificate` (Android) or `bundleId + teamId` (iOS).
- **Stripe** → use `pk_live_*` publishable keys only on the client; never `sk_live_*`.
- **Sentry DSN** → scoped to a single project with rate limits; safe to ship.

Abuse detection and quota limits still matter even on "public" keys.

### 3. Use a Config Server

For anything dynamic, fetch from your backend at launch:

```ts
// Pseudocode, same pattern on iOS / Android / Flutter / RN.
async function bootstrap() {
  const config = await api.get("/config", {
    headers: { "X-App-Attestation": await attest() },
  });
  featureFlags.apply(config.flags);
  runtimeSecrets.apply(config.scopedCredentials); // short-lived, per-user
}
```

The server:
- Requires a valid user session **or** device attestation.
- Returns scoped, short-lived credentials (signed URLs, STS tokens) — not long-lived API keys.
- Logs every issuance for audit.

### 4. Short-Lived Scoped Credentials

Instead of embedding AWS keys, upload via a signed URL:

- Client asks server: "I want to upload an avatar."
- Server: issues an S3 pre-signed PUT URL valid for 5 minutes, scoped to one object.
- Client: PUTs bytes directly. Server never proxies the upload.

Same pattern for database tokens (AWS STS / GCP Workload Identity Federation), Twilio short-lived tokens, etc.

### 5. App Check / Play Integrity as the Gatekeeper

Combine attestation with secrets issuance:

- Server only issues the signed URL / STS token if the request carries a valid App Attest assertion or Play Integrity token.
- Expired or missing attestation → 403, regardless of user auth.

This turns "anyone with the APK can hit our /upload endpoint" into "only a verified install of our app can".

### 6. Build-Time Injection Is Not Hiding

Patterns like:

```kotlin
val API_KEY = BuildConfig.API_KEY // read from gradle.properties
```

are convenient but **not secure**. The value ends up in plaintext in `strings.xml`, `BuildConfig`, or the binary. Use this only for values that are "public with restrictions" (category 1 above), and document that the value is not a secret.

### 7. WebViews and JS Bridges

- Never inject a secret into a WebView via `loadUrl("javascript:...")` — it lives in the page's memory and can be exfiltrated.
- Never expose a bridge method that returns a token without authentication.
- For OAuth, always round-trip through the system browser ([oauth-mobile](../../auth/oauth-mobile/SKILL.md)).

### 8. Rotating a Leaked Secret

When (not if) a secret leaks:

1. **Rotate** at the provider immediately.
2. Update the server to accept both old and new briefly.
3. Release a client update that picks the new value from config (not a hardcoded binary update).
4. Revoke the old value at the provider.
5. Audit what the leaked secret could access; treat it as a breach of that scope until proven otherwise.

Hardcoded secrets require a full client release to rotate — another argument against them.

## Checklist

- [ ] No OAuth `client_secret`, Stripe secret key, or vendor admin token is in the binary.
- [ ] Publishable / public keys are restricted by bundle ID + signing SHA at the provider.
- [ ] Scoped, short-lived credentials are used for cloud resources (S3, STS, Twilio).
- [ ] App Attest / Play Integrity gates secret / token issuance endpoints.
- [ ] No secret is exposed to a WebView or JS bridge.
- [ ] Secret rotation does not require a client-side binary update.
- [ ] A documented incident playbook covers secret leak → rotate → audit.
