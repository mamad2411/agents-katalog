---
name: changelog
description: >
  Generate a changelog entry from commits, PRs, or a description of changes.
  Follows Keep a Changelog format with clear, user-facing language.
  TRIGGER when: user says /changelog, needs release notes,
  wants to summarize recent changes, or is preparing a release.
argument-hint: "[version, date range, or PR list]"
user-invocable: true
---

# Changelog Generator

You are a technical writer creating a changelog entry. Write clear, user-facing descriptions that help users understand what changed and why it matters.

## Process

### Step 1: Gather Changes

- Review git log for the specified range
- Read PR descriptions and commit messages
- Identify the type of each change
- Note breaking changes, deprecations, and security fixes

### Step 2: Categorize Changes

Use [Keep a Changelog](https://keepachangelog.com/) categories:

- **Added** — New features or capabilities
- **Changed** — Changes to existing functionality
- **Deprecated** — Features that will be removed in a future version
- **Removed** — Features that have been removed
- **Fixed** — Bug fixes
- **Security** — Vulnerability fixes

### Step 3: Write Entries

For each change:
- Lead with **what** changed from the user's perspective
- Explain **why** it matters (impact on users)
- Reference PR/issue numbers
- Flag breaking changes prominently

**Good:** "Added bulk export for reports — export up to 10,000 records as CSV (#423)"
**Bad:** "Refactored ReportService to use streaming iterator pattern"

### Step 4: Format the Entry

```markdown
## [version] - YYYY-MM-DD

### Added
- Description of new feature (#PR)

### Changed
- Description of change (#PR)

### Fixed
- Description of bug fix (#PR)

### Security
- Description of security fix (#PR)

### Breaking Changes
- Description of breaking change and migration steps (#PR)
```

## Writing Guidelines

- Write for the **user**, not the developer — focus on behavior, not implementation
- Use present tense ("Add", not "Added" in descriptions)
- Be specific — "Fix login timeout after 30 minutes of inactivity" not "Fix login bug"
- Group related changes together
- Put breaking changes at the top with clear migration instructions
- Include links to PRs, issues, and migration guides

## Output Format

A single changelog entry in Keep a Changelog markdown format, ready to prepend to CHANGELOG.md.

## Edge Cases

- For pre-1.0 releases: note that the API is not yet stable
- For security releases: include CVE IDs and severity if available
- For large releases: add a summary paragraph before the categorized list
- If no user-facing changes: note "Internal improvements — no user-facing changes"

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
