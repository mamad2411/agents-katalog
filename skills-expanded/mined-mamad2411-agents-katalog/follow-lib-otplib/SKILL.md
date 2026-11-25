---
name: follow-lib-otplib
description: Use otplib for TOTP/HOTP 2FA — generate secret, verify token, QR provisioning
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - follow-lib-qrcode

---

## Goal

Use otplib for TOTP/HOTP 2FA — generate secret, verify token, QR provisioning

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (lib otplib)

- Covers: TOTP/HOTP secret generation, token generate/verify, `otpauth://` URI provisioning, crypto plugins, secret storage
- Not covered: rendering the QR image from an otpauth URI — use `/follow-lib-qrcode`; general auth/session design — see sibling skills per stack
- No CLI — used via programmatic API only (thus none)
- Latest: `otplib@13.5.0` (verified 2026-09-13) — v13 is a complete rewrite (breaking changes)
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-otplib/SKILL.md` — install, TOTP generate/verify, secret storage 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Use the functional API `import { generateSecret, generate, verify, generateURI } from 'otplib'` — or the class API `new OTP()` (v13 has no `preset-default`/`authenticator` anymore)
1. Generate a secret with `generateSecret()`, then create the otpauth:// URI with `generateURI({issuer, label, secret})` for the QR
1. Verify with `await verify({secret, token})` — returns a `VerifyResult`, check `.valid` (not a boolean) — set `epochTolerance` for clock drift
1. The API is async-first — `generateSync`/`verifySync` work only with a sync crypto plugin (`@otplib/plugin-crypto-node`/`@otplib/plugin-crypto-noble`)
1. Store the secret encrypted — never put it in a JWT or response

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib otplib)

## Rules

- Prefer TOTP (time-based) — HOTP only for specific use cases
- Always verify server-side, never verify on the client
- Rate-limit verify attempts to prevent brute-force
- `verify`/`verifySync` return an object `{valid}`, not a boolean — always check `result.valid`
- Migrate from v12 with `@otplib/v12-adapter` as a temporary bridge only, then move to the v13 API

- Use `/run-verify` if needed
- Use `/run-test` if needed
- Use `/follow-lib-qrcode` if rendering a QR from an `otpauth://` URI is needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib otplib)
- No known security/performance pitfalls (lib otplib)
- Lint, typecheck, tests pass
