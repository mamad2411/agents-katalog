---
name: follow-tool-semantic-release
description: Use Semantic Release for automated version management and package publishing
argument-hint: "[scope]"
related:
  - follow-release
  - follow-tool-github-actions
  - follow-tool-changesets
  - follow-tool-release-it
  - follow-tool-changelogen
  - follow-tool-git
  - follow-test
  - fix
  - run-release
---

## Goal

Use Semantic Release for automated version management, changelog generation, and package publishing per semantic versioning

## Scope

For projects using conventional commits that want to automate release, changelog, and npm/GitHub publish

- `semantic-release` suits a fully automated release — the version is derived from conventional commits with no manual step
- Use `follow-tool-release-it` when you want an interactive/manual release where you pick the version and hooks yourself
- Use `follow-tool-changesets` for monorepo/workspaces that need to version several packages at once
- Use `follow-tool-changelogen` when you only want to generate a changelog without publishing

- Latest: `semantic-release@25.0.9` (verified 2026-09-13) — requires Node.js `^22.14.0 | >=24.10.0`

## Execute

### Workflows

| Topic | Workflow |-------|----------| Install, CI auth tokens, workflow integration | `workflows/setup-semantic-release/SKILL.md` | `branches`, `plugins`, `tagFormat` config | `workflows/config-semantic-release/SKILL.md` 
### 1. Installation

> Goal: Install semantic-release in the project

1. Check `package.json` and the repository URL
2. Install with `bun add -D semantic-release`
3. Install additional plugins when needed, e.g. `bun add -D @semantic-release/changelog @semantic-release/git`
4. See the plugin list in 

### 2. Configuration

> Goal: Set the release config per the project needs

1. Create `.releaserc`, `release.config.cjs`, or a `release` field in `package.json`
2. Define `branches`, `tagFormat`, `plugins`
3. Set plugin options such as `changelogFile`, `assets`
4. Verify the authentication tokens (`GITHUB_TOKEN`, `NPM_TOKEN`)
5. See the config options in 

### 3. Local Dry Run

> Goal: Test the release without publishing for real

1. Run `bunx semantic-release --dry-run`
2. Check the version that would be produced and the release notes
3. Fix the conventional commits if the version is not as expected
4. Use `--debug` when you need verbose output

### 4. CI Integration

> Goal: Run semantic-release in CI/CD

1. Create a GitHub Actions workflow for verify and release
2. Set permissions `contents: write`, `pull-requests: write`, `id-token: write`
3. Run `bunx semantic-release` in the release job after tests pass
4. Use trusted publishing (OIDC) for npm when possible
5. See the CI example in 

### 5. Validate and Monitor

> Goal: Verify the release works correctly

1. Check the version bump, git tag, GitHub release, and npm package
2. Check the changelog was updated
3. Check that the publish is not duplicated
4. Run `/follow-release` to follow the release process

## Rules

### 1. Commits

- Use conventional commits for every commit
- Check the commit history before a release
- Use `feat`, `fix`, `BREAKING CHANGE` correctly

### 2. Configuration

- Use a clear `release.config.cjs` or `.releaserc`
- Never hard-code tokens or secrets
- Declare the branches allowed to release

### 3. CI/CD

- Run the release in CI only, except local dry runs
- Use `dry-run` to validate before publishing
- Set the permissions correctly

### 4. Publishing

- Use trusted publishing when possible
- Check that the package passes tests and lint before publishing
- Never publish from a branch that is not allowed

- Use /follow-tool-github-actions if needed (tool semantic release)
- Use /follow-tool-changesets if needed
- Use /follow-tool-git if needed
- Use /follow-test if needed
- Use /fix if needed (e.g. the release failed from config or commits)

## References

- [CLI reference](references/cli.md)

- Use /run-release if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Version management is fully automated
- The changelog is generated correctly
- GitHub release and npm publish work
- The release process is safe and reproducible

