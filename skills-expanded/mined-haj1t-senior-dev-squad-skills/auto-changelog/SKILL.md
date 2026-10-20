---
name: auto-changelog
description: "Commit analysis, change categorization, breaking change detection, semver recommendation, CHANGELOG.md. Use when generating or updating a project changelog."
---

# Auto Changelog

## Overview

Generates CHANGELOG.md automatically from commit history. It categorizes changes using the Conventional Commits standard (`feat:`, `fix:`, `chore:`, `docs:`, etc.), detects breaking changes, recommends semantic versioning (SemVer) increments, and produces human-readable changelogs in the keepachangelog.com format.

**Core principle:** THE CHANGELOG IS AS IMPORTANT AS THE CODE. What each release changes must be clear, traceable, and meaningful to the user.

## The Iron Law

```
THE CHANGELOG MUST BE UPDATED BEFORE EVERY RELEASE. AUTOMATED CHANGELOGS ARE ALWAYS MORE RELIABLE THAN MANUAL ONES.
```

## When to Use

**Use this when:**
- You need to generate a changelog before a release.
- Commit history is written in the Conventional Commits format.
- You want to automatically determine the next version number (major/minor/patch).
- You need to prepare release notes for users.

**Use this ESPECIALLY when:**
- You are working in a fast-paced release cycle (daily/weekly releases).
- You want to generate changelogs automatically within a CI pipeline.
- There is a high risk of missing breaking changes.

**Don't skip when:**
- "There is only one commit" — changelogs apply to projects of all sizes.
- "Commit messages are messy" — analyze messy commits and extract a structured changelog regardless.

## Workflow

Work through the six phases in order. Each gate must be confirmed before proceeding.

**Phase 1 — Commit history analysis.** Determine the range (first changelog vs. since last tag vs. specific range), parse commits by Conventional Commits type, and extract scope and breaking-change metadata. See [REFERENCE.md](REFERENCE.md) for the full commit-type table, scope/breaking-change syntax, and git log commands.

**Phase 2 — Breaking change detection.** Scan for explicit `!` modifier commits and implicit breaking changes (API endpoints, DB schema, dependency majors, config format, public signatures). Prepare migration notes for each. See [REFERENCE.md](REFERENCE.md) for detection commands and implicit-change checklist.

**Phase 3 — Change categorization.** Sort commits into Added / Fixed / Changed / Deprecated / Removed / Security / Infrastructure, group by scope, and order chronologically. See [REFERENCE.md](REFERENCE.md) for the category-to-commit-type mapping and grouping shell commands.

**Phase 4 — Version bump recommendation.** Apply SemVer rules (breaking → major, feat → minor, fix/perf → patch, rest → no bump), read the current version, and calculate the new version. See [REFERENCE.md](REFERENCE.md) for the full SemVer rules table, version-source commands, and worked examples.

**Phase 5 — CHANGELOG.md generation.** Write or prepend the release section using the keepachangelog.com format (reverse chronological, `## [version] - YYYY-MM-DD`, Unreleased section, comparison links). See [REFERENCE.md](REFERENCE.md) for the full CHANGELOG.md template.

**Phase 6 — Release notes generation.** Write user-oriented notes (features, fixes, breaking changes with migration guide) ordered by importance, with PR/issue links. See [REFERENCE.md](REFERENCE.md) for the release notes template and language guidelines.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Commit messages are obvious enough, no need to parse them" — Always parse systematically, manual parsing misses edge cases.
- "It only contains fixes, so a patch bump is fine" — Breaking changes can be implicit, check the file diff.
- "I will write the changelog manually" — Automated changelogs are more accurate and comprehensive.
- "Scope information isn't important" — Scope is the key element that makes changelogs readable.
- "Release notes aren't necessary, the changelog is enough" — Release notes are for users, changelogs are for developers.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You missed a breaking change" — Phase 2 was skipped, perform an implicit breaking change check.
- "This commit is a fix, not a feature" — Parsing error occurred, check conventional commit typing regex.
- "The changelog format is wrong, not proper markdown" — keepachangelog.com format was violated, return to Phase 5.
- "Version recommendation is wrong, should be major instead of minor" — A breaking change was missed, return to Phase 2 and Phase 4.
- "Incorrect date format" — Use ISO 8601 format (YYYY-MM-DD), return to Phase 5.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Commit messages are messy and not in conventional commits format" | They can still be categorized using regex and pattern matching; some structure is better than none. |
| "There are no breaking changes, only fixes" | Unintentional changes can still cause breaking outcomes — audit the diffs. |
| "Creating a CHANGELOG.md is a waste of time" | A clean changelog is crucial for user adoption and confidence — it is a high-value time investment. |
| "I'll bump the version manually" | Manual versioning leads to inconsistency and is highly prone to human error. |
| "Release notes are only for major releases" | Every release (even patch releases) deserves notes — users want to know what changed. |

## Related Skills

- **devops-release-engineer** — Automates changelogs and release steps in the CI pipeline.
- **pr-babysitter** — Triggers changelog updates post-PR merges.
- **ship-readiness-checklist** — Evaluates release-readiness metrics.
- **code-reviewer** — Reviews commit messages for conventional standard compliance.

## Verification

Before marking complete:

- [ ] All commits have been successfully parsed according to the Conventional Commits specification.
- [ ] Commits are categorized accurately (Added/Fixed/Changed/Removed etc.).
- [ ] Breaking changes have been detected and migration paths documented.
- [ ] Changes are grouped by scope.
- [ ] Version bump recommendation is correctly calculated (major/minor/patch).
- [ ] CHANGELOG.md is correctly structured using keepachangelog.com guidelines.
- [ ] Release notes are user-friendly and clear.
- [ ] Comparison links at the bottom are accurate and active.
- [ ] Dates match the YYYY-MM-DD format.
- [ ] CHANGELOG.md changes have been written to the target file.
