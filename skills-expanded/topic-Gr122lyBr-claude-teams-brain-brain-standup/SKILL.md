---
name: brain-standup
description: |
  Launch the standup meeting UI — a cinematic visualization of each agent role's status report.
  Trigger: /brain-standup
user_invocable: true
---

# brain-standup

Launch an animated standup meeting visualization. Each agent role "presents" their status — what they did, what's next, and any blockers — with a cinematic walk-in animation and typewriter effect.

## Instructions

Launch the standup server:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/standup_server.py --project-dir "$CLAUDE_PROJECT_DIR" &
```

Then open in browser:
```
python3 -m webbrowser "http://localhost:7433"
```

Tell the user:
- Standup meeting is running at http://localhost:7433
- Each agent role will present their report with animations
- Use the controls at the bottom to pause, skip, or replay
- Close the terminal or press Ctrl+C to stop the server
