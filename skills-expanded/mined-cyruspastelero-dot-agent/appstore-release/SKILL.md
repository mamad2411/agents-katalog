---
name: appstore-release
description: Use when cutting an App Store release, uploading a build to App Store Connect / TestFlight, bumping an iOS app version, or when fastlane release/deliver/gym fails with signing errors like "Cloud signing permission error". Covers XcodeGen and plain Xcode projects.
disable-model-invocation: true
---

# App Store Release

## Overview

Build → upload → submit an iOS app for App Store review with fastlane, without
tripping the known signing, versioning, and process traps. Proven on real
several releases. One lane run takes ~10 min end to end.

## When to Use

- "Release the app", "prepare a build for the App Store", "submit for review"
- Version/build bump questions for iOS apps
- Fastlane export failing with **"Cloud signing permission error"**
- NOT for: Android, TestFlight-only beta distribution (adapt the lane), or
  App Store metadata/screenshot-only updates (use `deliver` directly).

## Preflight (do ALL of these before touching anything)

1. **Read the app's own runbook first** — look for `AGENTS.md` / `CLAUDE.md` in
   the repo. Per-app facts (bundle id, Apple ID, team, lane names) live there.
   Never assume facts from a sibling app — these apps share a machine
   (each app differs).
2. **Check what's live** (needs `fastlane/api_key.json`):
   ```bash
   fastlane run app_store_build_number app_identifier:<bundle.id> live:true api_key_path:fastlane/api_key.json
   ```
   New version string must be **greater than live**; build number **greater
   than the latest uploaded build** for any train.
3. **Schema-migration check (SwiftData/CoreData apps)**: diff the model files
   since the last release commit. If any `@Model`/entity changed, STOP and test
   the upgrade against a previous version's store (device or dedicated sim App
   Group path) before releasing — a green suite does NOT catch launch crashes
   on upgrade (this shipped a crash once).
4. **Suites green** — run the app's test suites; never release on a red or
   unknown baseline.
4b. **The app tells users about updates (user rule, 2026-09-27).** Every
   shipped app carries the same `AppUpdateChecker.swift` as its siblings
   (e.g. `<App>/Services/AppUpdateChecker.swift`): daily iTunes Lookup, 24h
   release grace, minimum-OS gate, skip-this-version, `--uitest-force-update`
   hook, wired on the root view with `.checkForAppUpdate()`. Before releasing:
   - `grep -rl "itunes.apple.com/lookup" <App>/` — if it finds nothing, port
     the file **before** cutting the build (one app's 1.0 shipped without it, so
     no 1.0 user is ever told about 1.0.1; build 5 had to be recut as 6).
   - Change only the App Store ID and the sheet's styling; the rules, the
     provider and the tests are copied verbatim (`AppUpdateCheckerTests.swift`,
     `AppUpdatePromptUITests.swift`). `diff` against a sibling app's file to prove the
     logic is identical.
   - A logic change in one app goes to all three in the same sitting.
4c. **Every sign-in provider, first run, against production (App Review 2.1(a),
   a real 2.1(a) rejection).** Apple tests Apple/Google sign-in with a
   **brand-new account** on iPhone *and* iPad. Before submitting any build that
   offers a provider:
   - Sign in on a real device with a fresh Apple ID and a fresh Google account —
     not the demo account, not one that already has a profile. Rejected shape:
     OAuth succeeded server-side, the app then showed "User profile not found"
     because nothing created the profile row for a first-time social user.
   - Headless proxy when a device tap is impossible: create an auth user through
     the raw `/auth/v1/signup` API (auth row, no profile — the reviewer's exact
     state), confirm zero profile rows, run the live smoke test with it, confirm
     the row afterwards, delete the account.
   - **Ported code ≠ ported backend.** One app's project creates profiles with an
     `on_auth_user_created` trigger; its sibling's has none. Before trusting sibling
     behavior, diff `pg_trigger` on `auth.users` and the profile table's columns
     (the sibling had no `subscription_tier`; a lenient decoder made every user
     free-tier). Same code, different project, different outcome.
   - Read the entitlements out of the **signed binary** (`scripts/check-entitlements.sh`
     in sibling iOS apps) — one build shipped without
     `applesignin` while the suite stayed green.
4d. **Demo account = durable full access, checked the same day.** Trials lapse:
   One app's demo trial ended 2026-09-07, the reviewer signed in 2026-09-09 and
   met usage caps the review notes said didn't exist. Give the demo account a
   permanent grant (app A: `subscription_tier = 'pro'`; app B: a
   `comp/active` row in `sc_subscriptions`), sign in with it through the auth API
   right before submitting, and make sure the review notes describe *this* build.
5. **Ask the user two things** (genuinely theirs to decide):
   - The version number (show them live version + build as context).
   - How far to go: full release (submit for review, usually with automatic
     release on approval) vs upload-only vs build-only. Submission is
     effectively irreversible once approved — never assume.

## Updating a live app: open the next version first

If the current version is `READY_FOR_SALE`, nothing is editable — What's New,
review notes and the build attachment all need a **new App Store version**.
`deliver` creates one implicitly, but on apps where `deliver` cannot run
against the record (e.g. it raises `No data` on localizations) do it through
the API before pushing any metadata:

```bash
python3 scripts/asc.py version 1.0.1   # POST /v1/appStoreVersions
python3 scripts/asc.py push            # then metadata + What's New land on 1.0.1
python3 scripts/asc.py notes           # reviewer notes on 1.0.1
python3 scripts/asc.py submit 5        # attach the processed build and submit
```

Scripts that pick "the" version must prefer the one whose state is not
`READY_FOR_SALE` / `REPLACED_WITH_NEW_VERSION`, otherwise they edit the live
one and Apple 409s. Reviewer notes are per version: rewrite the paragraph that
describes what this build changes, and put it through `humanizer` too.

## Version Bump

**XcodeGen apps** (`project.yml` present): the ONLY source of truth is
```yaml
settings:
  base:
    MARKETING_VERSION: "1.5"        # > live version
    CURRENT_PROJECT_VERSION: "9"    # > latest uploaded build
```
then `xcodegen generate`. Never hand-edit `.xcodeproj`. With
`GENERATE_INFOPLIST_FILE=YES` the version comes from these build settings, NOT
from any Info.plist — editing plists does nothing.

**Plain Xcode apps**: `agvtool new-marketing-version X.Y && agvtool new-version -all N`,
or edit the build settings — find where the existing version is defined first.

## Release Notes & Metadata

- "What's New" = `fastlane/metadata/en-US/release_notes.txt`. Write it for
  users, honestly — internal-only releases still need a user-relevant lead
  (e.g. the one behavior improvement), not "misc fixes".
- **De-slop the copy before uploading — MANDATORY (user rule, 2026-08-31,
  reaffirmed 2026-09-26)**: ALWAYS run the drafted release notes and any
  changed description through the `humanizer` skill before writing them to
  `fastlane/metadata/` — this is a required step, not an optional polish; do
  not upload store copy that hasn't been through it. Only if `humanizer` is
  genuinely not installed, strip the AI tells by hand: "We're excited to
  announce", "seamless/robust/elevate/enhance", "delve", stacked em-dashes,
  rule-of-three padding, exclamation-mark enthusiasm. Release notes should
  read like the developer wrote them.
- **The pass covers every string the release touches, as one set** — not just
  `release_notes.txt`. That means: What's New, description, subtitle,
  promotional text, keywords, **the App Review notes** (reviewer-facing text
  is still text a person reads; one app's 1.0.1 shipped its reviewer paragraph
  without the pass and had to redo it), and any **in-app strings added in the
  release** (alerts, empty states, button labels). Do it the way the skill
  says: collect 3–5 lines of the app's existing copy as the voice to match,
  then rewrite. Running it on one string in isolation flattens the voice.
- Record in the final message which strings went through the pass, so the
  user can see it happened rather than take it on trust.
- Screenshots: release lanes typically set `skip_screenshots: true` — the live
  listing's screenshots carry over. Changed screenshots need a separate upload
  in App Store Connect; say so instead of silently skipping.

## Run the Lane

```bash
fastlane ios release version:1.5 build:9
```
(Lane name/options per the app's Fastfile — read it.) Run it **in the
background without piping through `tail`/`grep`** — pipes buffer, so the
output file stays empty until the end and you can't monitor progress. Give it
15+ min: `upload_to_testflight` with `skip_waiting_for_build_processing: false`
waits for Apple processing, which alone can exceed 10 min.

**Success looks like** (grep the output for these, in order):
`Successfully exported and signed the ipa` → `Successfully uploaded the new
binary` → `Successfully finished processing the build X - N` →
`Successfully set the version` → `Successfully submitted the app for review!`
Missing any of these = not done; find out which step stopped.

## Signing — the gotcha that WILL bite

- Export must regenerate distribution profiles: `-allowProvisioningUpdates`
  goes on **`export_xcargs` only** (uses the Apple ID logged into Xcode).
- The ASC API key usually has the **App Manager** role, which **cannot cloud
  sign** — passing it to the export step (`-authenticationKey*`) fails with
  *"Cloud signing permission error"*. The key is only for upload/submit steps.
- Don't put provisioning args on gym's `xcargs` — gym applies `xcargs` to the
  export too and duplicates the flag. `build_app` has no `api_key` option;
  don't add one.

## Commit

Stage **selectively** — the version bump, regenerated project, and release
notes only. Never `git add -A` (working trees carry unrelated churn):
```bash
git add project.yml <App>.xcodeproj/project.pbxproj fastlane/metadata/en-US/release_notes.txt
git commit -m "chore(release): bump to 1.5 (9) and submit for review"
```
If the repo has commit gates (e.g. a verification-matrix hook), satisfy them
honestly (update the release row) rather than bypassing.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Bumping Info.plist versions | With generated Info.plists the build settings win; bump `project.yml` / build settings |
| Passing the API key to gym/export | App Manager role can't cloud-sign; key is for upload/submit only |
| Piping the lane through `tail` to "watch" it | Buffers everything; run bare in background, read the output file |
| 10-min timeout on the lane | Apple processing alone can blow past it; allow 15+ min |
| Releasing with a changed data model, suite green | Green tests don't open old stores; test the upgrade path first |
| `git add -A` for the release commit | Sweeps in unrelated working-tree churn; stage the release files only |
| Reusing facts from another app's release | Bundle id / Apple ID / lane options are per-app; read that repo's runbook |
| Diagnosing a rejection without the reviewer's text | Apple's API never exposes Resolution Center; ask the user to paste the message (and screenshot) FIRST. A parity-diff guess found a real bug but not the one Apple cited |
| Resubmitting after a rejection with a new `reviewSubmissions` | 409 — the version is still attached to the original submission. Attach the new build, then `PATCH submitted: true` on the ORIGINAL submission. A probing POST leaves an empty draft only the web UI can delete |
| Trusting a green suite for social sign-in | Units substitute placeholder Supabase creds and `ASAuthorization` can't be constructed; only a device tap or the orphan-account live smoke proves the first-run path |
