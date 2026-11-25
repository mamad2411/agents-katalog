---
name: mobile-authentication
description: Implement secure mobile auth. Use when handling sign-in, tokens,
  and sessions in apps.
metadata:
  tags: mobile, authentication
---

# Mobile Authentication

## Use this skill when
- Secure token storage on device
- Biometric and OAuth sign-in on mobile
- Session refresh and logout

## Do not use this skill when
- Web cookie sessions
- Server-side auth architecture (use its own skill)

## Instructions
1. Store tokens in secure storage (Keychain, Keystore), never plaintext.
2. Prefer OAuth code flow with PKCE and a browser/ASWebAuthenticationSession.
3. Add biometrics as a convenience layer over a secure credential.
4. Handle refresh token rotation and silent re-auth.
5. Clear local data securely on logout.
6. Avoid cutting corners: no tokens in shared prefs or logs.

## Checklist
- Tokens in secure enclave storage
- PKCE in use
- Logout purges local data

## Output Format
- Token storage | flows | biometrics | logout

## Common Mistakes
- Tokens in insecure storage
- Skipping PKCE
- Stale user data after logout
