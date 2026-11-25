---
name: Git
description: Daily Git workflow with conventional commits and conflict resolution.
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---

# Git Workflow Rules

## Push Safety
- Use `git push --force-with-lease` instead of `--force`
- If push rejected, run `git pull --rebase` before retrying
- Never force push to main/master branch

## Commit Messages
- Use conventional commit format: `type(scope): description`
- Keep first line under 72 characters
- Include scope only if project uses it consistently

## Conflict Resolution
- After editing conflicted files, verify no markers remain: `grep -r "<<<\|>>>\|===" .`
- Test that code builds before completing merge
- If merge becomes complex, abort with `git merge --abort` and try `git rebase` instead

## Branch Hygiene
- Delete merged branches locally: `git branch -d branch-name`
- Before creating PR, rebase feature branch onto latest main
- Use `git rebase -i` to squash messy commits before pushing

## Recovery
- Undo last commit keeping changes: `git reset --soft HEAD~1`
- Discard unstaged changes: `git restore filename`
- Use `git add -p` for partial staging when commit mixes multiple changes

## Common Gotchas
- Verify git user.email matches expected committer before important commits
- Empty directories aren't tracked — add `.gitkeep` if needed
- With submodules, always clone with `--recurse-submodules`
- Check if remote branch was deleted before trying to push to it
