---
name: follow-tool-changelogen
description: Generate changelogs and manage releases with changelogen
argument-hint: "[scope]"
related:
  - fix
  - refactor
  - run-release
  - follow-tool-changesets
  - follow-tool-release-it
  - follow-tool-semantic-release
  - follow-tool-auto-it
---

## Goal

Use changelogen for automated changelog generation and release management

## Scope

Use for projects that need automated changelog generation and release management

- Boundary: changelogen generates a changelog + bumps versions from conventional commits in a single git repo — for monorepo multi-package versioning use `/follow-tool-changesets`; for PR-label-based releases use `/follow-tool-auto-it`; for full release pipelines see `/follow-tool-release-it` or `/follow-tool-semantic-release`
- Latest: `changelogen@0.6.2` (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Install, changelog generation, release command | `workflows/setup-changelogen/SKILL.md` 
### 1. Configure Changelogen

> Goal: create `changelog.config.ts` for the project

Configure changelogen for the project — config is loaded via c12 from `changelog.config.{ts,js,mjs,cjs}`, `changelog.config.json`, `.changelogrc`, or the `changelog` field in `package.json`

1. Create `changelog.config.ts` in the root with `defineConfig` from `changelogen`
2. Set `types` (commit type → title + semver bump) and `scopeMap` (map scope → display name)
3. Set `output` if a custom changelog path is needed (default `CHANGELOG.md`)
4. Set `templates` (commitMessage, tagMessage, tagBody), `excludeAuthors`, and `publish` as needed

### 2. Setup Package Scripts

> Goal: add changelog scripts to `package.json`

Add scripts to `package.json`

1. Add `"changelog": "bunx changelogen@latest --release"` for a full release
2. Add `"changelog:version": "bunx changelogen@latest --bump"` for a version bump only
3. Add `"changelog:generate": "bunx changelogen@latest"` for generate only

### 3. Generate Changelog

> Goal: generate the changelog from git commits

Generate the changelog from git commits

1. Run `bun run changelog` for a full release
2. Run `bun run changelog:version` to bump the version only
3. Run `bun run changelog:generate` to generate the changelog only
4. Review the generated `CHANGELOG.md`

### 4. Review And Commit

> Goal: review and commit the generated changelog

Review and commit the changelog

1. Verify the version bump is correct
2. Verify the changelog format is correct
3. Commit and push to the remote

## Rules

### 1. Conventional Commits

Use conventional commits for changelog generation

- Use the format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`
- Use the breaking change indicator: `feat!:` or `BREAKING CHANGE:`
- Use scopes for categorization in monorepos

### 2. Configuration

Configure changelogen to fit the project

- Use `changelog.config.ts` for TypeScript projects (the config name is `changelog`, not `changelogen`)
- Set `types` for custom commit types
- Set `scopeMap` to map commit scope → display name
- Set `repo` if auto-detection from `package.json` fails

### 3. Version Management

Manage semantic versioning correctly

- Use `--bump` for a version bump only
- Use `--release` for a full release (bump + changelog + git commit + tag + GitHub release)
- Disable release sub-steps with `--no-commit`, `--no-tag`, `--no-github`
- Use `--push` to auto-push after the release
- Specify the version directly with `-r <version>` or force the bump with `--major` / `--minor` / `--patch` / `--pre*` flags
- Use `--canary` for a canary release (equivalent to `--bump --versionSuffix`)

### 4. Monorepo Support

changelogen works per git repository — there are no `--workspace`/`--all` flags

- Use `--dir <path>` to point at a sub-package in the monorepo
- Use `scopeMap` to group commits by scope in the changelog
- For multi-package versioning, run per-package or use `/follow-tool-changesets` instead

### 5. Release Automation

Use automation for the release workflow

- Use `--release` for an automated release — the GitHub release syncs automatically when the repo is on GitHub
- Set `CHANGELOGEN_TOKENS_GITHUB`, `GITHUB_TOKEN`, or `GH_TOKEN` for GitHub releases (without a token, a browser link opens for manual creation)
- Use `--publish` to publish to npm (auth via `.npmrc` or env) and `--publishTag` for a custom dist-tag
- Use `bunx changelogen gh release` to sync GitHub releases from `CHANGELOG.md` without bumping again
- Use `--clean` to require a clean working directory before release

- Use /fix if needed
- Use /refactor if needed
- Use /run-release if needed
- Use /follow-tool-changesets if needed
- Use /follow-tool-release-it if needed
- Use /follow-tool-semantic-release if needed
- Use /follow-tool-auto-it if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Changelog generated automatically from conventional commits
- Version bump correct per semantic versioning
- Release workflow fully automated
- Monorepo support working correctly
