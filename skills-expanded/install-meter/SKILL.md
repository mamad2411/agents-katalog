---
name: install-meter
description: Add the terse context meter to the Claude Code status line. Use when the user asks to install, enable or show the context meter or percentage in the status line.
disable-model-invocation: true
---

Install the meter in two steps. Paths below are already substituted by Claude Code, use them verbatim.

1. Copy the meter script to the plugin's data directory, which survives plugin updates:

```
mkdir -p "${CLAUDE_PLUGIN_DATA}" && cp "${CLAUDE_PLUGIN_ROOT}/statusline/context-meter.js" "${CLAUDE_PLUGIN_DATA}/context-meter.js"
```

2. Add this entry to the user's `~/.claude/settings.json` (create the key if missing, keep every other key as is):

```json
"statusLine": {
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_DATA}/context-meter.js\""
}
```

Claude Code reloads the status line on save, no restart needed. Edit the file in place and leave no backup copies.
Then tell the user: the meter shows model name and context fill percentage. Colours: green below 37%, yellow from 37%, orange from 49%, skull from 60%. The thresholds are below the usual 50, 65 and 80 percent because retrieval quality degrades before a large window fills. Sources are linked in the README, meter section. The thresholds are the three numbers near the top of the copied `context-meter.js`. A plugin update does not touch the copy, so rerun `/terse:install-meter` after an update to pick up a changed meter.
