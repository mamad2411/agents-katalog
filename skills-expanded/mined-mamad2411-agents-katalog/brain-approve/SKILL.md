---
name: brain-approve
description: |
  Approve, reject, or manage pending brain memories.
  Use: /brain-approve [all|<id>]
user_invocable: true
---

# brain-approve

Manage pending brain memories. Memories from `/brain-remember` start as PENDING and need approval before being injected into teammates.

## Instructions

If the user provides "all" as argument:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py approve-all-pending "$CLAUDE_PROJECT_DIR"
```

If the user provides a specific task/decision ID:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py approve-task "$ARGS" "$CLAUDE_PROJECT_DIR"
```

If no argument provided, list pending items first:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py list-pending "$CLAUDE_PROJECT_DIR"
```

Then ask the user which items to approve or if they want to approve all.

Report the results back to the user.
