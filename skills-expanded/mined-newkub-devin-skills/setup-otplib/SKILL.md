---
name: follow-lib-otplib-setup-otplib
description: Install otplib v13 and set up TOTP generate/verify with secure secret storage
argument-hint: "[scope]"
related:
  - follow-lib-otplib
  - follow-lib-qrcode
  - follow-secret-manager
  - learn
  - resolve-errors
---

## Goal

Install `otplib` v13 and set up the TOTP 2FA flow — generate secret, QR provisioning, verify — with secure secret storage — first-time setup only

## Scope

- Use when the project doesn't have otplib yet (already present → verify only; on v12 → migrate via `@otplib/v12-adapter` as a bridge)
- Covers: install, `generateSecret`/`generate`/`verify`/`generateURI`, crypto plugin, secret storage
- v13 is a rewrite — functional API, async-first, no more `preset-default`/`authenticator`

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. Read `package.json` — if `otplib` is present, check the version (the v12 API differs a lot from v13)
2. Determine where verify runs — server only; never verify on the client
3. Determine storage for TOTP secrets — a database field that can be encrypted
4. If unsure about the API → run `/learn-from-web` on the official docs

### 2. Install

> Goal: install otplib and the crypto plugin for the runtime

1. Run `bun add otplib` (or the package manager matching the lockfile)
2. Install the crypto plugin for the runtime — e.g. `@otplib/plugin-crypto-node` or `@otplib/plugin-crypto-noble` (required for the sync APIs)
3. Confirm it lands in `dependencies`

### 3. TOTP Flow

> Goal: the enroll and verify flows work

1. Enroll: `generateSecret()` per user → store the secret encrypted in the DB (don't activate until the first verify passes)
2. QR provisioning: `generateURI({ issuer, label, secret })` → render the QR with `/follow-lib-qrcode` or the lib the project uses
3. Verify: `await verify({ secret, token })` — returns a `VerifyResult`, check `.valid` (not a boolean)
4. Set `epochTolerance` for clock drift of the authenticator app
5. `generateSync`/`verifySync` work only when a sync crypto plugin is registered — use the async APIs by default

### 4. Secure Secret Storage

> Goal: secrets don't leak and verify resists brute force

1. Encrypt the secret before storing it in the DB (app-level or DB encryption) — no plaintext in production
2. Never put the secret in JWTs, API responses, or logs — the URI is sent once at enrollment only
3. Rate-limit verify attempts per user/IP — guards against brute-forcing 6-digit codes
4. Add recovery codes or a fallback method — a user who loses a device must still get back in

### 5. Verify

> Goal: the enroll→verify round-trip actually passes

1. Smoke: `generateSecret` → `generate({ secret })` or a token from the authenticator → `verify` returns `.valid === true`
2. Wrong token → `.valid === false`; the rate limit works
3. Run lint/typecheck — if it fails → run `/resolve-errors` max 3 rounds then stop and report; passes → `/suggest-next-action`

## Rules

- Idempotent — if setup already happened, verify only
- Prefer TOTP — HOTP for specific use cases only
- Always verify on the server — the client sends just the token
- `verify`/`verifySync` return `{ valid }` — always check `result.valid`
- Migrate v12 → v13 via `@otplib/v12-adapter` as a temporary bridge only

## Expected Outcome

- `otplib` v13 + crypto plugin installed; the enroll/verify flow passes
- Secrets encrypted at rest, rate limiting enabled
- Ready to integrate into the project's auth flow
