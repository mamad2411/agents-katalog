---
name: gh-publish
description: Publish local changes to GitHub by confirming scope, committing intentionally, pushing the branch, and opening a draft pull request. Use only when the user explicitly wants the full publish flow from a local checkout.
---

# Publish Changes

## Overview

Use this only when the user wants the whole flow from a local checkout: branch
if needed, stage, commit, push, open a PR.

The split is fixed. `git` owns everything local, because the GitHub API cannot
see a working tree. `github_create_pull_request` opens the PR once the branch is
on the remote. `gh` is the fallback for cross-repository and fork heads.

If the user is on the desktop with a local checkout, the builtin `/pr` command
runs this flow with its command approvals already armed and is usually the
better path. Say so and use it.

## Prerequisites

- A local git repository, and a clear understanding of which changes belong in
  this PR.
- A connected GitHub app for the PR step. If the `github_*` tools are missing,
  fall back to `gh pr create` and tell the user why.

## Naming

- Branch: `agent/{short-description}` when starting from a default branch.
- Commit subject: terse, imperative, under 72 characters.
- PR title: what the whole diff does, not what the last commit did.

## Workflow

1. Confirm scope before touching anything.
   - `git status -sb` and read the diff.
   - If the worktree has unrelated changes, do NOT `git add -A`. List what you
     see and ask which files belong in this PR.
2. Branch.
   - On `main`, `master`, or another default branch, create
     `agent/{description}`.
   - Otherwise stay on the current branch.
3. Stage only what was agreed. Explicit paths when the tree is mixed.
4. Commit with the confirmed message. Never `--no-verify`: a failing hook is a
   real signal, so fix the cause.
5. Run the most relevant checks that have not already run. If they fail for a
   missing dependency, install it and retry once. If they fail for a real
   reason, stop and report.
6. Push: `git push -u origin $(git branch --show-current)`.
7. Open the PR as a draft.
   - `github_create_pull_request` with `draft: true`.
   - Derive `owner` and `repo` from the remote, `head` from the current branch,
     and `base` from the user's request or the repository default branch
     (`github_get_repo` returns it).
   - For a fork or a cross-repository target, use
     `gh pr create --draft --fill --head $(git branch --show-current)` instead.
     The native tool expects a single repository target and does not encode
     cross-repository head semantics.
   - When using the CLI, write the body to a temp file with real newlines so the
     Markdown renders.
8. Report the branch, the commit, the PR URL, what was validated, and anything
   still unverified.

## PR body

Real Markdown prose covering:

- what changed
- why it changed
- the impact on users or developers
- the root cause, when this is a fix
- the checks used to validate it

## Write safety

- Never stage unrelated changes silently.
- Never push without confirming scope on a mixed worktree.
- Draft by default. Ready-for-review only on an explicit request.
- Never force push, never rewrite history, never merge.
- If the repository has no accessible GitHub remote, stop and say so rather
  than inventing a target.
