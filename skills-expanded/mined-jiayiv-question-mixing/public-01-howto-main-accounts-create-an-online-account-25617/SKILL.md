---
name: create-an-online-account
domain: accounts
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: [have-email-address]
status: draft
last_verified: 2026-07-20
---

## Goal

Hold a working account on a target website or app: you can sign out, sign back in, and reach the service's logged-in home surface.

## Preconditions

- An email address you can read (or a phone number that receives SMS).
- The service's name or URL is known.
- A password manager or a way to store a new password.

## Steps

1. **Open the service's official site or app.** Type the URL directly or use an app store — avoid links from unsolicited messages. → *Expect:* the landing page shows the service's name and a "Sign up" / "Create account" / "Register" affordance.
2. **Start registration.** Click "Sign up". [BRANCH: email signup | single-sign-on (Google/Apple)] SSO is faster but couples this account to the identity provider; email signup keeps them independent. → *Expect:* a form asking for email/username and password, or a provider chooser.
3. **Enter identity fields.** Provide email and any required profile fields. Give only what is marked required. → *Expect:* no validation errors on the form.
4. **Set a strong unique password.** Generate it in a password manager and save the entry before submitting. → *Expect:* the password field accepts it (meets the site's stated rules).
5. **Submit the form.** ⚠️ *Irreversible:* some services bind a username permanently — confirm the username is the one you want before submitting. → *Expect:* a "verify your email" notice, or direct entry into the logged-in state.
6. **Verify your email or phone.** Open the verification message and click the link or enter the code within its validity window. → *Expect:* the site confirms verification; the account is active.
7. **Log out and log back in once.** → *Expect:* your saved credentials work; you land on the logged-in home surface.

## Decision points

- The form demands a phone number you don't want to give → check if email-only signup exists; otherwise decide whether the service is worth it.
- Email verification message doesn't arrive → F1.
- The site says the email is already registered → switch to `accounts/recover-a-password`.

## Failure modes & recovery

- **F1 Verification email missing:** check spam; use "resend"; confirm the address was typed correctly (re-enter it if the site allows editing).
- **F2 Password rejected repeatedly:** read the site's exact rules (length, symbol classes); regenerate to match.
- **F3 CAPTCHA loop:** disable VPN, switch browser, or wait — repeated failures often mean IP throttling.

## Verification

A full sign-out → sign-in cycle succeeds with the stored credentials, and the account shows as verified (no pending-verification banner).

## Variations

- `mobile-app`: verification may use a deep link that must be opened on the same device.
- Services with 2FA prompts at signup: complete 2FA enrollment immediately and store recovery codes with the password entry.

## Safety & privacy

Medium risk: you are creating an identity. Give the minimum data required, never reuse a password, and store recovery codes. The verification step is a common phishing target — only click verification links that match the service's exact domain.
