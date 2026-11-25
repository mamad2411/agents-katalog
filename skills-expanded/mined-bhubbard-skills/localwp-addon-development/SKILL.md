---
name: localwp-addon-development
description: Guide for developing custom Add-ons for the LocalWP platform.
---

# LocalWP Add-on Development

Use this skill to build, test, and package add-ons for LocalWP.

## Setup & Architecture
LocalWP add-ons are built using React (for the UI) and Node.js (for main process logic).
- Ensure you have Node.js and Yarn installed.
- Add-ons reside in `~/Library/Application Support/Local/addons/` (macOS) or `%AppData%\Roaming\Local\addons\` (Windows).

## Basic Structure
An add-on requires:
- `package.json`: Defines `name`, `version`, and `localAddon` metadata.
- `src/main.ts`: Main process code (hooks into Local's backend).
- `src/renderer.tsx`: Renderer process code (React components for the UI).

## Developing
1. Create a directory in the addons folder.
2. Run `yarn init` and add Local API dependencies.
3. Use `@getflywheel/local-components` for pre-built UI components matching Local's styling.
4. Compile your TypeScript code using `tsc` or a bundler like webpack/esbuild.

## Testing & Packaging
- Restart LocalWP to load the new add-on or clear the add-on cache.
- Ensure the add-on is enabled in the Add-ons menu.
- To share, package the add-on by zipping the folder (excluding `node_modules` if compiling to a bundle) or publishing to npm.
