---
name: "changelog-patterns"
description: "Changelog conventions: Keep a Changelog principles, category order, entry writing and grammar rules, the SemVer relationship, the Unreleased section, and comparison links. Use when writing or reviewing changelog entries."
---

# Changelog Patterns

> Standards, conventions, and best practices for maintaining project changelogs.

## Knowledge Base

### Keep a Changelog Principles

1. Changelogs are for **humans**, not machines.
2. There should be an entry for every **single version**.
3. The same types of changes should be **grouped**.
4. Versions and sections should be **linkable**.
5. The latest version comes **first**.
6. The **release date** of each version is displayed (ISO 8601: YYYY-MM-DD).
7. State whether you follow **Semantic Versioning**.

### Change Categories (in order)

| Category | When to Use | Example |
|----------|-------------|---------|
| **Added** | New features | "Added dark mode support" |
| **Changed** | Behavior changes to existing features | "Changed default pagination to 25 items" |
| **Deprecated** | Features that will be removed | "Deprecated XML response format" |
| **Removed** | Features that were removed | "Removed legacy v1 API endpoints" |
| **Fixed** | Bug fixes | "Fixed crash when uploading files over 10MB" |
| **Security** | Vulnerability patches | "Updated lodash to fix prototype pollution" |

### Entry Writing Guidelines

**Good entries:**
- "Added `--dry-run` flag to deploy command for previewing changes without applying them"
- "Fixed authentication failure when session token contains special characters (#234)"
- "Changed minimum supported Python version from 3.8 to 3.10"

**Bad entries:**
- "Updated dependencies" (what dependencies? why?)
- "Bug fixes" (which bugs?)
- "Fixed #234" (what was #234?)
- "Misc improvements" (what improved?)

### Entry Grammar Rules

- Start with a past-tense verb: Added, Changed, Fixed, Removed, Deprecated
- End with a PR or issue reference in parentheses when available
- One line per change, no multi-line entries
- No trailing periods (the entry is a title, not a sentence)
- Use backticks for code references: "Added `--verbose` flag"

### SemVer Relationship

| Change Type | Version Bump | Example |
|------------|-------------|---------|
| Breaking change | Major (X.0.0) | Removed deprecated endpoints |
| New feature (backward compatible) | Minor (0.X.0) | Added search endpoint |
| Bug fix (backward compatible) | Patch (0.0.X) | Fixed pagination offset |
| Security fix | Patch (0.0.X) | Patched XSS vulnerability |
| Deprecation notice | Minor (0.X.0) | Deprecated old auth flow |

### The Unreleased Section

Always maintain an `## [Unreleased]` section at the top of CHANGELOG.md. This is where changes accumulate between releases. When cutting a release:

1. Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`
2. Add a new empty `## [Unreleased]` above it
3. Update the comparison links at the bottom

### Comparison Links

Every version heading should be a link to the diff between that version and the previous one:

```markdown
[Unreleased]: https://github.com/owner/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/owner/repo/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/owner/repo/releases/tag/v1.1.0
```

The oldest version links to its release tag (no previous version to compare to).

## Patterns

1. **One Entry Per User-Visible Change**: If three commits implement one feature, that is one changelog entry.
2. **Breaking Changes Front and Center**: Mark breaking changes with bold or a dedicated subsection.
3. **Contributor Credit**: "@username" references for external contributors.
4. **Migration Notes Inline**: For breaking changes, include a brief migration hint in the entry.
5. **Release Cadence Transparency**: If you follow a release schedule, note it in the changelog header.

## Anti-Patterns

1. **Git log dump**: Copying commit messages verbatim into the changelog. Commits are for developers; changelogs are for users.
2. **Category confusion**: Listing a bug fix under "Changed" or a new feature under "Fixed."
3. **Missing versions**: Skipping changelog entries for patch releases. Every version needs an entry.
4. **Stale Unreleased**: An Unreleased section with months of accumulated changes. Release or document why.
5. **Internal-only entries**: "Refactored auth module" in the changelog. Users do not care about internal refactors unless behavior changed.
6. **No links**: Entries without PR/issue references. Every entry should be traceable.

## References

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Release Please](https://github.com/googleapis/release-please)
- [Changesets](https://github.com/changesets/changesets)
