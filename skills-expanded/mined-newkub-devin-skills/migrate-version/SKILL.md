---
name: follow-lang-nodejs-migrate-version
description: Move a Node.js project between major versions safely, one step at a time
related:
  - follow-lang-nodejs
  - deep-review-codebase
  - improve
  - resolve-errors
  - run-test
  - run-typecheck
  - deep-research
---

## Goal

Upgrade a Node.js project to a newer major with no regression in build, tests, or runtime behavior

## Scope

For bumping the pinned Node.js line of an existing project; live-check the current release schedule via `/deep-research` before choosing the target

## Execute

### 1. Baseline

1. Record the current version: `node --version`, `engines.node`, `.nvmrc`/`mise.toml`
2. Full green baseline first — run tests and typecheck; fix pre-existing failures before the bump

### 2. Read The Breaking Changes

1. Read the official release notes/changelog for every major between old and new — one major at a time, never skip intermediate majors on large jumps
2. Grep the codebase for deprecated APIs touched by those notes → `/deep-review-codebase` for a systematic deprecation scan if the jump is large

### 3. Switch The Runtime

1. `mise use node@<line>` (project pin) or `mise use -g node@<line>`; update `.nvmrc`/`engines.node` in the same commit
2. Reinstall dependencies on the new line: remove `node_modules` + reinstall; `npm rebuild` for native modules

### 4. Fix And Verify Per Bump

1. Run tests and typecheck after each single major bump — not after the whole migration
2. Check libraries still support the target → `/improve deps` for the dependency audit
3. On failure → run `/resolve-errors`

### 5. Ship

1. Commit the pin + lockfile + code fixes together; CI must run on the same pinned line (matrix entry updated)
2. Report before/after versions, deprecations fixed, and test results

## Rules

- Never mix runtime upgrade with unrelated refactors in one commit

## Expected Outcome

- Project running on the target Node.js line with green tests, updated pins everywhere, and no leftover deprecated APIs
