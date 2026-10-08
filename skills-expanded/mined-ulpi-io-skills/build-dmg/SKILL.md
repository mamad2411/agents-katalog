---
name: build-dmg
version: 2.0.0
description: |
  Build a distributable macOS DMG from an Xcode project via the bundled local helper — archive → export →
  package into one signed artifact. Resolves the project/workspace, scheme, team ID, and export options,
  regenerates the project first when `xcodegen` is detected, then runs `helpers/build-dmg.sh` from the
  project root instead of inlining xcodebuild. User-only workflow that touches code signing and
  provisioning: it never GUESSES the signing identity, never overwrites `ExportOptions.plist` without
  approval, and reports the built DMG path, version, and signing status. Use only when the user explicitly
  asks to build or package a DMG.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Write
disable-model-invocation: true
user-invocable: true
argument-hint: "[project, workspace, or scheme hint]"
arguments:
  - request
when_to_use: |
  Use when the user explicitly asks to build a DMG, package a macOS app for distribution, or create a
  signed installer — "build a DMG", "package this Mac app", "create a distributable installer". Do NOT use
  proactively or to run ad-hoc xcodebuild commands; it drives code signing and export, so it is user-only
  and asks before guessing any signing or export input.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill runs `xcodebuild archive` + `exportArchive` and packages the result into a DMG. It touches code signing, provisioning, and export options.

Non-negotiable rules:
1. Detect project/workspace, scheme, and team ID before building — never guess signing identity.
2. If multiple schemes exist, ask the user which one to build.
3. Do not auto-create or overwrite `ExportOptions.plist` without explicit approval — wrong export options produce unsigned or wrong-distribution builds.
4. Use the helper script (`helpers/build-dmg.sh`) from the project root. Do not inline xcodebuild commands.
5. If `xcodegen` is detected (`project.yml` present), run `xcodegen generate` before building.
6. Report the built DMG path, app version, and signing status clearly.
</EXTREMELY-IMPORTANT>

# build-dmg

## Inputs

- `$request`: Optional project, workspace, scheme, or signing hint

## Goal

Produce a DMG build by:

- resolving the right Xcode target inputs
- running the bundled helper script from the project root
- reporting the resulting DMG path and any packaging blockers

## Step 0: Detect the packaging inputs

Read the repo and resolve:

- app name
- scheme
- project or workspace path
- `ExportOptions.plist` location if it exists
- `VERSION` file if present
- whether `project.yml` indicates `xcodegen`
- team ID or signing hints if already present

If a required input is ambiguous, ask before building.

**Success criteria**: The build configuration is explicit before the helper runs.

## Step 1: Confirm helper and working directory

The helper script lives next to this skill at:

- `helpers/build-dmg.sh`

Run it from the project root so it can use the current repository as the build context.

**Success criteria**: The correct helper path and project root are established.

## Step 2: Build with explicit environment

Provide the required environment variables such as:

- `APP_NAME`
- `SCHEME`

Add optional variables only when the project actually needs them:

- `PROJECT`
- `WORKSPACE`
- `INFO_PLIST`
- `EXPORT_OPTIONS`
- `TEAM_ID`
- `VERSION_FILE`
- `USE_XCODEGEN`
- `DMG_BACKGROUND`

**Success criteria**: The helper has all required inputs and only the needed optional ones.

## Step 3: Handle success or failure cleanly

On success, report:

- DMG output path
- app version and build number if available
- whether the `VERSION` file was changed

On failure:

- summarize the real error
- surface the relevant `xcodebuild` or export failure lines
- identify whether the blocker is signing, scheme selection, export options, or build failure

**Success criteria**: The user gets either a usable artifact path or a clear blocker summary.

## Guardrails

- Do not run this skill proactively.
- Do not assume `.claude`-local helper paths; use the helper inside this skill directory.
- Do not auto-create or overwrite export options without approval.
- Do not hide signing failures behind generic "build failed" summaries.

## Output Contract

Report:

1. resolved app/project/workspace/scheme inputs
2. whether the helper ran successfully
3. DMG path on success
4. version/build info if available
5. exact blocker category on failure
