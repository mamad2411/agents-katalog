---
name: verify-build
description: Runs npm run build to catch Vite/Rollup failures before merge. Use when validating frontend changes or in CI pre-merge loops.
paths:
  - "package.json"
  - "**/*.vue"
  - "**/*.ts"
---


# Verify Build

## When to use

- Before opening or approving a PR with frontend changes
- After refactoring imports, routes, or Vite config
- When static generation or bundle errors are suspected

## Instructions

1. Ensure dependencies are installed (`npm ci` or `npm install`).
2. Run `bash scripts/verify_build.sh --project-root <root>`.
3. If build fails, read the Rollup/Vite stack trace and fix imports or types.
4. Re-run until output shows success.

## Scripts

- `verify_build.sh` — executes `npm run build` and returns combined output
