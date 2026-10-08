---
name: commit-message-enforcer
description: "Standardize, review, and enforce enterprise-grade commit messages using Conventional Commits, scoped types, breaking-change footers, and clear history hygiene. Use when asked to harden commit messaging, review commit history, configure commitlint, or prepare clean commits."
---

# Commit Message Enforcer

Use this skill when creating, reviewing, or enforcing commit messages.

## Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

- `feat`: user-visible capability.
- `fix`: bug fix.
- `docs`: documentation or standards.
- `ci`: workflow, automation, or ruleset change.
- `chore`: repository maintenance.
- `refactor`: behavior-preserving code restructuring.
- `test`: test-only change.
- `security`: security hardening or vulnerability remediation.
- `deps`: dependency update.
- `revert`: revert a prior change.

## Decision Rules

- Use one primary purpose per commit. Split unrelated changes.
- Use scopes when they add clarity, such as `ci`, `api`, `web`, `license`, `skills`, or a package name.
- Use `!` or a `BREAKING CHANGE:` footer for incompatible behavior.
- Keep the subject imperative, lowercase after the type, and specific.
- Put verification details in the body when the commit affects release confidence.

## Verification

- Check the staged diff matches the commit subject.
- Confirm no generated or unrelated files are staged.
- If enforcing in CI, validate with commitlint or an equivalent parser.

## References

- Conventional Commits baseline: `references/conventional-commits.md`
