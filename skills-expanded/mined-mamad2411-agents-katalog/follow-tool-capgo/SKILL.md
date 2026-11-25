---
name: follow-tool-capgo
description: Use @capgo/capacitor-updater OTA updates and native-biometric auth in Capacitor apps
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - follow-secret-manager
  - setup-cicd

---

## Goal

Use @capgo/capacitor-updater OTA updates and native-biometric auth in Capacitor apps

## Scope

Use when a task involves this library/tool — setup, usage, debugging, or best practices (tool capgo)

- Boundary: Capgo OTA updates cover only the web assets of a Capacitor app — native code changes must always ship through the App Store/Play Store; for general web releases see `/follow-tool-changesets` or `/follow-tool-changelogen`
- Latest: `@capgo/capacitor-updater@8.51.25` / `@capgo/cli@8.66.0` (verified 2026-09-26)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Install Plugins And CLI

> Goal: install the updater/biometric plugins and the Capgo CLI

1. Install the updater in the app: `bun add @capgo/capacitor-updater` — requires `@capacitor/core` `^8.0.0` as a peer dependency
2. If using biometrics: `bun add @capgo/capacitor-native-biometric`
3. Install the CLI as dev tooling: `bun add -D @capgo/cli`
4. Sync native projects after adding a plugin: `bunx cap sync`

### 2. Configure Capgo Account

> Goal: authenticate and register the app on Capgo

1. Prepare `CAPGO_TOKEN` via `/follow-secret-manager` — never hardcode
2. Run `bunx capgo init` or `bunx capgo login --apikey <key>`
3. Register the app: `bunx capgo app add --name <app-name>`
4. For signed updates: `bunx capgo key save --key <key-file>`

### 3. Implement OTA Update Flow

> Goal: the updater works correctly and can roll back

1. Call `CapacitorUpdater.notifyAppReady()` after a successful boot — without it the bundle auto-rolls back
2. Choose the `autoUpdate` or manual `download()`/`set()` flow
3. Test the rollback path — a broken bundle must revert automatically

### 4. Implement Biometric Auth

> Goal: biometric login with a fallback

1. Check `NativeBiometric.isAvailable()` before `verifyIdentity()` — fall back to PIN when the hardware is unsupported
2. Store credentials with `setCredentials()` (Keychain/Keystore), not plain storage

### 5. Upload Bundle Via CI

> Goal: deploy the web bundle to a channel through CI

1. Upload: `bunx capgo bundle upload --channel production --path dist`
2. Assign the channel: `bunx capgo channel set --channel production --latest`
3. Set `CAPGO_TOKEN` in CI secrets — see `/setup-cicd` for the workflow

### 6. Verify

> Goal: confirm everything is correct

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if relevant tests exist
3. Check the latest official docs before using an uncertain API (tool capgo)

## Rules

- OTA updates cover web assets only — native changes must go through the app store
- `@capgo/capacitor-updater` v8 requires `@capacitor/core` `^8.0.0` (peer dependency)
- Test the rollback path — a broken bundle must revert automatically
- Biometrics must have a fallback when the hardware is unsupported

- Use /follow-secret-manager if needed
- Use /setup-cicd if needed
- Use /run-verify if needed
- Use /run-test if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library used correctly per best practices (tool capgo)
- No known security/performance pitfalls (tool capgo)
- Lint, typecheck, tests pass
