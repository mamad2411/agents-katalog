---
name: start-feature
description: "Start a new feature, fix or change on a git flow feature branch from develop and open its PR against develop. Use for new work, start a feature, begin a change."
---

# start-feature

1. Check git flow is set up: `git flow version` and `git config --get gitflow.branch.develop`. If git flow is missing, stop and tell the owner to install it with `brew install git-flow`; never hand-roll it. If uninitialized, run the init commands in [Maintaining the kit](../../../docs/maintaining.md#release).
2. Check `git status --porcelain`, fetch origin, and compare the starting branch with its origin ref. Stop on a dirty tree or a branch behind/diverged from origin; never stash or reset the owner's work. Require the starting branch to be up to date before proceeding.
3. Start from up-to-date `develop`: `git switch develop`, then `git flow feature start <name>`.
4. Implement the requested scope and tests; run the `run-gates` skill. Follow [Maintaining the kit](../../../docs/maintaining.md).
5. Commit the reviewed work, push `feature/<name>` with upstream tracking, and open a PR against `develop`. Run `run-gates` for that PR too. Do not run `git flow feature finish`; review happens on GitHub.

Tagging, pushing `main`/tags, creating a release and publishing the `gemini` branch need the owner's explicit go-ahead in that session. Stop before each unless that session's explicit go-ahead covers it.
