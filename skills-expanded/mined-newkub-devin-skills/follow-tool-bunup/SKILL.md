---
name: follow-tool-bunup
description: Set up Bunup to bundle TypeScript libraries with ESM, CJS, and dts
argument-hint: "[scope]"
related:
  - use-agent-browser
  - use-astgrep
  - follow-tool-aube
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - use-bun-native-api
  - follow-tool-tsdown
  - follow-tool-rolldown
  - follow-tool-vite
---

## Goal

Set up Bunup as the library bundler for TypeScript libraries using Bun's native bundler

## Scope

For TypeScript library projects that want bundling with Bun's native bundler — see `/use-bun-native-api` for Bun runtime setup

- Boundary: Bunup suits library bundling (ESM/CJS + dts) on Bun — if the project is not tied to Bun or wants a Rolldown-based bundler see `/follow-tool-tsdown`; for a low-level bundler see `/follow-tool-rolldown`; for app dev server/build see `/follow-tool-vite`
- Latest: `bunup@0.16.32` (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Analyze Project

> Goal: check the project, entry points, output formats, and prerequisites before using Bunup

1. Confirm it is a TypeScript library project
2. Confirm Bun is installed
3. Confirm a `package.json` already exists
4. Identify the desired output formats (ESM, CJS)

### 2. Setup Bunup

> Goal: install Bunup, set up config, build scripts, and try a build

1. Install Bunup with `bun add --dev bunup`
2. Create `bunup.config.ts` defining `entry`, `format`, `dts`
3. Add build scripts to `package.json` (`build`, `dev`, `build:watch`)
4. Run the build to verify it works correctly

### 3. Verify Setup

> Goal: check build output, type declarations, and build scripts

1. Verify `dist/` output is generated correctly
2. Confirm type declarations (`.d.ts`) are complete
3. Test that the build scripts work

## Rules

### 1. Installation

- Use `bun add --dev bunup` only
- Verify the installation succeeded before continuing

### 2. Configuration

- Create `bunup.config.ts` in TypeScript format
- Bunup auto-detects entry points: `index.ts`, `index.tsx`, `src/index.ts`, `src/index.tsx`, `cli.ts`, `src/cli.ts`, `src/cli/index.ts`
- Set output formats with the `--format` flag in CLI or config
- dts generation is enabled by default (auto-generate)

### 3. Build Scripts

- Add `"build": "bunup"` script to `package.json`
- Add `"dev": "bun run src/index.ts"` script for development
- Add `"build:watch": "bunup --watch"` script for watch builds

### 4. Output Configuration

- Use `--format esm,cjs` for multiple formats
- Use `--exports` to generate and sync package exports automatically
- Use `--watch` for development mode

### 5. Project Structure

```text
project/
├── bunup.config.ts      # Bundle config (optional)
├── package.json          # Build scripts
├── src/
│   ├── index.ts         # Entry point (auto-detected)
│   └── cli.ts           # CLI entry (auto-detected)
└── dist/                 # Output
```

- Use /use-agent-browser if needed
- Use /use-astgrep if needed
- Use /follow-tool-aube if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /follow-tool-tsdown if needed
- Use /follow-tool-rolldown if needed
- Use /follow-tool-vite if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Bunup installed and configured in the project
- `bunup.config.ts` with entry points and output formats
- `package.json` with build scripts for bunup
- ESM and CJS formats supported
- Type declarations (dts) generated automatically

For all CLI options, default entry points, config file format, and scaffolding (`bunx @bunup/cli@latest create`) see `references/apis.md` and `references/cli.md`
