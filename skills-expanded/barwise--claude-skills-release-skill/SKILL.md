---
name: release
description: Use when cutting a barwise release - bumping the single monorepo version, tagging, and creating the GitHub release that builds the downloadable artifacts. Carries the bump-sequence gotchas (workspace dependency refs, SERVER_VERSION sync, tutorial regeneration) that make a naive npm version fail CI.
---

# Cutting a Barwise Release

The project uses a single version number across all packages, tracked
by git tags on the main branch. Versions follow semver. Changes
accumulate on main; a release is an intentional act, not automatic.

1. **Develop** -- merge PRs to main. CI runs build + test + lint.
2. **Decide to release** -- when a meaningful set of changes has landed.
3. **Bump versions** -- update package.json files and tag (below).
4. **Create a GitHub release** -- triggers the artifact build workflow.

To review what changed since the last release:

```bash
git log --oneline v1.2.0..HEAD
```

## Bump versions and tag

All commands run from `barwise/`. The `--no-workspaces-update` flag
prevents npm from resolving workspace dependencies against the public
registry (these packages are not published). Use `patch` for bug fixes
and small improvements, `minor` for new features or format support:

```bash
npm version patch --workspaces --include-workspace-root \
  --no-git-tag-version --no-workspaces-update
VER=$(node -p "require('./package.json').version")
git add -A && git commit -m "bump to $VER"
git tag -a "v$VER" -m "v$VER: brief description"
git push origin main --tags
```

Three gotchas, each of which fails CI if skipped:

- `--no-workspaces-update` leaves each package's internal `@barwise/*`
  dependency refs at the previous version. Bump those to the new
  version too (a one-pass rewrite of the `@barwise/*` entries in every
  `packages/*/package.json`), then run `npm install` to refresh the
  lockfile -- otherwise `npm ci` fails trying to fetch the old version
  from the registry.
- Bump the pinned `SERVER_VERSION` in `packages/mcp/src/server.ts`; a
  version-sync test asserts it matches package.json.
- Run `npm run regen:tutorial`: the committed tutorial Markdown stamps
  the tool version, and its drift test fails until regenerated.

The `barwise-vscode` extension has its own version (visible in the VS
Code marketplace) which may differ from the library packages. The
`npm version` command bumps each package relative to its current
version, so they stay in sync if they start in sync.

## Create a GitHub release

```bash
gh release create v1.3.0 --title "v1.3.0" --generate-notes
```

`--generate-notes` builds the changelog from merged PRs since the last
tag. (Remote sessions have no `gh` CLI; use the GitHub MCP release
tools instead.) The `release.yml` workflow then builds and attaches
the artifacts: the VS Code extension (`.vsix`), the standalone CLI
bundle (`barwise-cli-<ver>.cjs`), the MCP server bundle
(`barwise-mcp-<ver>.cjs`), and a `SHA256SUMS` file. The same workflow
refreshes a rolling `edge` pre-release on every push to `main`, so a
current download always exists between tagged releases.

## Minor releases: run the Phase A architecture review

A minor release is the cadence point for the deep assessment in
`barwise/docs/specs/archive/architecture-analysis.spec.md`: walk the scenario
catalog in `docs/architecture-scenarios.md`, refresh the reflexion and
hotspot snapshot via `npm run arch:triage -- --base <last-release-tag>`
(so the ranking covers only the changes since that release), and
commit a new dated `docs/REPO_REVIEW-<YYYY-MM-DD>.md`. The continuous
fitness functions (`npm run depcruise`, `npm run purity`) guard the
structural pillars between releases; this review covers the judgment
calls they cannot.
