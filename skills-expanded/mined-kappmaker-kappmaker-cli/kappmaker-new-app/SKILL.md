---
name: kappmaker-new-app
description: Scaffold a new mobile app with the KAppMaker CLI — clone the template, run the full create flow, and set up git remotes. Use when the user wants to build a new app, start a new project, has an app idea, or asks to clone or create a KAppMaker app.
---

# KAppMaker — New App

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.

## Starting from a raw idea

The `new-app` interview skill ships **inside** a project, so it does not exist until one is cloned.
Order: `kappmaker clone <AppName>` → `cd` in and read its `CLAUDE.md` + `.claude/skills/README.md`
→ then follow that project's bundled **`new-app`** skill for the PRD interview.


### create — Full App Setup

**Syntax**: `kappmaker create <AppName> [--template-repo <url>] [--organization <org>]`

**Prerequisites**:
- External CLIs: `git`, `firebase`, `pod`, `bundle` (the CLI auto-installs missing ones with user consent)
- Config: `templateRepo` (has default), `bundleIdPrefix` (optional), `androidSdkPath` (has default)

**App name rules**: Must be PascalCase, start with uppercase, alphanumeric only (e.g., `Remimi`, `FitTracker`).

**What it does** (13 steps):
1. Clone template repository
2. Firebase login (interactive)
3. Create Firebase project
4. Create Firebase apps (Android + iOS)
5. Enable anonymous authentication (if brand-new project, prompts user to click "Get started" in Firebase Console, then retries via API)
6. Download Firebase SDK configs (verifies google-services.json package match)
7. Logo generation (optional — asks user)
8. Package refactor (renames packages, IDs, app name across all modules)
9. Build environment + keystore (local.properties, signing keystore; iOS deps via SwiftPM)
10. Git remotes (template as upstream)
   -> Pre-store reminder: prompts user to create Google Play Console app; ASC is created automatically
11. App Store Connect setup (optional — full asc CLI flow, app created automatically)
12. Google Play Console setup (optional — Fastlane builds + uploads AAB to internal track, then full gpc setup)
13. Adapty setup (optional — links to products created in steps 11-12)

**Interactive prompts**: This command has multiple y/n prompts during execution. The user will need to respond in the terminal. Before running, ask the user:
- What app name they want (validate PascalCase)
- Whether they want a custom template repo
- Whether they plan to use the optional steps (logo, ASC, Google Play Console, Adapty) so they know what to expect. The build + refactor happens BEFORE store setup (steps 8-11), then the CLI pauses and reminds the user to create their app in App Store Connect and/or Google Play Console before continuing. Google Play Console setup (step 12) auto-uploads the AAB to the internal track first.

Run the command and let the user interact with it directly.

**Setup progress file (`PROGRESS_SETUP.md`)**: right after cloning, `create` writes a committed checklist of all 13 steps to the project root and ticks each step off as it completes (optional steps the user declines are checked with a "(skipped — run later)" note). **If a setup was interrupted** (crash, Ctrl-C, network) — read `<project>/PROGRESS_SETUP.md`, find the first unchecked item, and resume with the standalone command listed next to it (`kappmaker firebase configs …`, `kappmaker gpc setup`, etc.) instead of re-running the full `create`. Every step is independently re-runnable and idempotent.

**After `create` finishes**: `cd` into the new project and continue with the template-bundled skills (see "Template-Bundled Agent Skills" above) — `new-app` first if the product isn't defined yet, then the `getting-started` guide to build the MVP.

---

### clone — Clone Template Only (step 1 of `create`)

**Syntax**: `kappmaker clone <AppName> [--template-repo <url>] [--target-dir <path>]`

**Prerequisites**: `git`, plus a `templateRepo` value in config (default: KAppMaker boilerplate).

**App name rules**: PascalCase, starts uppercase, alphanumeric only — same rules as `create`.

**What it does**:
1. Triggers `config init` if `~/.config/kappmaker/config.json` doesn't exist yet
2. Prompts to delete + start fresh if the target directory already exists
3. Runs `git clone <templateRepo> <targetDir>`

**When to suggest this over `create`**: If the user explicitly says they only want to clone, scaffold, or "set up the project without Firebase / store stuff," reach for `clone` instead of the full `create`. Common minimal flow:

```bash
kappmaker clone MyApp
cd MyApp-All/MobileApp
kappmaker refactor --app-id com.example.myapp --app-name MyApp
```

`clone` is also what the full `create` calls under the hood for step 1 — same overwrite prompt and config-init-on-first-run behavior.

---

### git setup-upstream — Rename origin to upstream (step 10 of `create`)

**Syntax**: `kappmaker git setup-upstream [path]`

**Prerequisites**: The target directory must be a git repository.

**What it does**: Runs `git remote rename origin upstream` so the template repo is preserved as the upstream remote, leaving the user free to add their own `origin` later. Exits non-zero if the path isn't a git repo.

**When to suggest this**: After the user has manually cloned the template (or used `kappmaker clone`) and is about to push to their own repo. The full `create` calls this automatically as step 10.

**Pulling template updates later**: the `upstream` remote this preserves is also how an app takes
newer boilerplate improvements — `git fetch upstream` then merge or cherry-pick, reviewing rather
than blind-merging (the project has been rebranded, so paths and package names differ). There is
no dedicated command for this; it is a normal git operation against `upstream`.

---

## Where this sits in the flow

- **Before this:** —
- **After this:** **kappmaker-firebase** (if the app needs auth/analytics), **kappmaker-monetization** (if it sells anything), **kappmaker-logo**. The product interview itself is the project's own bundled `new-app` skill.
