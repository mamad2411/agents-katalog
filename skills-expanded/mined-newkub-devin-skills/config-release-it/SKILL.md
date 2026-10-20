---
name: follow-tool-release-it-config-release-it
description: Configure `.release-it.json` — git, github, npm, hooks, changelog options
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - run-release
  - follow-tool-github-actions
---

## Goal

Configure `.release-it.json` to match the release policy — `git`, `github`, `npm`, `hooks`, plugins — merging with the existing config without overwriting

## Scope

Use when editing an existing release-it config — install/scripts are in `workflows/setup-release-it/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: read the existing config before editing

1. Read `.release-it.json` (or the `release` field in `package.json`) — record the current keys
2. Check the plugins installed in devDependencies
3. If no config exists → create `.release-it.json` at the root (or run `workflows/setup-release-it/SKILL.md` first)

### 2. Git Options

> Goal: configure the `git` section

1. `git.commitMessage` — commit message format, e.g. `"chore: release v${version}"`
2. `git.tagName` — tag format, e.g. `"v${version}"`
3. `git.requireCleanWorkingDir` — `true` for local; `false` only when CI must run without clean
4. `git.push` — `true` to push the commit+tag automatically
5. `git.requireBranch` — restrict releases to a branch, e.g. `"main"`

### 3. GitHub Options

> Goal: configure the `github` section for GitHub releases

1. `github.release: true` — create GitHub releases automatically
2. `github.releaseName` — release name format, e.g. `"v${version}"`
3. `github.autoGenerate` — use GitHub auto-generated release notes, or disable when using a changelog plugin
4. `github.draft`/`github.prerelease` — per release policy
5. auth via the `GITHUB_TOKEN` env — never put a token in config

### 4. npm And Changelog Options

> Goal: configure the `npm` section and changelog

1. `npm.publish` — `true` to publish to the registry; `false` for private repos
2. `npm.publishPath`/`npm.tag` — dist-tags such as `"latest"`, `"beta"` per channel
3. Use `@release-it/conventional-changelog` — set `plugins."@release-it/conventional-changelog".preset`, e.g. `"conventionalcommits"` (check official docs for preset names)
4. `hooks` — `"before:init"`, `"after:bump"`, `"after:release"` for build/test/notify steps

### 5. Verify

> Goal: check the config with a dry run

1. Run `bunx release-it --dry-run` — the config must parse and show the right plan
2. Check tag format, release notes, and publish target in the dry-run output
3. If it breaks → revert the changed keys and report the diff with `/report-before-after`

## Rules

### 1. Merge Discipline

- Edit only the necessary keys — never overwrite the whole file
- Strict CLI parsing: unknown options are rejected — use only keys that actually exist (check official docs)

### 2. Safety

- Always `--dry-run` before a real release
- Use `--no-npm.publish` for a test run if needed
- Don't change the `tagName` format on a repo with existing tags without checking the convention

### 3. Secrets

- Tokens via env vars (`GITHUB_TOKEN`, `NPM_TOKEN`) only — never in config
- Use `/follow-secret-manager` to manage tokens

- Use /run-release if needed

## Expected Outcome

- `.release-it.json` has git/github/npm options matching the release policy
- `--dry-run` shows a correct release plan
- Changelog/plugins work per config
