---
name: github
description: Interact with GitHub using the GitHub CLI (gh). Use when the user asks to create repos, manage issues, pull requests, releases, gists, browse code, manage labels/milestones, review PRs, or perform any GitHub operation. Also use for reading issue details, commenting, searching issues/PRs, and checking CI status.
---

# GitHub CLI

Perform GitHub operations using the `gh` CLI, which is pre-authenticated in the environment. This skill covers repositories, issues, pull requests, releases, gists, and the GitHub API.

## Available Commands

### Repositories

```bash
# List user's repos
gh repo list [owner] --limit 50

# Create a new repo (private by default; add --public only if explicitly requested)
gh repo create <name> --private [--description "desc"] [--clone]

# Clone a repo (always clone into the repos/ folder)
gh repo clone <owner/repo> repos/<repo>

# View repo info
gh repo view <owner/repo>

# Fork a repo (clone into repos/ folder)
gh repo fork <owner/repo> --clone -- repos/<repo>

# Delete a repo (REQUIRES user approval before executing)
gh repo delete <owner/repo> --yes
```

### Issues

```bash
# List issues
gh issue list [-R owner/repo] [--state open|closed|all] [--label "bug"] [--assignee @me]

# View issue details
gh issue view <number> [-R owner/repo]

# Create an issue
gh issue create [-R owner/repo] --title "Title" --body "Body" [--label "bug,urgent"] [--assignee "user"]

# Close an issue
gh issue close <number> [-R owner/repo] [--reason "completed"|"not_planned"]

# Reopen an issue
gh issue reopen <number> [-R owner/repo]

# Comment on an issue
gh issue comment <number> [-R owner/repo] --body "Comment text"

# Edit an issue
gh issue edit <number> [-R owner/repo] [--title "New title"] [--body "New body"] [--add-label "label"] [--add-assignee "user"]

# Pin/unpin an issue
gh issue pin <number> [-R owner/repo]
gh issue unpin <number> [-R owner/repo]

# Transfer an issue
gh issue transfer <number> <destination-repo> [-R owner/repo]
```

### Pull Requests

```bash
# List PRs
gh pr list [-R owner/repo] [--state open|closed|merged|all] [--author "user"] [--base main]

# View PR details
gh pr view <number> [-R owner/repo]

# Create a PR
gh pr create [-R owner/repo] --title "Title" --body "Body" [--base main] [--head feature-branch] [--draft] [--label "label"]

# Merge a PR
gh pr merge <number> [-R owner/repo] [--merge|--squash|--rebase] [--delete-branch]

# Review a PR
gh pr review <number> [-R owner/repo] --approve|--request-changes|--comment --body "Review text"

# Check PR status (CI checks)
gh pr checks <number> [-R owner/repo]

# Checkout a PR locally
gh pr checkout <number> [-R owner/repo]

# Close a PR without merging
gh pr close <number> [-R owner/repo]

# Comment on a PR
gh pr comment <number> [-R owner/repo] --body "Comment text"

# View PR diff
gh pr diff <number> [-R owner/repo]

# Edit a PR
gh pr edit <number> [-R owner/repo] [--title "New title"] [--body "New body"] [--add-label "label"] [--add-reviewer "user"]

# Mark PR as ready for review
gh pr ready <number> [-R owner/repo]
```

### Releases

```bash
# List releases
gh release list [-R owner/repo]

# Create a release (REQUIRES user approval before executing)
gh release create <tag> [-R owner/repo] --title "Title" --notes "Release notes" [--draft] [--prerelease]

# View a release
gh release view <tag> [-R owner/repo]

# Delete a release (REQUIRES user approval before executing)
gh release delete <tag> [-R owner/repo] --yes
```

### Gists

```bash
# Create a gist
gh gist create <file> [--public] [--desc "description"]

# List gists
gh gist list

# View a gist
gh gist view <id>
```

### Search

```bash
# Search issues
gh search issues "query" [--repo owner/repo] [--state open] [--label "bug"]

# Search PRs
gh search prs "query" [--repo owner/repo] [--state open]

# Search repos
gh search repos "query" [--language typescript] [--sort stars]

# Search code
gh search code "query" [--repo owner/repo] [--language typescript]
```

### GitHub API (for anything not covered above)

```bash
# GET request
gh api repos/{owner}/{repo}

# POST request
gh api repos/{owner}/{repo}/labels -f name="priority" -f color="ff0000" -f description="High priority"

# GraphQL query
gh api graphql -f query='{ viewer { login } }'

# With JQ filtering
gh api repos/{owner}/{repo}/issues --jq '.[].title'

# Paginated listing
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].title'
```

### Labels and Milestones

```bash
# List labels
gh label list [-R owner/repo]

# Create a label
gh label create "name" [-R owner/repo] --color "ff0000" --description "desc"

# Delete a label
gh label delete "name" [-R owner/repo] --yes

# Milestones (via API)
gh api repos/{owner}/{repo}/milestones --jq '.[].title'
gh api repos/{owner}/{repo}/milestones -f title="v1.0" -f due_on="2026-06-01T00:00:00Z"
```

### Workflow / CI

```bash
# List workflow runs
gh run list [-R owner/repo] [--workflow "ci.yml"]

# View a run
gh run view <run-id> [-R owner/repo]

# Watch a run in progress
gh run watch <run-id> [-R owner/repo]

# Re-run a failed workflow
gh run rerun <run-id> [-R owner/repo]
```

## Important Rules

- **Workspace repo management**: All repos must be created, cloned, and managed from the `repos/` folder of the workspace. Always use `repos/` as the target directory for clone and fork operations.
- **Private by default**: When creating new repos, always use `--private` unless the user explicitly requests a public repo.
- **Destructive operations require approval**: Any potentially destructive operation — including deleting repos, deleting releases, deleting labels, force pushing, and any other irreversible action — **MUST** be confirmed with the user before executing. Never run these automatically.
- **Always use `-R owner/repo`** when operating on a repo other than the current working directory's repo.
- **Branch safety**: When creating PRs for bot-managed code changes, always use `cp-*` branch prefix.
- **Use `--json` for structured output** when you need to parse results programmatically:
  ```bash
  gh issue list --json number,title,state,labels
  gh pr list --json number,title,state,headRefName
  ```
- **Use `--jq` for filtering** JSON output directly:
  ```bash
  gh issue list --json number,title --jq '.[] | "\(.number): \(.title)"'
  ```
- **Pagination**: For large result sets, use `--limit` or `--paginate` to control output.

## Examples

User: "What are the open bugs in my-app repo?"
→ `gh issue list -R owner/my-app --label "bug" --state open --json number,title,assignees`

User: "Create an issue for the login timeout problem"
→ `gh issue create -R owner/my-app --title "Login timeout on slow connections" --body "..." --label "bug"`

User: "Review the latest PR"
→ `gh pr list -R owner/my-app --state open --limit 1 --json number,title` → `gh pr view <number>` → `gh pr diff <number>`

User: "What's the CI status on PR #42?"
→ `gh pr checks 42 -R owner/my-app`

User: "Merge PR #42 with squash"
→ Confirm with user → `gh pr merge 42 -R owner/my-app --squash --delete-branch`
