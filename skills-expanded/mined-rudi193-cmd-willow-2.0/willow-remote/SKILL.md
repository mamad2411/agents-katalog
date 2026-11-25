---
name: willow-remote
description: Start Willow Discord remote control — phone ↔ Claude Code CLI via Discord REST bridge
skill_args: $ARGUMENTS
---

# /willow-remote

Connects this Claude Code session to Discord so USER can send commands from their phone and see responses.

## What this does

1. Starts `scripts/discord_remote.py run` as a background daemon (if not already running)
2. Posts a "Willow remote online" message to Discord
3. Sets a persistent Monitor on the bridge log — fires immediately when an inbound Discord message arrives, no polling delay
4. On each notification: reads Grove `hanuman` for the command, processes it, posts the response back so the bridge forwards it to Discord

## Steps

### 1. Start the bridge daemon

Tell the user to run in a separate terminal (daemon cannot persist inside bwrap/kart):
```
cd ~/github/willow-2.0 && source ~/github/.willow/env && python3 scripts/discord_remote.py run --interval 15
```

Or check if it is already running: `python3 scripts/discord_remote.py status`.

### 2. Announce online

Post to Grove `hanuman` as `hanuman`:
```
grove_send_message(channel_name="hanuman", content="willow-remote online — listening for Discord commands", sender="hanuman")
```

The bridge will forward this to Discord within 15 seconds.

### 3. Set the Monitor

```python
Monitor(
    description="Discord inbound commands",
    command="tail -n 0 -f $WILLOW_HOME/discord_remote.log | grep --line-buffered 'inbound Discord'",
    persistent=True,
)
```

This fires a notification each time a new inbound Discord message lands — reaction time is bounded by the bridge poll interval (15s), not a separate Claude Code loop.

### 4. On each Monitor notification

The notification line contains the Grove message id and a content snippet. When it fires:

**4a. Claim the message first** (multi-agent coordination):

Extract the grove_id from the notification line (`id=NNN`). Run:
```python
from scripts.willow_discord_responder import claim_for
claimed = claim_for(grove_id=NNN, claimer_id="claude-code")
```
If `claimed` is False — `willow_discord_responder` already handled it. Skip.
If `claimed` is True — proceed.

**4b. Process and reply:**
1. Call `grove_get_history(channel_name="hanuman", since_id=<last_cursor>)` to get the full message
2. Strip the `[Discord/<username>] ` prefix to get the raw command
3. Process it — answer questions, run fleet checks, execute tasks as appropriate
4. Post the response: `grove_send_message(channel_name="hanuman", content=<response>, sender="hanuman")`
   - The bridge picks this up on its next poll and forwards to Discord

Store `last_cursor` as the highest Grove message id seen so far (start from the id in the Monitor notification line).

### 5. Stopping

USER types `stop willow-remote` in Discord → bridge routes to Grove → Claude Code sees it in the Monitor notification, stops monitoring, posts "willow-remote offline" to Grove.

## Commands USER can send from Discord

Any free-form message is routed to Claude Code. Examples:
- `fleet status` → run fleet_status, reply with summary
- `what's on the docket` → summarize open threads from handoff
- `handoff hanuman` → post latest handoff summary
- Anything else → Claude Code processes and replies

## Notes

- Bridge daemon: `$WILLOW_HOME/discord_remote.pid` / `$WILLOW_HOME/discord_remote.log`
- Token: `DISCORD_BOT_TOKEN` in `$WILLOW_HOME/env`
- Channel: `1509605940578615487`
- Loop-prevention: bridge only forwards `hanuman`-sender Grove messages to Discord (not its own `discord-bridge` posts)
- Claim file: `$WILLOW_HOME/discord_claims.json` — shared by Claude Code and `willow_discord_responder.py`. First claimer wins; claims expire after 1 hour.
- Always-on fallback: `scripts/willow_discord_responder.py` (Ollama/llama3.1:8b) handles commands when no Claude Code session is live. Run as systemd service `willow-discord-responder.service`.
