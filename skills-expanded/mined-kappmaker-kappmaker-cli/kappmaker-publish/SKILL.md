---
name: kappmaker-publish
description: Build, sign and ship a KAppMaker app — Fastlane setup, signed Android AAB, keystore generation, and uploading to Google Play and the App Store. Use when the user asks to build a release, create a keystore, configure fastlane, ship, upload or publish the app. Building iOS without a Mac is kappmaker-ios-ci.
---

# KAppMaker — Publish

## Shipping order — read this first

Publishing is a chain, and the first release differs from later ones.

**Android, first ever release**
1. **Keystore** — `generate-keystore` (below). One per app, forever. Losing it means you can never
   update that app again, so back it up before continuing.
2. The Play app record must exist → **kappmaker-gpc**.
3. `android-release-build` (below) — signed AAB.
4. `publish` (below) — upload.

**Android, every release after that**
Skip the keystore, it already exists. Bump the version first (**kappmaker-version**), then
`android-release-build` → `publish`.

**iOS**
The App Store Connect record must exist first → **kappmaker-asc**. Signing is handled by Fastlane
(`fastlane configure` below), not by a keystore.

**No Mac?** Xcode is the only genuinely Mac-locked step, and it can run on a GitHub macOS runner
instead: `kappmaker publish --platform ios --remote`, or `kappmaker ios-ci build` directly. One-time
setup is `kappmaker ios-ci init` — see **kappmaker-ios-ci**. On a non-Mac, plain
`publish --platform ios` now fails with a pointer there rather than an opaque Xcode error.

If a step fails because something upstream is missing, go to that skill and come back — do not
improvise around it.

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### fastlane configure — Set Up Fastlane

**Syntax**: `kappmaker fastlane configure`

**Prerequisites**: Ruby and Bundler (`gem install bundler`). Run from the project root or inside `MobileApp/`.

**What it does**: Creates `Gemfile` + `fastlane/Fastfile` in the mobile app directory, then runs `bundle install`. Skips files that already exist. This is a prerequisite for `kappmaker publish`.

---

### publish — Build & Upload to Stores

**Syntax**: `kappmaker publish [options]`

**Options**:
- `--platform <name>` — Platform to publish: `android`, `ios` (repeatable, default: both)
- `--track <name>` — Android Play Store track: internal/alpha/beta/production (default: `production`)
- `--upload-metadata` — Upload metadata texts (default: false)
- `--upload-screenshots` — Upload screenshots (default: false)
- `--upload-images` — Upload images — icon, feature graphic, Android only (default: false)
- `--submit-for-review <bool>` — Submit for review after upload (default: `true`; pass
  `--submit-for-review false` to upload without submitting — the flag REQUIRES a value, a bare
  `--submit-for-review` is a Commander error)

**Prerequisites**:
- Fastlane via Bundler (`Gemfile` + `fastlane/Fastfile` in mobileDir)
- **Android**: `googleServiceAccountPath` set in config (Google Play service account JSON)
- **iOS**: `ascKeyId`, `ascIssuerId`, `ascPrivateKeyPath` set in config (CLI generates Fastlane publisher JSON automatically)

Run from the project root or inside `MobileApp/`.

**What it does**: Builds and uploads via Fastlane's `playstore_release` (Android) and `appstore_release` (iOS) lanes. With no `--platform`, publishes to both stores sequentially.

---

### generate-keystore — Android Signing Keystore

**Syntax**: `kappmaker generate-keystore [options]`

**Options**:
- `--first-name <name>` — Developer name for keystore (required if no `--organization`)
- `--organization <name>` — Organization name for keystore (required if no `--first-name`)
- `--output <dir>` — Output directory (default: `distribution/android/keystore` inside mobileDir)

**Prerequisites**: `keytool` (comes with JDK). Run from the project root or inside `MobileApp/`.

**What it does**: Generates `keystore.jks` and `keystore.properties` with a secure random password. At least one of `--first-name` or `--organization` must be provided.

---

### android-release-build — Signed Android AAB

**Syntax**: `kappmaker android-release-build [options]`

**Options**:
- `--organization <name>` — Organization for keystore if it needs generating (default: from config)
- `--first-name <name>` — Developer name for keystore if it needs generating
- `--output <dir>` — Output directory for AAB (default: `distribution/android` inside mobileDir)

**Prerequisites**: `gradlew` in the mobile app directory, JDK. Run from the project root or inside `MobileApp/`.

**What it does**:
1. Generates keystore if `distribution/android/keystore/keystore.properties` doesn't exist
2. Builds AAB via `./gradlew :androidApp:bundleRelease`
3. Copies AAB to output directory
4. Logs path to the built AAB

---

## Where this sits in the flow

- **Before this:** **kappmaker-version** (stores reject an already-seen build number), and the
  store records — **kappmaker-asc** / **kappmaker-gpc**.
- **After this:** the release is in review. Iterate with **kappmaker-aso** / **kappmaker-screenshots**
  while you wait.
