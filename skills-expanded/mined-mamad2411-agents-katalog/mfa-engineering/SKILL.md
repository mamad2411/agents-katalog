---
name: mfa-engineering
description: Implement multi-factor authentication. Use when adding a second
  factor to login flows.
metadata:
  tags: mfa, engineering
---

# Multi-Factor Authentication

## Use this skill when
- Adding TOTP, WebAuthn, or backup codes
- Designing enrollment and recovery
- Handling compromised-device scenarios

## Do not use this skill when
- SMS OTP as the sole strong factor (prefer TOTP/WebAuthn)
- Auth architecture itself (use its own skill)

## Instructions
1. Prefer WebAuthn (passkeys) and TOTP over SMS for strength.
2. Enroll after password verification; generate backup codes.
3. Rate limit and lock out on MFA failures.
4. Bind MFA to sessions and refresh flows.
5. Provide a safe, tested recovery flow (backup codes, recovery tokens).
6. Force re-auth (step-up) for sensitive actions.
7. Never log OTPs or codes.

## Checklist
- Backup codes issued and stored securely
- Re-auth for privilege escalation
- No OTPs in logs

## Output Format
- Factors | enrollment flow | recovery flow | step-up rules

## Common Mistakes
- SMS as the only factor
- MFA bypass on password reset
- No recovery path (account lockout)
