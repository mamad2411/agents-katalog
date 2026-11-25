---
name: eas-mobile-deployment
description: Explains how EAS Build and Submit work together for App Store and Google Play deployment. Use when configuring eas.json, troubleshooting mobile builds/submissions, or understanding version management, submit profiles, and the build-then-submit pipeline.
---

# EAS Mobile Deployment

## How It Works

BUILD and SUBMIT are independent EAS services. A build creates the binary. A submit uploads an existing binary to a store. They never need to run together.

- `eas build` creates an IPA (iOS) or AAB (Android) and stores it on EAS
- `eas submit` takes an existing build artifact and uploads it to App Store Connect or Google Play
- A single build can be submitted multiple times (e.g. first to internal track, then to production)
- A failed submission does not require a rebuild

### Distribution Settings (CRITICAL)

The `distribution` field controls build type, but does NOT automatically upload to stores:

| Setting | Purpose | Required For |
|---------|---------|--------------|
| `"distribution": "store"` | Creates store-ready binaries | App Store / Play Store submissions |

**Important:** `distribution: "store"` alone does NOT upload to stores. You must explicitly submit builds using a separate `eas submit` command after the build completes.

**CI/CD Pattern:** Split build and submit into separate jobs:
1. Build job: `eas build --platform ios --profile production --non-interactive`
2. Submit job: `eas submit --platform ios --profile production --latest --non-interactive`

This allows builds to succeed even if submission fails, and enables retrying submissions without rebuilding.

## Version Management

Two separate version concepts:

| Version | Where | Who manages | Purpose |
|---------|-------|-------------|---------|
| `version` | app.json | You, manually | User-facing (e.g. `1.2.0`). Shown on App Store / Play Store. |
| `buildNumber` / `versionCode` | EAS remote | EAS, automatically | Developer-facing. Must be unique per store upload. Auto-incremented. |

This is controlled by two `eas.json` fields:

- **`appVersionSource: "remote"`** -- EAS stores build numbers on its servers, not in local files. Required for CI/CD where builds happen on different machines/branches.
- **`autoIncrement: true`** (on the build profile) -- EAS bumps the build number on every build. You never touch it.

This means you can build 10 times for version `1.2.0` -- each gets a unique build number (1, 2, 3...) and the stores accept all of them. You only bump `version` in app.json when you want a new user-facing release.

For apps already in stores, sync the current store build number to EAS first:
```bash
eas build:version:set
```

## Submit Profiles

Submit profiles in `eas.json` control where a build goes:

| Profile | Android Track | Android Status | iOS | Use Case |
|---------|--------------|----------------|-----|----------|
| `internal` | `internal` | `draft` | n/a | QA testing (up to 100 testers) |
| `production` | `production` | `draft` | Submits to App Store Connect | Public release |

Android track options: `internal`, `alpha`, `beta`, `production`.
Android releaseStatus options: `draft`, `completed`, `inProgress`, `halted`.

**Note:** Use `"draft"` for new apps. Builds upload successfully but require manual publish in Google Play Console. Once your app is published and you want automatic rollouts, you can change to `"completed"`.

iOS submit requires `ascAppId` -- your App Store Connect App ID (numeric, found in the ASC URL for your app). When submitted, builds appear in TestFlight after ~10-15 min of Apple processing.

**Note:** Submit profiles are used with `eas submit --profile NAME`, not with `eas build`. The profile name passed to `eas submit` determines the destination (e.g., `--profile internal` submits to Android internal track).

## Key CLI Flags

### Build Flags
| Flag | What it does |
|------|-------------|
| `--profile NAME` | Specifies which build profile to use from eas.json (e.g., `production`, `preview`) |
| `--platform ios\|android\|all` | Which platform(s) to build |
| `--non-interactive` | Required for CI. Skips all prompts. |
| `--no-wait` | Queues the build on EAS and returns immediately. Doesn't block CI runner. |

### Submit Flags
| Flag | What it does |
|------|-------------|
| `--profile NAME` | Specifies which submit profile to use from eas.json (e.g., `production`, `internal`) |
| `--latest` | Picks the most recent successful build for that platform. Use in CI. |
| `--id BUILD_ID` | Submits a specific build. Use when `--latest` isn't precise enough. |
| `--non-interactive` | Required for CI. Skips all prompts. |

## CI/CD Workflow Pattern

The recommended pattern splits build and submit into separate jobs:

```yaml
build-ios:
  steps:
    - run: eas build --platform ios --profile production --non-interactive

submit-ios:
  needs: build-ios
  steps:
    - run: eas submit --platform ios --profile production --latest --non-interactive
```

**Benefits:**
- Builds can succeed even if submission fails
- Retry submissions without rebuilding
- Clearer separation of concerns
- Better error isolation

**For Android:** Use `--profile internal` for submit to send to internal testing track, or `--profile production` for production track.

**For iOS:** Use `--profile production` for submit to send to TestFlight (appears after ~10-15 min Apple processing).

## Credentials

Only `EXPO_TOKEN` needs to be a GitHub secret. All store credentials (Apple ASC API key, Google Play service account JSON) are managed by EAS and configured once locally via:
```bash
eas credentials
```
EAS stores them encrypted and uses them during cloud builds/submissions.

## Gotchas

**iOS build succeeds but not in TestFlight** -- Build succeeded but submit step didn't run or failed. The IPA is built but not uploaded. Fix: Run `eas submit --platform ios --profile production --latest --non-interactive` to submit the existing build.

**"Build number already exists"** -- Missing `appVersionSource: "remote"` + `autoIncrement: true`, or stale local version. Fix with `eas build:version:set`.

**Android "track not found"** -- The track must exist in Google Play Console first. Create it and upload one build manually before CI submissions work.

**iOS not in TestFlight after upload** -- Apple processing takes 10-15 min. Check App Store Connect status.

**`--latest` picks wrong build** -- It always picks the most recent successful build. Use `--id` for precision, or check with `eas build:list --platform ios`.

**First Android submission ever** -- Google requires the very first AAB to be uploaded manually via Play Console. After that, EAS Submit works.

**Profile name confusion** -- `--profile production` in `eas build` refers to the BUILD PROFILE NAME, not the release destination. It means "production-quality build" (optimized, release config). The `distribution: "store"` creates store-ready binaries. After building, you submit with `eas submit --profile production` which uses the SUBMIT PROFILE. iOS goes to TestFlight first, then you manually promote to App Store when ready.

## Reference

See [eas.json](references/eas.json) for the complete configuration template with submit profiles.
