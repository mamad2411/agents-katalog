---
name: commit-standards
description: "Use when writing a commit message or a changelog-feeding PR title, or checking whether one is well-formed. This team's Conventional Commits types, scope charset and release impact. Not for branch names (use issue-tracker-core:branch-and-title-conventions)."
license: MIT
---

# Commit Standards

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **Header**: a lowercase type from the table below, an optional scope in parentheses, an
  optional `!` immediately before the colon, then a colon, one space and the subject.
- **Scope**: the team charset is letters, digits, `_`, `/` and `-` (`api`, `PROJ-123`,
  `web/auth`). The `dev-guardrails` commit hook enforces it and rejects anything else, such as dots
  or spaces. A repo's `conventional-pre-commit` hook accepts a wider set by default; the team
  charset still applies.
- **Subject**: imperative mood ("add", not "added"), lowercase first word, no trailing period,
  header under about 72 characters.
- **Body** (optional): explain why, not what; the diff already shows what. Blank line after the
  header, wrap at about 72 columns.
- **Footer** (optional): `BREAKING CHANGE: …` (uppercase), `Refs: …`, and trailers.

## Types and release impact

| Type | Use for | Release impact |
| --- | --- | --- |
| `feat` | A new capability | MINOR |
| `fix` | A bug fix | PATCH |
| `perf` | A performance improvement | none by default |
| `refactor` | Restructuring with no behaviour change | none by default |
| `docs` | Documentation only | none by default |
| `test` | Adding or fixing tests | none by default |
| `build` | Build system or packaging config | none by default |
| `ci` | CI configuration | none by default |
| `chore` | Dependency bumps and housekeeping that fits no other type | none by default |
| `style` | Formatting only: whitespace, semicolons, formatter runs | none by default |
| `revert` | Reverting an earlier commit | as the reverted change |

A `!` before the colon or a `BREAKING CHANGE:` footer makes any type MAJOR. "None by default"
follows the Conventional Commits spec; a repo whose release tool bumps PATCH for other types
says so in its own config, and that config wins.

## Scope

- On an issue-tracked branch, the scope is the issue key: `feat(PROJ-123): add search filter`.
  The key shape comes from `CLAUDE_TICKET_PATTERN` (default `[A-Z][A-Z0-9]+-[0-9]+`).
- With no tracker, use the component or package: `fix(api): handle null response`.
- Omit the scope for repo-wide changes: `chore: update dependencies`.

Use one scope vocabulary per repo so history stays filterable.

## Examples

<example>
fix(api): handle null user response

The upstream directory returns 204 with an empty body for suspended
accounts; we were dereferencing the parsed payload unconditionally.
</example>

<example>
feat(api)!: remove deprecated v1 endpoints

BREAKING CHANGE: /api/v1/* is removed. Migrate callers to /api/v2/*.
</example>

<example>
revert: feat(PROJ-123): add search filter

Refs: 676104e
</example>

Subjects git writes itself (`Merge …`, `Revert "…"`, `fixup! …`, `squash! …`, `amend! …`) are
accepted as they are.

## Attribution

If the project requires a co-author trailer for assistant-written commits, put it in the footer in
the form the project's `CONTRIBUTING.md` or agent instructions specify.

## Verify

Take the first non-blank line of the message. If it matches
`^(Merge |Revert "|(fixup|squash|amend)! )`, git wrote it; accept it. Otherwise check it against
`^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([A-Za-z0-9_/-]+\))?!?: .+`
(the same types and scope charset the `dev-guardrails` hook uses). If the repo also has a
`commit-msg` hook (`commitlint`, `conventional-pre-commit`), run it locally too, because a rejected
message after a long rebase is expensive. Without a checkout, check a pasted message the same way.
