---
name: merge-conflict
description: Finds all merge conflict markers in the repo and resolves them with explanation
user-invocable: true
allowed-tools: Bash(git *) Read Edit Grep
effort: medium
---

## Resolve Merge Conflicts

1. Find all files with conflicts:
```bash
git diff --name-only --diff-filter=U
grep -rl "<<<<<<< " . --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.go" 2>/dev/null
```

2. For each conflicted file:
   - Read the full file
   - For each conflict block (`<<<<<<< / ======= / >>>>>>>`) explain:
     - What **HEAD** (ours) is trying to do
     - What **theirs** is trying to do
     - Why there's a conflict

3. Propose the resolution for each conflict. Explain the reasoning.

4. Ask for confirmation, then apply.

5. After all conflicts resolved:
```bash
git add .
```

Remind the user to run tests before committing.
