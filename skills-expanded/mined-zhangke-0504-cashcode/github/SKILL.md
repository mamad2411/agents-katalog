---
name: github
description: Work with GitHub pull requests, issues, Actions runs, and API data through the gh CLI.
version: 1
tags: [github, pull-request, issue, actions]
triggers: [check pull request, github issue, workflow run, CI status]
requires:
  tools: [exec]
  bins: [gh]
---

# GitHub CLI

1. Run `gh auth status` before an operation that requires authentication.
2. Use `gh pr`, `gh issue`, and `gh run` for normal workflows.
3. Use `gh api` with `--json`/`--jq` for structured queries not covered by a subcommand.
4. Specify `--repo owner/repo` when the working directory does not identify the repository.
5. Never print, persist, or request an authentication token in chat.

Examples:

```text
gh pr checks 55 --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
gh issue list --repo owner/repo --json number,title
```
