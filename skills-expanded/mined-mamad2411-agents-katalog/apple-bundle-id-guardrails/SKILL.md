---
name: apple-bundle-id-guardrails
description: "Use when creating a new Xcode or mobile app project, choosing or entering an Apple bundle ID / App ID, configuring a signing team (especially a free personal team), setting up a macOS app that requests TCC permissions (Accessibility, Input Monitoring, Screen Recording), auditing a repo for identifier leaks, or hitting 'An App ID with Identifier is not available' / 'Failed to register bundle identifier' errors."
---

# Apple Bundle ID Guardrails

Use this skill whenever an Apple bundle identifier meets a signing configuration: new Xcode or mobile project setup, entering a bundle ID or signing team, repo audits for identifier leaks, and App ID registration errors. This skill owns registration safety; character-level identifier syntax is owned by the `flutter-flavors` skill's identifier rules.

## Why This Exists

App IDs (explicit bundle IDs) are globally unique across the entire Apple Developer Program, across all teams. Merely running an iOS app on a device lets Xcode automatic signing register the App ID to the currently selected team — including a free personal team, which cannot access the portal Identifiers list, so a wrongly registered ID is hard to reclaim. macOS builds usually skip registration unless a restricted entitlement requires a provisioning profile (TN3125), but apply the same rules to macOS conservatively.

macOS carries a second, independent hazard that does not depend on registration at all. TCC permission grants (Accessibility, Input Monitoring, Screen Recording) are keyed to bundle ID plus code signature, and `UserDefaults` domains are keyed to bundle ID alone. One ID shared between a development build and an installed release means one grant and one preferences domain between them, each overwriting the other — and since macOS never revokes a grant when an app is deleted, a build silently inherits whatever that ID was granted before. Suffixed personal and `.dev` IDs isolate both. Details and the `tccutil` workflow: `references/xcconfig-guardrail.md`.

## Rules

1. Never enter the canonical ID (`com.<org>.<product>`) into any signing configuration until the organization team exists and has registered it. This is the only fatal mistake.
2. Personal development uses `<canonical>.<github-handle>`; development builds append `.dev` (example shape: `com.acme.myapp.alice.dev`). App ID uniqueness is exact-string, so registering a suffixed ID never blocks the canonical one — a mistake's blast radius is one personal suffix.
3. The first action after the organization team opens is to register every canonical App ID to it. From that moment these guardrails become unnecessary.
4. Repos — public ones especially — carry the canonical ID in no build or signing configuration: an outside contributor's automatic signing could try to register it. Prose documentation is exempt — uninstall and support instructions need the shipping ID to work, and Xcode reads no markdown. Rule 5 is the mechanism.
5. Check in only a sacrificial ID with no organization namespace (convention: `forked.<product>.local`) and no `DEVELOPMENT_TEAM`; personal bundle IDs and the signing team live in a git-ignored xcconfig override. Setup procedure: `references/xcconfig-guardrail.md`.

Resolve real org, product, and github-handle values from the user or project docs before writing anything; never apply the example IDs above literally.

## Workflow

1. Identify the branch: new-project or retrofit setup, audit, personal-ID choice, org-team handover, or registration-error recovery.
2. Setup (new project or retrofit): follow `references/xcconfig-guardrail.md`. Done when a clean clone builds with the sacrificial ID and the org namespace appears nowhere in tracked files.
3. Audit: search every tracked file — `project.pbxproj`, `*.xcconfig`, `*.plist`, `*.entitlements`, export options, CI configs — for the org namespace and for `DEVELOPMENT_TEAM` literals. Done when every hit is reported with its file and line (org namespace as a registration hazard, `DEVELOPMENT_TEAM` as a hygiene leak), and the override file is confirmed git-ignored.
4. Org-team handover checklist:
   - Enumerate every canonical explicit bundle ID: each app, plus each extension and widget, is its own App ID.
   - Register each in the org team's portal (Certificates, Identifiers & Profiles → Identifiers).
   - Only then move canonical IDs into signing configs and release lanes; personal suffixed IDs stay for local development.
5. Recovery from "An App ID with Identifier … is not available" / "Failed to register bundle identifier": the ID is already registered to some team. If a team you control owns it, delete it from that team's Identifiers list to release it. A free personal team cannot see Identifiers — treat that ID as burned and switch to a suffixed personal ID.

## Output

Report which branch ran, the exact IDs written or audited (sacrificial, personal, canonical), every file changed or flagged, and any decision still needing a human — signing team selection and portal registration always do.
