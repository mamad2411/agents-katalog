---
name: follow-service-workos-setup-workos
description: Install the WorkOS SDK, create credentials from the dashboard, and init the client so it can call the APIs — first-time setup only
related:
  - follow-service-workos
---

## Goal

Install the WorkOS SDK, create credentials from the dashboard, and init the client so it can call the APIs — first-time setup only

## Scope

- Install the SDK per runtime (`@workos-inc/node`, `workos-python`, etc.)
- Create and store `WORKOS_API_KEY`, `WORKOS_CLIENT_ID` securely
- Init the client and smoke check
- Does not cover AuthKit/SSO/Directory config → use `workflows/config-workos/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: Confirm the runtime and current state (idempotent)

1. Read `package.json` to identify the runtime and package manager
2. Check whether `@workos-inc/node` or another SDK is already installed → if so, skip to verify
3. Do `/check-secrets env-vars` to see whether `WORKOS_API_KEY`, `WORKOS_CLIENT_ID` already exist
4. If there is no WorkOS account → stop and tell the user to create one from the dashboard

### 2. Install SDK

> Goal: Install the SDK per runtime

1. Node/Bun: `bun add @workos-inc/node` (or the detected package manager)
2. Python: `pip install workos` — for other languages check official docs
3. Confirm the dependency is in the project manifest

### 3. Create And Store Credentials

> Goal: Prepare the API key and client ID securely

1. Create an API key and read the client ID from the WorkOS Dashboard — use `/open-web-for-config-secret` (service workos) if the dashboard must be opened
2. Store `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` in `/follow-secret-manager` — never put the real `.env`
3. Inject them into the dev/staging/prod environments separately

### 4. Init Client And Verify

> Goal: init the client and smoke check against the real API

1. Create the client such as `new WorkOS(process.env.WORKOS_API_KEY)` in a server-side module
2. Smoke check with a read-only call such as listing users/organizations — check official docs for the latest methods
3. Do `/run-verify` — if it fails → do `resolve-errors` max 3 rounds, then stop and report

## Rules

- Never hardcode the API key or commit secrets — always use `/follow-secret-manager`
- The client must be initialized server-side only — never expose `WORKOS_API_KEY` to the browser
- Separate keys per environment (dev/staging/prod)
- If unsure about an API/method → check official docs or `learn` (web) first

## Expected Outcome

- WorkOS SDK installed and present in the manifest
- `WORKOS_API_KEY`, `WORKOS_CLIENT_ID` secure and correctly injected
- Client initialized and smoke check passes
