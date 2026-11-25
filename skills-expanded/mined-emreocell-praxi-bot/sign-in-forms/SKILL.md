---
name: sign-in-forms
description: Handle multi-step sign-in flows, SSO redirects, and 2FA prompts safely using stored fill secrets.
version: 0.1.0
when:
  keywords: [sign in, login, log in, two-factor, 2fa, sso, authenticate]
---
# Sign-in forms

Goal: sign in safely without ever typing raw passwords from chat or bypassing verification.

1. Run `browser_snapshot` to inspect the login form before acting.
2. Check whether the form is single-step (email + password together) or split across pages (email first, "Next" / "Continue", then password).
3. If an email or username field is shown and the user provided an identifier, fill it with `browser_fill`. For passwords or passcodes, only use `browser_fill` with a `secret` reference if the owner has configured one.
4. For SSO ("Continue with Google / GitHub / Microsoft") or multi-step redirects, click the provider button, then `browser_wait` for navigation to settle and re-snapshot.
5. When a CAPTCHA, human verification gate, 2FA/OTP prompt, or security key check appears, stop and use `ask_user` so the user can complete it directly.
6. After sign-in completes, run `browser_snapshot` to confirm the expected account or dashboard view is loaded.

Safety:
- Never ask the user to paste a raw password in chat, and never invent or guess credentials.
- Never attempt to solve or bypass CAPTCHAs or anti-bot challenges.
