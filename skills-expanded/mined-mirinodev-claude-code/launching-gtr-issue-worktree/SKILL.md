---
name: launching-gtr-issue-worktree
description: >
  Create a git worktree via gtr (git-worktree-runner) for a GitHub issue and generate a CLAUDE.local.md
  with issue context so that Claude Code launched in that worktree knows what to work on.
  Issue-specific context is written to CLAUDE.local.md (not .claude/CLAUDE.md) to avoid
  Git conflicts when merging PRs from multiple worktrees.
  Use when user mentions "gtr issue", "issue worktree", "issueでworktree", "issueに着手",
  "gtr-issue", or wants to set up an isolated worktree for a specific GitHub issue.
  Requires: gtr (git-worktree-runner) and gh CLI installed.
---

# Launch GTR Issue Worktree

Set up an isolated worktree for a GitHub issue with full context injection.

## Workflow

### 1. Parse Input

Extract the issue number from user input. Accept formats:
- `42`, `#42`, `issue 42`

### 2. Fetch Issue

```bash
gh issue view <NUMBER> --json number,title,body,labels,assignees
```

If the command fails, check:
- `gh auth status` for authentication
- Whether the issue number exists

### 3. Derive Branch Name

Convert issue title to a branch name:
- Format: `issue-<NUMBER>-<slugified-title>`
- Slugify: lowercase, replace spaces/special chars with `-`, truncate to 50 chars
- Example: Issue #42 "Add user authentication" -> `issue-42-add-user-authentication`

### 4. Create Worktree

```bash
git gtr new <branch-name>
```

If gtr is not installed, show install instructions:
```
brew tap coderabbitai/tap && brew install git-gtr
```

Capture the worktree path from gtr output or derive it:
```bash
git gtr go <branch-name>
```

### 5. Generate ToDo Checklist

Analyze the issue body and generate a checklist of actionable tasks.

Rules:
- Parse the issue body to identify concrete, actionable steps
- Each task should be a single, verifiable action (not vague)
- Format as GitHub-flavored markdown checkboxes: `- [ ] task description`
- Typically 3-7 items depending on issue complexity
- Include setup/preparation steps if needed
- End with a verification/confirmation step

Example output:
```markdown
## ToDo

- [ ] Set up environment / prerequisites
- [ ] Implement core feature
- [ ] Test the feature works as expected
- [ ] Document findings or observations
```

### 6. Update Issue Description

Append the generated ToDo checklist to the issue body on GitHub:

```bash
# Get current issue body
CURRENT_BODY=$(gh issue view <NUMBER> --json body -q .body)

# Append ToDo section (only if no checklist exists yet)
# Check: if body already contains "- [ ]" or "- [x]", skip this step
NEW_BODY="${CURRENT_BODY}

## ToDo

- [ ] task 1
- [ ] task 2
..."

gh issue edit <NUMBER> --body "$NEW_BODY"
```

Important:
- **Do NOT overwrite** existing content — always append
- If the issue body already contains a checklist (`- [ ]` or `- [x]`), skip this step and reuse the existing checklist
- Preserve all original markdown formatting

### 7. Ensure CLAUDE.local.md is in .gitignore

Before writing `CLAUDE.local.md`, ensure it is listed in the worktree's `.gitignore`.

```bash
WORKTREE_PATH="$(git gtr go <branch-name>)"
if ! grep -q 'CLAUDE.local.md' "$WORKTREE_PATH/.gitignore" 2>/dev/null; then
  echo -e '\n# Worktree用ローカルコンテキスト\nCLAUDE.local.md' >> "$WORKTREE_PATH/.gitignore"
fi
```

This prevents `CLAUDE.local.md` from being accidentally committed.
Also add to the **main repo's** `.gitignore` if not already present:

```bash
MAIN_GITIGNORE="$(git rev-parse --show-toplevel)/.gitignore"
if ! grep -q 'CLAUDE.local.md' "$MAIN_GITIGNORE" 2>/dev/null; then
  echo -e '\n# Worktree用ローカルコンテキスト\nCLAUDE.local.md' >> "$MAIN_GITIGNORE"
fi
```

### 8. Generate CLAUDE.local.md

Write `CLAUDE.local.md` in the worktree root directory using the template
at `assets/worktree-claude-md.template`.

Replace placeholders:
- `{{NUMBER}}` -> issue number
- `{{TITLE}}` -> issue title
- `{{BODY}}` -> issue body (the updated body including ToDo checklist)
- `{{LABELS_SECTION}}` -> formatted labels list, or empty string if none
- `{{TODO_SECTION}}` -> the ToDo checklist (same one added to the issue)

**Important**: Write to `CLAUDE.local.md` (project root), NOT `.claude/CLAUDE.md`.
`CLAUDE.local.md` is automatically loaded by Claude Code and is excluded via `.gitignore` (ensured in step 7),
so it won't cause merge conflicts when PRs from different worktrees are merged.

### 9. Report Completion

Show the user:
- Worktree path
- Branch name
- ToDo items added to the issue
- How to start working: `git gtr ai <branch-name>` or `cd "$(git gtr go <branch-name>)" && claude`
