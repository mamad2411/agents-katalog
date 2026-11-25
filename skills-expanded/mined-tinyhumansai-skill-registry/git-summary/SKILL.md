---
name: git-summary
description: "Summarize the current git repository: branch, recent commits, changed files, and overall health. Use when asked for a repo overview or status check."
metadata:
  version: "1.0.0"
  author: "tinyhumansai"
  tags: ["git", "summary", "status"]
license: MIT
---

# Git Summary

Produce a concise summary of the current git repository state.

## Steps

1. Run `git rev-parse --abbrev-ref HEAD` to get the current branch.
2. Run `git log --oneline -10` to list the 10 most recent commits.
3. Run `git status --short` to show uncommitted changes.
4. Run `git stash list` to check for stashed work.
5. Run `git remote -v` to list configured remotes.

## Output format

Present the summary as a structured report:

```
## Repository Summary

**Branch**: <current branch>
**Remotes**: <list of remotes>
**Recent commits** (last 10):
  - <commit hash> <message>
  ...
**Working tree**: <clean | N files changed>
**Stashes**: <none | N stashes>
```

## Notes

- If the directory is not a git repository, say so and stop.
- Do not modify any files or git state — this skill is read-only.
