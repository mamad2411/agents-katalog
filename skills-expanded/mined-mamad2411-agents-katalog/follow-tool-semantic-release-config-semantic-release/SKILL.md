---
name: follow-tool-semantic-release-config-semantic-release
description: Configure semantic-release — branches, plugins, tagFormat, changelog
argument-hint: "[scope]"
related:
  - follow-tool-github-actions
  - follow-tool-git
  - run-release
---

## Goal

Configure the semantic-release release config — `branches`, `plugins`, `tagFormat`, plugin options — to match the branching and publishing policy

## Scope

Use when defining/editing the release config — install/auth live in `workflows/setup-semantic-release/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Read the existing config before editing

1. Find the existing config: `.releaserc`, `release.config.cjs`/`release.config.mjs`, or the `"release"` field in `package.json`
2. Read the plugins installed in devDependencies
3. If no config exists → create `release.config.cjs` (or `.releaserc`) at the root

### 2. Configure Branches

> Goal: Define the branches that can release

1. `branches` — list the release branches, e.g. `["main"]` or `["main", { name: "beta", prerelease: true }]`
2. Add prerelease channels (`beta`, `alpha`, `next`) per the release policy — use the `{ name, prerelease: true }` object form
3. List only the branches allowed to release — other branches dry-run/skip by default

### 3. Configure Plugins

> Goal: Set the plugin pipeline

1. Default plugins (ship with semantic-release): `@semantic-release/commit-analyzer`, `@semantic-release/release-notes-generator`, `@semantic-release/npm`, `@semantic-release/github`
2. Add as needed:
   - `@semantic-release/changelog` — writes `CHANGELOG.md` (options: `changelogFile`)
   - `@semantic-release/git` — commits the changelog/package.json back to the repo (options: `assets`, `message`)
   - `@semantic-release/exec` — custom commands in the lifecycle (see official docs)
3. Use the plugin object form `["@semantic-release/npm", { "npmPublish": false }]` when adjusting options
4. Don't add a plugin that isn't installed — it fails at load

### 4. Tag And Other Options

> Goal: Set the tag format and extra options

1. `tagFormat` — default `v${version}`; for a monorepo `${name}@${version}` may fit an existing convention — never change it on a repo with existing tags without checking
2. `repositoryUrl` — override only when auto-detect is wrong
3. `preset`/`parserOpts`/`releaseRules` — tune commit analysis when not using standard conventional commits (see official docs)

### 5. Verify

> Goal: Check the config with a dry run

1. Run `bunx semantic-release --dry-run --debug` — check the branch check, plugin loading, and the resulting version
2. Check that the changelog and git commit steps run in the plan
3. If it breaks → revert the changed keys, then report the diff with `/report-before-after`

## Rules

### 1. Config Discipline

- Use a clear `release.config.cjs` or `.releaserc` — don't scatter config across places
- Never hard-code tokens or secrets in the config — auth goes through env vars
- Merge with the existing config, never overwrite unless necessary

### 2. Branches

- Define `branches` explicitly — never release on a branch that wasn't allowed
- Prerelease branches use `{ name, prerelease: true }`

### 3. Plugins

- Plugin order affects the lifecycle — the commit/git plugins belong at the end of the pipeline
- Every plugin in the config must be installed in devDependencies

- Use /follow-tool-git if needed
- Use /run-release if needed

## Expected Outcome

- A release config matching the branching and publishing policy
- Plugins load and the lifecycle works completely
- `--dry-run` shows the correct plan
