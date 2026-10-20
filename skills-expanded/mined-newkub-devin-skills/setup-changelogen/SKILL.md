---
name: follow-tool-changelogen-setup-changelogen
description: Install changelogen, set up changelog generation and release commands
argument-hint: "[scope]"
related:
  - follow-tool-changesets
  - run-release
  - follow-secret-manager
---

## Goal

Install and configure changelogen to generate changelogs from conventional commits and run release commands — first-time setup

## Scope

Use for projects that need automated changelog generation and releases with changelogen — config, package scripts, release commands

## Execute

### 1. Check Prerequisites

> Goal: check state before setup

1. Check whether `changelog.config.ts` or a `changelog` field in `package.json` already exists — if present → skip to verify
2. Check that the project uses conventional commits — changelogen parses `type(scope): description`
3. changelogen runs via `bunx changelogen@latest` without installing — or `bun add -D changelogen` to pin a version

### 2. Configure

> Goal: create the config for the project

1. Create `changelog.config.ts` at the root with `defineConfig` from `changelogen` — config is loaded via c12 from `changelog.config.{ts,js,mjs,cjs}`, `.changelogrc`, or the `changelog` field in `package.json`
2. Set `types` (commit type → title + semver bump) and `scopeMap` (map scope → display name)
3. Set `output` if a custom path is needed (default `CHANGELOG.md`)
4. Set `templates` (commitMessage, tagMessage, tagBody), `excludeAuthors`, `publish`, and `repo` as needed

### 3. Setup Package Scripts

> Goal: add changelog/release scripts

1. `"changelog": "bunx changelogen@latest --release"` — full release (bump + changelog + commit + tag + GitHub release)
2. `"changelog:version": "bunx changelogen@latest --bump"` — version bump only
3. `"changelog:generate": "bunx changelogen@latest"` — changelog generation only

### 4. Release Flow

> Goal: use release commands correctly

1. `--release` — full release: bump + changelog + git commit + tag + GitHub release sync
2. Disable sub-steps with `--no-commit`, `--no-tag`, `--no-github`; use `--push` to auto-push after release
3. `-r <version>` to specify the version directly; `--major`/`--minor`/`--patch`/`--pre*` to force the bump; `--canary` for a canary release
4. `--publish` publishes to npm (auth via `.npmrc`/env), `--publishTag` for a custom dist-tag
5. `bunx changelogen gh release` — sync GitHub releases from `CHANGELOG.md` without bumping again
6. `--clean` requires a clean working directory before release
7. GitHub tokens: `CHANGELOGEN_TOKENS_GITHUB`, `GITHUB_TOKEN`, or `GH_TOKEN` — use `/follow-secret-manager`

### 5. Verify

> Goal: confirm changelog generation works

1. Run `bun run changelog:generate` — check the `CHANGELOG.md` output is correct
2. Preview the version bump with `--bump` on a test branch (revert after checking)
3. If it fails → run `/resolve-errors` for max 3 rounds, then stop and report

## Rules

### 1. Conventional Commits

- format `type(scope): description`; types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`
- breaking change: `feat!:` or `BREAKING CHANGE:`

### 2. Monorepo

- changelogen works per git repo — no `--workspace`/`--all`; use `--dir <path>` to point at a sub-package
- multi-package versioning → run per-package or use `/follow-tool-changesets` instead

### 3. Secrets

- tokens via env only, never commit — use `/follow-secret-manager`

- Use /follow-tool-changesets if needed
- Use /run-release if needed

## Expected Outcome

- `changelog.config.ts` created and parseable
- Scripts for generate/bump/release ready to use
- `CHANGELOG.md` generated correctly from conventional commits
