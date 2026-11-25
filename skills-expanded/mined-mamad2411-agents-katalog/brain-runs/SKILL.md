---
name: brain-runs
description: |
  List past Agent Team sessions stored in claude-teams-brain
user_invocable: true
---

# brain-runs

List all past Agent Team sessions recorded in the brain for this project.

## Instructions

Run:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py list-runs "$CLAUDE_PROJECT_DIR"
```

Display results as a table sorted newest first:
- Session ID (truncated)
- Date
- Agents involved
- Tasks completed
- One-line summary

If no runs are recorded yet, explain that sessions are indexed automatically once Agent Teams are used.
