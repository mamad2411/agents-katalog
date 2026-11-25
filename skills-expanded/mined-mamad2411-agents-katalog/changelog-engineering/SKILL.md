---
name: changelog-engineering
description: Maintain changelogs that serve users. Use when writing or
  automating release notes.
metadata:
  tags: changelog, engineering
---

# Changelog Engineering

## Use this skill when
- Writing user-facing release notes
- Automating changelog generation
- Categorizing changes

## Do not use this skill when
- Full internal commit lists
- Marketing copy

## Instructions
1. Group by relevance: Breaking, Added, Changed, Fixed.
2. Lead with the user impact; link issues for detail.
3. Automate from conventional commits; hand-tune major releases.
4. Keep one un-released/beta section current.
5. Mention upgrade and migration steps for breaking changes.
6. Date versions and keep semantic versioning consistent.

## Checklist
- Breaking changes called out
- User-impact phrasing
- Automation wired if feasible

## Output Format
- Changelog structure | automation | release process

## Common Mistakes
- Dumping raw commit titles
- Hiding breaking changes in “misc”
- Version bump without changelog
