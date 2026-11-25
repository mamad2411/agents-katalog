---
name: follow-lib-simplewebauthn-setup-simplewebauthn
description: Install simplewebauthn server+browser and set up the registration/authentication flow
argument-hint: "[ceremony-or-scope]"
related:
  - follow-lib-simplewebauthn
  - follow-lib-better-auth
  - learn
  - resolve-errors
---

## Goal

Install `@simplewebauthn/server` + `@simplewebauthn/browser` and set up the passkey registration/authentication ceremonies to work end-to-end — first-time setup only

## Scope

- use when the project has no simplewebauthn yet (if it exists already → verify only)
- covers: installing both sides, rpID/origin config, the registration + authentication ceremony flows
- if using Better Auth → consider the `passkey()` plugin via `/follow-lib-better-auth` instead of manual setup

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. read `package.json` — if `@simplewebauthn/*` is already present → skip to verify
2. determine `rpID` (domain, no protocol/port), `rpName`, `origin` (full URL including protocol+port) — a mismatch = ceremony fail
3. confirm HTTPS in production — WebAuthn needs a secure context (localhost dev is the exception)
4. determine the storage for credentials per user (id, publicKey, counter, transports)

### 2. Install

> Goal: install the packages for both server and browser

1. Server: `bun add @simplewebauthn/server`
2. Browser: `bun add @simplewebauthn/browser`
3. Types: import directly from `@simplewebauthn/server`/`browser` — `@simplewebauthn/types` was retired since v13
4. confirm both land in `dependencies`

### 3. Registration Ceremony

> Goal: enroll a new passkey per user

1. Server: `generateRegistrationOptions({ rpName, rpID, userName, ... })` → send the options to the client, store the challenge (session/DB, short-lived)
2. Browser: `startRegistration({ optionsJSON })` — v11+ accepts a single object only, never positional args
3. Server: `verifyRegistrationResponse({ response, expectedChallenge, expectedOrigin, expectedRPID })` → check `verified`
4. store the credential: `id`, `publicKey`, `counter`, `transports` bound to the user — support multiple credentials per user

### 4. Authentication Ceremony

> Goal: log in with a passkey

1. Server: `generateAuthenticationOptions({ rpID, allowCredentials })` → store the challenge
2. Browser: `startAuthentication({ optionsJSON })` — `useBrowserAutofill: true` for conditional UI (passkey autofill on the username field)
3. Server: `verifyAuthenticationResponse({ response, expectedChallenge, expectedOrigin, expectedRPID, credential })` → check `verified`
4. update `counter` from the response — a counter going backwards = possible cloned authenticator → flag/deny

### 5. Verify

> Goal: ceremonies really pass in a browser

1. test registration on a real browser (platform authenticator or security key)
2. test authentication — log in with the passkey just enrolled
3. wrong origin/rpID → the ceremony must fail (confirms the config is right)
4. run lint/typecheck — if it fails → run `/resolve-errors` max 3 rounds, then stop and report; passing → `/suggest-next-action`

## Rules

- Idempotent — if already set up, verify only
- The challenge must be random + one-time + short-lived — always verify server-side, never trust the client
- `rpID`/`origin` must match the actually deployed domain — a mismatch is the #1 cause of ceremony failures
- Always store and update `counter` — detects cloned authenticators
- Set `userVerification` per the required security level — if unsure about options → check the official docs (simplewebauthn.dev)

## Expected Outcome

- Server + browser packages installed, rpID/origin config correct
- Registration and authentication ceremonies pass end-to-end
- Credentials + counter stored securely per user
