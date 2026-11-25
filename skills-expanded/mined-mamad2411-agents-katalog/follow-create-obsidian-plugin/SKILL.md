---
name: follow-create-obsidian-plugin
description: Build an Obsidian plugin in TypeScript with manifest, commands, and settings
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - follow-create-web
  - follow-lang-typescript
  - run-test
  - update-dot-vscode
  - deep-review-codebase
  - report

---

## Goal

Build an Obsidian plugin project in TypeScript with a correct manifest, commands, a settings tab, build, and release readiness.

## Scope

Use for creating Obsidian desktop/mobile plugins from the sample plugin or a manual setup, with esbuild, manifest, styles, and GitHub release.

- Package: `obsidian` (npm typings — track the app API) — always confirm the latest version via `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`); `manifest.json` `minAppVersion` must match a real release.

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create obsidian plugin)
3. Record the rationale for the chosen stack and libraries for later reference (create obsidian plugin)

### 2. Setup Project

> Goal: Create the plugin structure

1. Clone https://github.com/obsidianmd/obsidian-sample-plugin or create the structure yourself
2. Create `src/`, `styles.css`, `manifest.json`, `versions.json`, `package.json`, `tsconfig.json`, `esbuild.config.mjs`
3. Rename the folder to match the `id` in `manifest.json`
4. Install dependencies with `bun install` (if the project primarily uses npm, use `npm install`)

### 3. Configure Manifest

> Goal: Define plugin metadata

1. Edit `manifest.json`:
   - `id`: unique identifier
   - `name`, `description`, `author`, `version`
   - `minAppVersion`: minimum Obsidian version
   - `isDesktopOnly`: `false` if mobile is supported
2. Edit `versions.json` to map versions to `minAppVersion`

### 4. Implement Plugin Class

> Goal: Create the `Plugin` subclass

1. Create `src/main.ts` with `import { Plugin, Notice } from 'obsidian'`
2. Create class `MyPlugin extends Plugin`
3. Implement `onload()` for `addCommand`, `addRibbonIcon`, `addSettingTab`
4. Implement `onunload()` for cleanup

### 5. Add Settings

> Goal: Create the settings tab

1. Create `src/settings.ts` with `PluginSettingTab`
2. Define an interface for the default settings
3. Use `this.loadData()` and `this.saveData()` to read/write settings
4. Build the UI with the `Setting` class

### 6. Build And Watch

> Goal: Build the plugin into `main.js`

1. Use `esbuild.config.mjs` to compile `src/main.ts` → `main.js`
2. Set `external: ['obsidian', 'fs', 'path']` in esbuild
3. Run `bun run dev` for watch mode (if the project primarily uses npm, use `npm run dev`)
4. Verify `main.js` and `styles.css` are at the root

### 7. Test In Obsidian

> Goal: Test the plugin in a vault

1. Copy the plugin folder to `vault/.obsidian/plugins/{id}/`
2. Open Obsidian → Settings → Community Plugins → enable the plugin
3. Test commands, ribbon icon, and settings tab
4. Use `Ctrl+Shift+I` / `Cmd+Opt+I` to inspect console errors

### 8. Release

> Goal: Create a GitHub release

1. Update `manifest.json` and `versions.json` with the new version
2. Create a git tag matching the version
3. Create a GitHub release attaching `main.js`, `manifest.json`, `styles.css`
4. Run `/ship`

## Rules

- The `id` in `manifest.json` must be unique and match the folder name
- `manifest.json`, `main.js`, `styles.css` must be at the root of the release
- Use `external: ['obsidian']` in esbuild; do not bundle `obsidian`
- Use `loadData` / `saveData` for settings; do not write files yourself
- Specify `minAppVersion` correctly for every release

- Use /follow-create-sdk when needed
- Use /follow-create-web when needed
- Use /follow-lang-typescript when needed
- Use /run-test when needed
- Use /update-dot-vscode when needed
- Use /report when needed

## Expected Outcome

- The Obsidian plugin builds via `bun run build`
- The plugin loads in an Obsidian vault
- Commands, ribbon icon, and settings tab work
- The release contains `main.js`, `manifest.json`, `styles.css`

