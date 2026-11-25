---
name: status
description: Show every ramify worktree of the current repository with its agent, activity, changes and ports, plus the branch graph.
disable-model-invocation: true
---

Run these and summarise the result for the user in a short table (worktree, branch, agent, running, changes, commits ahead, ports), then point out anything that needs attention (uncommitted changes, unpushed commits, idle worktrees that are already merged):

```bash
NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify ls
NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify graph -n 25
```
