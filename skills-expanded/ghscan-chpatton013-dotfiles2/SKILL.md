---
name: committing-changes
description: Use when creating a git commit. Load it before running git commit.
---

# Make a good commit

## Before committing

- Run the project's linter and auto-formatter to ensure commit content is valid.
- `git status` and `git diff` (and `git diff --staged`) to see exactly what
  will go in. Never blind-stage with `git add -A` without reviewing.
- Split unrelated changes into separate commits. Each commit should build on
  its own and represent one coherent change.
  - Ensure that your split commits would each pass the project's linter and
    auto-formatter.
- Scan the diff for secrets (API keys, tokens, `.env` values, private hosts you
  weren't asked to expose). If you find one, stop and flag it — do not commit.

## Identity — do not override it

- Just run `git commit`. Let git resolve the author from the repo's configured
  identity.
- Never pass `-c user.name=…` / `-c user.email=…`, `--author=…`, or set
  `GIT_AUTHOR_*` / `GIT_COMMITTER_*`. Never reuse an email from the session or
  environment as the author — it may be the wrong identity for this repo.

## Message

- Subject: lowercase `area: summary`, imperative, no trailing period.
  Examples: `parser: handle empty input`, `docs: fix broken link`.
- Keep the subject ~50 chars; wrap the body at ~72. Use the body to explain
  *why* when the change isn't self-evident. Omit the body for trivial changes.
- Follow the project's own commit convention if it documents a different one.

## Scope of action

- Commit to the current local branch. If on the default branch (`main`/
  `master`) and about to make nontrivial changes, create a branch first.
- Do not `git push`, force-push, amend already-pushed commits, or open a PR
  unless I explicitly ask.
- Committing a change is not the same as finishing a branch — once every task
  on a feature branch is committed and verified, see `finish-branch` for the
  merge/PR/keep decision.
