---
name: follow-lib-line-liff
description: Use @line/liff to build LIFF mini-apps — init, profile, login, shareTargetPicker
argument-hint: "[target-or-scope]"
related:
  - follow-secret-manager
  - run-verify
  - run-test

---

## Goal

Use @line/liff to build LIFF mini-apps — init, profile, login, shareTargetPicker

## Scope

Use when the task involves `@line/liff` — the client-side (browser/LINE app) LIFF SDK only (lib line liff)

- `@line/liff` is a browser-only SDK — use it in SPA/frontend only, not server-side
- Server-side: verifying the ID token via the LINE verify endpoint + Messaging API is out of this skill's scope
- Channel secrets/credentials are managed via `/follow-secret-manager` — never commit

- Latest: `@line/liff@2.31.0` (verified 2026-09-13)
- References: [apis](references/apis.md) 
## Execute

### 1. Check Preconditions

> Goal: prepare the LIFF app and channel before writing code

1. Create a LIFF app in the LINE Developers Console attached to a channel — get the `liffId`
1. Set the LIFF app's endpoint URL in the console to match the URL actually hosting the app
1. Install `bun add @line/liff` — types are included in the package
1. Keep the `liffId` in env/config — never hardcode if it differs per environment

### 2. Setup And Usage

> Goal: use correctly per the official docs

1. Initialize with `liff.init({liffId})` on the client — await the promise before using other APIs; `withLoginOnExternalBrowser` for auto-login outside the LINE app
1. Check `liff.isInClient()`/`isLoggedIn()` before using APIs — outside the LINE app you need `liff.login()` (OAuth redirect, accepts `redirectUri`)
1. Use `liff.getProfile()` for display and send `liff.getIDToken()` to the server for verification — never trust client-side profile data
1. Use `shareTargetPicker`, `sendMessages`, `scanCodeV2`, `getContext()` (type, userId, chatId) per feature — some APIs work only inside the LINE app

### 3. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib line liff)

## Rules

- Always verify the ID token server-side with the LINE API
- LIFF v2 — the SDK works in the LINE app or an external browser (behavior differs)
- Test both in-client and external browser modes
- Handle init failures — liff.init is a promise

- Use `/follow-secret-manager` if channel secrets management is needed
- Use `/run-verify` if needed
- Use `/run-test` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib line liff)
- No known security/performance pitfalls (lib line liff)
- Lint, typecheck, tests pass
