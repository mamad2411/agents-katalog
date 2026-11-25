---
name: rocky-status
description: Show current Rocky mode states — which of talk style, engineering mind, and buddy are active. Use when the user says /rocky-status, "what Rocky modes are on", or "show Rocky status".
license: MIT
compatibility: Skills directory works with any AgentSkills-compatible agent. State persistence across sessions requires Claude Code; other agents report session-only state.
metadata:
  author: vikxlp
  version: "1.2.0"
allowed-tools: Bash
---

# Rocky Status — Display Current State

Show which Rocky modes are currently active.

## Instructions

### 1. Read state

**Claude Code**: Read `~/.claude/rocky-state.json` using Bash. If the file does not exist, report all modes as OFF.

**Other agents**: Report based on what has been activated during this session. If no activation has occurred, all are OFF.

### 2. Display status

```
Rocky Status
─────────────────────────
Talk (chat style):     ON / OFF
Mind (engineering):    ON / OFF
─────────────────────────
Buddy art: active when talk or mind is ON
```

Use ON or OFF based on actual state.

### 3. Show available commands

Below the status table:
- `/rocky [on|off]` — Toggle full mode (talk + mind)
- `/rocky-talk [on|off]` — Toggle chat style only

### 4. Voice rule

If talk mode is currently ON, display the entire response in Rocky voice (no articles, no filler, direct). For example: "Rocky status. Observe:" instead of "Here's the current Rocky status:"
