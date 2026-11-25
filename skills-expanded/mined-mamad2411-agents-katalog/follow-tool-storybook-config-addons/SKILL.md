---
name: follow-tool-storybook-config-addons
description: Configure `.storybook/main.ts` addons — essentials, docs, a11y, vitest
argument-hint: "[scope]"
related:
  - follow-tool-vitest
  - follow-tool-playwright
  - run-test
---

## Goal

Configure Storybook addons in `.storybook/main.ts` — docs, a11y, vitest integration, and other addons as needed — merging with the existing config

## Scope

Use when adding/editing addons or the main.ts config — init/framework setup lives in `workflows/setup-storybook/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Read the existing config before editing

1. Read `.storybook/main.ts` — the current `framework`, `stories`, `addons`
2. Check the Storybook version — **important**: in v10+ controls/actions/interactions/viewport/backgrounds are core features (no need to install `@storybook/addon-essentials`/`addon-interactions`); earlier versions rely on essentials — always check the version in `package.json` first
3. Check the addons already installed in devDependencies

### 2. Configure Addons

> Goal: Register the wanted addons in the `addons` array

1. `@storybook/addon-docs` — auto-docs from stories
2. `@storybook/addon-a11y` — accessibility testing panel
3. `@storybook/addon-vitest` — component/interaction testing via Vitest (requires a vitest setup — run `/follow-tool-vitest` first)
4. Other addons (theming, design tools, i18n) — install the package first, then add its name to the `addons` array; see the official docs for unsure addon names
5. Addons with options use the object form `{ name: "...", options: {...} }`

### 3. Adjust main.ts Options

> Goal: Set options that support the addons

1. `staticDirs` — static assets used by addons/stories
2. `docs`/`features` flags per version (see official docs)
3. `framework` options (builder config) when adjustments are needed
4. `.storybook/preview.ts` — global parameters the addons read (e.g. a11y config, docs settings)

### 4. Verify

> Goal: Check the addons load correctly

1. Run the dev server — open the UI and check the addon panels appear (Docs tab, Accessibility tab, etc.)
2. Run `bunx storybook build` — the build passes with no addon errors
3. If an addon fails → check version compatibility against the Storybook version, then fix (max 3 rounds)

## Rules

### 1. Version Awareness

- Always check the Storybook version first — v10 moved many addons into core; don't install an addon that has become core
- Addon versions must be compatible with the Storybook major version

### 2. Config Discipline

- Merge with the existing `addons` array — never overwrite
- Every addon in `addons` must be installed in devDependencies

### 3. Testing

- `@storybook/addon-vitest` needs a vitest environment — set it up before registering
- Run `storybook test`/`test-storybook` in CI when using testing addons

- Use /follow-tool-vitest if needed
- Use /deep-test visual if needed

## Expected Outcome

- The wanted addons are registered and work in the dev server
- `storybook build` passes with the new addons
- Docs/a11y/testing panels are usable
