---
name: git-workflow
description: Use this skill for anything related to Git and version control workflows. Trigger when the developer asks for help with commit messages, PR descriptions, pull request reviews, branching strategies, changelog generation, release notes, code review etiquette, or Git conventions. Keywords: commit, PR, pull request, branch, merge, release, changelog, code review, diff, git.
---

# Git Workflow

## Commit Message Convention

Follow the **Conventional Commits** specification. This enables automated versioning, changelogs, and semantic releases.

### Format
```
type(scope): short description

[optional body — explain the WHY, not the WHAT]

[optional footer — breaking changes, issue refs]
```

### Types
| Type | When to Use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Build process, dependency updates, tooling |
| `ci` | CI/CD configuration changes |
| `style` | Formatting, whitespace (no logic change) |
| `revert` | Reverting a previous commit |

### Examples
```
feat(auth): add OAuth2 login with Google

fix(api): handle null response from payment gateway

refactor(db): extract query builder into separate module

docs(readme): update local setup instructions

chore(deps): upgrade dependencies to latest versions
```

### Rules
- Subject line: max 72 characters, imperative mood ("add" not "added")
- Body: explain WHY the change was made, not what (the diff shows what)
- Reference issue/ticket IDs in footer: `Closes #123` or `Refs US-2111704`
- If AI-assisted, note it: `Co-authored-by: GitHub Copilot`

---

## PR Description Template

Every PR should answer three questions:

```markdown
## What
Brief summary of what changed.

## Why
The business or technical reason for this change.

## How
Key implementation decisions or approach taken.

## Testing
How was this verified? (unit tests, manual testing, E2E)

## Checklist
- [ ] Tests added/updated
- [ ] No new security vulnerabilities introduced
- [ ] Documentation updated if needed
- [ ] No breaking changes (or documented if there are)
```

---

## Branching Strategy

### GitHub Flow (Recommended for most teams)
```
main
└── feature/US-1234-short-description
└── fix/bug-short-description
└── chore/update-dependencies
```
- Branch from `main`, merge back to `main` via PR
- Deploy from `main` continuously

### Git Flow (For versioned releases)
```
main          ← production
develop       ← integration
└── feature/* ← new features
└── release/* ← release prep
└── hotfix/*  ← urgent production fixes
```

### Branch Naming Convention
```
type/ticket-id-short-description

Examples:
feat/US-2111704-query-clarity-agent
fix/US-2098686-btt-ui-button-alignment
chore/update-langchain-dependencies
```

---

## Code Review Etiquette

### Feedback Categories
Tag all review comments to set expectations:

| Tag | Meaning |
|---|---|
| `BLOCKER` | Must be fixed before merge. Breaks functionality or violates standards. |
| `WARNING` | Should be fixed. Technical debt or potential issue. |
| `SUGGESTION` | Optional improvement. Worth considering but not required. |
| `QUESTION` | Asking for clarification, not requesting a change. |
| `NITPICK` | Minor style or preference. Author can decide. |

### Reviewer Mindset
- Review the code, not the person
- Explain the reason behind every BLOCKER or WARNING
- Acknowledge good work — not just problems
- Ask questions before assuming intent: "What was the reason for this approach?"
- Focus on architecture and logic issues first, style issues last (that's what linters are for)

### Author Mindset
- Keep PRs small and focused — one concern per PR
- Respond to every comment, even if just acknowledging
- Mark resolved conversations as resolved
- Don't merge until all BLOCKERs are addressed

---

## Changelog Generation

When generating a changelog from commits, group by type:

```markdown
## [1.2.0] - 2026-03-20

### Features
- feat(auth): add OAuth2 login with Google (#45)

### Bug Fixes
- fix(api): handle null response from payment gateway (#46)

### Performance
- perf(db): optimize query for large datasets (#47)
```

---

## AI Attribution in Commits

When code was AI-assisted, be transparent in the commit:
```
feat(api): generate REST endpoint scaffolding

Scaffolded with GitHub Copilot, reviewed and modified by developer.
Co-authored-by: GitHub Copilot <copilot@github.com>
```
