---
name: conventional-commit
description: Write and apply Conventional Commits — type(scope): subject, imperative mood, with body and BREAKING CHANGE footer when needed. Use when committing staged work or asked to write, review, or standardize a commit message.
---

# Conventional Commit

Produce commit messages that follow the
[Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification):
`type(scope): description`.

## Workflow

1. Run `git status` to review changed files.
2. Run `git diff` (or `git diff --cached`) to inspect the changes — the message must describe
   what the diff actually does.
3. Stage only the files that belong to this change: `git add <file>`.
4. Construct the message with the structure below and commit:
   `git commit -m "type(scope): description"` (multi-line body/footer when needed).
5. Stop there — never push, open, or merge a PR/MR; that is always a human action.

## Message structure

```
type(scope): description

[optional body — the why and any context the diff doesn't show]

[optional footer — BREAKING CHANGE: details, or issue references]
```

- **type** — one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`,
  `chore`, `revert`. Append `!` for breaking changes (`feat!:`).
- **scope** — optional but recommended: the module/area touched (e.g. `auth`, `parser`, `ui`).
- **description** — required, short, **imperative mood** ("add", not "added"/"adds"), no
  trailing period.
- **body** — optional; explain motivation and contrast with previous behavior.
- **footer** — `BREAKING CHANGE: <details>` and/or issue references (`Closes #123`).

## Examples

```
feat(parser): add ability to parse arrays
fix(ui): correct button alignment
docs: update README with usage instructions
refactor: improve performance of data processing
chore: update dependencies
feat!: send email on registration (BREAKING CHANGE: email service required)
```

## Validation

Before committing, check: the type is in the allowed list, the description is imperative and
matches the staged diff, breaking changes carry `!` and a `BREAKING CHANGE:` footer, and the
commit contains only the files of this one logical change (split unrelated changes into
separate commits).
