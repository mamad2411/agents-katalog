---
name: enable-two-factor-authentication
domain: accounts
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: [accounts/log-in]
status: draft
last_verified: 2026-07-20
---

## Goal

The account requires a second factor at login, and you hold working recovery codes stored safely.

## Preconditions

- You can log in to the account (`accounts/log-in`).
- A second-factor option: an authenticator app installed, a phone number, or a hardware security key.
- A place to store recovery codes (password manager entry, printed copy in a safe place).

## Steps

1. **Open the account's security settings.** Usually Account → Settings → Security → "Two-factor authentication" / "2-step verification". → *Expect:* a 2FA section showing status "off".
2. **Choose the factor type.** [BRANCH: authenticator app (recommended) | hardware key (strongest) | SMS (weakest — SIM-swap risk)] → *Expect:* the setup flow for the chosen factor starts; the site may re-ask your password.
3. **For an authenticator app: scan the QR code.** Open the app → add account → scan. → *Expect:* the app shows a 6-digit code for this service, refreshing every 30 s.
4. **Enter the current code to confirm pairing.** → *Expect:* the site accepts it and 2FA flips to "on".
5. **Save the recovery codes — do not skip.** Copy every code into the password manager entry (or print). ⚠️ *Irreversible:* losing both your factor and these codes can permanently lock the account; this step is the insurance. → *Expect:* codes stored and readable outside this device.
6. **Test the full loop.** Log out, log in, complete the 2FA challenge. → *Expect:* login succeeds through the new challenge.
7. **Review trusted devices and fallback factors.** Remove stale devices; delete the SMS fallback if you chose app/key and the service allows it. → *Expect:* only intended devices and factors remain listed.

## Decision points

- Service offers passkeys → prefer a passkey over TOTP where both exist; it resists phishing.
- Shared/team account → the factor must live somewhere all owners can reach (shared vault), not one person's phone.
- Old phone being replaced soon → enroll the new device *before* wiping the old one, or export the authenticator's accounts.

## Failure modes & recovery

- **F1 QR won't scan:** use the "enter key manually" option — type the setup key into the app.
- **F2 Codes rejected at step 4:** device clock skew — enable network time on the phone and retry with a fresh code.
- **F3 Recovery codes never shown:** find "generate recovery codes" in the same settings section; generating anew invalidates old ones.

## Verification

A fresh logout/login requires and accepts the second factor, and the recovery codes exist in storage independent of the enrolled device.

## Variations

- Hardware key: steps 3–4 become "insert/tap the key when prompted"; register a second backup key.
- `mobile-app`-only services: settings live in the app; the QR path is replaced by an in-app approval toggle.

## Safety & privacy

Medium risk, high payoff: 2FA is the single most effective account protection. The dangerous step is 5 — treat recovery codes like the password itself; anyone holding them can bypass the factor.
