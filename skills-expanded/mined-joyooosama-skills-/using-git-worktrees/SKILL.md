---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# using git worktrees

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always use `git check-ignore` before creating project-local worktree
- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing > CLAUDE.md > ask
- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed
- **Problem:** Breaks on projects using different tools
- **Fix:** Auto-detect from project files (package.json, etc.)

## Available sections

- Using Git Worktrees
- Overview
- Directory Selection Process
- 1. Check Existing Directories
- Check in priority order
- 2. Check CLAUDE.md
- 3. Ask User
- Safety Verification
- For Project-Local Directories (.worktrees or worktrees)
- Check if directory is ignored (respects local, global, and system gitignore)
- For Global Directory (~/.config/superpowers/worktrees)
- Creation Steps

