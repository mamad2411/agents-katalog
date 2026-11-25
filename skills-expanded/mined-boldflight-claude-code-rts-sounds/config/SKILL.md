---
name: config
description: View or change RTS sounds settings — volume, pack, headphones-only, event toggles
allowed-tools: Bash, Read, Edit, Write
user_invocable: true
---

# RTS Sounds Config

Config file: `~/.claude/rts-sounds.json`

## If user wants to VIEW current config

Read `~/.claude/rts-sounds.json` using the Read tool. If the file doesn't exist, report defaults:
- volume: 0.7
- pack: mixed
- headphones_only: false
- categories: all enabled

## If user wants to CHANGE config

1. Read `~/.claude/rts-sounds.json` (or create it with defaults if missing)
2. Edit the requested field(s) using the Edit tool
3. Confirm the change

## Available settings

- **volume** (0.0–1.0): Sound volume. Example: `0.5`
- **pack** (`mixed`, `peon`, `scv`, `trek`): Which sound universe to use. `mixed` picks randomly from all.
- **headphones_only** (true/false): Only play when headphones/external audio detected (macOS).
- **use_sound_effects_device** (true/false): Route through macOS Sound Effects device instead of default output. Keeps notification sounds separate from music. macOS only.
- **categories**: Toggle individual events:
  - `ready` — session start
  - `yes` — prompt submitted
  - `what` — notification
  - `complete` — task done
  - `error` — tool failure

## Default config (create if missing)

```json
{
  "volume": 0.7,
  "pack": "mixed",
  "headphones_only": false,
  "use_sound_effects_device": false,
  "categories": {
    "ready": true,
    "yes": true,
    "what": true,
    "complete": true,
    "error": true
  }
}
```

Changes take effect immediately — no restart needed.
