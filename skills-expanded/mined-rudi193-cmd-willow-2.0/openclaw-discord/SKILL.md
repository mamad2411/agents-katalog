---
name: openclaw-discord
description: Mode A phone bridge — Discord app on phone ↔ OpenClaw gateway on desktop ↔ Grove fleet. Alerts out, grove: commands in.
---

# OpenClaw + Discord (Mode A)

Use the **Discord app on your phone** as the fleet pocket terminal. Grove stays on Postgres; OpenClaw carries messages.

## Architecture

- **Outbound:** `#alerts`, `#handoffs` (configurable) → bridge → Discord channel
- **Inbound:** You message the bot in Discord → OpenClaw transcript → bridge → `grove_send`

## One-time setup

**Full Discord Dev Portal walkthrough:** [`docs/OPENCLAW_DISCORD_SETUP.md`](../../../docs/OPENCLAW_DISCORD_SETUP.md)

1. [Discord Developer Portal](https://discord.com/developers/applications) — bot token, Message Content Intent, invite to your server.
2. Desktop OpenClaw: `willow skills openclaw-setup --with-cli` (if config invalid: `python3 scripts/setup_openclaw_skills.py --repair-config`) then configure `channels.discord` in `~/.openclaw/openclaw.json` (see [OpenClaw docs](https://docs.openclaw.ai/channels/discord)).
3. Start gateway: `openclaw gateway` (or daemon from onboard).
4. Willow config:
   ```bash
   willow.sh openclaw-discord init-config
   # edit $WILLOW_HOME/openclaw_discord.json — set discord_channel_id
   willow.sh openclaw-discord test-discord
   willow.sh openclaw-discord test-grove
   ```

## Run the bridge (desktop, alongside gateway)

```bash
willow.sh openclaw-discord run          # loop every 30s
willow.sh openclaw-discord run --once  # single tick
```

Optional: systemd user unit or `willow-termux`-style wrapper on the machine that runs Postgres + OpenClaw.

## Commands from Discord (phone)

| Message | Action |
|---------|--------|
| `grove:general @hanuman ping` | Post to Grove `#general` |
| `grove:dispatch fix upstream PR #5` | Post to `#dispatch` |
| `status-all` | Run `./willow.sh status-all`, reply on Discord |
| `health` | Run `./willow.sh health` |
| `fleet_status` | Run `./willow.sh fleet_status` |
| `handoff willow` | Latest handoff text on Discord |

Prefix `grove:` is required for Grove posts (avoids accidental spam).

## What this does not do

- Mirror full `#general` firehose to Discord (use Mode B later if needed).
- Replace Grove bus semantics or MCP — bridge only.
- Run without OpenClaw gateway + Discord token on the desktop host.

## Related

- `scripts/openclaw_discord_bridge.py`
- `sap/openclaw_mcp.py` — agents can also `openclaw_send` to Discord
- `sap/openclaw_ingest.py` — optional KB ingest from OpenClaw transcripts
