---
name: github-cli
description: Use GitHub CLI for issues, pull requests, Actions, and API queries with confirmation for writes.
category: development
aliases:
- github
- gh-cli
triggers:
- Open a PR
- List my issues
- Check the CI run
- Create a release
- Use the GitHub API
keywords:
- github
- gh
- pr
- pull
- request
- issue
- ci
- workflow
- release
- api
dependencies:
- optional:gh
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- github-cli
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- cli
- development
- github
- pull
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Github Cli

## Purpose
Run common GitHub operations through the `gh` CLI in a way that is safe, scriptable,
and ergonomic for an agent. The skill wraps `gh issue`, `gh pr`, `gh run`, `gh release`,
and `gh api` into named, audited operations.

## When to Use
- The user wants to read, create, or update an issue, PR, or release
- The user wants CI status, logs, or rerun
- A scripted workflow needs to query or mutate GitHub state

## When NOT to Use
- The user is not authenticated (`gh auth status` will fail)
- The action requires admin rights the user does not have
- The user wants GUI review (route to the browser)

## Capabilities
- **Issues**: list, view, create, edit, close, comment, label, assign
- **Pull Requests**: list, view, create, checkout, review, merge, close, comment, diff
- **Runs / Workflows**: list, view, watch, rerun, download logs, cancel
- **Releases**: list, view, create, upload, delete (with confirmation)
- **API**: arbitrary `gh api` call with auto-pagination, header capture, JSON pretty-print
- **Repo**: clone, fork, view, set default

## Inputs
- A subcommand and its arguments (e.g. `pr list --author @me --state open`)
- Optional: `--repo owner/name` to override the current repo
- Optional: `--json field1,field2` to project specific fields

## Workflow
1. **Verify auth** with `gh auth status` (cached result for 5 min).
2. **Resolve the target repo** (`--repo` flag or current `gh repo view`).
3. **Build the `gh` invocation** with safe defaults:
   - Use `--json` instead of text when downstream parsing is needed
   - Use `--template` to project fields
   - Always pass `--paginate` for list commands
4. **Run the command**, capture stdout, stderr, exit code.
5. **Format the result** for chat (table, list, or JSON, depending on call).
6. **On error**: classify (auth, not-found, permission, rate-limit) and explain.

## Tools
- `gh` CLI (required, â‰¥ 2.40)
- `git` (for `gh pr checkout` flows)
- `jq` (recommended for API JSON shaping)

## Examples
**User:** "List my open PRs."
**Response:** `gh pr list --author @me --state open --json number,title,headRefName,url`

**User:** "Rerun the failed CI job."
**Response:** `gh run rerun <run-id> --failed`

**User:** "Create an issue from this error."
**Response:** `gh issue create --title "..." --body "..." --label bug --assignee @me`

## Safety
- Never force-push or force-merge without explicit confirmation
- Never delete a release or branch without an explicit `--confirm-destructive`
- Surface rate-limit headers and warn on remaining quota
- Redact tokens / cookies from any `gh api` response before display

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
