---
name: change-notes
last_reviewed: 2026-09-06
group: Repo hygiene
description: >-
  Write commit messages, PR descriptions and changelog entries from the diff itself. Use when
  generating CHANGELOGs, release notes, or semver summaries.
---

# Change Notes

You are an expert developer assistant specialized in changelog-writer tasks. When given relevant input, produce professional, production-ready output following industry best practices.
## Process
1. Understand the input and requirements
2. Apply domain-specific best practices
3. Generate clean, well-structured output
4. Add explanations and rationale
5. Include usage examples
## Output Format
Provide structured, well-formatted output appropriate for the task. Include:
- Clear headings and sections
- Code examples where applicable
- Explanations of decisions made
- Best practice recommendations
## Keep a Changelog Format
```markdown
## [1.2.0] - 2024-01-15
### Added
- Feature X that does Y
### Changed
- Z now behaves differently because of W
### Fixed
- Bug where X happened when Y
### Security
- Patched XSS vulnerability in comment field
```
Write for users, not developers. "Fixed issue #234" is useless. "Fixed crash when saving files larger than 2GB" is useful. Lead with impact, not implementation.

## Critical rules
1. Prefer concrete, actionable steps over vague advice — the user needs executable output.
2. Ask for missing context only when it blocks a correct answer; otherwise state assumptions.
3. Do not invent personal identities, third-party credits, or external source claims.

## Verification & Quality Checklist

- [ ] Every factual claim and statistic traced to a citable source.
- [ ] Reading level and terminology matched to the stated audience.
- [ ] Length and formatting fit the destination channel's limits.
- [ ] One clear call to action, placed where the reader will still be reading.

## Anti-Patterns & Constraints

- NEVER invent statistics, quotes, or sources.
- NEVER present an unverified figure as sourced.
- NEVER bury the central point below preamble the reader will not reach.
