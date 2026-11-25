---
name: skill-lifecycle-management
description: Manage skill versioning, freshness tracking, deprecation, changelog generation, and maintenance workflows for skill repository maintainers.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: governance
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global]
priority: medium
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
license: MIT
---

# Skill Lifecycle Management

## When to Use

- Publishing a new skill to a registry
- Updating a skill after regulatory or API changes
- Deciding whether to deprecate or archive a skill
- Setting up freshness monitoring
- Reviewing skill quality over time

## Lifecycle Stages

```
Draft → Review → Published → Maintained → Stale → Deprecated → Archived
```

| Stage | Duration | Actions |
|-------|----------|---------|
| Draft | Days | Write, test locally, self-review |
| Review | Days | PR review, CI lint, security scan |
| Published | Indefinite | Available for installation |
| Maintained | Ongoing | Respond to issues, update for changes |
| Stale | >90 days no update | Flag [STALE], prioritize review |
| Deprecated | Announced | Mark deprecated, point to replacement |
| Archived | Final | Read-only, no longer maintained |

## Versioning (SemVer)

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (renamed fields, removed sections, new required dependencies)
MINOR: New content (added steps, new references, expanded coverage)
PATCH: Fixes (typos, URL updates, date corrections)
```

Examples:
- `1.0.0 → 1.0.1`: Fixed broken URL in references
- `1.0.1 → 1.1.0`: Added new section on DORA RTS
- `1.1.0 → 2.0.0`: Restructured skill, changed frontmatter fields

## Freshness Rules

| Age | Status | Action |
|-----|--------|--------|
| < 30 days | Fresh | No action |
| 30-60 days | OK | Review if regulatory |
| 60-90 days | Review needed | Check update_sources |
| > 90 days | [STALE] | Mandatory review before use |

**Regulatory skills**: Review whenever source legislation changes, regardless of age.

## Changelog Format

```markdown
## [1.1.0] - 2026-04-17
### Added
- Section on DORA RTS Level 2 requirements
- Reference to new EDPB DPIA template (April 2026)

### Changed
- Updated e-invoicing timeline (September 2026 confirmed)

### Fixed
- Corrected NIS2 transposition deadline
```

## Deprecation Process

1. **Announce**: Add `deprecated: true` to frontmatter + reason
2. **Point**: Reference replacement skill in description
3. **Grace period**: Keep available for 90 days
4. **Archive**: Move to `skills/_archived/` directory

## Quality Metrics

| Metric | Good | Watch | Bad |
|--------|------|-------|-----|
| Last updated | < 60 days | 60-90 days | > 90 days |
| Open issues | 0 | 1-2 | 3+ |
| Token size | < 1500 | 1500-3000 | > 3000 |
| Broken URLs | 0 | — | Any |
| Missing fields | 0 | — | Any |

## What This Skill Does NOT Do

- Does not auto-update skills (flags for human review)
- Does not manage skill registry publishing
- Does not enforce versioning (guides the process)
- Does not handle skill discovery (see `find-skills`)
