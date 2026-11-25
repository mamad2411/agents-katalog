---
name: sloth-commit
description: "Use when saving, committing, pushing, or syncing Claude Code memory changes to the private GitHub memory repo."
---

# Sloth Commit

## Overview
Commits and pushes all changes in the Claude Code memory directory to the private GitHub repo (`coreymaypray/claude-code-memory`). Auto-generates a commit message summarizing what changed.

## Memory Directory
`C:\Users\Owner\.claude\projects\C--Users-Owner-Downloads-Projects\memory`

## Process

Execute these steps exactly:

### Step 1 — Check for changes
```bash
cd "C:\Users\Owner\.claude\projects\C--Users-Owner-Downloads-Projects\memory" && git status --short
```

If no changes, tell the user "Memory is clean — nothing to commit." and stop.

### Step 2 — Show what changed
Run `git diff` and `git diff --cached` to see all modifications. Also check for untracked files.

### Step 3 — Stage all memory files
```bash
cd "C:\Users\Owner\.claude\projects\C--Users-Owner-Downloads-Projects\memory" && git add -A
```

### Step 4 — Generate commit message
Analyze the staged changes and create a commit message following this format:
```
memory: <brief summary of what changed>

Files: <list of files added/modified/deleted>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Examples:
- `memory: add feedback on testing preferences`
- `memory: update user profile with new project context`
- `memory: add security assessment for new-tool-name`
- `memory: update project status for TIE Platform milestone`

### Step 5 — Commit and push
```bash
cd "C:\Users\Owner\.claude\projects\C--Users-Owner-Downloads-Projects\memory" && git commit -m "<message>" && git push
```

### Step 6 — Confirm
Tell the user what was committed and pushed. Keep it short.

## Rules
- NEVER commit files matching `.env`, `.key`, `.pem`, `credentials.*` — warn the user if these exist
- Always use the `memory:` prefix in commit messages
- Always include the Co-Authored-By trailer
- If push fails (network, auth), tell the user the commit succeeded locally and they can push later with `git push`
- Do not modify any memory file contents during this process — commit only
