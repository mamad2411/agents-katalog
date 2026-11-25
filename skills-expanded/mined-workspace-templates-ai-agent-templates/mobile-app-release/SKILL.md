---
name: mobile-app-release
description: "Prepares an iOS or Android store release: version and build bump, signing check, changelog, screenshots list and review notes, without uploading anything."
---

# Mobile app release

Prepare, verify and report. Never upload, submit or change store settings.

## Steps

1. Detect the project: Xcode project or workspace, Gradle app module, Flutter, React Native or Expo. Find the last release tag with `git describe --tags --abbrev=0` and list commits since it.
2. Versions. Show the current marketing version and build number (`CFBundleShortVersionString` and `CFBundleVersion`, or `versionName` and `versionCode`). Propose the next values: build numbers only go up and must never repeat. Apply them only after the user agrees.
3. Configuration audit. Confirm release builds have debugging off, no staging API URLs, no test keys, analytics set to production, and minification enabled on Android. Search shipped code for unfinished-work markers, `localhost` and `10.0.2.2`.
4. Signing. Verify that the signing config exists and names a keystore or profile by reference. Check the provisioning profile and certificate expiry dates where visible. Never print or copy secrets.
5. Permissions and privacy. List every requested permission, check each has a usage description on iOS or a stated reason on Android, and flag any that no code uses.
6. Build a release artifact locally (`xcodebuild archive`, `./gradlew bundleRelease` or the framework equivalent) and report success or the first error.
7. Draft materials: release notes from the commit list, in user language and under 500 characters, plus a list of screenshots that need refreshing because their screens changed.
8. Reviewer notes: demo account steps, anything that needs hardware or a region, and the reason for sensitive permissions.

## Report

A checklist with pass, fail or unknown for each step, then the draft notes. Mark anything you could not verify.
