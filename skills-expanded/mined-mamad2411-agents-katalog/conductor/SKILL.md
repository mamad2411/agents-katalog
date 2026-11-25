---
name: conductor
description: >
  View what all active Claude Code sessions are doing
  and optionally send instructions to them via inbox
---

# Conductor: Cross-Session Awareness

Aggregate state from all active Claude Code sessions
and optionally send instructions to any of them.

## Helper script

A pre-built script collects all session data in one pass.
Run it first to avoid spending tokens on individual calls.

```bash
~/code/seabbs/dotfiles/scripts/claude-conductor-gather.sh
```

If the script is missing or not executable, flag this to
the user and stop.

The script outputs a JSON object with:
- `sessions`: array sorted by priority (permission first,
  then running, waiting, idle, stale), each entry has:
  - `session_id`: UUID
  - `state`: running, waiting, idle, permission, stale
  - `icon`: state indicator character
  - `project`: project basename
  - `name`: session display name (may be empty)
  - `cwd`: working directory
  - `tmux_session`, `tmux_window`, `tmux_window_name`,
    `tmux_pane`: tmux location
  - `age`: human-readable age string (e.g. "3m", "2h")
  - `recent_prompts`: last 3 user prompts (truncated)
  - `last_response`: last assistant text response (truncated
    to 200 chars, may be empty if session has no history)

## Present dashboard

Start with a compact summary table. One row per session.
Skip stale sessions unless the user asks for them.

```
| # | ◉ | Session    | Window | Age | Last prompt       | Last response        |
|---|---|------------|--------|-----|-------------------|----------------------|
| 1 | ● | dotfiles   | main   | 2m  | /conductor demo   | Working on table...  |
| 2 | ◐ | epinowcast | main   | 1h  | fix failing test  | Fixed, now running…  |
```

Columns:
- `#` — row number, used for drill-down
- `◉` — state icon only (● running, ◐ waiting, ○ idle, ▲ permission)
- `Session` — tmux session name (or project)
- `Window` — tmux window name
- `Age` — compact age string from gather output
- `Last prompt` — most recent user prompt, ~30 chars
- `Last response` — last assistant text, ~40 chars

Keep the table under 10 rows. If more sessions exist,
note the count and offer to show all.

After the table, ask ONE question:

"Pick a row to see details, send a message, or say
'stale' for old sessions — or skip."

## Drill-down

When the user picks a row number, show the full entry:

```
Session: {name or project} [{state}]
  Location: {tmux_session}:{tmux_window} ({cwd})
  Age: {age}
  Recent prompts:
    1. {most recent}
    2. {second most recent}
    3. {third most recent}
  Last response:
    {last_response}
```

Then ask again what they want to do.

## Send instructions (optional)

After presenting the dashboard, ask:
"Send instructions to a session? (name/project or skip)"

If the user names a session:

1. Ask what message to send.
2. Write the message to the inbox file using the Write
   tool: `~/.claude/inbox/{session-id}.md`

### Inbox file format

```markdown
---
from: conductor
timestamp: {ISO 8601}
---

{user's message text}
```

The delivery hook reads and deletes this file after
injecting it via `tmux send-keys` when the target
session next finishes a turn (Stop hook).

3. Confirm delivery is queued.

Multiple messages can be sent in one conductor session.

## Delivery timing

- If target is `waiting` or `idle`, delivery happens on
  the next hook fire (nearly instant).
- If target is `running` or `permission`, delivery is
  delayed until the session finishes its current turn.
  Warn the user about this.
- New writes overwrite pending undelivered messages.

## Prerequisites

If the gather script reports no sessions or errors,
check these are in place:

1. Session tracking hook in `settings.json` on all
   lifecycle events calling
   `~/code/seabbs/dotfiles/scripts/claude-session-track.sh`
2. Inbox delivery script at
   `~/code/seabbs/dotfiles/scripts/claude-inbox-deliver.sh`
   (called by the tracking hook on Stop)
3. Inbox directory: `mkdir -p ~/.claude/inbox`
