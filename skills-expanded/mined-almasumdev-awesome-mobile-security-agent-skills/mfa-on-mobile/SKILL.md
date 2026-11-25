---
name: mfa-on-mobile
description: Multi-factor authentication on mobile — TOTP, push-based MFA, and recovery UX. Use when adding or reviewing a second factor.
---

# MFA on Mobile

## Instructions

MFA on mobile covers both the **app as the authenticator** (TOTP / push) and the **app as the user** (consuming a second factor during login).

### 1. Factor Types

| Factor | Strength | Notes |
| ------ | -------- | ----- |
| SMS OTP | Weak | SIM swap, SS7. Avoid unless regulation forces it. |
| Email OTP | Weak–medium | Inherits email account security. |
| TOTP (RFC 6238) | Medium | No phishing resistance on its own. |
| Push approval | Medium | Good UX; vulnerable to MFA fatigue. |
| FIDO2 / passkeys | Strong | Phishing-resistant. Prefer where available. |

### 2. TOTP as an Authenticator App

- Use the standard **RFC 6238** with SHA-1 or SHA-256, 6 digits, 30-second period for maximum compatibility. Document any deviation.
- Store the shared secret **only** in Keystore / Keychain, wrapped by a biometric-gated key.
- Never back up TOTP secrets to iCloud / Google Drive in plaintext.

```kotlin
fun generateTotp(secret: ByteArray, time: Long = System.currentTimeMillis()): String {
    val counter = ByteBuffer.allocate(8).putLong(time / 1000 / 30).array()
    val mac = Mac.getInstance("HmacSHA1").apply { init(SecretKeySpec(secret, "HmacSHA1")) }
    val hash = mac.doFinal(counter)
    val offset = hash.last().toInt() and 0x0f
    val bin = ((hash[offset].toInt() and 0x7f) shl 24) or
              ((hash[offset + 1].toInt() and 0xff) shl 16) or
              ((hash[offset + 2].toInt() and 0xff) shl 8) or
               (hash[offset + 3].toInt() and 0xff)
    return "%06d".format(bin % 1_000_000)
}
```

### 3. Push-Based MFA (Done Right)

Push MFA is a signing operation, not a boolean tap:

1. Server sends a push with a `challenge_id` — **not** an "approve / deny" payload alone.
2. App fetches the challenge detail (amount, merchant, IP, location) over an authenticated channel.
3. User reviews human-readable context and confirms.
4. App signs `challenge_id || context_hash` with a biometric-gated Keystore key.
5. Server verifies the signature against the registered device public key.

Never auto-approve. Never accept a push whose contents you didn't fetch over HTTPS from the server.

### 4. Preventing MFA Fatigue

- Require **number matching** (user types a 2-digit code shown on the origin device).
- Throttle push requests server-side; after N rapid prompts, fall back to a stronger factor.
- Log and surface unusual prompts (new country, new device) in an in-app audit log.

### 5. Consuming MFA During Login

If your app is an OAuth client:

- Prefer `acr_values` / `amr` claims in the `id_token` so the server tells you what factors were used.
- Support the browser flow's step-up — do not re-implement the challenge in the native app.
- On step-up failure, clearly distinguish "wrong code" from "account locked".

### 6. Recovery UX

Recovery is where MFA projects usually fail:

- Provide **backup codes** at enrollment (one-time, downloadable, printable). Store the hash server-side.
- Support **FIDO2 security keys** as a non-lose-your-phone recovery option when feasible.
- Document an account-recovery flow that is slower and more verified than normal login (identity check, cooling-off period).
- Never allow "email a reset link" to fully bypass MFA on high-value accounts.

### 7. Platform APIs

- iOS: `ASAuthorizationController` + `ASAuthorizationPlatformPublicKeyCredentialProvider` for passkeys.
- Android: `CredentialManager` for passkeys / saved passwords.
- Flutter: `credential_manager` package.
- React Native: `react-native-passkey`.

Passkeys are strictly better than TOTP for most apps; ship them where the user base has device support.

## Checklist

- [ ] SMS is not the only second factor offered on high-value accounts.
- [ ] TOTP secrets live in Keystore / Keychain, biometric-gated.
- [ ] Push MFA signs a server-provided challenge (not a boolean approval).
- [ ] Number matching or equivalent anti-fatigue control is in place.
- [ ] Backup codes and/or passkey recovery are offered at enrollment.
- [ ] Account recovery is explicitly slower / more verified than normal login.
- [ ] Passkeys are supported where the platform allows.
