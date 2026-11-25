---
name: configure-statusbar
description: Configure which segments are shown in the awesome-claude-statusbar (disk, mem, batt, docker, model).
disable-model-invocation: true
allowed-tools: Read, Bash(bash:*), Bash(sh:*), Write
---

# Configure Awesome Claude Statusbar

Read and modify the statusbar configuration file at `~/.claude/awesome-statusbar.json`.

## Config format

```json
{
  "segments": {
    "disk": true,
    "mem": true,
    "batt": true,
    "docker": true,
    "model": true
  }
}
```

Each segment can be `true` (shown) or `false` (hidden).

## Behavior

1. Read the current config from `~/.claude/awesome-statusbar.json`
2. If the file doesn't exist, treat all segments as enabled
3. Show the user the current state of each segment as a checklist
4. If the user provided arguments (e.g., `/configure-statusbar disable docker`), apply the requested changes
5. If no arguments, ask the user which segments they want to toggle
6. Write the updated config back to `~/.claude/awesome-statusbar.json`
7. Tell the user the changes will take effect on the next statusline refresh

## Argument format

Arguments follow the pattern: `<enable|disable> <segment> [segment...]`

Examples:
- `/configure-statusbar disable docker batt`
- `/configure-statusbar enable disk`
- `/configure-statusbar` (interactive -- show current state and ask)
