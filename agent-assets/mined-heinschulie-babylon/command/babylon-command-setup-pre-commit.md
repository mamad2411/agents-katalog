---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
description: Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests
model: opus
---

# Purpose

Set up a complete pre-commit hook pipeline using Husky, lint-staged, and Prettier in the current repo. Follows the Instructions and Workflow sections to detect the package manager, install dependencies, configure hooks, and verify everything works.

## Instructions

- Detect the package manager by checking for lock files: `bun.lockb` (bun), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `package-lock.json` (npm). Default to npm if unclear.
- Install `husky`, `lint-staged`, and `prettier` as devDependencies using the detected package manager.
- Use Husky v9+ conventions — no shebangs needed in hook files.
- Adapt all commands in `.husky/pre-commit` to use the detected package manager (e.g., `bun run` instead of `npm run`).
- Before adding `typecheck` or `test` lines to the pre-commit hook, check if those scripts exist in `package.json`. Omit any that don't exist and inform the user.
- Only create `.prettierrc` if no Prettier config already exists (check for `.prettierrc`, `.prettierrc.json`, `.prettierrc.js`, `prettier.config.js`, or a `prettier` key in `package.json`).
- Use `prettier --ignore-unknown` in lint-staged so non-parseable files (images, etc.) are skipped.
- The pre-commit hook should run lint-staged first (fast, staged-only), then full typecheck and tests.
- After setup, run `npx lint-staged` to smoke-test the configuration.
- Stage all changed/created files and commit with message: `Add pre-commit hooks (husky + lint-staged + prettier)` — this itself exercises the new hooks.

## Workflow

1. Read `package.json` and detect the package manager from lock files in the project root.
2. Install devDependencies: `husky`, `lint-staged`, `prettier`.
3. Run `npx husky init` to create `.husky/` directory and add the `prepare` script to `package.json`.
4. Write `.husky/pre-commit` with the following lines (adapted to detected package manager, omitting missing scripts):
   - `npx lint-staged`
   - `<pkg-manager> run typecheck` (if script exists)
   - `<pkg-manager> run test` (if script exists)
5. Write `.lintstagedrc` with contents: `{ "*": "prettier --ignore-unknown --write" }`
6. If no Prettier config exists, create `.prettierrc` with sensible defaults (2-space indent, semicolons, double quotes, trailing commas es5, printWidth 80).
7. Verify the setup:
   - `.husky/pre-commit` exists and is executable
   - `.lintstagedrc` exists
   - `prepare` script in `package.json` equals `"husky"`
   - A Prettier config exists
   - `npx lint-staged` runs without errors
8. Stage all changed/created files and commit.

## Report

- State which package manager was detected.
- List all files created or modified.
- Note any scripts (`typecheck`, `test`) that were omitted from the pre-commit hook because they don't exist in `package.json`.
- Note whether a new `.prettierrc` was created or an existing Prettier config was found.
- Confirm whether the verification commit succeeded (proving the hooks work).