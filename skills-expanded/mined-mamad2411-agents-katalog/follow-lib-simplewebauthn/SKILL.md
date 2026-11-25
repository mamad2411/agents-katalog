---
name: follow-lib-simplewebauthn
description: Use simplewebauthn for passkeys/WebAuthn — registration + authentication ceremonies
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - follow-lib-better-auth

---

## Goal

Use simplewebauthn for passkeys/WebAuthn — registration + authentication ceremonies

## Scope

Use when the task involves manual passkeys/WebAuthn — setup, ceremonies, credential storage, debugging, or best practices

- Use this skill when implementing WebAuthn yourself with `@simplewebauthn/server` + `@simplewebauthn/browser`
- If the project already uses Better Auth, use the `passkey()` plugin via `/follow-lib-better-auth` instead of manual setup

- Latest: `@simplewebauthn/server@14.0.2` / `@simplewebauthn/browser@14.0.0` (verified 2026-09-16)
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-simplewebauthn/SKILL.md` — server+browser install, ceremony flow 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. server: `generateRegistrationOptions` → client `startRegistration({ optionsJSON })` → `verifyRegistrationResponse`
1. server: `generateAuthenticationOptions` → client `startAuthentication({ optionsJSON })` → `verifyAuthenticationResponse`
1. Since v11 browser methods accept a single object only — never pass options as a positional arg directly; `useBrowserAutofill: true` for conditional UI (passkey autofill)
1. Store the credential: id, publicKey, counter, transports — per user
1. Set `rpID`, `rpName`, `origin` to match the domain — a mismatch = ceremony fail

### 2. Store Credentials

> Goal: persist credentials so ceremonies can repeat

1. Store the per-user credential: `id`, `publicKey`, `counter`, `transports` — tied to the user record
2. Update `counter` from `verifyAuthenticationResponse` every time — a non-increasing counter = possible cloned authenticator
3. Support multiple credentials per user (multiple devices)

### 3. Common Pitfalls

> Goal: avoid the most common ceremony failures

1. `rpID` is the domain only (no protocol/port); `expectedOrigin` is the full origin like `https://app.com` — dev uses `http://localhost:5173`
2. The challenge must be random + one-time + short-lived — verify server-side only
3. Production requires HTTPS — WebAuthn works only in a secure context (localhost excepted)
4. Passkey autofill: `startAuthentication({ optionsJSON, useBrowserAutofill: true })` + `<input autocomplete="username webauthn">`

### 4. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib simplewebauthn)

## Rules

- The challenge must be random + one-time + short-lived — verify server-side
- Store the `counter` to detect cloned authenticators
- Require `userVerification` per the security level
- Support multiple credentials per user
- `@simplewebauthn/types` was retired since v13 — import types directly from `@simplewebauthn/server`/`browser`
- Use `preferredAuthenticatorType` in `generateRegistrationOptions` (`'securityKey'`, `'localDevice'`, `'remoteDevice'`) when you want to set hints

- Use `/run-verify` if needed
- Use `/run-test` if needed
- Use `/follow-lib-better-auth` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib simplewebauthn)
- No known security/performance pitfalls (lib simplewebauthn)
- Lint, typecheck, tests pass
