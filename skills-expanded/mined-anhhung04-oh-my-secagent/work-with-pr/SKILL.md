---
name: work-with-pr
description: Fixture for project skill tool reference tests.
---

Use the project task tool with a real category when committing from a worktree:

```text
task(category="quick", load_skills=["git-master"], prompt="Commit the changes atomically following git-master conventions. Repository is at {WORKTREE_PATH}.")
```

