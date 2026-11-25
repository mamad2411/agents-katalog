---
name: changelog-generator
description: |
  Generate CHANGELOG.md from git history grouped by Conventional Commit types.
  Triggers on "generate changelog", "write changelog", "release notes".
metadata:
  type: workflow
  version: "1.0.0"
  author: community
  tags: [changelog, release, git, conventional-commits]
triggers:
  - "generate changelog"
  - "write changelog"
  - "release notes"
  - "update changelog"
allowed-tools:
  - Bash
  - Read
  - Write
---

# Changelog Generator

Generate a Keep a Changelog-formatted CHANGELOG.md from git history.

## When to Use
- Preparing a release and need release notes
- User mentions "changelog", "release notes"
- Project follows Conventional Commits

## When NOT to Use
- First commit of a project (no history yet)
- Non-Conventional Commits repos (output will be poorly categorized)

## Workflow
1. Determine the version range: ask user for `from` and `to` tags/commits
2. Run `git log <from>..<to> --oneline` to get commits in range
3. Categorize commits by Conventional Commit type:
   - `feat` → Added
   - `fix` → Fixed
   - `perf` → Changed (performance)
   - `refactor` → Changed
   - `docs` → (skip for changelog, user-facing only)
   - `BREAKING CHANGE` → Changed (breaking)
4. Group by category, format as bullet list
5. Prepend to existing CHANGELOG.md or create new one
6. Add version header with date

## Output Format
```markdown
# Changelog

## [1.2.0] - 2026-05-29

### Added
- JWT refresh token rotation (#234)
- Rate limiting on login endpoint (#235)

### Fixed
- Race condition in order status update (#231)
- Memory leak in WebSocket connection handler (#228)

### Changed
- **Breaking:** Refresh token response format updated
- Improved database connection pool management
```

## Key Principles
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Human-readable descriptions, not raw commit messages
- Group by impact: Added → Fixed → Changed → Deprecated → Removed → Security
- Link to issue/PR numbers when available
- Breaking changes MUST be clearly marked

## Notes
- Skip chore/test/docs commits (not user-facing)
- If no tag exists, use the first and last commit of the range
- Confirm version number and date before writing
