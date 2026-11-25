---
name: pr-spring-cleaning
description: Triage open PRs for a GitHub repo. Gathers all open PRs for a user, summarizes status breakdown, creates a todo list, then walks through each PR one-by-one for the user to decide keep draft, mark ready, or close. Use when asked to clean up PRs, triage PRs, or do PR spring cleaning.
allowed-tools: Bash(bun:*) Bash(gh:*)
---

# PR Spring Cleaning

Interactively triage all open PRs for a user on a given GitHub repo. Walk through each PR one-by-one so the user can decide what to do with it.

## When to Use

- User wants to clean up their open PRs
- User wants to triage stale PRs
- User mentions "PR spring cleaning" or similar

## Workflow

### Step 1: Gather & Summarize PRs

Run the fetch-and-summarize script. If the user doesn't specify a repo, ask them which repo to target.

**`scripts/fetch-and-summarize.ts`** - Run using bun

The script outputs:
- A **summary** with total counts, drafts vs ready, oldest, and most recently updated
- A **per-PR detail list** sorted oldest-first with status, branch, dates, labels, and truncated description

Present the summary section to the user.

### Step 2: Create Todo List

Create a task for each PR. The task name should include the PR number and a short title:

```
PR #1234: Add user authentication
```

Mark all tasks as `pending` initially.

### Step 3: Walk Through PRs One-by-One

For each PR (oldest first), present the detail block from the script output and ask:

```
What would you like to do?
- **Keep as draft** — no changes
- **Mark ready for review** — move from draft to open
- **Close** — close with an optional comment
- **Skip** — decide later
```

Wait for the user's response before proceeding. Do NOT batch multiple PRs in one message.

### Step 4: Execute the User's Decision

Use `gh` CLI directly based on what the user asks:

- **Close**: `gh pr close <NUMBER> --repo <REPO> --comment "<message>"`
- **Mark ready**: `gh pr ready <NUMBER> --repo <REPO>`
- **Convert to draft**: `gh pr ready <NUMBER> --repo <REPO> --undo`
- **Keep / Skip**: no action needed

If the user asks to close without providing a reason, ask if they want to add a comment — a brief reason helps future archaeology.

After executing, update the corresponding task to `completed` with the action taken.

### Step 5: Final Recap

After all PRs have been reviewed, present a summary:

```
## Spring Cleaning Complete!

**Before**: 13 open PRs (8 drafts, 5 ready)
**After**: 3 open PRs (2 drafts, 1 ready)

### Actions Taken
- Closed: 7 PRs
- Marked ready: 1 PR
- Kept as draft: 2 PRs
- Already merged: 3 PRs (no action needed)

### Remaining PRs
| # | Title | Status |
|---|-------|--------|
| 2212 | BetterAuth staff migration | Ready for review |
| 2260 | pnpm migration | Draft |
| 2048 | React PDF summaries | Draft |
```

## Edge Cases

- **PR was merged between fetch and action**: If a `gh` command fails because the PR is already merged/closed, note it and move on.
- **Network errors**: If a `gh` command fails with an EOF or network error, retry once before reporting the error.
- **User wants to skip**: Mark the task as completed with "skipped" and move to the next one.
- **User wants to batch-close**: If the user says something like "close the rest", confirm the list of PRs that will be closed before executing.

## Notes

- Always use `--repo <REPO>` flag to be explicit about which repository.
- Present PRs in chronological order (oldest first) — stale PRs are the primary cleanup target.
- Keep summaries brief. The user can ask for more detail on any specific PR.
