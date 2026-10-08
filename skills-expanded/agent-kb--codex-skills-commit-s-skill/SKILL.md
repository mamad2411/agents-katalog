---
name: commit-s
description: Quick git commit with auto-generated or specified message. Use when user wants to create a git commit with /commit-s.
---

# Commit Skill (/commit-s)

Create a git commit with staged or specified changes.

## Input

- `$ARGUMENTS`: Optional commit message
- Current git state: staged and unstaged changes

## Process

### Step 1: Check Git Status

Run `git status` to see current state of the repository.

### Step 2: Stage Changes

If nothing is staged:
- Run `git add .` to stage all changes

### Step 3: Review Changes

Run `git diff --staged` to review what will be committed.

### Step 4: Create Commit

If `$ARGUMENTS` is provided:
- Use it directly as the commit message
- Run `git commit -m "$ARGUMENTS"`

If no message provided:
- Analyze staged changes with `git diff --staged`
- Generate a concise commit message following the format below
- Run `git commit -m "message"`

## Commit Message Format

- Start with type: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Be concise but descriptive (max 72 chars for first line)
- Example: `feat: add user authentication with JWT`

## Output

Show a brief confirmation:
```
✓ Committed: [commit message]
  [number] files changed
```

## Guidelines

- Never commit sensitive files (.env, credentials, secrets)
- Create descriptive commit messages that explain the "why" not just the "what"
- Keep first line under 72 characters
- Use imperative mood ("add feature" not "added feature")
