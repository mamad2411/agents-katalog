---
name: create-pr
description: Create a GitHub pull request from the current branch with a typed Conventional Commits title (feat, chore, refactor, fix, docs), a 3-point body, a version bump, and a CHANGELOG.md entry for that PR. Use whenever the user asks to open, create, raise, publish, or prepare a PR, or says things like "push this and make a PR", "ship this branch", or "write the PR for these changes", even if they do not mention titles, versions, or the changelog.
---

# Create Pull Request

Open a PR that a reviewer understands from the title and three bullets alone. The PR also carries its own version bump and changelog entry, so history stays readable after squash-merge.

## Workflow

1. Inspect the repo: `git status`, current branch, remotes, default branch, `.github/PULL_REQUEST_TEMPLATE*`, and `AGENTS.md` / `CONTRIBUTING.md` for PR rules.
2. Compute the merge base against the target branch and record the exact `base...head` range. If the branch is stacked on another unmerged branch, target that branch and describe only this PR's own changes.
3. Read the full diff (`git diff --stat <base>...HEAD`, then the content).
4. Pick the type and scope. See [type-selection](references/type-selection.md). Ask the user when that file says to.
5. Bump the version and write the changelog entry. See [changelog-and-versioning](references/changelog-and-versioning.md).
6. Run the checks that match the changed surfaces (focused tests, typecheck, lint). Record exact commands and results.
7. Commit the version bump and changelog in this branch, using the PR title as the commit message.
8. Write the body to a temp file following [pr-body](references/pr-body.md). Push the branch. Run `gh pr create --title "..." --body-file ...`. Use `--draft` when checks are still running or the work is not review-ready.
9. Open the created PR and verify title, base, head, and rendered body.

## Types at a glance

| Type | Use for | Rule |
| --- | --- | --- |
| `feat(scope)` | New features | Any file count |
| `chore(scope)` | Small updates and version changes | Max 2 files |
| `refactor(scope)` | Many code changes or many updates | Min 3 files, up to the whole project |
| `fix(scope)` | Bug fix in live production | Only after the user confirms it is a live production bug |
| `docs` | Documentation only, for example clarify worktree setup | No scope |

Decision order: docs-only, then feat, then fix, then file count. First match wins. Details and edge cases are in [type-selection](references/type-selection.md).

## Title

```
feat(auth): add refresh token rotation
chore(deps): bump bullmq and release 2.3.1
refactor(listings): split search service into query and ranking
fix(payments): avoid duplicate capture on webhook retry
docs: clarify worktree setup
```

- Lowercase, imperative, no trailing period, under ~70 characters.
- Scope is the package, module, or feature name the repo already uses. Check recent `git log` and the folder layout to match it. Omit the scope when the change is repo-wide.
- Squash-merge repos turn the title into the commit message; write it as the commit you want in history.
- Append `!` after the scope for a breaking change (`feat(api)!: ...`) and confirm with the user first.

## Rules

- Say what is verified, what is assumed, and what is not verified. Do not write "safe", "fixed", or "backward compatible" without pointing at the evidence.
- Green CI proves only the checks CI runs. Focused tests prove only the behavior they cover.
- Do not describe inherited changes from a parent branch as this PR's changes.
- Use plain hyphens; never em dashes or en dashes.
- No filler ("this PR aims to", "comprehensive", "robust"). Start sentences with the fact.
- Do not paste tokens, secrets, user records, or full payloads into the body or changelog.
- If the PR was written with the help of an agent, say so in one line at the end of the body.

## References

- [type-selection](references/type-selection.md): decision flow, file counting, the live-production question, edge cases. Read at step 4.
- [changelog-and-versioning](references/changelog-and-versioning.md): bump table, manifest handling, entry format. Read at step 5.
- [pr-body](references/pr-body.md): body template, three-bullet rules, one example per type. Read at step 8.
