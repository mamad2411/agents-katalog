---
name: follow-tool-release-it
description: Set up release-it for automated version bump, tag, and npm publish
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - follow-tool-semantic-release
  - follow-tool-changesets
  - follow-tool-changelogen
  - follow-tool-github-actions
  - follow-tool-pkg-new
  - follow-lang-nodejs
  - open-web-for-config-secret
  - run-release
---

## Goal

Set up `release-it` for automated releases to npm and GitHub

## Scope

Use for Node.js projects that want automated version bump, git tag, changelog, npm publish, and GitHub release

- Pick the tool by workflow: `release-it` fits interactive/manual releases where you choose the version and flex the hooks
- Use `follow-tool-semantic-release` when you want fully automated releases from conventional commits without picking versions yourself
- Use `follow-tool-changesets` for monorepo/workspaces that need several packages versioned at once
- Use `follow-tool-changelogen` when you only need changelog generation, no publishing

- Latest: `release-it@21.1.0` (verified 2026-09-24) — v21 requires Node.js `^22.21.0 | >=24.0.0`

## Execute

### Workflows

| Topic | Workflow |-------|----------| Install, release script, hooks/plugins basics | `workflows/setup-release-it/SKILL.md` | `.release-it.json` — git, github, npm, changelog options | `workflows/config-release-it/SKILL.md` 
### 1. Install

> Goal: install release-it in the project

1. Run `bun add -D release-it`
2. Add a script in `package.json`: `"release": "release-it"`
3. Verify with `bunx release-it --version`
4. See details in 

### 2. Configure

> Goal: create a config for release-it

1. Create `.release-it.json` at the project root
2. Set `git`, `npm`, `github`, and `hooks` per the project policy
3. Use `requireCleanWorkingDir: false` only when CI runs without a clean working dir
4. See details in 

### 3. Manual Release

> Goal: run a release locally or in CI

1. Run `bun run release` for interactive mode
2. Run `bun run release --ci` for non-interactive mode
3. Use `major`, `minor`, `patch`, or `--release-version` to control the version
4. See details in 

### 4. GitHub Actions Workflow

> Goal: release automatically on push to main

1. Create `.github/workflows/release.yml`
2. Use `/follow-secret-manager` to manage the `NPM_TOKEN` and `GITHUB_TOKEN` secrets, or `/open-web-for-config-secret` to open the token-creation URLs
3. Use `actions/checkout@v7` and `oven-sh/setup-bun@v2`
4. Run `bun install` then `bun run release --ci`
5. See details in 

### 5. Plugins

> Goal: extend release-it with plugins

1. Use `@release-it/conventional-changelog` for an auto changelog
2. Use `@release-it/bumper` for custom manifest files
3. Use `@release-it/keep-a-changelog` to maintain `CHANGELOG.md`
4. See details in 

## Rules

### 1. Safety

- Verify publish rights to npm before running a release
- Use `requireCleanWorkingDir: true` for local releases
- Set `NPM_TOKEN` and `GITHUB_TOKEN` as repository secrets

### 2. CI

- Use `--ci` in GitHub Actions to disable interactive prompts
- Use `fetch-depth: 0` in `actions/checkout` to have the full history
- Never run release on a pull request

### 3. Versioning

- Use conventional commits or the correct bump type
- Check the `package.json` version before releasing
- Use `--no-npm.publish` for a test run if needed
- v21: CLI parsing is strict — unknown options, invalid booleans, and extra positional args are rejected
- v21: GitLab server certificates are verified by default — use a private CA or `gitlab.secure: false` if needed

### 4. Secrets

- Never hard-code tokens in config or workflow
- Use `/follow-secret-manager` to manage `NPM_TOKEN` and `GITHUB_TOKEN`
- Use `/open-web-for-config-secret` to open the API-key creation URLs
- Use `secrets.NPM_TOKEN` and `secrets.GITHUB_TOKEN` via GitHub Actions
- If needed, use `gh secret set` to configure via CLI

- Use /follow-tool-semantic-release if needed (tool release it)
- Use /follow-tool-changesets if needed
- Use /follow-tool-github-actions if needed (tool release it)
- Use /follow-tool-pkg-new if needed
- Use /follow-lang-nodejs if needed

## References

- [CLI reference](references/cli.md)

- Use /run-release if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `release-it` installed and configured in the project
- `bun run release` works both locally and in CI
- Version, tag, npm publish, and GitHub release happen automatically
- Secrets and permissions configured correctly
- The plugins you need work per config

