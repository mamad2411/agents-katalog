---
name: edit-pr
description: Use when work has been committed and the PR needs to reflect the current state of the branch - creates a new PR or updates an existing one with title, purpose, checklist, and ticket links
---

# Edit PR

Create or update a GitHub Pull Request to match the current state of the branch. Reads the repo's PR template, analyzes the diff, and builds on any existing PR body incrementally.

## Iron Law

```
NEVER push to remote (only updates PR metadata via gh)
NEVER update PR without user approval via AskUserQuestion
NEVER delete or close a PR
ALWAYS request review from @copilot after creating or updating a PR (automatic, no user approval needed)
```

## Process

### Step 1: Gather context

1. Run `git branch --show-current` to get the branch name.
2. Extract the Jira ticket ID from the branch name: everything before the first underscore (e.g., `PROJ-123` from `PROJ-123_add_user_validation`). If no underscore or no ticket pattern found, omit the ticket.
3. Run `git log main..HEAD --oneline` to see all commits on the branch.
4. Run `git diff main...HEAD --stat` to see which files changed, then `git diff main...HEAD` for the full diff.
5. Check if a PR exists: `gh pr view --json number,title,body`. Read the current title and body if it does.
6. Check if the branch is pushed: `git ls-remote --heads origin $(git branch --show-current)`.

**Branching logic:**
- Branch not pushed to remote: stop. Tell the user to push first (or run `/conventional-commit`).
- Branch pushed, no PR exists: **create mode**.
- PR exists: **update mode**.

### Step 2: Read the PR template

Look for `.github/PULL_REQUEST_TEMPLATE.md` in the repo root. Use it as the structural skeleton for the PR body. If no template exists, use a simple Purpose + Related Tickets structure.

### Step 3: Analyze and draft

Build the PR body section by section:

**Title:** Use conventional commit format: `type(scope): [TICKET-ID] subject`. In update mode, propose a new title only if the current one is stale or misaligned with the changes.

**Purpose:** In create mode, write a clear explanation of what changed and why based on the diff and commit messages. In update mode, read the existing purpose text and add or adjust based on new commits. Match the tone of what's already there. Don't rewrite from scratch.

**Related Tickets:** Auto-link the Jira ticket extracted from the branch name. Format: `[TICKET-ID](https://yourcompany.atlassian.net/browse/TICKET-ID)`

**Checklist:** Check off items based on file analysis:
- "title includes Jira ticket" — auto-check if the title contains the ticket ID
- "unit test coverage" — check if `_test.go` files were modified or added in the diff
- "updated docs/md files" — check if `.md` files were modified in the diff
- "narrow scope", "avoids mixing refactoring with features", "input validation" — leave unchecked for user judgment

**New logs:** Check if new logging calls (e.g., `logger.`, `zap.`, `.Info(`, `.Error(`, `.Warn(`) appear in the diff. If no new logs were added, leave all boxes unchecked. If new logs exist, leave boxes unchecked for the user to verify compliance.

### Step 4: Present for approval

Show the complete proposed PR body and title via `AskUserQuestion`. In update mode, make it clear what changed from the current version. Wait for the user to approve, edit, or reject.

Do not show the raw diff. The user already knows what changed.

### Step 5: Execute

If approved:
- **Create mode:** `gh pr create --title "..." --body "$(cat <<'EOF' ... EOF)"`
- **Update mode:** `gh pr edit --title "..." --body "$(cat <<'EOF' ... EOF)"`
- Then always request Copilot review (no user approval needed). This also works as a re-request when Copilot has already reviewed a previous revision:
  ```
  REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
  gh api "repos/$REPO/pulls/NUMBER/requested_reviewers" \
    --method POST --input - <<< '{"reviewers":["copilot-pull-request-reviewer[bot]"]}'
  ```
  where `NUMBER` is the PR number from step 1 or the create output.
  If this fails (e.g. Copilot not enabled on the repo), log the error and continue — don't block the PR workflow.

If the user provided edits, incorporate them before executing.

If rejected, stop.

## Writing Style

- Plain English, not bullet-point soup
- Sound like a developer explaining to a teammate
- When adding to existing text, match the tone already there
- Concise: a few sentences to a short paragraph per logical change
- Explain "why" alongside "what"
- No em dashes, no emojis
- Use numbered lists only when there are genuinely distinct items (e.g., multiple unrelated changes in one PR)

## Integration

- Typically runs after `/conventional-commit` has committed and pushed.
- Depends on `gh` CLI being authenticated and available.
- Does NOT push branches. That's conventional-commit's job.
