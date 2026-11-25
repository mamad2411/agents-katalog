---
name: bump
description: Bump version, update CHANGELOG.md and README.md, then tag and release on GitHub
argument-hint: "<version>"
---

Bump the project version, update documentation, create a git tag, and publish a GitHub release.

<execution>
## Prerequisites

- Version argument is REQUIRED (e.g., `$bump 0.4.0`)
- Should be on `main` branch (warn if not, but proceed)
- `gh` CLI must be authenticated
- Dirty working tree is allowed — uncommitted changes will be included in the release commit

## Phase 1: Validate

1. **Check version argument**:
   - If no version provided, STOP and ask: "Please provide a version (e.g., `$bump 0.4.0`)"
   - Version must be valid semver (e.g., `0.4.0`, `1.0.0-beta.1`)

2. **Check git status**:

   ```bash
   git status --porcelain
   ```

   - If there are uncommitted changes, WARN the user but **proceed anyway** — these changes will be staged and included in the release commit.

3. **Check current branch**:

   ```bash
   git branch --show-current
   ```

   - Warn if not on `main` branch (but allow to proceed)

4. **Get current version**:
   ```bash
   node -p "require('./package.json').version"
   ```

## Phase 2: Extract Changelog from Git Commits

**CRITICAL**: Do NOT use placeholder text like "Version bump". Extract real changes from git commits.

1. **Get commits since last version tag**:
   ```bash
   git log v<previous_version>..HEAD --oneline --no-merges
   ```

2. **For each meaningful commit, examine changes**:
   ```bash
   git show --stat <commit_hash>
   git diff v<previous_version>..HEAD -- <key_files>
   ```

3. **Categorize changes** into Keep a Changelog format:
   - **Added**: New features, capabilities, or files
   - **Changed**: Modifications to existing behavior, enhancements, updated defaults
   - **Fixed**: Bug fixes, error corrections
   - **Removed**: Removed features or code
   - **Deprecated**: Features marked for future removal
   - **Security**: Security-related changes

4. **Write specific, detailed changelog entries**:
   - Describe WHAT changed and WHY (from user perspective)
   - Include concrete details (e.g., "timeout increased from 120s to 300s")
   - Reference specific configuration changes, default values, etc.
   - ONLY use "Version bump" if literally nothing changed (empty git diff)

## Phase 3: Update Files

### 3.1 Update package.json

Use the Edit tool to update the version field in `package.json`:

- Change `"version": "<old>"` to `"version": "<new>"`

### 3.2 Update CHANGELOG.md

Read `CHANGELOG.md` and make these changes:

1. **Find the `## [Unreleased]` section**

2. **If there are entries under [Unreleased]**:
   - Insert a new version section after `## [Unreleased]`:
     ```
     ## [<version>] - <YYYY-MM-DD>
     ```
   - Move all content from [Unreleased] to the new version section
   - Leave [Unreleased] empty (just the header)

3. **If [Unreleased] is empty**:
   - Insert a new version section with the changes extracted from git commits (Phase 2)
   - Use the categorized changelog entries from Phase 2
   - Example:
     ```
     ## [<version>] - <YYYY-MM-DD>

     ### Added
     - Feature 1 with specific details
     - Feature 2 with configuration changes

     ### Changed
     - Specific change with old → new values
     - Configuration update with details
     ```

4. **Update the version links at the bottom**:
   - Update `[Unreleased]` link: `[Unreleased]: https://github.com/GeoloeG-IsT/agents-reverse-engineer/compare/v<version>...HEAD`
   - Add new version link after [Unreleased]: `[<version>]: https://github.com/GeoloeG-IsT/agents-reverse-engineer/compare/v<previous>...v<version>`

### 3.3 Check README.md (Optional)

Scan `README.md` for any hardcoded version references that need updating:

- Badge URLs
- Installation commands with specific versions
- Only update if explicitly version-pinned (not `@latest`)

## Phase 4: Commit and Tag

1. **Stage all changes** (including any pre-existing dirty files):

   ```bash
   git add -A
   ```

2. **Create commit**:

   ```bash
   git commit -m "$(cat <<'EOF'
   chore: release v<version>
   EOF
   )"
   ```

3. **Create annotated tag**:
   ```bash
   git tag -a v<version> -m "Release v<version>"
   ```

## Phase 5: Push and Release

1. **Push commit and tag**:

   ```bash
   git push && git push --tags
   ```

2. **Create GitHub release**:
   Extract the changelog section for this version and use it as release notes:
   ```bash
   gh release create v<version> --title "v<version>" --notes "$(cat <<'EOF'
   <changelog section for this version>
   EOF
   )"
   ```

## Phase 6: Report

Summarize what was done:

- Version bumped: `<old>` → `<new>`
- Files updated: package.json, CHANGELOG.md, (README.md if changed)
- Git tag: `v<version>`
- GitHub release: link to the release

**Remind user**: The GitHub Actions workflow will automatically publish to npm when the release is created.
</execution>
