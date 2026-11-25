---
name: open-pull-request
description: 'Open a GitHub pull request from the current branch, filling the repo PR template. Use when the user wants to open, create, or raise a PR — to the default base branch or a branch they name. Triggers on "open a PR", "create a pull request", "raise a PR to <branch>", "PR this branch".'
allowed-tools: Bash(git *), Bash(gh *), Read
---

# Open Pull Request

Open a PR from the current branch with `gh`, filling `.github/pull_request_template.md` from the actual diff.

## Steps

1. **Resolve head and base.** Head = `git branch --show-current`. Base = the branch the user named, else the remote default from `git symbolic-ref refs/remotes/origin/HEAD`. If head equals base, stop — there is nothing to PR; tell the user to switch to a feature branch. Done when you hold a head and base that differ.

2. **Push the branch.** Run `git push -u origin HEAD`. Done when the head branch has an upstream on origin.

3. **Reuse an existing PR.** Run `gh pr view --json url,state`. If it returns an open PR for this branch, report the URL and stop. Done when no open PR exists.

4. **Draft the body from the template.** Read `.github/pull_request_template.md` and fill **every** section from the real change — `git log <base>..HEAD` and `git diff <base>...HEAD --stat`:

   Keep it terse: bullets, not prose. Done when no template placeholder comment (`<!-- … -->`) survives.

5. **Create the PR.** Write the body to a temp file, then run `gh pr create --base <base> --title "<title>" --body-file <file>`, where title is a concise summary drawn from the commits. Report the returned URL. Done when `gh` returns a PR URL.
