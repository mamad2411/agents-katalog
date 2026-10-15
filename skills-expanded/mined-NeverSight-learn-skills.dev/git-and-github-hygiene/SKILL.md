---
name: git-and-github-hygiene
description: Use when branching, committing, pushing, opening or updating a PR, or creating, editing, or closing an issue.
---

# Git and GitHub Hygiene

Load only the reference file relevant to the current task:

- [GIT.md](GIT.md): branches, commits, pushes
- [PULL-REQUESTS.md](PULL-REQUESTS.md)
- [ISSUES.md](ISSUES.md)

## Never use the user's name in GitHub artifacts

Issues, pull requests, comments, and commit messages use role phrasing, e.g. "dev verified locally".
Where a tag is genuinely needed, use the user's handle, e.g. `@bellcd`.

This covers issue drafts written as repo files. They become the issue body verbatim, so the name has to be gone by the time the draft is approved, not by the time it is posted.

## `gh pr edit` breaks where Projects classic is deprecated

`gh pr edit` requests the deprecated `projectCards` field and fails on it, before touching the body. The error names the deprecation and says nothing about the edit you were making, so it reads as unrelated.

Fall back to the REST endpoint, which never goes near the project fields:

```bash
gh api repos/{owner}/{repo}/pulls/<n> -X PATCH -f body="$(cat new.md)"
```

`gh issue edit --body-file` is unaffected and works. Verified live, both directions, rather than assumed from the PR behavior.

Any command that asks for `projectCards` fails the same way. `gh pr view <n> --json projectCards` reproduces it as a pure read, which is the cheap way to check whether a given `gh` version still has the problem.

<!-- TODO: rerun that pure-read check against the current gh. Once it stops failing, delete this
     whole section rather than leaving the workaround as sediment. -->

