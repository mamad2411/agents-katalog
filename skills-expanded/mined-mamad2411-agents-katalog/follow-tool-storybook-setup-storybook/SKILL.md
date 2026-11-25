---
name: follow-tool-storybook-setup-storybook
description: Install Storybook with the CLI init and framework detection plus basic config
argument-hint: "[scope]"
related:
  - follow-tool-vite
  - follow-tool-vitest
  - run-verify
---

## Goal

Install Storybook in the project with the official CLI — framework detection, `.storybook/` config files, scripts — so the dev server starts

## Scope

For frontend projects without Storybook yet — init, framework setup, minimal config. Addons live in `workflows/config-addons/SKILL.md`

- If `.storybook/` already exists → verify only

## Execute

### 1. Check Prerequisites

> Goal: Check the state before setup

1. Check whether a `.storybook/` directory or `storybook` in devDependencies already exists — if yes → skip to verify
2. Identify the project's framework from `package.json` (React, Vue, Svelte, Angular, etc.) and the builder (Vite, webpack)
3. Identify the package manager from the lockfile

### 2. Init Storybook

> Goal: Install with the CLI init

1. Run `bun create storybook@latest` (or `bunx storybook@latest init`/`create` depending on the version — see the parent skill for the latest commands)
2. The CLI detects the framework automatically — if it fails, specify it with `--type <framework>` (see `storybook init --help` for type names)
3. Check what the CLI created: `.storybook/main.ts`, `.storybook/preview.ts`, example stories, scripts in `package.json`
4. Check that the installed framework package matches the project (e.g. `@storybook/react-vite` for React+Vite)

### 3. Verify Config Files

> Goal: Verify the minimal `.storybook/` config is correct

1. `.storybook/main.ts` — `framework`, a `stories` glob covering the real source dirs, `addons` array
2. `.storybook/preview.ts` — global parameters/decorators/styles
3. `staticDirs` — if the project has static assets (public/, images)
4. Add scripts: `storybook` (dev server), `build-storybook` (static build) — see the scripts the CLI generated

### 4. Verify Run

> Goal: Confirm the dev server and build work

1. Run the dev server (`bun run storybook` or the script the CLI created) — open the URL it prints, the example stories must appear
2. Run `bunx storybook build` — the static build passes and creates `storybook-static/`
3. If it fails → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

### 1. Init

- Always use the official CLI init — never hand-write boilerplate when the CLI can do it
- Use `--type` when auto-detect fails
- Use only the official framework packages

### 2. Config

- The `stories` glob must cover the dirs that really contain components
- `.storybook/preview.ts` for global rendering; `manager.ts` for UI behavior

### 3. Verification

- Dev server start + static build must pass before treating the setup as done

- Use /follow-tool-vite if needed
- Use /follow-tool-vitest if needed

## Expected Outcome

- Storybook installed with the correct framework package
- `.storybook/main.ts` + `preview.ts` created
- The dev server and `build-storybook` work
