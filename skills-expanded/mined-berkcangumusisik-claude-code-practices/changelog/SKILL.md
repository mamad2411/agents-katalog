---
name: changelog
description: Updates CHANGELOG.md with commits since the last entry
user-invocable: true
allowed-tools: Bash(git *) Read Edit
effort: low
---

## Update CHANGELOG.md

1. Find the last version in CHANGELOG.md:
```bash
head -50 CHANGELOG.md 2>/dev/null || echo "No changelog yet"
git tag --sort=-creatordate | head -1
```

2. Get commits since last tag:
```bash
git log $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD --oneline --no-merges
```

3. Prepend a new section to CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com) format:

```markdown
## [Unreleased] - YYYY-MM-DD

### Added
### Changed
### Fixed
### Removed
### Security
```

Only include non-empty sections. Group commits intelligently.
Rewrite raw commit messages into human-readable changelog entries.
