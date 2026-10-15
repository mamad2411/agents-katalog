---
name: claude-ping-me
description: Plays a notification sound when Claude Code is waiting for your input
---

# claude-ping-me

You give Claude a task. You switch tabs. Claude pings you when it needs you. Never miss a prompt again.

## Install

**Step 1:** Install the skill

```bash
npx skills add nerdynikhil/claude-ping-me -g -y
```

**Step 2:** Add hooks to your `~/.claude/settings.json`

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "bash $HOME/.agents/skills/claude-ping-me/hooks/play-sound.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash $HOME/.agents/skills/claude-ping-me/hooks/play-sound.sh"
          }
        ]
      }
    ]
  }
}
```

If you already have stuff in your settings file, just merge the `hooks` key in — don't overwrite.

**Step 3:** Restart Claude Code. Done.

## What it does

Plays a short chime when:
- Claude **finishes responding** and is waiting for your next prompt
- Claude has been **idle** and needs your input (approve a plan, pick an approach, etc.)

## Platform support

- **macOS** — uses built-in `afplay` (no dependencies)
- **Linux** — uses `mpg123`, `ffplay`, or `paplay`
- **Windows** — uses PowerShell `MediaPlayer`

## Customization

Replace `sounds/ping.mp3` with any MP3 file to use your own sound.
