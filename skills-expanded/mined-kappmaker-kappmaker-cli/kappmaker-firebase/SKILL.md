---
name: kappmaker-firebase
description: Set up Firebase for a KAppMaker app — project, Android and iOS apps, and the google-services config files. Use when the user asks to set up Firebase, add google-services.json or GoogleService-Info.plist, or enable Firebase auth or analytics.
---

# KAppMaker — Firebase

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### firebase — Firebase Setup Steps (steps 2–6 of `create`)

Five subcommands, each running one part of `create`'s Firebase flow as a standalone. Run them individually for partial setups (e.g. an existing Firebase project that just needs SDK configs), or chain them together to replicate `create`.

**Subcommands**:
- `kappmaker firebase login` — `firebase login` (interactive)
- `kappmaker firebase project --app-name <Name>` — create the project (or `--project-id <id> --display-name <name>`)
- `kappmaker firebase apps --project <id> --app-name <Name> --package-name <pkg>` — create Android + iOS apps
- `kappmaker firebase auth-anonymous --project <id>` — enable anonymous auth (handles the "click Get started" Auth init flow)
- `kappmaker firebase configs --project <id> --app-name <Name> [--package-name <pkg>]` — download SDK configs

**Prerequisites**:
- `firebase` CLI installed (`which firebase`; auto-installs via `npm install -g firebase-tools` if missing)
- `firebase login` must have been run before any of `project`/`apps`/`auth-anonymous`/`configs`

**Naming conventions used by `create`** — match these if you want to replicate what `create` does:
- Project ID: `<lowercase-app-name>-app` (e.g. `myapp-app` for `MyApp`). The `--app-name` shortcut on `firebase project` derives this for you.
- App display names: `${appName} (Android App)` and `${appName} (iOS App)`. `firebase configs` looks up apps by these names unless you pass `--android-app-id`/`--ios-app-id`.

**`firebase configs` output paths** auto-detect from cwd:
1. `MobileApp/androidApp/google-services.json` if `MobileApp/androidApp/` exists (AGP 9 layout)
2. `MobileApp/composeApp/google-services.json` if `MobileApp/composeApp/` exists (legacy)
3. `Assets/google-services.json` as last-resort fallback

Same probe for iOS (`MobileApp/iosApp/iosApp/GoogleService-Info.plist` first). Override via `--android-output` / `--ios-output`.

**Idempotency**:
- `firebase project` skips creation if the project already exists.
- `firebase apps` reuses apps that match the expected display name instead of creating duplicates.
- `firebase configs` always re-downloads (cheap, no side effects).

**`--package-name` on configs** — when set, the downloaded `google-services.json` is verified to contain the expected package and patched in-place if mismatched (e.g. when the Firebase app was registered with a different `bundleIdPrefix` previously). Pass it whenever you have the new package name handy.

**When to suggest these standalone over `create`**:
- User has an existing Firebase project and just needs SDK configs → `firebase configs`.
- User wants to set up a Firebase project for an already-cloned project → `firebase project` → `firebase apps` → `firebase auth-anonymous` → `firebase configs`.
- CI step that just needs to refresh `google-services.json` → `firebase configs --project ... --android-app-id ...`.

The full `create` orchestrator calls these five commands internally for steps 2–6.

---

## Where this sits in the flow

- **Before this:** **kappmaker-new-app** — the project must exist.
- **After this:** **kappmaker-monetization**, or straight to building features.
