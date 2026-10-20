---
name: dev-release
description: Release preparation — changelog generation, version bump, tag creation. Generic version (not project-specific). For EvoNexus releases, use custom-release instead.
---

# Dev Release

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Generic release preparation: changelog generation from git log, version bump, tag creation. **For EvoNexus-specific releases, use `custom-release`** (the existing skill that handles git-flow develop→main).

## Use When
- Releasing a non-EvoNexus project (Evolution API, Evo AI, Evo Go, etc.)
- Generic semver bump on a library you're maintaining

## Do Not Use When
- Releasing EvoNexus itself → use `custom-release` instead
- Project has its own custom release process → follow that

## Workflow

### Phase 1 — Pre-flight
- Verify on the right branch (not `main`/`master` directly)
- Verify clean working tree (no uncommitted changes)
- Verify CI is green on the target commit
- Verify tests pass locally (`dev-verify`)

### Phase 2 — Determine version
- Read current version from manifest (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`)
- Determine bump type: major / minor / patch (semver)
- Confirm with user

### Phase 3 — Generate changelog
- Read commits since last tag: `git log {last-tag}..HEAD --oneline`
- Group by type (feat / fix / docs / etc.) if conventional commits
- Save to `CHANGELOG.md` with new version section

### Phase 4 — Bump version
- Update manifest file
- Update any version references in docs

### Phase 5 — Commit and tag
- `git commit -m "chore(release): vX.Y.Z"`
- `git tag vX.Y.Z`
- `git push origin vX.Y.Z` (after user confirmation)

### Phase 6 — Verify
- `@oath-verifier` confirms the release commit and tag are correct

## Output
Save release notes to `workspace/development/research/[C]release-{version}-{date}.md`.

## Pairs With
- `@flow-git` (commits and tags)
- `@oath-verifier` (verification)
- `@quill-writer` (changelog formatting)
- `dev-verify` (pre-flight)

## EvoNexus-Specific Note

EvoNexus has its own release skill (`custom-release`) that handles the git-flow develop→main workflow with EvoNexus-specific gates (CHANGELOG entry, version sync across files, GitHub release creation). Use `custom-release` for EvoNexus releases. Use `dev-release` only for projects in `workspace/projects/` that have their own release lifecycle.
