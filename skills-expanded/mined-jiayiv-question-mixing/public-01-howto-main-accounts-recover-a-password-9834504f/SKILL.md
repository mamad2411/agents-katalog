---
name: recover-a-password
domain: accounts
locale: [generic]
interface: web
difficulty: basic
est_time: 15min
risk: medium
prerequisites: [have-email-address]
status: draft
last_verified: 2026-07-20
---

## Goal

Regain access to an existing account whose password you cannot produce, and leave it with a new stored password.

## Preconditions

- You control the email address or phone number the account was registered with.
- The service's login page is reachable.

## Steps

1. **Go to the official login page.** Type the URL or use a stored bookmark — never a link from an email claiming your account has a problem. → *Expect:* the service's normal login form.
2. **Trigger the reset flow.** Click "Forgot password?" and enter the account's email or username. → *Expect:* a notice that reset instructions were sent (services deliberately say this even for unknown addresses).
3. **Open the reset message.** Find the email/SMS; check spam after ~2 minutes. Confirm the sender domain matches the service exactly. → *Expect:* a reset link or one-time code with a validity window.
4. **Set the new password.** Follow the link, generate a new unique password in your password manager, and save the entry *before* submitting. → *Expect:* "password changed" confirmation.
5. **Log in with the new password.** → *Expect:* you reach the logged-in home surface.
6. **Review account security.** Check active sessions and recent-activity pages if offered; sign out unknown sessions. ⚠️ *Irreversible:* "sign out all devices" will disconnect legitimate devices too — reconnect them afterward. → *Expect:* only your devices remain listed.

## Decision points

- No reset email after resend + spam check → F1.
- You no longer control the registered email → F2 (account-recovery form; expect identity questions and a waiting period).
- The account has 2FA and you lost the second factor → use stored recovery codes; without them, F2.

## Failure modes & recovery

- **F1 Reset message never arrives:** the account may exist under a different email — try alternates; or the account may not exist — try `accounts/create-an-online-account`.
- **F2 Registered contact lost:** use the service's dedicated account-recovery form (search "<service> account recovery"); prepare previous passwords, payment records, and creation date as evidence.
- **F3 Reset link expired:** restart from step 2; complete within the validity window.

## Verification

A fresh login with the new stored password succeeds, and no unknown active sessions remain on the account.

## Variations

- `phone-call`: banks and telecoms often require a call with identity verification instead of a web flow.
- SSO accounts ("Sign in with Google"): there is no service password — recover the provider account instead.

## Safety & privacy

Medium risk: reset flows are the #1 phishing vector. Initiate the flow yourself from the official site; treat unsolicited "reset your password" messages as hostile unless you triggered them seconds earlier.
