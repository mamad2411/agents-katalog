---
name: branch-cleanup
description: Lists and removes stale local and remote branches that have been merged
user-invocable: true
allowed-tools: Bash(git *)
effort: low
---

## Branch Cleanup

1. Show current state:
```bash
git branch -vv
git branch --merged main 2>/dev/null || git branch --merged master
```

2. List candidates for deletion:
- Local branches merged into main/master
- Local branches with gone remote tracking refs
- Remote branches merged into main (requires confirmation)

3. Show the list to the user with what would be deleted. Ask for confirmation before deleting anything.

4. On confirmation:
```bash
# Delete merged local branches (never delete main/master/develop/staging)
git branch --merged main | grep -vE '^\*|main|master|develop|staging' | xargs -r git branch -d
```

5. Report what was deleted and what was skipped.
