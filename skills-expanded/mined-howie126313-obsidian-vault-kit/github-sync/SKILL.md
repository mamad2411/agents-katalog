---
name: github-sync
description: |
  Sync local Obsidian vault to GitHub — auto-update README.md and push.
  Triggers: /github-sync, "sync to github", "push to github", "update repo"
allowed-tools:
  - Agent
---

# GitHub Sync — Subagent Dispatcher

When this skill is triggered, **do not execute sync steps yourself**. Immediately use the Agent tool to launch an independent subagent in the background to handle the entire sync workflow.

## Dispatch

Call the Agent tool with the following parameters:

```
Agent({
  description: "GitHub Sync",
  model: "sonnet",
  run_in_background: true,
  mode: "bypassPermissions",
  prompt: <full content of the sync-workflow block below>
})
```

After dispatching, inform the user that sync has started in the background. They can continue other work and will be notified on completion.

---

## sync-workflow

Pass the following content as the Agent prompt (copy verbatim, do not modify):

<sync-workflow>
You are a GitHub Sync automation agent. Follow these steps strictly to sync the Obsidian vault to GitHub.

## Step 1: Environment Detection & Status Check

**1a. Detect project root and remote (run in parallel):**

```bash
git rev-parse --show-toplevel    # project root
git remote get-url origin        # remote URL
git branch --show-current        # current branch
```

**1b. Check Git status:**

```bash
git status
git diff --stat
```

If there are no changes (no unstaged modifications, no untracked files), output "Nothing to sync" and end.

## Step 2: Analyze Changes and Update README.md

**2a. Categorize all changed files into three groups:**
- **Added**: new articles or directories
- **Modified**: updated content
- **Deleted**: removed content

**2b. Update README.md:**

1. Read current README.md content
2. Use `Glob("**/*.md")` to scan the project directory structure, count Markdown files (exclude .claude/ directory)
3. Update knowledge base sections based on added/deleted articles and directories
4. Update statistics (Markdown file count, directory categories) and custom Skills list (if changed)
5. Preserve existing README.md format and style

**Update principle:** only update sections with actual changes, do not rewrite unnecessarily.

## Step 3: Commit and Push

1. `git add` all changes (including README.md), exclude .playwright-mcp/ log files
2. Generate a commit message based on changes, format: `type: brief description`
   - Types: add, update, delete, refactor, fix (use the most prominent type if multiple apply)
   - Append to commit message: `\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
3. `git commit` (use HEREDOC format for the commit message)
4. `git push origin $BRANCH`

## Step 4: Output Results

Output a brief sync report including:
- Summary of changes synced (what was added/modified/deleted)
- README.md update details
- Push status (success/failure; if failed, analyze the cause)

## Notes

- If conflicts are encountered, output conflict details — do not force overwrite
- Do not stage files under the .playwright-mcp/ directory
</sync-workflow>
