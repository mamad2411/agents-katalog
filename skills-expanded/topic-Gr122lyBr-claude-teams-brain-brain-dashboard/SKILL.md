---
name: brain-dashboard
description: |
  Launch the brain dashboard web UI to visualize and curate memories, decisions, and files.
  Trigger: /brain-dashboard
user_invocable: true
---

# brain-dashboard

Launch an interactive web dashboard showing all brain memory — tasks, decisions, files, and sessions. Includes memory curation (approve/reject/flag) and activity timeline.

## Instructions

Launch the dashboard server:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/dashboard_server.py --project-dir "$CLAUDE_PROJECT_DIR" &
```

Then open in browser:
```
python3 -m webbrowser "http://localhost:7432"
```

Tell the user:
- Dashboard is running at http://localhost:7432
- They can approve, reject, or flag memories from the Memory Curation tab
- The dashboard auto-refreshes every 30 seconds
- Close the terminal or press Ctrl+C to stop the server
