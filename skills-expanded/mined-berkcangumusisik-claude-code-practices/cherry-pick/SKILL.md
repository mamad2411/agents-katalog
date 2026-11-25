---
name: cherry-pick
description: Finds a commit by description and cherry-picks it to the current branch
argument-hint: <commit-description-or-hash>
user-invocable: true
allowed-tools: Bash(git *)
effort: low
---

## Cherry-pick Commit

Looking for: **$ARGUMENTS**

1. Search for the commit:
```bash
git log --all --oneline | grep -i "$ARGUMENTS" | head -10
```

2. Show the matching commits and ask which one to cherry-pick (if multiple).

3. Show the diff of the selected commit:
```bash
git show <hash> --stat
```

4. Confirm with user, then:
```bash
git cherry-pick <hash>
```

5. If conflicts arise, list them and ask how to proceed.

6. Report success: which commit was applied and what changed.
