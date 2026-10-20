---
description: Creates a new worktree
---

When this command is invoked:

1. Check if the user has provided a github issue or a worktree name.

2. If no parameters provided, respond with:

   ```
   Before switching to a new worktree I need to know its name

   Please either provide a github issue ID (`issues/<id>`) or a readable name.

   Tip: You can also invoke this command with a name directly: `/new_worktree issues/955`
   ```

   **IMPORTANT PATH USAGE:**
   - The knowledge/ directory is synced between the main repo and worktrees
   - Always use ONLY the relative path starting with `knowledge/shared/...` without any directory prefix
   - Example: `knowledge/shared/plans/fix-mcp-keepalive-proper.md` (not the full absolute path)
   - This works because knowledge is synced and accessible from the worktree

3. confirm with the user by sending a message to the Human

```
Based on the input, I plan to create a worktree with the following details:

worktree path: ~/wt/repo/feature/issue/33
branch name: BRANCH_NAME
path to plan file: $FILEPATH
```

Then:

- Read `.claude/scripts/create_worktree.sh` and use it to set up a new worktree
- `cd` to the new worktree and initialize the project
- If a github issue was provided use the `github` skill to fetch any relevant information from the issue and then save it in `knowledge/local/notes/issue_<worktree_name>.md`
