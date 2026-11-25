---
name: open-pr
description: Push the current branch and open a pull request against the detected base branch, with an AI-drafted title and body confirmed by the user before creating. Use when the user wants to open, create, or submit a PR — phrases like "PR 올려줘", "PR 열어줘", "PR 만들어줘", "open a PR", "create a pull request", "submit for review", "/open-pr". Do NOT use to review, comment on, or update an existing PR.
license: MIT
metadata:
  author: dkmqflx
  version: "1.0.0"
---

# Open PR

Push the current branch and open a pull request via `gh pr create`.

Run this after committing your changes (see `commit-each`). Once the PR is merged, clean up with `branch-done` or `worktree-done`.

## When to apply

Opening a **new** PR for the current branch. **Do not apply** to update, review, or comment on an existing PR.

## Steps

1. Determine the base branch:
   - Try `git symbolic-ref refs/remotes/origin/HEAD` and strip the `refs/remotes/origin/` prefix.
   - If that fails, use the first of `dev`, `main`, `master` that exists locally (`git show-ref --verify --quiet refs/heads/<name>`).
   - If none exist, stop and ask the user which branch is the base.
2. Record the current branch: `git rev-parse --abbrev-ref HEAD`. If it equals the base branch, stop and notify the user — there's nothing to open a PR from.
3. Check for uncommitted changes (`git status --porcelain`). If any exist, stop and tell the user to commit first.
4. Check whether a PR already exists for this branch: `gh pr view --json url 2>/dev/null`. If one does, stop and report its URL instead of creating a duplicate.
5. Push the branch: `git push -u origin HEAD`.
6. Gather context for the PR description:
   ```bash
   git log <base branch>..HEAD --oneline
   git diff <base branch>...HEAD
   ```
7. Draft a title (under 70 characters) and a body with a `## Summary` (1–3 bullets) and `## Test plan` (checklist) section, covering **all** commits on the branch — not just the latest.
8. Show the drafted title and body to the user and get confirmation before creating.
9. Create the PR:
   ```bash
   gh pr create --base <base branch> --title "<title>" --body "$(cat <<'EOF'
   <body>
   EOF
   )"
   ```
10. Report the returned PR URL.

## Guardrails

- Always confirm the drafted title/body with the user before running `gh pr create` — opening a PR is visible to others and not easily undone.
- If `gh` is not installed or not authenticated, stop and tell the user to run `gh auth login`.
- Never force-push (`git push -f`) to publish the branch.
- Do not create a second PR if one already exists for this branch.
