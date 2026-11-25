---
description: "Guide users through choosing and configuring a channel adapter (WebSocket, Telegram, Discord, Slack, etc.). Use when user asks about channel setup, switching channels, or configuring TALON_CHANNEL."
allowed-tools: [Bash, Read, Edit]
---

# Channel Adapter Setup Guide

Help the user choose and configure which channel adapter to use with the Talon Channels plugin. There are 22 options: the default WebSocket server plus 21 platform-specific adapters.

## Development Mode

During the research preview, channels require the official allowlist. To use talon-channels:

```bash
claude --dangerously-load-development-channels plugin:channels@gettalon-talon-plugins
```

The `plugin:` prefix tells Claude Code to load this channel plugin and bypass the allowlist check.

## Available Channels

| Channel | Env Var Value | Typical Required Env Vars |
|---------|---------------|---------------------------|
| WebSocket (default) | `websocket` | None (runs locally) |
| Telegram | `telegram` | `TELEGRAM_BOT_TOKEN` |
| Discord | `discord` | `DISCORD_BOT_TOKEN` |
| Slack | `slack` | `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` |
| WhatsApp | `whatsapp` | `WHATSAPP_API_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID` |
| Signal | `signal` | `SIGNAL_CLI_PATH`, `SIGNAL_PHONE_NUMBER` |
| iMessage | `imessage` | None (macOS only, uses local iMessage) |
| IRC | `irc` | `IRC_SERVER`, `IRC_NICK`, `IRC_CHANNEL` |
| Google Chat | `googlechat` | `GOOGLE_CHAT_CREDENTIALS`, `GOOGLE_CHAT_SPACE` |
| LINE | `line` | `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_CHANNEL_SECRET` |
| Feishu | `feishu` | `FEISHU_APP_ID`, `FEISHU_APP_SECRET` |
| Matrix | `matrix` | `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN` |
| Mattermost | `mattermost` | `MATTERMOST_URL`, `MATTERMOST_TOKEN` |
| MS Teams | `msteams` | `MSTEAMS_APP_ID`, `MSTEAMS_APP_PASSWORD` |
| BlueBubbles | `bluebubbles` | `BLUEBUBBLES_URL`, `BLUEBUBBLES_PASSWORD` |
| Nostr | `nostr` | `NOSTR_PRIVATE_KEY` |
| Nextcloud Talk | `nextcloud-talk` | `NEXTCLOUD_URL`, `NEXTCLOUD_TOKEN` |
| Synology Chat | `synology-chat` | `SYNOLOGY_URL`, `SYNOLOGY_TOKEN` |
| Tlon | `tlon` | `TLON_SHIP_URL`, `TLON_AUTH_CODE` |
| Twitch | `twitch` | `TWITCH_OAUTH_TOKEN`, `TWITCH_CHANNEL` |
| Zalo | `zalo` | `ZALO_OA_ACCESS_TOKEN` |
| Zalo User | `zalouser` | `ZALO_USER_ACCESS_TOKEN` |

## Steps

### 1. Ask Which Channel

Ask the user which platform they want Claude Code to be reachable on. If they are unsure, explain:

- **WebSocket** (default): Best for custom integrations, local dashboards, browser extensions, or any app that can speak WebSocket. No external accounts needed.
- **Platform adapters**: Best when the user wants to interact with Claude Code directly from Telegram, Discord, Slack, etc. Requires API credentials for that platform.

### 2. Check Current Configuration

```bash
# Check what channel is currently configured
cat "${CLAUDE_PLUGIN_ROOT}/../.mcp.json" 2>/dev/null || echo "No .mcp.json found"
```

```bash
# Check if there's a project-level MCP config
cat .mcp.json 2>/dev/null || echo "No project .mcp.json"
```

### 3. Configure the Channel

To switch channels, update the `.mcp.json` file to include the `TALON_CHANNEL` env var and any platform-specific credentials.

#### For WebSocket (default — no changes needed):

The default configuration works out of the box:

```json
{
  "channels": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"]
  }
}
```

#### For a platform adapter (e.g., Telegram):

Update the plugin's `.mcp.json` to set the channel and required env vars:

```json
{
  "channels": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"],
    "env": {
      "TALON_CHANNEL": "telegram",
      "TELEGRAM_BOT_TOKEN": "your-bot-token-here"
    }
  }
}
```

Alternatively, set env vars in the user's shell profile (`~/.zshrc`, `~/.bashrc`) so they persist:

```bash
export TALON_CHANNEL=telegram
export TELEGRAM_BOT_TOKEN=your-bot-token-here
```

### 4. Apply the Configuration

After updating the `.mcp.json` or env vars, use the Edit tool to write the changes. Then tell the user to restart Claude Code for the changes to take effect:

```
Restart Claude Code for the new channel configuration to take effect.
Run: claude
```

### 5. Verify It Works

For **WebSocket** mode:
```bash
# Check if server is running
curl -s http://localhost:21568/health 2>/dev/null || echo "Server not running — start Claude Code first"
```

For **platform adapters**, the server logs will show the channel starting:
```
[talon-channels] Starting platform channel: telegram
[talon-channels] Platform channel "telegram" is ready
```

If the adapter fails to start, it usually means a required env var is missing. Check the logs for error messages.

### 6. Switching Back to WebSocket

To switch back to the default WebSocket mode, either:
- Remove the `TALON_CHANNEL` env var from `.mcp.json`
- Or set it explicitly to `"websocket"`

### 7. Using Multiple Channels

To use multiple channels simultaneously (e.g., WebSocket + Telegram), create separate MCP server entries in `.mcp.json`:

```json
{
  "channels-ws": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"],
    "env": {
      "TALON_CHANNEL": "websocket"
    }
  },
  "channels-telegram": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"],
    "env": {
      "TALON_CHANNEL": "telegram",
      "TELEGRAM_BOT_TOKEN": "your-bot-token-here"
    }
  }
}
```

### 8. Troubleshooting

**"Unknown channel type"**: The `TALON_CHANNEL` value does not match any supported adapter. Check spelling — it must be one of: websocket, telegram, discord, slack, whatsapp, signal, imessage, irc, googlechat, line, feishu, matrix, mattermost, msteams, bluebubbles, nostr, nextcloud-talk, synology-chat, tlon, twitch, zalo, zalouser.

**"No creator function found"**: The `@gettalon/channels-sdk` version may not include this adapter yet. Try updating: `npm install @gettalon/channels-sdk@latest` in the mcp-server directory.

**Platform adapter won't start**: Check that all required environment variables are set. Each platform has its own requirements — see the table above for typical env vars needed.

**WebSocket port conflict**: If port 21568 is in use, set `TALON_CHANNELS_PORT` to a different port, or let the server auto-select by leaving it to fail over to a random port.

### 9. Access Control

For platform adapters (Telegram, Discord, etc.), Claude Code requires a **sender allowlist**:

- Only approved sender IDs can push messages
- During research preview, use `--dangerously-load-development-channels` to bypass
- For production, implement your own pairing flow and allowlist logic

### 10. Migrating from Official Plugins

To migrate from the official `telegram@claude-plugins-official` or `discord@claude-plugins-official` plugins:

**Step 1: Copy your existing credentials**

```bash
# For Telegram - copy the bot token
cat ~/.claude/channels/telegram/.env
```

**Step 2: Disable the official plugin**

Edit `~/.claude/settings.json` and set the official plugin to `false`:

```json
{
  "enabledPlugins": {
    "telegram@claude-plugins-official": false
  }
}
```

**Step 3: Configure talon-channels**

Update the talon plugin's `.mcp.json` with your credentials:

```json
{
  "channels": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"],
    "env": {
      "TALON_CHANNEL": "telegram",
      "TELEGRAM_BOT_TOKEN": "YOUR_TOKEN_FROM_STEP_1"
    }
  }
}
```

**Step 4: Restart with dev mode**

```bash
claude --dangerously-load-development-channels
```

**Step 5: Copy access control (optional)**

If you had approved senders in the official plugin, copy the allowlist:

```bash
cat ~/.claude/channels/telegram/access.json
```

You'll need to implement equivalent allowlist checking in talon-channels or use dev mode for now.
