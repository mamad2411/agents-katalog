---
name: expo-eas-release-ota
description: "Release Expo apps with EAS builds, submission, OTA channels, staged rollout, and rollback."
---

# Expo EAS Release OTA

Plan and review Expo releases as two linked paths: native store or internal binaries through EAS Build/Submit, and JavaScript/assets updates through EAS Update with runtime compatibility.

## Process

1. Inspect Expo SDK/RN pins, package manager, Node version, `app.config.*`, `eas.json`, EAS CLI version policy, `expo-updates`, runtime version, channels, credentials, app variants, CI, store metadata, source maps, monitoring, and release evidence.
2. For an existing repo, detect repo-pinned Expo SDK, React Native, EAS CLI, Node, package manager, `expo-updates`, and platform target versions before judging commands or config. For a new app, use latest stable. For EAS Build, Submit, Update, runtime, rollout, rollback, credentials, or store behavior, check current official docs through `itsol-current-tech-context`.
3. Classify the change: development/preview build, release-candidate store build, production store release, OTA update, republish, rollback, credentials rotation, or CI/CD change.
4. Gate release with compatibility checks, lint/typecheck/tests, `expo-doctor`, generated-code checks, prebuild/config-plugin validation when relevant, build/submit checks, release-like E2E, monitoring, and rollback readiness.
5. Plan rollback before release: previous binaries, compatible runtime, update republish, channel freeze, feature flag or kill switch, local migration safety, support notes, and owner.

## Output

For plans, produce build/update classification, profile/channel/runtime decisions, required credentials, artifact and submit path, CI gates, QA matrix, rollout, rollback, monitoring, and residual risks. For reviews, lead with blockers that could ship the wrong binary, wrong channel, incompatible OTA, leaked credentials, unreviewed store release, or unrollbackable migration.

## Focused References

- [01-build-profiles-credentials.md](./references/01-build-profiles-credentials.md) - EAS Build profiles, app variants, environments, credentials, signing, local/cloud builds, and artifact evidence.
- [02-versioning-distribution-submit.md](./references/02-versioning-distribution-submit.md) - app versions, build numbers, version source, internal/store distribution, EAS Submit, store tracks, and release metadata.
- [03-ota-runtime-channels.md](./references/03-ota-runtime-channels.md) - OTA eligibility, runtime versions, channels/branches, update staging, code signing, and update UX.
- [04-rollout-rollback-ci.md](./references/04-rollout-rollback-ci.md) - rollout, rollback, CI/CD gates, EAS Workflows or external CI, monitoring, post-release checks, and incident recovery.
