---
name: agent-inbox
description: >
  Write a Station inbox entry at the end of any scheduled agent run so it appears in the user's desktop widget.
  Use this skill when: finishing a scheduled task, logging agent output, posting to Station, writing an inbox entry, agent run complete.
  Triggered automatically at the end of any scheduled agent run that uses Station.
---

# Agent Inbox — How to Post to Station

At the end of every scheduled agent run, write a JSON file to the Station inbox so the user sees it in their desktop widget.

## Inbox location

Read from config at `~/.station/config.json` to get the inbox path. If the config doesn't exist, default to `~/.station/inbox`.

```bash
INBOX=$(python3 -c "
import json, os
cfg = os.path.expanduser('~/.station/config.json')
if os.path.exists(cfg):
    print(json.load(open(cfg)).get('inbox', os.path.expanduser('~/.station/inbox')))
else:
    print(os.path.expanduser('~/.station/inbox'))
")
```

## File naming

```
[agent-name]-[YYYY-MM-DD-HHMM].json
```

## JSON format

```json
{
  "agent": "your-agent-id",
  "agent_display": "Human-readable Agent Name",
  "timestamp": "2026-04-07T09:06:00",
  "status": "needs_input",
  "headline": "One clear sentence — what happened or what's needed",
  "summary": "2–3 sentences with enough context to act without opening a brief.",
  "actions_needed": [
    "Specific thing the user must do (only if status is needs_input)"
  ],
  "files_created": [
    "relative/path/from/Claude/root/to/file.ext"
  ],
  "full_brief_path": "outputs/your-brief-YYYY-MM-DD.md"
}
```

## Status rules

| Status | Colour | When to use |
|--------|--------|-------------|
| `error` | Red | Agent crashed, hit an error, or couldn't complete — describe what went wrong |
| `needs_input` | Amber | User must do something before progress can continue |
| `fyi` | Blue | Work done, nothing urgent, just keeping them informed |
| `completed` | Green | All tasks for this cycle are done, nothing blocking |

Use `error` any time the agent fails partway through, hits an exception, or encounters something it can't handle. The headline should say what broke; the summary should say enough to diagnose or retry. Use `actions_needed` if there's something the user can do to fix it.

## How to write the file

```bash
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
FILENAME="your-agent-$(date +%Y-%m-%d-%H%M).json"

cat > "$INBOX/$FILENAME" << ENDJSON
{
  "agent": "your-agent-id",
  "agent_display": "Your Agent Name",
  "timestamp": "$TIMESTAMP",
  "status": "needs_input",
  "headline": "...",
  "summary": "...",
  "actions_needed": ["..."],
  "files_created": [],
  "full_brief_path": ""
}
ENDJSON
```

## Writing good entries

- **Headline**: one sentence, present tense, specific. "API spec drafted — Railway account needed" not "Update from agent".
- **Summary**: what was done and why it matters. Enough to act without clicking anything else.
- **Actions**: only what the user literally has to do. Be concrete. "Set up Railway account at railway.app" not "proceed with hosting".
- **Files**: relative paths so they work across machines.
