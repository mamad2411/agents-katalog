---
name: memory
description: Small persistent key-value store at .dragoon/memory.json for project-specific facts dragoon (and the user) want to remember across sessions. Subcommands list/get/set/remove/clear. Keys are lowercase ascii (./_/-, max 64). Values are plain text (max 8KB, max 256 keys). Use to remember conventions, decisions, gotchas. Run as `node ~/.claude/skills/dragoon/skills/memory/scripts/memory.js <subcommand>`.
version: 1.0.0
---

# /memory

Persistent project memory. Tiny key-value store.

## When to use

- Capturing a decision the agent should remember next session
- Convention notes, gotchas, where the bodies are buried

## Commands

```
dragoon memory list
dragoon memory get auth-pattern
dragoon memory set auth-pattern "token from cookie, not header"
dragoon memory remove auth-pattern
dragoon memory clear --yes
```

## Limits

- max 256 keys
- max 8KB per value
- keys: lowercase ascii, plus `.` `_` `-`, max 64 chars
