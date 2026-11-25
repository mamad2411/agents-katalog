---
name: release-notes
description: Generates release notes from commits since the last tag
argument-hint: [version]
user-invocable: true
allowed-tools: Bash(git *)
effort: low
---

## Generate Release Notes

Target version: **$1** (or infer from package.json if not provided)

```bash
git tag --sort=-creatordate | head -5
git log $(git describe --tags --abbrev=0)..HEAD --oneline --no-merges
```

## Format

Group commits by type and write release notes in this structure:

```markdown
## [version] - YYYY-MM-DD

### New Features
- ...

### Bug Fixes
- ...

### Performance
- ...

### Breaking Changes
- ...

### Internal
- ...
```

Rules:
- Skip chore/style/ci commits from user-facing sections
- Rewrite commit messages as user-friendly sentences (not "fix: null check" → "Fixed crash when user data is missing")
- If a commit references an issue/PR, link it: `([#123](...))`
- BREAKING CHANGE footer entries go to Breaking Changes section

Output the final markdown, ready to paste into CHANGELOG.md or a GitHub release.
