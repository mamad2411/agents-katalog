---
name: follow-tool-release-it-setup-release-it
description: Install release-it, add the release script, and set up basic hooks/plugins
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - follow-tool-github-actions
  - run-release
---

## Goal

Install `release-it` in the project and set up the basic release workflow — script, hooks, plugins — so `bun run release` works both locally and in CI

## Scope

Use for Node.js projects starting with release-it — install, scripts, basic hooks/plugins. Config option details live in `workflows/config-release-it/SKILL.md`

- If `release-it` is already installed and the config exists → verify only

## Execute

### 1. Check Prerequisites

> Goal: check state before setup

1. Check `package.json` — it must have a `version` field and a clean git repository
2. Check whether `release-it` is already in devDependencies — if present → skip to verify
3. Check the Node.js version matches the requirement of the release-it version being installed (see the parent skill or official docs)

### 2. Install And Script

> Goal: install and add the release script

1. Run `bun add -D release-it` (or the project's package manager)
2. Add a script in `package.json`: `"release": "release-it"`
3. Verify with `bunx release-it --version`

### 3. Basic Hooks And Plugins

> Goal: set up basic hooks/plugins

1. Create a minimal `.release-it.json` at the root — detailed options continue in `workflows/config-release-it/SKILL.md`
2. Add `hooks` if wanted, e.g. `"after:bump": "bun run build"` to build before publish
3. Install plugins as needed:
   - `@release-it/conventional-changelog` — auto changelog from conventional commits
   - `@release-it/bumper` — bump versions in other manifest files
   - `@release-it/keep-a-changelog` — maintain `CHANGELOG.md`
4. Plugin details: see [references/release-it.md](../../references/release-it.md) or the official docs

### 4. CI Workflow (Optional)

> Goal: release automatically in CI

1. Create `.github/workflows/release.yml` — trigger on push to main or on tags
2. Use `fetch-depth: 0` in checkout so the full git history is available
3. Run `bun run release --ci` for non-interactive mode
4. Use `/follow-secret-manager` to set `NPM_TOKEN` and `GITHUB_TOKEN` as secrets

### 5. Verify

> Goal: confirm the release flow works

1. Run `bunx release-it --dry-run` — check the version bump, changelog, and publish steps that would happen
2. If the dry run shows unexpected output → fix the config and dry-run again
3. If verify fails → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

### 1. Safety

- Always test with `--dry-run` before a real release
- Use `requireCleanWorkingDir: true` for local releases
- Never run release on a pull request

### 2. Secrets

- `NPM_TOKEN`/`GITHUB_TOKEN` via a secrets manager only, never hard-code

### 3. Idempotent

- If the setup already exists → verify with `--dry-run` only

- Use /follow-tool-github-actions if needed
- Use /follow-secret-manager if needed

## Expected Outcome

- `release-it` installed with a `release` script
- Basic `.release-it.json` and the wanted plugins ready to use
- `--dry-run` shows a correct release plan
