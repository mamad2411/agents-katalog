---
name: releasing
description: >
  Automate the full release workflow: version bumping (major/minor/patch), changelog generation,
  git tagging, pushing, and GitHub release creation. Handles semver across Node.js, Python, Rust,
  Go, and generic projects. Enforces mandatory confirmations before irreversible actions (push, release).
  USE WHEN: user says "release", "bump version", "cut a release", "tag and release", "/releasing",
  or asks to prepare a new version of their project.
category: deployment
---

# Releasing

Automate version bumps, changelog, git tags, and GitHub releases. Stop gates enforce confirmation before every irreversible action.

## Workflow

1. Detect ecosystem and current version
2. Confirm bump type with user
3. Execute release pipeline

## Step 1: Pre-flight Checks

Run all checks. Stop and report on any failure.

```bash
# Must be in a git repo
git rev-parse --is-inside-work-tree

# Must have clean working tree (no uncommitted changes)
git status --porcelain

# Must be on a releasable branch (main, master, or release/*)
git branch --show-current

# Must have a remote configured
git remote -v

# Check if gh CLI is available (needed for GitHub release)
command -v gh
```

**Dirty tree:** Stop. User must commit or stash first.
**Wrong branch:** Stop. Report branch, ask to continue.
**No gh CLI:** Warn, skip GitHub release step.

## Step 2: Detect Version

Scan version files in priority order:

| Priority | File | Ecosystem | Pattern |
|----------|------|-----------|---------|
| 1 | `package.json` | Node.js | `"version": "X.Y.Z"` |
| 2 | `pyproject.toml` | Python | `version = "X.Y.Z"` |
| 3 | `Cargo.toml` | Rust | `version = "X.Y.Z"` |
| 4 | `setup.cfg` | Python (legacy) | `version = X.Y.Z` |
| 5 | `VERSION` | Generic | Plain text `X.Y.Z` |
| 6 | Latest git tag | Any | `vX.Y.Z` or `X.Y.Z` |

For full detection patterns and edge cases, load `references/version-detection.md`.

**Report to user:** "Current version: **X.Y.Z** (detected from `<file>`)"

## Step 3: Determine Bump Type

Use user-specified type if provided. Otherwise:

**Stop Condition (Mandatory):** Ask user to choose bump type.
- **patch** (X.Y.Z -> X.Y.Z+1) - Bug fixes, small changes
- **minor** (X.Y.Z -> X.Y+1.0) - New features, backward compatible
- **major** (X.Y.Z -> X+1.0.0) - Breaking changes

Calculate and show the new version before proceeding.

## Step 4: Update Version File

Apply the version bump to the detected file:

```bash
# Node.js - use npm version without git tag (we handle tagging ourselves)
npm version <patch|minor|major> --no-git-tag-version

# Python (pyproject.toml) - sed replacement
# Rust (Cargo.toml) - sed replacement
# Generic - direct file write
```

**Important:** Only update the version file. Do NOT run `npm version` with default behavior (it creates its own tag).

Also update `package-lock.json` if it exists (Node.js):
```bash
[ -f package-lock.json ] && npm install --package-lock-only
```

## Step 5: Update Changelog

Check if `CHANGELOG.md` exists. If not, create it.

Generate changelog entries from git log since last tag:

```bash
# Get last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# Get commits since last tag (or all commits if no tag)
if [ -n "$LAST_TAG" ]; then
  git log "$LAST_TAG"..HEAD --pretty=format:"- %s (%h)" --no-merges
else
  git log --pretty=format:"- %s (%h)" --no-merges
fi
```

Prepend new section to CHANGELOG.md in this format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Changes
- commit message 1 (abc1234)
- commit message 2 (def5678)
```

**Categorize commits if conventional commits are used:**
- `feat:` -> "Added"
- `fix:` -> "Fixed"
- `docs:` -> "Documentation"
- `refactor:` -> "Changed"
- `BREAKING CHANGE:` -> "Breaking Changes" (at top)
- Other -> "Changes"

## Step 6: Commit Version Bump

```bash
git add -A
git commit -m "chore(release): v<NEW_VERSION>"
```

Show the commit to user for awareness.

## Step 7: Create Git Tag

```bash
git tag -a "v<NEW_VERSION>" -m "Release v<NEW_VERSION>"
```

## Step 8: Push (with confirmation)

**Stop Condition (Mandatory):** This is irreversible. Ask user before pushing.

Show exactly what will be pushed:
- Branch: `<branch_name>`
- Remote: `<remote_name>` (`<remote_url>`)
- Commits: list new commits
- Tag: `v<NEW_VERSION>`

Only after user confirms:

```bash
git push origin <branch_name>
git push origin "v<NEW_VERSION>"
```

## Step 9: Create GitHub Release (with confirmation)

Skip if `gh` CLI is not available.

**Stop Condition (Mandatory):** Ask user before creating public release.

```bash
# Extract changelog for this version to use as release notes
gh release create "v<NEW_VERSION>" \
  --title "v<NEW_VERSION>" \
  --notes "<changelog_for_this_version>" \
  --latest
```

For pre-release versions (contains `-alpha`, `-beta`, `-rc`):
```bash
gh release create "v<NEW_VERSION>" \
  --title "v<NEW_VERSION>" \
  --notes "<changelog>" \
  --prerelease
```

## Step 10: Post-release Verification

Verify everything succeeded:

```bash
# Verify tag exists on remote
git ls-remote --tags origin "v<NEW_VERSION>"

# Verify GitHub release (if created)
gh release view "v<NEW_VERSION>" --json tagName,isDraft,isPrerelease
```

Report final summary:
```
Release v<NEW_VERSION> complete:
  Version file: <file> updated
  Changelog: CHANGELOG.md updated
  Tag: v<NEW_VERSION> created and pushed
  GitHub Release: published (or: skipped)
```

## Quick Reference: Common Invocations

| User says | Bump type | Notes |
|-----------|-----------|-------|
| "release patch" | patch | Fastest path |
| "bump minor" | minor | New feature release |
| "major release" | major | Breaking change |
| "release" / "cut a release" | ask user | Must confirm type |
| "release 2.0.0" | explicit | Use exact version given |
| "prerelease" / "release beta" | prepatch with `-beta.1` | Mark as prerelease |

## Error Recovery

| Error | Recovery |
|-------|----------|
| Push rejected (behind remote) | `git pull --rebase` then retry push |
| Tag already exists | Ask user: force-update tag or use different version? |
| gh auth failed | Run `gh auth login` and retry |
| Version file not found | Ask user which file contains the version |
| Merge conflict in changelog | Open file for manual resolution, then continue |
