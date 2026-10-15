---
name: git-versioning
description: Use when working with Git — branching strategies, conventional commits, semantic versioning, changelog management, and release workflows. Applies to all CDB projects.
version: 0.1.0
---

# Git & Versioning

## Core Principles

1. **Commit Early, Commit Often** — small, focused commits that represent one logical unit of work
2. **Meaningful Messages** — future you and teammates need to understand *why* changes were made
3. **Branch for Features** — isolate work in feature branches to keep main stable
4. **Tag Releases** — use semantic versioning tags to mark release points

## Branching Strategy

```bash
# Recommended: Trunk-based with staging
main           # Production
staging        # Pre-production / integration
feature/*      # Feature branches (merge to staging)
hotfix/*       # Emergency fixes (merge to main + staging)

# Feature workflow
git checkout staging && git pull origin staging
git checkout -b feature/my-feature

git commit -m "feat(scope): add thing"
git push origin feature/my-feature
# Open PR: feature/my-feature → staging
# After review + merge, PR: staging → main

# Hotfix workflow
git checkout main && git pull origin main
git checkout -b hotfix/critical-bug
git commit -m "fix(auth): correct redirect after login"
# PRs to both main and staging
```

## Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change, no new feature or fix |
| `test` | Adding/updating tests |
| `chore` | Maintenance, dependencies |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |

### Examples

```bash
# Feature
git commit -m "feat(auth): add password reset flow

Users can now reset password via email link.
Link expires after 1 hour.

Closes #42"

# Bug fix
git commit -m "fix(window): prevent dragging outside viewport

Fixes #567"

# Breaking change
git commit -m "feat(api)!: change upload API to streaming

BREAKING CHANGE: uploadFile() now expects a stream, not a blob.

Before: uploadFile({ name, content })
After:  uploadFileStream(name, stream)"
```

### DO / DON'T

```bash
# DON'T
git commit -m "fix stuff"
git commit -m "wip"
git commit -m "update files"
git commit -m "fixed the thing where the window resize didn't work properly"

# DO
git commit -m "fix(window): handle resize event on unmount"
git commit -m "feat(editor): add autosave with 30s interval"
git commit -m "docs(readme): add Docker setup instructions"
```

## Semantic Versioning

```
MAJOR.MINOR.PATCH

1.4.2
├── 1 = breaking changes
├── 4 = new features (backward compatible)
└── 2 = bug fixes
```

```bash
# PATCH (1.0.0 → 1.0.1) — bug fixes
npm version patch

# MINOR (1.0.1 → 1.1.0) — new features
npm version minor

# MAJOR (1.1.0 → 2.0.0) — breaking changes
npm version major
```

## Changelog (CHANGELOG.md)

```markdown
# Changelog

## [Unreleased]

### Added
- New feature in progress

## [1.1.0] - 2026-01-15

### Added
- Feature A
- Feature B

### Fixed
- Bug fix C (#567)

### Security
- Updated vulnerable dependency

## [1.0.0] - 2026-01-01

### Added
- Initial release
```

## Release Workflow

```bash
# 1. Ensure on main, up to date
git checkout main && git pull origin main

# 2. Run tests
npm test && npm run build

# 3. Bump version + update changelog
npm version minor  # updates package.json + creates git tag

# 4. Push with tags
git push origin main --tags

# 5. Create GitHub release from tag
```

## Best Practices

**DO:**
- Use conventional commits for all commits
- Reference issues: `Closes #123`, `Fixes #456`
- Keep commits atomic — one logical change
- Rebase feature branches before merging
- Document breaking changes with migration guide
- Tag all releases

**DON'T:**
- Don't commit directly to main (use PRs)
- Don't use vague messages
- Don't mix unrelated changes in one commit
- Don't push untested code
- Don't force push to shared branches
- Don't commit secrets or .env files

## When to Use This Skill

- Starting a feature (set up branch)
- Writing commits (format + message quality)
- Preparing a release (version bump + tag)
- Reviewing a PR (commit quality check)
- Fixing a production bug (hotfix workflow)
- Breaking API changes (document migration)
