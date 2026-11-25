---
name: brain-update
description: |
  Update claude-teams-brain from GitHub.
  Pulls latest changes, syncs to plugin cache, and reports what changed.
  Trigger: /brain-update
user_invocable: true
---

# brain-update

Pull the latest version of claude-teams-brain from GitHub and sync it to the local plugin cache.

## Instructions

Run:
```
bash "${CLAUDE_PLUGIN_ROOT}/scripts/update.sh"
```

After the script completes, display the results as markdown:
```
## claude-teams-brain update
- [x] Pulled latest from GitHub
- [x] Synced to plugin cache
- [x] Version: <version>
- [x] Changes: <summary of changed files or "already up to date">
```

Use `[x]` for success, `[ ]` for failed steps.
If hooks or settings changed, tell the user to restart Claude Code to apply them.
