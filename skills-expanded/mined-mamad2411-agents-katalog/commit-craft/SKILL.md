---
name: commit-craft
description: Use before any git commit, branch, or pull request — defines the project's conventions for atomic commits, message format, branch naming, and PR hygiene so history stays navigable, bisectable, and safe to ship.
---

# Commit Craft

## Overview

Version-control history is documentation that outlives every summary. A commit is read far more
often than it's written — during review, bisects, blame, and reverts months later. Sloppy history
turns those into archaeology; disciplined history makes them a one-line answer.

**Core principle:** every commit should be a single, reversible, explainable unit of change.

## When this applies

Any time work reaches git: staging a commit, cutting a branch, or opening a PR. Skip it only for
throwaway experiments you never intend to keep. It does not depend on any other plugin being
installed.

## Permission gate (do this first)

- **Only commit, push, or open a PR when the user asks.** Finishing a code change is not implicit
  permission to commit it — surface the diff and let them decide.
- **Never commit directly to the default branch without asking.** If the current branch is `main`/
  `master` and the user hasn't said otherwise, branch first (see naming below), then commit.
- **Never use `--no-verify`, `--no-gpg-sign`, or skip hooks** unless the user explicitly asks. A
  failing hook is a signal to fix, not to bypass.

## Commits

**Atomic.** One logical change per commit. Don't mix a refactor with a feature, or a formatting
sweep with a bug fix — a reviewer (and a future `git revert`) should be able to take or drop the
change as a whole. Split unrelated work into separate commits.

**Message format:**

```
<imperative subject, ~50 chars, no trailing period>

<body: wrap ~72 chars. Explain WHY the change is needed and what it
affects — the diff already shows what changed. Reference issues/PRs.>

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

- Subject in the imperative mood: "Add retry to uploader", not "Added" / "Adds" / "Fixing".
- Body is optional for genuinely trivial commits, required when the *why* isn't obvious from the
  subject. Prefer prose that answers "why now / why this way" over restating the diff.
- End the message with the `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` trailer.

**Never commit:** secrets, credentials, `.env` files, generated/build artifacts, large binaries, or
anything already ignored. If `git status` shows something that should be ignored, fix `.gitignore`
first — don't commit it "just this once."

## Branches

Name branches `<type>/<short-kebab-summary>`, using the same type vocabulary as commits/PRs:

- `feat/` — new capability   · `fix/` — bug fix   · `chore/` — tooling, deps, config
- `docs/` — documentation     · `refactor/` — behavior-preserving restructure

Examples: `feat/search-filters`, `fix/quiz-empty-wordlist`, `chore/pin-actions-sha`.

## History hygiene

- **Squash fixup noise** ("wip", "typo", "address review") before merging, so each landed commit is
  meaningful and the branch stays bisectable.
- **Rebase your own unpushed local branch** to keep history linear; **never rebase or force-push a
  branch others may have pulled.** If you must update a shared branch, prefer `--force-with-lease`
  over `--force`, and only when the user has agreed.
- Prefer a new commit over amending a commit that's already pushed.

## Pull requests

- **Small and focused** beats large and sweeping — easier to review, safer to revert.
- **Title:** same imperative style as a commit subject.
- **Body:** what changed and *why*, how it was tested/verified, and links to any issue it closes
  (`Closes #123`). End the PR body with:

  ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)
  ```

- **Green before merge:** the most recent CI run on the branch must pass. Don't merge red, and don't
  disable a check to go green.
- Reference PRs/issues as full markdown links, never a bare `#123`.

## Red flags

| Thought | Reality |
|---|---|
| "I finished the change, so I'll just commit it" | Completing work isn't permission to commit. Ask first. |
| "I'll bundle these three unrelated fixes into one commit" | That's not atomic — split them so each can be reverted alone. |
| "The subject says it all, skip the body" | Fine only if *why* is obvious. If it isn't, the body is where it belongs. |
| "I'm on main but it's a tiny change" | Branch first. Size doesn't change the rule. |
| "The hook is failing, I'll add `--no-verify`" | The hook caught something. Fix it, don't bypass it. |
| "I'll force-push to clean up the shared branch" | You may clobber someone's work. `--force-with-lease`, and only with agreement. |
