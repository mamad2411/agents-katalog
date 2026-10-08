---
name: "ios-testflight-release-cycle"
description: "Run a consistent iOS TestFlight release cycle across projects. Use when an iOS app needs a new build number, release notes, archive/export/upload to App Store Connect, TestFlight metadata updates, or tester group assignment. Discovers repo-specific schemes and version files while preferring local App Store Connect credentials with ASC_ISSUER_ID, ASC_KEY_ID, and ASC_PRIVATE_KEY_PATH."
---

# iOS TestFlight Release Cycle

Use this skill to cut a new TestFlight build for any iOS app while preserving the repo's own release conventions.

## Goals

- Release from the merged source of truth, normally `origin/main`.
- Increment build numbers consistently without changing marketing versions unless asked.
- Generate concise, tester-facing TestFlight notes in a standard format.
- Archive, export, upload, poll processing, update TestFlight metadata, and assign the intended tester group.
- Keep App Store Connect credentials local and stable, without runtime password-manager prompts.

## Before Changing Code

Read the repo's local instructions and release surfaces first:

- `AGENTS.md`, `README.md`, and release docs
- `project.yml`, `.xcodeproj`, `.xcworkspace`, `.xcconfig`, and app `Info.plist` files
- release scripts under `Scripts/`, `scripts/`, `fastlane/`, or `tools/`
- existing release notes, changelog, release highlights, or App Store metadata files

Report the discovered release context before editing: app target, scheme, version source, build source, release-note location, archive/export convention, App Store Connect env names, and tester group target.

## App Store Connect Credential Standard

Prefer local machine configuration for release automation:

- `ASC_ISSUER_ID`: literal App Store Connect issuer id
- `ASC_KEY_ID`: literal key id
- `ASC_PRIVATE_KEY_PATH`: path to a local `.p8` API key
- app id env, for example `ASC_<APP_KEY>_APP_ID`
- beta group env, for example `ASC_<APP_KEY>_INTERNAL_GROUP_ID` or `ASC_<APP_KEY>_EXTERNAL_GROUP_ID`

Best default place for the private key:

```text
~/.appstoreconnect/private_keys/AuthKey_<ASC_KEY_ID>.p8
```

Recommended permissions:

```bash
chmod 700 ~/.appstoreconnect ~/.appstoreconnect/private_keys
chmod 600 ~/.appstoreconnect/private_keys/AuthKey_<ASC_KEY_ID>.p8
```

If a repo uses an environment loader such as `.env.apple.local`, source it before every App Store Connect, upload, polling, or metadata command. If credentials are missing, unreadable, or still point to runtime secret resolution such as `op://`, stop and tell the user the best local place to store them before continuing.

## Build Increment Rules

- Start from synced `main` or the repo's release branch.
- Read the current marketing version and build number from the repo's source of truth.
- Increment only the build number unless the user explicitly asks for a marketing version bump.
- Regenerate derived project files when the repo uses XcodeGen or another generator.
- Verify the resulting values with `xcodebuild -showBuildSettings` or an equivalent repo script.
- Keep build-number changes in a release-prep commit or PR before archiving when protected branches or repo policy require it.

## Standard TestFlight Notes

Create or update the repo's release-testing file when one exists. Otherwise create the smallest repo-appropriate release note artifact, usually under `docs/`.

Use this format:

```text
<App Name> build <build-number>

Focus this build on <one-line release focus>.

What to test:
- <high-value flow or changed behavior>
- <high-value flow or changed behavior>
- <regression area testers should verify>

Known notes:
- <important limitation, migration note, or "No known release blockers.">
```

Keep notes tester-facing, concrete, and short. Do not paste commit logs. Mention product names exactly as the app uses them.

## Release Workflow

1. Fetch and sync the release base.
2. Create a release branch if the repo uses PRs or branch protection.
3. Increment the build number and update release notes.
4. Regenerate project files if needed.
5. Run the repo's focused validation, usually unit tests plus `make build` or the equivalent.
6. Commit only release-prep files. Never stage archives, IPAs, derived data, or logs.
7. Push, open PR, and merge if required.
8. Archive from merged `main` unless the user explicitly accepts branch/archive mismatch.
9. Export the IPA using the repo's existing export options or a fresh timestamped export options file.
10. Upload with App Store Connect API key credentials.
11. Poll App Store Connect until the build is visible and valid, or report processing status if Apple is still working.
12. Update TestFlight `What to Test` metadata from the release notes.
13. Assign the build to the configured beta group when the repo expects explicit assignment.
14. Final report includes build number, upload delivery UUID, build id, group assignment, release notes path, validation commands, and unresolved release risks.

## Archive Layout

Use the repo's existing layout when available. Otherwise use a timestamped local archive directory ignored by Git:

```text
.archives/<app-slug>-<marketing-version>-<build-number>-<timestamp>/
  <AppName>.xcarchive
  ExportOptions.plist
  export/<AppName>.ipa
  logs/archive.log
  logs/export.log
  logs/upload.log
```

## Upload Guidance

Use existing repo helpers when they are correct. Otherwise prefer:

```bash
source <repo-or-local-env-loader>
test -n "${ASC_ISSUER_ID:-}"
test -n "${ASC_KEY_ID:-}"
test -n "${ASC_PRIVATE_KEY_PATH:-}"
test -r "$ASC_PRIVATE_KEY_PATH"
xcrun altool --upload-app \
  -f "$IPA" \
  --type ios \
  --apiKey "$ASC_KEY_ID" \
  --apiIssuer "$ASC_ISSUER_ID" \
  --output-format json
```

If `altool` expects the key in its default directory, symlink from `ASC_PRIVATE_KEY_PATH` to `~/.appstoreconnect/private_keys/AuthKey_<ASC_KEY_ID>.p8` rather than resolving secrets at runtime.

## Metadata And Tester Assignment

- Poll `/v1/builds` for the app id and new build number.
- Treat `VALID` as ready for TestFlight metadata updates.
- Stop on `FAILED` or `INVALID` and report Apple processing details.
- Update `betaBuildLocalizations.whatsNew`, usually `en-US`, from the release note artifact.
- Use the configured beta group env var. Do not assume internal or external; follow the repo and user's current instruction.
- If the repo helper refuses a group type, use the lower-level App Store Connect API only when the user's target group is explicit.

## Validation Checklist

Before reporting success, verify:

- release branch or main state matches repo policy
- build number changed in the correct source of truth
- generated project files are current
- release notes exist and match the uploaded build
- archive succeeded
- export succeeded
- upload succeeded and delivery UUID is recorded
- App Store Connect build is visible
- TestFlight notes were updated or exact manual fallback text was provided
- beta group assignment or availability was confirmed
- no archive artifacts are staged

## Do Not Do These

- Do not use runtime `op://` resolution for release-critical credentials when local API key files can be used.
- Do not archive from an unmerged branch and imply it came from `main`.
- Do not stage `.archives`, IPAs, derived data, or local env files.
- Do not change marketing version, bundle id, signing team, or tester group target unless explicitly requested.
- Do not claim metadata or assignment succeeded without an App Store Connect response.
