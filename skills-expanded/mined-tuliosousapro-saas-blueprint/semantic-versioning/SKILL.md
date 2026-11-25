---
name: semantic-versioning
description: Manages project versioning following Semantic Versioning (SemVer) principles. Calculates increments based on changes and synchronizes version across documentation and metadata. Use when the user asks to "bump the version", "prepare a release", or when the `changelog` skill calls for a release.
---

# Semantic Versioning Skill

## Instructions

### 1. Detect Current Version

- Read the latest version from `CHANGELOG.md` (e.g., the most recent header `## [X.Y.Z]`).
- Read the version from `.github/repository-metadata.json`.
- If they differ, flag the mismatch to the user and ask which is authoritative.

### 2. Analyze Changes

Scan the changes since the last release:

- If using `changelog` skill: Look at the items under `[Unreleased]` or the new version block being prepared.
- If using `git log`: Scan for Conventional Commits types.

### 3. Determine Increment Type

Follow these priority rules:

1. **MAJOR** (X.0.0): Any "BREAKING CHANGE" footer or `!` after the type (e.g., `feat!:`).
2. **MINOR** (x.Y.0): Any `feat` commit or "Added" entry in the changelog.
3. **PATCH** (x.y.Z): Any `fix`, `perf`, `refactor` commit or "Fixed"/"Changed" entry in the changelog.
4. **No Change**: If only `docs`, `chore`, `style`, `test`, `build`, or `ci` changes are found, default to PATCH unless the user specifies otherwise.

### 4. Apply Version Update

Update the following files in a single pass:

- **CHANGELOG.md**: Rename the `## [Unreleased]` section to `## [NEW_VERSION] - CURRENT_DATE` or update the latest entry.
- **.github/repository-metadata.json**: Update the `"version"` field.

## Quality Gates

- Version follows `MAJOR.MINOR.PATCH` format.
- No regression in version number.
- All version-tracking files are synchronized.
- Date in `CHANGELOG.md` is in `YYYY-MM-DD` format.
