---
name: hud
description: Switch this Claude Code session into hud mode (the compact heads-up view). Use when the user types /hud or asks to go back to the hud.
allowed-tools: Bash
---

# Hand this session back to the hud

The user wants to leave the full Claude Code TUI and continue this session in
`hud` - a compact wrapper that resumes the same session via `--resume`.

Do exactly the following, then stop:

1. Find this session's ID and write a handoff file, in a single Bash command:

```bash
PROJ_DIR="$HOME/.claude/projects/$(pwd | sed 's/[^a-zA-Z0-9]/-/g')"
SID=$(ls -t "$PROJ_DIR"/*.jsonl 2>/dev/null | head -1 | xargs -n1 basename 2>/dev/null | sed 's/\.jsonl$//')
mkdir -p "$HOME/.claude/hud"
printf '{"action":"hud","sessionId":"%s","cwd":"%s","ts":%s}\n' "$SID" "$(pwd)" "$(date +%s)000" > "$HOME/.claude/hud/handoff.json"
echo "handoff written for session $SID (HUD_MODE=${HUD_MODE:-0})"
```

2. Reply to the user with ONE short line and nothing else:
   - If the command output shows `HUD_MODE=1` (this CLI was launched by the
     hud wrapper): say `◆ Returning to the hud…` - the wrapper is watching
     the handoff file and will take over immediately.
   - Otherwise: say `◆ Handoff armed - exit this CLI (Ctrl+C twice or /exit) and run` `hud` `in this directory to continue.`

Do not summarize the session, do not take any other action.
