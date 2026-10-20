---
name: log-in
domain: accounts
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: medium
prerequisites: [accounts/create-an-online-account]
status: draft
last_verified: 2026-07-20
---

## Goal

You are authenticated on a service where you already hold an account, at its logged-in home surface.

## Preconditions

- An existing account and its credentials (password manager entry, or SSO provider access).
- If 2FA is enabled: the second factor (phone, authenticator app, or hardware key) at hand.

## Steps

1. **Open the service's official login page.** Type the URL, use a bookmark, or the app — never a login link from an unexpected email or message. → *Expect:* the domain in the address bar is the service's real domain; a login form is shown.
2. **Choose the login method.** [BRANCH: username + password | SSO ("Sign in with Google/Apple") | passkey] Use the method the account was created with. → *Expect:* the corresponding prompt appears.
3. **Enter credentials.** Autofill from the password manager where possible — autofill refusing to fill is itself a phishing warning (domain mismatch). → *Expect:* fields populated; no manager warning.
4. **Submit.** → *Expect:* either the logged-in home surface, or a 2FA challenge.
5. **Complete 2FA if challenged.** Enter the app/SMS code, or approve the push prompt *only if you initiated this login seconds ago*. ⚠️ *Irreversible:* approving a push you didn't initiate hands your account to an attacker — deny unexpected prompts. → *Expect:* challenge accepted.
6. **Confirm you are logged in.** → *Expect:* your account name/avatar visible; the URL is a logged-in surface, not the login page.

## Decision points

- "Remember this device?" → accept only on your own private device.
- Password not accepted → one careful retype, then `accounts/recover-a-password` — repeated guesses trigger lockouts.
- Login alerts of a new device email arrives → expected if this is a new device; investigate immediately if not.

## Failure modes & recovery

- **F1 Lockout after failed attempts:** wait the stated cooldown, then use `accounts/recover-a-password`.
- **F2 2FA code rejected:** check the device clock (TOTP drifts), use the freshest code; fall back to recovery codes.
- **F3 Login loop (accepted then bounced back):** clear the site's cookies or try a private window — a stale session cookie is the usual cause.

## Verification

The logged-in home surface shows your identity, and a page refresh keeps you logged in.

## Variations

- `mobile-app`: biometrics may replace the password after first login; the ⚠️ push-approval rule is identical.
- Passkeys: device biometric prompt replaces steps 3–5.

## Safety & privacy

Medium risk: credentials are the target. The two boundaries: verify the domain before typing anything, and never approve a 2FA prompt you didn't just cause.
