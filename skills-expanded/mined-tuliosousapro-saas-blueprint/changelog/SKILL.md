---
name: changelog
description: Generates and maintains changelogs following Keep a Changelog format. Use when updating release notes, finishing tasks, or tagging versions. For version bumps, see semantic-versioning.
---

# Changelog Skill

## When to Use

- After completing a sprint or shipping a feature.
- Before tagging a release or pushing to main.
- When the user asks "what changed?" or "update the changelog".

## Reference

[Keep a Changelog v1.1.0](https://keepachangelog.com/en/1.1.0/)

## Instructions

### 1. Locate or Create CHANGELOG.md

- Check project root for `CHANGELOG.md`.
- If missing, create it with the header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

### 2. Gather Changes

Scan recent work using:

- `git log --oneline` since last tagged version.
- `tasks/todo.md` completed items.
- User description of what was shipped.

### 3. Categorize Changes

Every change goes into exactly one category:

| Category | When to Use |
| :--- | :--- |
| **Added** | New features, new files, new capabilities |
| **Changed** | Modifications to existing functionality |
| **Deprecated** | Features that will be removed in future versions |
| **Removed** | Features that were removed |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability patches |

### 4. Determine New Version

- **Automatically invoke the `semantic-versioning` skill.**
- Use the categorized changes to determine if the next version should be Major, Minor, or Patch.
- Ensure the version is updated in both `CHANGELOG.md` and `.github/repository-metadata.json`.

### 5. Write Entry

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Brief description of what was added

### Changed
- Brief description of what changed

### Fixed
- Brief description of what was fixed
```

### 6. Rules

- Most recent version at the top.
- Always include the date in ISO format (YYYY-MM-DD).
- One line per change, starting with a verb.
- Group related changes under the same category.
- Keep an `[Unreleased]` section at the top for ongoing work.
- Never delete old entries.
- **Synchronization**: Always ensure the version number matches between `CHANGELOG.md` and `.github/repository-metadata.json`.

## Quality Gates

- Every entry has a date.
- No empty categories (remove the heading if nothing to list).
- Entries are human-readable (not git commit hashes).
- **Version Integrity**: The new version strictly follows SemVer logic and is synchronized across the workspace.
