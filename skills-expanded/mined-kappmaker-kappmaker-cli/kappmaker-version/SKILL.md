---
name: kappmaker-version
description: Bump the version of a KAppMaker app. Use when the user asks to bump, raise or set the version or build number.
---

# KAppMaker — Version

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### update-version — Version Bumping

**Syntax**: `kappmaker update-version [-v <version>]`

**Options**:
- `-v, --version <name>` — Set explicit version name (e.g., `2.0.0`). If omitted, auto-increments patch (e.g., `1.2.3` → `1.2.4`).

**Prerequisites**: None. Run from the project root (containing `MobileApp/`) or inside `MobileApp/`.

**What it updates**:
- Android: `versionCode` (+1) and `versionName` in `androidApp/build.gradle.kts`
- iOS: `CURRENT_PROJECT_VERSION` (+1) and `MARKETING_VERSION` in `project.pbxproj` + `Info.plist`

If a platform's files are missing, that platform is skipped with a warning.

---

## Where this sits in the flow

- **Before this:** a finished change worth releasing. Every release after the first starts here —
  the stores reject an upload whose versionCode/build number they have already seen.
- **After this:** **kappmaker-publish** — bump, then ship.
