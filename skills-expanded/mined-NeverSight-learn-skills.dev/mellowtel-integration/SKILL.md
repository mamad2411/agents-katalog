---
name: mellowtel-integration
description: Integrates Mellowtel consensual bandwidth monetization into browser extensions
  (Plasmo, WXT, vanilla), Electron apps, and Windows .NET apps. Use when the user
  wants to add Mellowtel or provides a Mellowtel API key for integration.
compatibility: Requires file read/write access to the project directory.
license: MIT
---

# Mellowtel Integration Skill

When invoked as `/mellowtel-integration <API_KEY>`, execute the following steps in order.

## Step 1: Resolve API Key

The API key is the argument passed after the command name (e.g. `/mellowtel-integration abc123` → key is `abc123`).

If no key was provided, ask the user: "Please provide your Mellowtel API key before we proceed."

Do not continue until a key is available. Store it — you will substitute it for every placeholder (`TEST_CONFIG_KEY`, `YOUR_API_KEY`, `YOUR_INTEGRATION_ID`, `PLASMO_PUBLIC_MELLOWTEL`) found in the guide.

## Step 2: Detect Project Type

Inspect the files in the current working directory to determine which guide to use. Apply the checks in this exact order — use the first one that matches:

| Check | Project type |
|---|---|
| `package.json` contains `"plasmo"` in dependencies or devDependencies | **Plasmo** |
| `wxt.config.ts` or `wxt.config.js` exists | **WXT** |
| Any `.csproj` file exists anywhere in the project tree | **Windows .NET** |
| `package.json` contains `"electron"` in dependencies or devDependencies | **Electron** |
| `manifest.json` exists in the root directory, `src/`, or `public/` | **Vanilla browser extension** |

If none of the above match, ask the user to describe their project type before choosing a guide.

## Step 3: Load the Matching Guide

Read the guide file that corresponds to the detected project type. All paths are relative to this skill directory (`mellowtel-integration/`):

| Project type | Guide file |
|---|---|
| Plasmo | `references/plasmo.md` |
| WXT | `references/wxt.md` |
| Electron | `references/electron.md` |
| Windows .NET | `references/windows-native.md` |
| Vanilla / other browser extension | `references/extensions-guide.md` |

Read the entire guide before making any file changes.

## Step 4: Execute the Integration

Follow the guide exactly as written. While doing so:

- Replace every occurrence of `TEST_CONFIG_KEY`, `YOUR_API_KEY`, `YOUR_INTEGRATION_ID`, and `PLASMO_PUBLIC_MELLOWTEL` with the actual API key from Step 1.
- Read existing project files before modifying them — never overwrite content blindly.
- Merge new permissions and configuration into existing files; do not replace them.
- Do not add `.md` documentation files to the user's project.
- Do not run build commands unless the guide explicitly requires them for validation.

## Step 5: Report

When the integration is complete, list every file that was created or modified so the developer knows exactly what changed. Format the list clearly:

**Created:**
- `path/to/new-file.ts`

**Modified:**
- `path/to/existing-file.json`
