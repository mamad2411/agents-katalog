---
name: kappmaker-refactor
description: Rename a KAppMaker app's package name, bundle ID or display name across the codebase. Use when the user asks to rename the app or change the package name or bundle identifier.
---

# KAppMaker — Refactor

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### refactor — Package & App Name Refactoring

**Syntax**: `kappmaker refactor --app-id <id> --app-name <name> [options]`

**Options**:
- `--app-id <id>` (required) — New applicationId / bundleId (e.g., `com.example.myapp`)
- `--app-name <name>` (required) — New display name (e.g., `MyApp`)
- `--old-app-id <id>` — Current applicationId to replace (default: `com.measify.kappmaker`)
- `--old-app-name <name>` — Current app name to replace (default: `KAppMakerAllModules`)
- `--skip-package-rename` — Only update IDs and app name, keep Kotlin package directories intact

**Prerequisites**: None. Run from the project root (containing `MobileApp/`) or inside `MobileApp/`.

**What it does**:
- **Full refactor** (default): Renames Kotlin packages in all source sets, moves directories, updates Gradle files, Firebase configs, iOS project files, GitHub workflows, and app display name.
- **Skip-package-rename mode**: Only updates applicationId/bundleId, Firebase configs, iOS files, workflows, and app name — keeps Kotlin package dirs intact. Useful for creating multiple apps from one codebase.

**Re-refactoring**: To refactor a project that was already refactored, pass `--old-app-id` and `--old-app-name` with the current values:
```
kappmaker refactor --app-id com.new.app --app-name NewApp --old-app-id com.previous.app --old-app-name PreviousApp
```

---

## Where this sits in the flow

- **Before this:** Do this EARLY, before any store record exists — the package name and bundle ID are what **kappmaker-asc** and **kappmaker-gpc** register.
- **After this:** Rebuild and re-run **kappmaker-publish**.
