---
name: follow-create-storybook-addon
description: Build a Storybook addon — manager UI, preview decorators, preset, and publish
argument-hint: "[addon-name]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - follow-tool-release-it
  - ship
---

## Goal

Build Storybook addons following the official architecture — manager API (panels/tools/tabs), preview decorators, preset, and publishable packaging

## Scope

For projects that need a new Storybook addon, or to turn an existing feature into an addon

- Package: `storybook` + addon APIs (`storybook/manager-api`, `preview-api`, `theming`) — always confirm the latest version and migration guide with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)
- Storybook 9 uses imports from `storybook/manager-api`, `storybook/theming`, `storybook/internal/components` — do `not use` `@storybook/addons`, `@storybook/api` (deprecated)
- `@storybook/addon-kit` has been archived — scaffold manually following the structure below

## Execute

### 1. Review Tech Stack

> Goal: Inspect the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the libraries to be used (react, storybook version, bundler)
3. Check that the target Storybook version matches the APIs used (9.x = `storybook/manager-api`)

### 2. Prepare

> Goal: Check requirements before starting

1. Node >= 18, Bun/pnpm/npm available
2. Have a Storybook project to test the local addon (or create a sandbox with `bunx storybook@latest init` in a subfolder)
3. Name the package `storybook-addon-<name>` — this prefix is required for the addon catalog

### 3. Addon Structure

> Goal: Create the standard addon skeleton

```text
src/
  constants.ts     — ADDON_ID, PANEL_ID, TOOL_ID, PARAM_KEY, EVENTS
  manager.ts       — addons.register() + addons.add() (manager UI)
  preview.ts       — decorators / globals (preview-side)
  preset.ts        — managerEntries, previewAnnotations (node-side)
  index.ts         — public API exports
  components/      — React components for panel/tool UI
```

### 4. Manager Side

> Goal: Register the addon in the manager UI

1. In `src/manager.ts`, use `addons.register(ADDON_ID, api => ...)` from `storybook/manager-api`
2. Add UI types as needed:
   - `types.PANEL` — a panel in the addons panel (use `AddonPanel` from `storybook/internal/components`)
   - `types.TOOL` — a toolbar button (use `ToggleButton`/`IconButton`)
   - `types.TAB` — a story-level tab
   - `types.SIDEBAR_BOTTOM`/`types.experimental_SIDEBAR_TOP` — sidebar
3. Use `useGlobals`, `useStorybookApi`, `useChannel` for state + communication
4. Set keyboard shortcuts via `api.setAddonShortcut()`
5. Use `@storybook/icons` for icons and `storybook/theming` for theming (`styled`, `themes`)

### 5. Preview Side

> Goal: Feed decorators/globals into the preview iframe

1. In `src/preview.ts`, export `decorators`, `globals`, `initialGlobals` as needed
2. Use `makeDecorator` from `storybook/preview-api` for decorators that read parameters
3. Communicate manager↔preview via `useChannel` + `addons.getChannel()` (events in constants)

### 6. Preset And Packaging

> Goal: Package the addon so Storybook can resolve it

1. `package.json` must have a `bundler` field:

```json
{
  "bundler": {
    "exportEntries": ["src/index.ts"],
    "managerEntries": ["src/manager.ts"],
    "previewEntries": ["src/preview.ts"],
    "nodeEntries": ["src/preset.ts"]
  },
  "exports": {
    ".": { "types": "./dist/index.d.ts", "default": "./dist/index.js" },
    "./manager": "./dist/manager.js",
    "./preview": "./dist/preview.js",
    "./preset": "./dist/preset.js",
    "./package.json": "./package.json"
  },
  "files": ["dist/**/*", "README.md"],
  "keywords": ["storybook", "storybook-addon", "storybook-addons"],
  "devDependencies": { "storybook": "^9.0.0" }
}
```

2. Build with `tsup` (entries per the bundler field) — `tsup src/index.ts src/manager.ts src/preview.ts src/preset.ts --format esm,cjs --dts`
3. `storybook` must be a `devDependency`/`peerDependency` — never bundle storybook packages into dist

### 7. Test Locally

> Goal: Verify the addon actually works in Storybook

1. Link the addon into the test project: add to `.storybook/main.ts` → `addons: ['<path-or-package>']`
2. Run `storybook dev` → check that the panel/tool/tab renders correctly, globals toggle, and channel events reach both sides
3. Check the production build: `storybook build` must not break
4. Use `/use-agents-capture all` to capture the panel UI as evidence if needed

### 8. Publish

> Goal: Publish the addon to the catalog

1. Use `/follow-tool-release-it` or `/follow-tool-auto-it` for the release flow
2. Add `"keywords": ["storybook-addons"]` so it appears in the addon catalog automatically
3. Have a `README.md` with usage + screenshot — the catalog pulls from npm

### 9. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. API Correctness

- Storybook 9: use only `storybook/manager-api`, `storybook/preview-api`, `storybook/theming`, `storybook/internal/components`
- Never import from `@storybook/addons`, `@storybook/api`, `@storybook/components` (moved/deprecated)
- `@storybook/icons` is still fine to use

### 2. Architecture Separation

- Manager code must never import preview-only code and vice versa — share only through `constants.ts`
- `src/preset.ts` is node-side — never import React/browser APIs
- The addon must work without extra config in the user project (convention over config)

### 3. Packaging

- The `bundler` field in package.json is required for entry resolution
- Never bundle `storybook`, `react`, `react-dom` into dist — use peer/dev deps
- The keyword `storybook-addons` is required for the catalog

## References

- Writing addons: https://storybook.js.org/docs/addons/writing-addons
- Addon API (manager): https://storybook.js.org/docs/addons/addons-api
- Addon migration guide: https://storybook.js.org/docs/addons/addon-migration-guide
- Use Context7 `/storybookjs/storybook` for additional docs

- Use /follow-create-sdk if needed
- Use /use-my-packages-on-registry if needed

## Expected Outcome

- An addon whose registered panel/tool/tab works in Storybook 9
- Standard structure: `manager.ts`, `preview.ts`, `preset.ts`, `constants.ts`
- `package.json` has a complete `bundler` + `exports` + `keywords` and can be published
- Tested in a local Storybook project in both dev and build
